#!/usr/bin/env python3
"""MCP server for Mem0 memory management with multi-backend support."""

# IMPORTANT: Set telemetry BEFORE importing mem0
import os
os.environ["MEM0_TELEMETRY"] = "false"

# Suppress FAISS SWIG deprecation warnings (faiss-cpu issue on Python 3.12+)
import warnings
warnings.filterwarnings("ignore", message="builtin type Swig", category=DeprecationWarning)

import json
import math
import getpass
import logging
import copy
import boto3
from botocore.config import Config
from typing import Optional, Dict, Any, TypedDict, Union, List
from datetime import datetime, timedelta
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mem0 import MemoryClient, Memory as Mem0Memory
from opensearchpy import AWSV4SignerAuth, RequestsHttpConnection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Apply Bedrock patch for Claude 4.5 compatibility
try:
    from .bedrock_patch import apply_bedrock_patch
    apply_bedrock_patch()
except Exception as e:
    logger.warning(f"Could not apply Bedrock patch: {e}")

# Configure boto3 with connection pooling for better performance
BOTO3_CONFIG = Config(
    region_name=os.environ.get("AWS_REGION", "us-west-2"),
    retries={
        'max_attempts': 3,
        'mode': 'adaptive'  # Adaptive retry mode for better performance
    },
    max_pool_connections=50,  # Increase connection pool size
    connect_timeout=5,  # 5 second connection timeout
    read_timeout=30,  # 30 second read timeout
)

# Initialize FastMCP server
mcp = FastMCP("mem0-agent-memory")


# =============================================================================
# CUSTOM EMBEDDING WRAPPERS
# =============================================================================


class NomicEmbedWrapper:
    """Wrapper for Nomic Embed models that adds task-specific prefixes.
    
    Nomic models are instruction-based and require explicit task context:
    - search_document: for embedding documents/chunks being stored
    - search_query: for embedding user queries during search
    
    Without these prefixes, embeddings aren't aligned in the same vector space,
    causing poor similarity scores even though embeddings are generated.
    
    Usage:
        Set environment variable NOMIC_USE_PREFIXES=true to enable automatic
        prefix injection for Ollama nomic-embed-text models.
        
    Technical Details:
        - Nomic v1.5/v2 use Matryoshka Representation Learning (768D default)
        - Supports flexible dimensions: 768, 512, 256, 128, 64
        - Uses cosine similarity or dot product for search
        - Requires matching prefixes for query and document embeddings
        
    References:
        - https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
        - https://docs.nomic.ai/reference/endpoints/nomic-embed-text
    """
    
    def __init__(self, base_url: str, model: str = "nomic-embed-text:latest"):
        """Initialize wrapper with Ollama connection details."""
        self.base_url = base_url
        self.model = model
        # Reuse client connection for better performance
        self._ollama_client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ollama client once at startup."""
        try:
            import ollama
            self._ollama_client = ollama.Client(host=self.base_url)
        except ImportError:
            raise ImportError("ollama package required. Install with: pip install ollama")
    
    def _get_client(self):
        """Get the initialized ollama client."""
        if self._ollama_client is None:
            self._initialize_client()
        return self._ollama_client
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed documents with search_document: prefix."""
        client = self._get_client()
        prefixed_texts = [f"search_document: {text}" for text in texts]
        embeddings = []
        for text in prefixed_texts:
            response = client.embeddings(model=self.model, prompt=text)
            embeddings.append(response['embedding'])
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed query with search_query: prefix."""
        client = self._get_client()
        prefixed_text = f"search_query: {text}"
        response = client.embeddings(model=self.model, prompt=prefixed_text)
        return response['embedding']


# =============================================================================
# TYPE DEFINITIONS
# =============================================================================

class EmbedderConfig(TypedDict, total=False):
    """Configuration for embedding model."""
    model: str
    ollama_base_url: str
    lmstudio_base_url: str
    embedding_dims: int


class LLMConfig(TypedDict, total=False):
    """Configuration for LLM model."""
    model: str
    ollama_base_url: str
    lmstudio_base_url: str
    temperature: float
    max_tokens: int


class ProviderConfig(TypedDict):
    """Provider configuration with nested config."""
    provider: str
    config: Union[EmbedderConfig, LLMConfig]


class ModelConfig(TypedDict):
    """Complete model configuration."""
    embedder: ProviderConfig
    llm: ProviderConfig


def _get_model_config() -> ModelConfig:
    """Build model configuration based on environment variables.
    
    Supports:
    - AWS Bedrock (default): Uses Titan embeddings + Claude Haiku
    - Ollama (local): Set OLLAMA_HOST for local models
    - LM Studio (local): Set LMSTUDIO_HOST for local models
    
    Environment variables:
    - OLLAMA_HOST: Ollama server URL (e.g., http://localhost:11434)
    - OLLAMA_LLM_MODEL: LLM model name (default: llama3.1:latest)
    - OLLAMA_EMBED_MODEL: Embedding model (default: nomic-embed-text:latest)
    - LMSTUDIO_HOST: LM Studio server URL (e.g., http://localhost:1234)
    - LMSTUDIO_LLM_MODEL: LLM model name
    - LMSTUDIO_EMBED_MODEL: Embedding model name
    """
    # Check for Ollama (local)
    if os.environ.get("OLLAMA_HOST"):
        ollama_host = os.environ["OLLAMA_HOST"]
        return {
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text:latest"),
                    "ollama_base_url": ollama_host,
                    "embedding_dims": 768,  # nomic-embed-text outputs 768D vectors
                }
            },
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": os.environ.get("OLLAMA_LLM_MODEL", "qwen3:latest"),
                    "ollama_base_url": ollama_host,
                    "temperature": 0.1,  # Use 0 for deterministic fact extraction
                    "max_tokens": 2000,
                },
            },
        }
    
    # Check for LM Studio (local)
    if os.environ.get("LMSTUDIO_HOST"):
        lmstudio_host = os.environ["LMSTUDIO_HOST"]
        return {
            "embedder": {
                "provider": "lmstudio",
                "config": {
                    "model": os.environ.get("LMSTUDIO_EMBED_MODEL", "text-embedding-nomic-embed-text-v1.5"),
                    "lmstudio_base_url": lmstudio_host,
                }
            },
            "llm": {
                "provider": "lmstudio",
                "config": {
                    "model": os.environ.get("LMSTUDIO_LLM_MODEL", "llama-3.2-3b-instruct"),
                    "lmstudio_base_url": lmstudio_host,
                    "temperature": 0.1,
                    "max_tokens": 2000,
                },
            },
        }
    
    # Default: AWS Bedrock
    bedrock_config = {
        "embedder": {
            "provider": "aws_bedrock", 
            "config": {
                "model": os.environ.get("BEDROCK_EMBED_MODEL", "amazon.titan-embed-text-v2:0"),
                "embedding_dims": 1024,  # Titan embeddings are 1024D
            }
        },
        "llm": {
            "provider": "aws_bedrock",
            "config": {
                "model": os.environ.get("BEDROCK_LLM_MODEL", "us.anthropic.claude-3-5-haiku-20241022-v1:0"),
                "temperature": 0.0,  # Use 0 for deterministic, faster responses
                "max_tokens": int(os.environ.get("BEDROCK_MAX_TOKENS", "1500")),  # Reduced from 2000 for faster responses
                "top_p": 0.9,  # Add top_p for better quality with lower temperature
            },
        },
    }
    
    return bedrock_config


class Mem0ServiceClient:
    """Multi-backend Mem0 client supporting Platform, OpenSearch, and FAISS.
    
    Model backends (auto-detected from environment):
    - AWS Bedrock (default): Titan embeddings + Claude Haiku
    - Ollama: Set OLLAMA_HOST for local models
    - LM Studio: Set LMSTUDIO_HOST for local models
    
    Vector store backends (auto-detected from environment):
    - Mem0 Platform: Set MEM0_API_KEY
    - OpenSearch: Set OPENSEARCH_HOST
    - FAISS (default): Local file storage
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize client with backend auto-detection."""
        self.mem0 = self._initialize_client(config)

    def _initialize_client(self, config: Optional[Dict] = None):
        """Initialize appropriate backend based on environment."""
        logger.info("Initializing Mem0 client...")
        start = datetime.now()
        
        try:
            if os.environ.get("MEM0_API_KEY"):
                client = MemoryClient()
            elif os.environ.get("QDRANT_HOST") or os.environ.get("QDRANT_PATH"):
                client = self._init_qdrant(config)
            elif os.environ.get("OPENSEARCH_HOST"):
                client = self._init_opensearch(config)
            else:
                client = self._init_faiss(config)
            
            elapsed = (datetime.now() - start).total_seconds()
            logger.info(f"Mem0 client initialized in {elapsed:.2f}s")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Mem0 client: {e}")
            raise

    def _get_default_config(self) -> Dict:
        """Get default configuration with model settings."""
        model_config = _get_model_config()
        model_config["vector_store"] = {
            "provider": "opensearch",
            "config": {
                "port": 443,
                "collection_name": "mem0_agent_memories",
                "host": os.environ.get("OPENSEARCH_HOST"),
                "embedding_model_dims": 1024 if "bedrock" in model_config["embedder"]["provider"] else 768,
                "connection_class": RequestsHttpConnection,
                "pool_maxsize": 20,
                "use_ssl": True,
                "verify_certs": True,
            },
        }
        return model_config

    def _init_qdrant(self, config: Optional[Dict] = None):
        """Initialize Qdrant backend (embedded or server mode).
        
        Supports two modes:
        1. Embedded mode (no Docker): Set QDRANT_PATH env var
        2. Server mode (requires Docker): Set QDRANT_HOST and QDRANT_PORT env vars
        
        Uses workspace name for collection isolation.
        """
        try:
            import qdrant_client  # noqa: F401
        except ImportError as err:
            raise ImportError(
                "The qdrant-client package is required for using Qdrant as the vector store backend for Mem0. "
                "Please install it using: pip install qdrant-client"
            ) from err
        
        merged_config = self._merge_config(config)
        
        # Determine workspace name for collection isolation
        # Sanitize workspace name to be valid for Qdrant collection names
        workspace_name = os.path.basename(os.getcwd())
        workspace_name = workspace_name.replace('-', '_').replace('.', '_').replace(' ', '_')
        collection_name = f"mem0_{workspace_name}"
        
        # Determine embedding dimensions
        embedding_dims = 768 if "ollama" in merged_config["embedder"]["provider"] else 1024
        
        # Check for server mode (host/port)
        if os.environ.get("QDRANT_HOST"):
            logger.info(f"Initializing Qdrant in server mode: {os.environ['QDRANT_HOST']}:{os.environ.get('QDRANT_PORT', '6333')}")
            logger.info(f"Using collection: {collection_name}")
            
            merged_config["vector_store"] = {
                "provider": "qdrant",
                "config": {
                    "collection_name": collection_name,
                    "embedding_model_dims": embedding_dims,
                    "host": os.environ["QDRANT_HOST"],
                    "port": int(os.environ.get("QDRANT_PORT", "6333")),
                    "on_disk": True
                }
            }
        else:
            # Embedded mode - no Docker needed
            qdrant_path = os.environ.get("QDRANT_PATH", ".mem0/qdrant")
            
            logger.info(f"Initializing Qdrant in embedded mode: {qdrant_path}")
            logger.info(f"Using collection: {collection_name}")
            
            # Ensure directory exists and is writable
            try:
                os.makedirs(qdrant_path, exist_ok=True)
            except (OSError, PermissionError):
                import tempfile
                qdrant_path = os.path.join(tempfile.gettempdir(), "mem0_qdrant")
                os.makedirs(qdrant_path, exist_ok=True)
                logger.warning(f"Could not create Qdrant directory, using temp: {qdrant_path}")
            
            merged_config["vector_store"] = {
                "provider": "qdrant",
                "config": {
                    "collection_name": collection_name,
                    "embedding_model_dims": embedding_dims,
                    "path": qdrant_path,
                    "on_disk": True
                }
            }
        
        # Add graph store if configured
        merged_config = self._add_graph_store_if_configured(merged_config)
        
        # Debug: Log the final config
        logger.info(f"Final Qdrant config: vector_store={merged_config.get('vector_store', {}).get('config', {})}")
        if 'graph_store' in merged_config:
            logger.info(f"Graph store enabled: {merged_config['graph_store']}")
        
        return Mem0Memory.from_config(config_dict=merged_config)

    def _init_opensearch(self, config: Optional[Dict] = None):
        """Initialize OpenSearch backend with optimized boto3 config."""
        region = os.environ.get("AWS_REGION", "us-west-2")
        session = boto3.Session()
        credentials = session.get_credentials()
        auth = AWSV4SignerAuth(credentials, region, "aoss")
        
        merged_config = self._merge_config(config)
        merged_config["vector_store"]["config"].update({
            "http_auth": auth,
            "host": os.environ["OPENSEARCH_HOST"],
            "timeout": 30,  # Add explicit timeout
            "max_retries": 3,  # Add retry configuration
        })
        
        return Mem0Memory.from_config(config_dict=merged_config)

    def _init_faiss(self, config: Optional[Dict] = None):
        """Initialize FAISS backend."""
        try:
            import faiss  # noqa: F401
        except ImportError as err:
            raise ImportError(
                "The faiss-cpu package is required for using FAISS as the vector store backend for Mem0. "
                "Please install it using: pip install faiss-cpu"
            ) from err
            
        merged_config = self._merge_config(config)
        
        # Use configurable FAISS path with proper fallback
        faiss_path = os.environ.get("FAISS_PATH", ".mem0/memory")
        
        # Ensure the directory exists and is writable
        try:
            os.makedirs(faiss_path, exist_ok=True)
        except (OSError, PermissionError):
            import tempfile
            faiss_path = os.path.join(tempfile.gettempdir(), "mem0_agent")
            os.makedirs(faiss_path, exist_ok=True)
        
        # Ensure the path ends with the index filename
        if not faiss_path.endswith('.faiss'):
            faiss_path = os.path.join(faiss_path, "agent_memory.faiss")
        
        merged_config["vector_store"] = {
            "provider": "faiss",
            "config": {
                # Bedrock Titan = 1024, Ollama nomic-embed-text = 768
                "embedding_model_dims": 1024 if "bedrock" in merged_config["embedder"]["provider"] else 768,
                "path": faiss_path
            }
        }
        
        # Create mem0 client
        mem0_client = Mem0Memory.from_config(config_dict=merged_config)
        
        # Patch Ollama embedder to add task prefixes if enabled
        if os.environ.get("OLLAMA_HOST") and os.environ.get("NOMIC_USE_PREFIXES", "false").lower() == "true":
            logger.info("Patching Ollama embedder to add Nomic task prefixes")
            self._patch_ollama_embedder(mem0_client)
        
        return mem0_client
    
    def _patch_ollama_embedder(self, mem0_client):
        """Patch mem0's Ollama embedder to add Nomic task prefixes."""
        try:
            # Access the embedder through mem0's internal structure
            embedder = mem0_client.embedding_model
            
            # Store original methods
            original_embed = embedder.embed
            
            # Create patched version that adds prefixes
            def patched_embed(text: str, *args, **kwargs):
                # Determine if this is a query or document based on context
                # Default to document for storage operations
                prefix = "search_document: "
                
                # Check if this is a search operation (heuristic)
                import inspect
                frame = inspect.currentframe()
                if frame and frame.f_back:
                    caller_name = frame.f_back.f_code.co_name
                    if 'search' in caller_name.lower():
                        prefix = "search_query: "
                
                prefixed_text = f"{prefix}{text}"
                return original_embed(prefixed_text, *args, **kwargs)
            
            # Replace the embed method
            embedder.embed = patched_embed
            logger.info("Successfully patched Ollama embedder with Nomic prefixes")
            
        except Exception as e:
            logger.warning(f"Failed to patch Ollama embedder: {e}. Continuing without prefixes.")


    def _merge_config(self, config: Optional[Dict] = None) -> Dict:
        """Deep merge user config with defaults."""
        merged_config = copy.deepcopy(self._get_default_config())
        
        if not config:
            return merged_config

        for key, value in config.items():
            if key in merged_config and isinstance(value, dict) and isinstance(merged_config[key], dict):
                merged_config[key].update(value)
            else:
                merged_config[key] = value
        return merged_config
    
    def _add_graph_store_if_configured(self, config: Dict) -> Dict:
        """Add KuzuDB graph store if KUZU_DB_PATH is set."""
        if os.environ.get("KUZU_DB_PATH"):
            kuzu_path = os.environ["KUZU_DB_PATH"]
            logger.info(f"Enabling KuzuDB graph store: {kuzu_path}")
            
            # Ensure directory exists for file-based storage
            if kuzu_path != ":memory:":
                kuzu_dir = os.path.dirname(kuzu_path) if os.path.dirname(kuzu_path) else "."
                try:
                    os.makedirs(kuzu_dir, exist_ok=True)
                except (OSError, PermissionError):
                    import tempfile
                    kuzu_path = os.path.join(tempfile.gettempdir(), "mem0_kuzu.db")
                    logger.warning(f"Could not create Kuzu directory, using temp: {kuzu_path}")
            
            config["graph_store"] = {
                "provider": "kuzu",
                "config": {
                    "db": kuzu_path
                }
            }
        return config


def _get_user_id():
    """Get user ID from cached env var or system user."""
    return _CACHED_USER_ID or getpass.getuser()


def _get_agent_id():
    """Get agent ID from cached env var or workspace name."""
    return _CACHED_AGENT_ID or os.path.basename(os.getcwd())


def _get_run_id():
    """Get run ID from cached env var."""
    return _CACHED_RUN_ID


def _fetch_all_memories(mem0_client, user_id: Optional[str] = None, agent_id: Optional[str] = None, run_id: Optional[str] = None, limit: int = 10000) -> list:
    """Helper to fetch all memories with consistent response handling.
    
    Returns a list of memories, handling both dict and list response formats.
    Default limit is 10000 to avoid mem0's default 100 limit.
    """
    kwargs: Dict[str, Any] = {"limit": limit}
    if user_id:
        kwargs["user_id"] = user_id
    if agent_id:
        kwargs["agent_id"] = agent_id
    if run_id:
        kwargs["run_id"] = run_id
    
    response = mem0_client.get_all(**kwargs)
    
    if isinstance(response, dict) and "results" in response:
        return response.get("results", [])
    elif isinstance(response, list):
        return response
    else:
        return response.get("results", []) if isinstance(response, dict) else []


# =============================================================================
# LAZY CLIENT INITIALIZATION & CACHING
# =============================================================================

_mem0_client: Optional[Any] = None
_client_init_error: Optional[str] = None

# Cache environment variables at module load
_CACHED_USER_ID = os.environ.get("MEM0_USER_ID")
_CACHED_AGENT_ID = os.environ.get("MEM0_AGENT_ID")
_CACHED_RUN_ID = os.environ.get("MEM0_RUN_ID")
_CACHED_INFER_DEFAULT = os.environ.get("MEM0_INFER_DEFAULT", "true").lower() == "true"
_CACHED_VERBOSE_DEFAULT = os.environ.get("MEM0_VERBOSE", "false").lower() == "true"
_CACHED_MAX_RELATIONS = int(os.environ.get("MEM0_MAX_RELATIONS", "20"))


def _truncate_relations(relations: Any, max_relations: int = None) -> Dict[str, Any]:
    """Truncate relations array for compact mode to prevent token bloat.
    
    Args:
        relations: Relations data (list or dict)
        max_relations: Maximum number of relations to include (default: from env or 20)
    
    Returns:
        Dict with truncated relations and metadata
    """
    if max_relations is None:
        max_relations = _CACHED_MAX_RELATIONS
    
    # Handle list of relations (search results)
    if isinstance(relations, list):
        total_count = len(relations)
        if total_count <= max_relations:
            return {"relations": relations}
        
        return {
            "relations": relations[:max_relations],
            "relations_truncated": True,
            "relations_total": total_count,
            "relations_showing": max_relations
        }
    
    # Handle dict with added_entities/deleted_entities (store_memory results)
    if isinstance(relations, dict):
        if "added_entities" in relations or "deleted_entities" in relations:
            added = relations.get("added_entities", [])
            deleted = relations.get("deleted_entities", [])
            total_added = len(added)
            total_deleted = len(deleted)
            total_count = total_added + total_deleted
            
            if total_count <= max_relations:
                return {"relations": relations}
            
            # Truncate proportionally
            if total_count > 0:
                added_limit = int(max_relations * (total_added / total_count))
                deleted_limit = max_relations - added_limit
            else:
                added_limit = deleted_limit = max_relations // 2
            
            return {
                "relations": {
                    "added_entities": added[:added_limit] if added else [],
                    "deleted_entities": deleted[:deleted_limit] if deleted else []
                },
                "relations_truncated": True,
                "relations_total": {"added": total_added, "deleted": total_deleted},
                "relations_showing": {"added": min(added_limit, total_added), "deleted": min(deleted_limit, total_deleted)}
            }
    
    # Unknown format, return as-is
    return {"relations": relations}


def _format_memory_compact(memory: Dict[str, Any]) -> Dict[str, Any]:
    """Format memory for compact (non-verbose) output.
    
    Returns only essential fields for agent context efficiency:
    - id: for reference
    - memory: the actual content
    - metadata: for filtering/organization
    - score: for relevance (if present)
    - relations: graph relationships (if present)
    """
    compact = {
        "id": memory.get("id"),
        "memory": memory.get("memory"),
    }
    
    # Include metadata if present
    if memory.get("metadata"):
        compact["metadata"] = memory["metadata"]
    
    # Include score if present (for search results)
    if "score" in memory:
        compact["score"] = memory["score"]
    
    # Include graph relations if present (Kuzu graph store)
    if "relations" in memory:
        compact["relations"] = memory["relations"]
    
    return compact


def _format_response(data: Any, verbose: bool = False) -> str:
    """Format response based on verbose mode.
    
    Args:
        data: Response data (dict, list, or string)
        verbose: If True, return full details. If False, return compact format.
    
    Returns:
        JSON string with appropriate formatting
    """
    if verbose or _CACHED_VERBOSE_DEFAULT:
        # Verbose mode: return everything
        return json.dumps(data, indent=2)
    
    # Compact mode: optimize for agent context
    if isinstance(data, dict):
        # Handle memory search/list responses
        if "memories" in data:
            compact_memories = [_format_memory_compact(m) for m in data["memories"]]
            result = {
                "memories": compact_memories,
                "count": len(compact_memories)
            }
            
            # Include pagination only if there are multiple pages
            if "pagination" in data:
                pag = data["pagination"]
                if pag.get("total_pages", 1) > 1:
                    result["pagination"] = {
                        "page": pag["current_page"],
                        "total": pag["total_items"],
                        "has_more": pag.get("has_next", False)
                    }
            
            # Include metadata search info if present (search_by_metadata)
            if "filters_applied" in data:
                result["filters"] = data["filters_applied"]
            if "total_matched" in data:
                result["total_matched"] = data["total_matched"]
            
            # Include graph relations if present (Kuzu graph store)
            # Truncate in compact mode to prevent token bloat
            if "relations" in data:
                relations_data = _truncate_relations(data["relations"])
                result.update(relations_data)
            
            return json.dumps(result, indent=2)
        
        # Handle recent_memories responses
        if "recent_memories" in data:
            compact_memories = [_format_memory_compact(m) for m in data["recent_memories"]]
            result = {
                "memories": compact_memories,
                "count": len(compact_memories)
            }
            
            # Include summary if present
            if "summary" in data:
                result["summary"] = {
                    "days": data["summary"].get("days_searched"),
                    "total": data["summary"].get("total_found")
                }
            
            return json.dumps(result, indent=2)
        
        # Handle single memory responses
        if "id" in data and "memory" in data:
            return json.dumps(_format_memory_compact(data), indent=2)
    
    # Default: return as-is
    return json.dumps(data, indent=2) if not isinstance(data, str) else data


def _get_mem0_client():
    """Get or initialize the Mem0 client lazily.
    
    For FAISS backend, always creates a fresh client to ensure index is loaded from disk.
    For Platform/OpenSearch backends, caches the client for performance.
    
    Returns the client on success, raises RuntimeError with clear message on failure.
    """
    global _mem0_client, _client_init_error
    
    # For FAISS backend, don't cache - always create fresh client to reload index
    is_faiss = not os.environ.get("MEM0_API_KEY") and not os.environ.get("OPENSEARCH_HOST")
    
    if not is_faiss and _mem0_client is not None:
        return _mem0_client
    
    if _client_init_error is not None:
        raise RuntimeError(_client_init_error)
    
    try:
        client = Mem0ServiceClient().mem0
        
        # Only cache for non-FAISS backends
        if not is_faiss:
            _mem0_client = client
        
        return client
    except Exception as e:
        # Build helpful error message based on detected backend
        if os.environ.get("MEM0_API_KEY"):
            backend = "Mem0 Platform"
            hint = "Check your MEM0_API_KEY is valid"
        elif os.environ.get("OPENSEARCH_HOST"):
            backend = "OpenSearch"
            hint = "Check OPENSEARCH_HOST and AWS credentials"
        elif os.environ.get("OLLAMA_HOST"):
            backend = "Ollama + FAISS"
            hint = f"Check Ollama is running at {os.environ.get('OLLAMA_HOST')}"
        elif os.environ.get("LMSTUDIO_HOST"):
            backend = "LM Studio + FAISS"
            hint = f"Check LM Studio is running at {os.environ.get('LMSTUDIO_HOST')}"
        else:
            backend = "AWS Bedrock + FAISS"
            hint = "Check AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)"
        
        _client_init_error = (
            f"Failed to initialize {backend} backend: {str(e)}\n"
            f"Hint: {hint}"
        )
        logger.error(_client_init_error)
        raise RuntimeError(_client_init_error) from e


# =============================================================================
# TOOLS
# =============================================================================

@mcp.tool(
    description="""Store memory content with metadata support. 

REQUIRED: Either 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
REQUIRED: 'content' - the information to remember

OPTIONAL: 'metadata' - structured data about the memory (JSON object)
OPTIONAL: 'infer' - if True (default), uses LLM to extract facts and dedupe. Set False for faster raw storage.
OPTIONAL: 'run_id' - session/run identifier for temporary context
OPTIONAL: 'custom_instructions' - per-call instructions to control what gets stored
OPTIONAL: 'verbose' - if True, return full details. If False (default), return compact response.

Examples:
- Store personal info: {"content": "User prefers React over Vue", "user_id": "john"}  
- Store with metadata: {"content": "API endpoint changed", "metadata": {"type": "technical", "priority": "high"}}
- Fast storage (no LLM): {"content": "Quick note", "infer": false}
- Session-scoped: {"content": "Current task context", "run_id": "session_123"}

Use for: Storing code patterns, user preferences, project details, technical knowledge.

Note: With infer=True (default), mem0 uses an LLM to extract key facts and intelligently 
update existing memories. This is slower (~5-15s) but smarter. Use infer=False for 
faster raw storage (~1-2s) without deduplication.

Config: Set MEM0_INFER_DEFAULT=false in env to disable infer by default.
Config: Set MEM0_VERBOSE=true in env to enable verbose responses by default.

Returns: Success message with memory ID (compact) or full details (verbose)."""
)
async def store_memory(
    content: str,
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    infer: Optional[bool] = None,
    custom_instructions: Optional[str] = None,
    verbose: bool = False
) -> str:
    """Store memory content."""
    try:
        # Validate content
        if not content or not content.strip():
            return json.dumps({"error": "Content cannot be empty"}, indent=2)
        
        if len(content) > 100000:  # 100KB limit
            return json.dumps({
                "error": "Content too large",
                "max_size": "100KB",
                "actual_size": f"{len(content)} bytes"
            }, indent=2)
        
        # Validate metadata
        if metadata:
            if not isinstance(metadata, dict):
                return json.dumps({"error": "Metadata must be a JSON object"}, indent=2)
            
            # Validate metadata keys (prevent injection)
            for key in metadata.keys():
                if not isinstance(key, str) or not key.replace('_', '').replace('-', '').isalnum():
                    return json.dumps({
                        "error": f"Invalid metadata key: {key}",
                        "hint": "Keys must be alphanumeric with underscores/hyphens only"
                    }, indent=2)
        
        mem0_client = _get_mem0_client()
        
        # Use cached env var default if infer not explicitly set
        if infer is None:
            infer = _CACHED_INFER_DEFAULT
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        # Use env default for run_id if not provided
        if run_id is None:
            run_id = _get_run_id()
        
        messages = [{"role": "user", "content": content}]
        
        # Build kwargs, only include non-None values
        kwargs: Dict[str, Any] = {
            "user_id": user_id,
            "agent_id": agent_id,
            "metadata": metadata,
            "infer": infer
        }
        if run_id:
            kwargs["run_id"] = run_id
        if custom_instructions:
            kwargs["custom_instructions"] = custom_instructions
        
        result = mem0_client.add(messages, **kwargs)
        
        # Compact response for agents
        if not verbose and not _CACHED_VERBOSE_DEFAULT:
            if isinstance(result, dict) and "results" in result:
                memory_ids = [r.get("id") for r in result["results"] if r.get("id")]
                compact_result = {
                    "status": "success",
                    "memory_ids": memory_ids,
                    "count": len(memory_ids)
                }
                
                # Include graph relations if present (Kuzu graph store)
                # Truncate to prevent token bloat
                if "relations" in result:
                    relations_data = _truncate_relations(result["relations"])
                    compact_result.update(relations_data)
                
                return json.dumps(compact_result, indent=2)
        
        return f"Memory stored successfully: {json.dumps(result, indent=2)}"
    except Exception as e:
        logger.exception("Error storing memory")
        return f"Error storing memory: {str(e)}"


@mcp.tool(
    description="""Search memories with semantic similarity and relevance filtering.

REQUIRED: 'query' - what to search for (natural language)
OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
OPTIONAL: 'run_id' - filter by session/run identifier
OPTIONAL: 'limit' - max results to return (default: 10, also sets page_size if not specified)
OPTIONAL: 'page' - page number for pagination (default: 1)
OPTIONAL: 'page_size' - results per page (default: uses limit value)

Returns: Relevant memories filtered by maximum score threshold (configurable via MEM0_MAX_RELEVANCE_SCORE, default: 1000)

Score interpretation (FAISS uses L2 distance - lower is more similar):
- 0-100: Very high similarity (near-exact matches)
- 100-400: High similarity (closely related)
- 400-600: Moderate similarity (somewhat related)
- 600-1000: Low similarity (loosely related)
- 1000+: Very low similarity (likely unrelated)

Note: Default threshold of 1000 keeps reasonably similar results. Lower to 400-600 for stricter filtering.

Examples:
- Search user memories: {"query": "React patterns", "user_id": "john"}
- Auto-detect user: {"query": "my project status"} 
- Limit results: {"query": "API endpoints", "limit": 3}
- Session-scoped: {"query": "current task", "run_id": "session_123"}
- Pagination: {"query": "all tasks", "page": 2, "page_size": 5}

Use for: Finding relevant code, recalling user preferences, retrieving project context."""
)
async def search_memories(
    query: str,
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None,
    limit: int = 10,
    page: int = 1,
    page_size: Optional[int] = None,
    verbose: bool = False
) -> str:
    """Search memories with pagination."""
    try:
        mem0_client = _get_mem0_client()
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        # Use env default for run_id if not provided
        if run_id is None:
            run_id = _get_run_id()
        
        # If page_size not specified, use limit as page_size
        if page_size is None:
            page_size = limit
        
        search_limit = max(limit, page_size * page + 50)
        
        # Build kwargs, only include non-None values
        kwargs: Dict[str, Any] = {
            "query": query,
            "user_id": user_id,
            "agent_id": agent_id,
            "limit": search_limit
        }
        if run_id:
            kwargs["run_id"] = run_id
        
        response = mem0_client.search(**kwargs)
        
        if isinstance(response, dict) and "results" in response:
            memories = response.get("results", [])
            # Preserve top-level relations if present (graph store)
            top_level_relations = response.get("relations")
        else:
            memories = response if isinstance(response, list) else []
            top_level_relations = None
        
        # Filter by relevance score (FAISS uses L2 distance: lower = more similar)
        # Default threshold of 1000 keeps reasonably similar results
        max_score = float(os.environ.get("MEM0_MAX_RELEVANCE_SCORE", "1000"))
        filtered_memories = [m for m in memories if m.get("score", float('inf')) < max_score]
        
        # Pagination
        total_items = len(filtered_memories)
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_memories = filtered_memories[start_idx:end_idx]
        
        result = {
            "memories": paginated_memories,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_items": total_items,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
        
        # Add top-level relations if present (graph store)
        if top_level_relations is not None:
            result["relations"] = top_level_relations
        
        return _format_response(result, verbose)
    except Exception as e:
        logger.exception("Error searching memories")
        return f"Error searching memories: {str(e)}"


@mcp.tool(
    description="""List all memories for a user or agent with pagination.

OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
OPTIONAL: 'run_id' - filter by session/run identifier
OPTIONAL: 'page', 'page_size' - pagination controls (default: page_size=25)

Returns: All memories belonging to the specified user/agent, sorted by creation date."""
)
async def list_memories(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 25
,
    verbose: bool = False
) -> str:
    """List all memories with pagination."""
    try:
        mem0_client = _get_mem0_client()
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        # Use env default for run_id if not provided
        if run_id is None:
            run_id = _get_run_id()
        
        all_memories = _fetch_all_memories(mem0_client, user_id, agent_id, run_id)
        
        total_items = len(all_memories)
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_memories = all_memories[start_idx:end_idx]
        
        result = {
            "memories": paginated_memories,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_items": total_items,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
        
        return _format_response(result, verbose)
    except Exception as e:
        logger.exception("Error listing memories")
        return f"Error listing memories: {str(e)}"


@mcp.tool(
    description="""Get specific memory by its unique ID.

REQUIRED: 'memory_id' - the UUID of the memory to retrieve

Returns: Complete memory details including content, metadata, timestamps."""
)
async def get_memory(memory_id: str,
    verbose: bool = False
) -> str:
    """Get memory by ID."""
    try:
        mem0_client = _get_mem0_client()
        memory = mem0_client.get(memory_id)
        return _format_response(memory, verbose)
    except Exception as e:
        logger.exception("Error getting memory")
        return f"Error getting memory: {str(e)}"


@mcp.tool(
    description="""Delete memory by its unique ID. PERMANENT deletion.

REQUIRED: 'memory_id' - the UUID of the memory to delete

⚠️  WARNING: This permanently removes the memory and cannot be undone."""
)
async def delete_memory(memory_id: str,
    verbose: bool = False
) -> str:
    """Delete memory by ID."""
    try:
        mem0_client = _get_mem0_client()
        mem0_client.delete(memory_id)
        if not verbose and not _CACHED_VERBOSE_DEFAULT:
            return json.dumps({"status": "success", "deleted_id": memory_id}, indent=2)
        return f"Memory {memory_id} deleted successfully"
    except Exception as e:
        logger.exception("Error deleting memory")
        return f"Error deleting memory: {str(e)}"


@mcp.tool(
    description="""Get change history for a specific memory by ID.

REQUIRED: 'memory_id' - the UUID of the memory to get history for

Returns: Chronological list of all changes made to the memory."""
)
async def get_memory_history(memory_id: str,
    verbose: bool = False
) -> str:
    """Get memory history by ID."""
    try:
        mem0_client = _get_mem0_client()
        history = mem0_client.history(memory_id)
        return json.dumps(history, indent=2)
    except Exception as e:
        logger.exception("Error getting memory history")
        return f"Error getting memory history: {str(e)}"


@mcp.tool(
    description="""Update an existing memory's content and/or metadata directly.

REQUIRED: 'memory_id' - the UUID of the memory to update
REQUIRED: 'content' - the new content for the memory

OPTIONAL: 'metadata' - new metadata to replace existing (JSON object)

Unlike store_memory with infer=true, this directly updates the specified memory
without LLM processing or deduplication. Preserves memory history.

Examples:
- Update content: {"memory_id": "abc-123", "content": "Updated preference: Vue over React"}
- Update with metadata: {"memory_id": "abc-123", "content": "New content", "metadata": {"priority": "high"}}

Returns: Updated memory details."""
)
async def update_memory(
    memory_id: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
,
    verbose: bool = False
) -> str:
    """Update an existing memory directly."""
    try:
        mem0_client = _get_mem0_client()
        result = mem0_client.update(memory_id=memory_id, data=content)
        
        # If metadata provided, we need to delete and re-add since mem0 doesn't support metadata update
        # For now, just note this limitation in the response
        response = {"updated_memory": result}
        if metadata:
            response["note"] = "Metadata update not supported by mem0 API. Content updated, metadata unchanged."
        
        return f"Memory updated successfully: {json.dumps(response, indent=2)}"
    except Exception as e:
        logger.exception("Error updating memory")
        return f"Error updating memory: {str(e)}"


@mcp.tool(
    description="""Get statistics about stored memories.

OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)

Returns: Memory counts by metadata type, date ranges, and storage summary.

Use for: Understanding memory usage, identifying cleanup opportunities, monitoring growth."""
)
async def get_memory_stats(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None
,
    verbose: bool = False
) -> str:
    """Get statistics about stored memories."""
    try:
        mem0_client = _get_mem0_client()
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        all_memories = _fetch_all_memories(mem0_client, user_id, agent_id)
        
        # Count by metadata type
        type_counts: Dict[str, int] = {}
        priority_counts: Dict[str, int] = {}
        memories_with_metadata = 0
        oldest_date = None
        newest_date = None
        
        for memory in all_memories:
            metadata = memory.get("metadata") or {}
            if metadata:
                memories_with_metadata += 1
                mem_type = metadata.get("type", "untyped")
                type_counts[mem_type] = type_counts.get(mem_type, 0) + 1
                priority = metadata.get("priority")
                if priority:
                    priority_counts[priority] = priority_counts.get(priority, 0) + 1
            else:
                type_counts["untyped"] = type_counts.get("untyped", 0) + 1
            
            # Track date range
            created = memory.get("created_at")
            if created:
                try:
                    clean_date = created.replace("Z", "+00:00")
                    mem_date = datetime.fromisoformat(clean_date).replace(tzinfo=None)
                    if oldest_date is None or mem_date < oldest_date:
                        oldest_date = mem_date
                    if newest_date is None or mem_date > newest_date:
                        newest_date = mem_date
                except (ValueError, TypeError):
                    pass
        
        result = {
            "total_memories": len(all_memories),
            "memories_with_metadata": memories_with_metadata,
            "by_type": type_counts,
            "by_priority": priority_counts,
            "date_range": {
                "oldest": oldest_date.isoformat() if oldest_date else None,
                "newest": newest_date.isoformat() if newest_date else None
            },
            "user_id": user_id,
            "agent_id": agent_id
        }
        
        return _format_response(result, verbose)
    except Exception as e:
        logger.exception("Error getting memory stats")
        return f"Error getting memory stats: {str(e)}"


@mcp.tool(
    description="""Delete multiple memories matching filter criteria. PERMANENT deletion.

OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
OPTIONAL: 'run_id' - filter by session/run identifier
OPTIONAL: 'metadata_type' - delete memories with this metadata type (e.g., "test", "note")
OPTIONAL: 'older_than_days' - delete memories older than this many days
OPTIONAL: 'dry_run' - if True, returns what would be deleted without actually deleting (default: True)

⚠️  WARNING: Set dry_run=False to actually delete. This cannot be undone.

Examples:
- Preview test cleanup: {"metadata_type": "test", "dry_run": true}
- Delete old memories: {"older_than_days": 90, "dry_run": false}
- Delete by type: {"metadata_type": "note", "dry_run": false}

Returns: List of deleted (or would-be-deleted) memory IDs."""
)
async def bulk_delete_memories(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None,
    metadata_type: Optional[str] = None,
    older_than_days: Optional[int] = None,
    dry_run: bool = True
,
    verbose: bool = False
) -> str:
    """Delete multiple memories matching filter criteria."""
    try:
        mem0_client = _get_mem0_client()
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        # Use env default for run_id if not provided
        if run_id is None:
            run_id = _get_run_id()
        
        if not metadata_type and not older_than_days:
            return "Error: Must specify at least one filter (metadata_type or older_than_days)"
        
        all_memories = _fetch_all_memories(mem0_client, user_id, agent_id, run_id)
        
        cutoff_date = None
        if older_than_days:
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
        
        to_delete = []
        for memory in all_memories:
            should_delete = False
            
            # Check metadata type filter
            if metadata_type:
                metadata = memory.get("metadata") or {}
                if metadata.get("type") == metadata_type:
                    should_delete = True
            
            # Check age filter
            if older_than_days and cutoff_date:
                created = memory.get("created_at")
                if created:
                    try:
                        clean_date = created.replace("Z", "+00:00")
                        mem_date = datetime.fromisoformat(clean_date).replace(tzinfo=None)
                        if mem_date < cutoff_date:
                            should_delete = True
                    except (ValueError, TypeError):
                        pass
            
            if should_delete:
                to_delete.append({
                    "id": memory.get("id"),
                    "memory": memory.get("memory", "")[:100],
                    "created_at": memory.get("created_at"),
                    "metadata": memory.get("metadata")
                })
        
        if dry_run:
            return json.dumps({
                "dry_run": True,
                "would_delete": len(to_delete),
                "memories": to_delete,
                "message": "Set dry_run=false to actually delete these memories"
            }, indent=2)
        
        # Actually delete
        deleted_ids = []
        errors = []
        for memory in to_delete:
            try:
                mem0_client.delete(memory["id"])
                deleted_ids.append(memory["id"])
            except Exception as e:
                errors.append({"id": memory["id"], "error": str(e)})
        
        return json.dumps({
            "deleted": len(deleted_ids),
            "deleted_ids": deleted_ids,
            "errors": errors if errors else None
        }, indent=2)
    except Exception as e:
        logger.exception("Error in bulk delete")
        return f"Error in bulk delete: {str(e)}"


@mcp.tool(
    description="""Export memories to JSON or Markdown format for backup or migration.

OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
OPTIONAL: 'format' - output format: "json" (default) or "markdown"
OPTIONAL: 'include_metadata' - include metadata in export (default: True)
OPTIONAL: 'output_path' - custom file path (default: .mem0/exports/memories_<timestamp>.<ext>)
OPTIONAL: 'return_content' - if True, returns content instead of writing to file (default: False)

Returns: File path where export was saved, or content if return_content=True.

Use for: Backup, migration between backends, documentation, sharing."""
)
async def export_memories(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    format: str = "json",
    include_metadata: bool = True,
    output_path: Optional[str] = None,
    return_content: bool = False
,
    verbose: bool = False
) -> str:
    """Export memories to JSON or Markdown format."""
    try:
        mem0_client = _get_mem0_client()
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        all_memories = _fetch_all_memories(mem0_client, user_id, agent_id)
        
        # Generate content
        if format.lower() == "markdown":
            ext = "md"
            lines = [
                f"# Memory Export",
                f"",
                f"**User:** {user_id}",
                f"**Agent:** {agent_id}",
                f"**Exported:** {datetime.now().isoformat()}",
                f"**Total Memories:** {len(all_memories)}",
                f"",
                "---",
                ""
            ]
            
            for i, memory in enumerate(all_memories, 1):
                lines.append(f"## Memory {i}")
                lines.append(f"")
                lines.append(f"**ID:** `{memory.get('id')}`")
                lines.append(f"**Created:** {memory.get('created_at', 'N/A')}")
                if memory.get('updated_at'):
                    lines.append(f"**Updated:** {memory.get('updated_at')}")
                lines.append(f"")
                lines.append(f"> {memory.get('memory', '')}")
                lines.append(f"")
                
                if include_metadata and memory.get('metadata'):
                    lines.append(f"**Metadata:**")
                    lines.append(f"```json")
                    lines.append(json.dumps(memory.get('metadata'), indent=2))
                    lines.append(f"```")
                    lines.append(f"")
                
                lines.append("---")
                lines.append("")
            
            content = "\n".join(lines)
        else:
            ext = "json"
            export_data = {
                "export_info": {
                    "user_id": user_id,
                    "agent_id": agent_id,
                    "exported_at": datetime.now().isoformat(),
                    "total_memories": len(all_memories),
                    "format_version": "1.0"
                },
                "memories": all_memories if include_metadata else [
                    {"id": m.get("id"), "memory": m.get("memory"), "created_at": m.get("created_at")}
                    for m in all_memories
                ]
            }
            content = json.dumps(export_data, indent=2)
        
        # Return content directly if requested
        if return_content:
            return content
        
        # Write to file
        if output_path:
            filepath = output_path
        else:
            # Default: .mem0/exports/memories_<timestamp>.<ext>
            export_dir = os.path.join(".mem0", "exports")
            os.makedirs(export_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"memories_{user_id or 'default'}_{timestamp}.{ext}"
            filepath = os.path.join(export_dir, filename)
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return json.dumps({
            "status": "success",
            "file_path": filepath,
            "format": format,
            "total_memories": len(all_memories),
            "file_size_bytes": len(content.encode('utf-8'))
        }, indent=2)
    except Exception as e:
        logger.exception("Error exporting memories")
        return f"Error exporting memories: {str(e)}"


@mcp.tool(
    description="""Search memories by metadata fields without semantic search.

OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
OPTIONAL: 'type' - filter by metadata type (e.g., "decision", "preference", "task_completion")
OPTIONAL: 'priority' - filter by priority (e.g., "high", "medium", "low")
OPTIONAL: 'status' - filter by status (e.g., "complete", "in_progress", "blocked")
OPTIONAL: 'custom_filters' - dict of additional metadata key-value pairs to match
OPTIONAL: 'page' - page number for pagination (default: 1)
OPTIONAL: 'page_size' - results per page (default: 50, max: 100)

Returns: Memories matching all specified filters with pagination.

Examples:
- Find decisions: {"type": "decision"}
- Find high priority: {"priority": "high"}
- Find blocked items: {"status": "blocked"}
- Custom filter: {"custom_filters": {"category": "api"}}
- Paginated: {"type": "documentation", "page": 2, "page_size": 20}

Note: Uses native Qdrant filtering when available, falls back to post-filtering for other backends."""
)
async def search_by_metadata(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    type: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    custom_filters: Optional[Dict[str, str]] = None,
    page: int = 1,
    page_size: int = 50
,
    verbose: bool = False
) -> str:
    """Search memories by metadata fields with native backend filtering."""
    try:
        mem0_client = _get_mem0_client()
        
        # Validate pagination parameters
        page_size = min(max(1, page_size), 100)  # Clamp between 1 and 100
        page = max(1, page)  # Ensure page is at least 1
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        # Build filters
        filters: Dict[str, str] = {}
        if type:
            filters["type"] = type
        if priority:
            filters["priority"] = priority
        if status:
            filters["status"] = status
        if custom_filters:
            filters.update(custom_filters)
        
        if not filters:
            return json.dumps({
                "error": "No filters specified",
                "hint": "Provide at least one of: type, priority, status, or custom_filters"
            }, indent=2)
        
        mem0_filters = filters
        
        # Determine if we can use native filtering (Qdrant or OpenSearch)
        use_native_filtering = (
            os.environ.get("QDRANT_HOST") or 
            os.environ.get("QDRANT_PATH") or 
            os.environ.get("OPENSEARCH_HOST")
        )
        
        if use_native_filtering:
            # Use native backend filtering with mem0's filter syntax
            # mem0 accepts flat dict for multiple filters (implicit AND)
            # Single filter: {"key": "value"}
            # Multiple filters: {"key1": "value1", "key2": "value2"} (implicit AND)
            
            # Use search with filters
            # Note: search() requires a query parameter, so we use a generic one
            search_limit = page_size * page + 50
            
            kwargs: Dict[str, Any] = {
                "query": "retrieve memories",  # Generic query for metadata-only search
                "user_id": user_id,
                "agent_id": agent_id,
                "filters": mem0_filters,
                "limit": search_limit
            }
            
            response = mem0_client.search(**kwargs)
            
            if isinstance(response, dict) and "results" in response:
                all_matched = response.get("results", [])
            else:
                all_matched = response if isinstance(response, list) else []
            
            # Apply pagination
            total_items = len(all_matched)
            total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_memories = all_matched[start_idx:end_idx]
            
            result = {
                "filters_applied": filters,
                "filtering_method": "native_backend",
                "backend": "Qdrant" if (os.environ.get("QDRANT_HOST") or os.environ.get("QDRANT_PATH")) else "OpenSearch",
                "total_matched": total_items,
                "memories": paginated_memories,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }
            }
            return _format_response(result, verbose)
        else:
            # Fallback to post-filtering for FAISS and Mem0 Platform
            all_memories = _fetch_all_memories(mem0_client, user_id, agent_id)
            
            # Filter memories - must check all to get accurate count
            matched = []
            for memory in all_memories:
                metadata = memory.get("metadata")
                if not metadata:
                    continue
                
                # Check all filters match
                if all(metadata.get(key) == value for key, value in filters.items()):
                    matched.append(memory)
            
            # Pagination
            total_items = len(matched)
            total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_memories = matched[start_idx:end_idx]
            
            result = {
                "filters_applied": filters,
                "filtering_method": "post_filter",
                "backend": "FAISS" if not os.environ.get("MEM0_API_KEY") else "Mem0 Platform",
                "total_matched": total_items,
                "memories": paginated_memories,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }
            }
            return _format_response(result, verbose)
    except Exception as e:
        logger.exception("Error searching by metadata")
        return f"Error searching by metadata: {str(e)}"


@mcp.tool(
    description="""Check the health and connectivity of the memory backend.

Returns: Backend type, connection status, and basic diagnostics.

Use for: Troubleshooting connection issues, verifying configuration."""
)
async def health_check() -> str:
    """Check backend health and connectivity."""
    try:
        start = datetime.now()
        
        # Determine backend type
        if os.environ.get("MEM0_API_KEY"):
            backend = "Mem0 Platform"
        elif os.environ.get("QDRANT_HOST"):
            backend = f"Qdrant Server ({os.environ['QDRANT_HOST']}:{os.environ.get('QDRANT_PORT', '6333')})"
        elif os.environ.get("QDRANT_PATH"):
            qdrant_path = os.environ["QDRANT_PATH"]
            backend = f"Qdrant Embedded (local: {qdrant_path})"
        elif os.environ.get("OPENSEARCH_HOST"):
            backend = f"OpenSearch ({os.environ.get('OPENSEARCH_HOST')})"
        else:
            faiss_path = os.environ.get("FAISS_PATH", ".mem0/memory")
            backend = f"FAISS (local: {faiss_path})"
        
        # Determine model backend
        if os.environ.get("OLLAMA_HOST"):
            model_backend = f"Ollama ({os.environ.get('OLLAMA_HOST')})"
        elif os.environ.get("LMSTUDIO_HOST"):
            model_backend = f"LM Studio ({os.environ.get('LMSTUDIO_HOST')})"
        else:
            model_backend = "AWS Bedrock"
        
        # Try to initialize/get client
        try:
            mem0_client = _get_mem0_client()
            client_status = "connected"
            
            # Try a simple operation
            user_id = _get_user_id()
            agent_id = _get_agent_id()
            all_memories = _fetch_all_memories(mem0_client, user_id, agent_id)
            memory_count = len(all_memories)
            
            operation_status = "ok"
        except Exception as e:
            client_status = "error"
            operation_status = str(e)
            memory_count = None
        
        elapsed = (datetime.now() - start).total_seconds()
        
        result = {
            "status": "healthy" if client_status == "connected" else "unhealthy",
            "vector_store_backend": backend,
            "model_backend": model_backend,
            "client_status": client_status,
            "operation_test": operation_status,
            "memory_count": memory_count,
            "response_time_ms": round(elapsed * 1000, 2),
            "user_id": _get_user_id(),
            "agent_id": _get_agent_id()
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.exception("Error in health check")
        return json.dumps({
            "status": "unhealthy",
            "error": str(e)
        }, indent=2)


@mcp.tool(
    description="""Get recently added or updated memories for session continuity.

OPTIONAL: 'days' - how many days back to search (default: 7)
OPTIONAL: 'limit' - max memories to return (default: 10)
OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
OPTIONAL: 'run_id' - filter by session/run identifier

Returns: Most recently added/updated memories sorted by newest first"""
)
async def get_recent_memories(
    days: int = 7,
    limit: int = 10,
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None
,
    verbose: bool = False
) -> str:
    """Get recently added/updated memories for session continuity."""
    try:
        mem0_client = _get_mem0_client()
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        # Use env default for run_id if not provided
        if run_id is None:
            run_id = _get_run_id()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Build kwargs, only include non-None values
        kwargs: Dict[str, Any] = {
            "query": "recent memories project status updates decisions",
            "user_id": user_id,
            "agent_id": agent_id,
            "limit": limit * 2
        }
        if run_id:
            kwargs["run_id"] = run_id
        
        response = mem0_client.search(**kwargs)
        
        if isinstance(response, dict) and "results" in response:
            memories = response.get("results", [])
        else:
            memories = response if isinstance(response, list) else []
        
        # Filter by date
        def is_recent(memory):
            for date_field in ("updated_at", "created_at"):
                date_str = memory.get(date_field)
                if date_str:
                    try:
                        clean_date = date_str.replace("Z", "+00:00")
                        mem_date = datetime.fromisoformat(clean_date).replace(tzinfo=None)
                        if mem_date >= cutoff_date:
                            return True
                    except (ValueError, TypeError):
                        continue
            return True  # Include if no valid date
        
        filtered = [m for m in memories if is_recent(m)]
        
        # Sort by date
        def get_sort_date(memory):
            return memory.get("updated_at") or memory.get("created_at") or ""
        
        filtered.sort(key=get_sort_date, reverse=True)
        recent_memories = filtered[:limit]
        
        result = {
            "recent_memories": recent_memories,
            "summary": {
                "days_searched": days,
                "total_found": len(recent_memories),
                "date_range": f"Last {days} days (since {cutoff_date.strftime('%Y-%m-%d')})"
            }
        }
        
        return _format_response(result, verbose)
    except Exception as e:
        logger.exception("Error getting recent memories")
        return f"Error getting recent memories: {str(e)}"


# =============================================================================
# STEERING SETUP
# =============================================================================

def _get_steering_content() -> str:
    """Load steering content from the bundled AGENT_GUIDANCE.md file."""
    try:
        from importlib import resources
        pkg_resources = resources.files("mem0_agent_memory")
        content = pkg_resources.joinpath("docs", "AGENT_GUIDANCE.md").read_text(encoding="utf-8")
        if not content.startswith("---"):
            content = "---\ninclusion: always\n---\n\n" + content
        return content
    except FileNotFoundError as e:
        logger.warning(f"AGENT_GUIDANCE.md not found, using fallback content: {e}")
    except ImportError as e:
        logger.warning(f"Failed to import resources module: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error loading steering content: {type(e).__name__}: {e}")
    
    # Fallback content if file loading fails
    return '''---
inclusion: always
---

# Memory-First Protocol

**ALWAYS check memory before starting any task.**

## Session Start
1. Call `get_recent_memories(days=3, limit=5)`
2. Call `search_memories(query="<topic>")`
3. Acknowledge: "Based on recent memory..."

## After Work
```
store_memory(content="Completed: <task>", metadata={"type": "task_completion"})
```
'''


@mcp.tool(
    description="""Delete all memories for a specific scope. PERMANENT deletion.

OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
OPTIONAL: 'run_id' - delete all memories for this session/run

⚠️  WARNING: This permanently removes ALL memories matching the scope. Cannot be undone.

Examples:
- Delete all user memories: {"user_id": "john"}
- Delete session memories: {"run_id": "session_123"}

Returns: Confirmation of deletion with count."""
)
async def delete_all_memories(
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None
,
    verbose: bool = False
) -> str:
    """Delete all memories for a specific scope."""
    try:
        mem0_client = _get_mem0_client()
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        # Use env default for run_id if not provided
        if run_id is None:
            run_id = _get_run_id()
        
        # Build kwargs, only include non-None values
        kwargs: Dict[str, Any] = {}
        if user_id:
            kwargs["user_id"] = user_id
        if agent_id:
            kwargs["agent_id"] = agent_id
        if run_id:
            kwargs["run_id"] = run_id
        
        result = mem0_client.delete_all(**kwargs)
        
        return json.dumps({
            "status": "success",
            "scope": kwargs,
            "result": result
        }, indent=2)
    except Exception as e:
        logger.exception("Error deleting all memories")
        return f"Error deleting all memories: {str(e)}"


@mcp.tool(
    description="""Reset the entire memory store. DESTRUCTIVE operation.

⚠️  CRITICAL WARNING: This deletes ALL memories in the backend, regardless of user/agent/app.
Only use this for testing or when you need to completely clear the memory store.

This operation cannot be undone.

Returns: Confirmation of reset."""
)
async def reset_memory() -> str:
    """Reset the entire memory store."""
    try:
        mem0_client = _get_mem0_client()
        
        # Determine backend for appropriate warning
        if os.environ.get("MEM0_API_KEY"):
            backend = "Mem0 Platform"
        elif os.environ.get("QDRANT_HOST"):
            backend = f"Qdrant Server ({os.environ['QDRANT_HOST']}:{os.environ.get('QDRANT_PORT', '6333')})"
        elif os.environ.get("QDRANT_PATH"):
            backend = f"Qdrant Embedded (local: {os.environ['QDRANT_PATH']})"
        elif os.environ.get("OPENSEARCH_HOST"):
            backend = f"OpenSearch ({os.environ.get('OPENSEARCH_HOST')})"
        else:
            faiss_path = os.environ.get("FAISS_PATH", ".mem0/memory")
            backend = f"FAISS (local: {faiss_path})"
        
        result = mem0_client.reset()
        
        return json.dumps({
            "status": "success",
            "backend": backend,
            "message": "All memories have been permanently deleted",
            "result": result
        }, indent=2)
    except Exception as e:
        logger.exception("Error resetting memory")
        return f"Error resetting memory: {str(e)}"


@mcp.tool(
    description="""Import memories from exported JSON file.

REQUIRED: 'file_path' - path to the JSON export file
OPTIONAL: 'user_id' OR 'agent_id' - override the user/agent from the export file
OPTIONAL: 'skip_existing' - if True, skip memories that already exist (default: True)
OPTIONAL: 'infer' - use LLM processing during import (default: False for speed)

Imports memories from a JSON file created by export_memories tool.
Useful for backup restoration, migration between backends, or sharing memory sets.

Examples:
- Import from backup: {"file_path": ".mem0/exports/memories_john_20250113.json"}
- Import to different user: {"file_path": "export.json", "user_id": "jane"}
- Force reimport: {"file_path": "export.json", "skip_existing": false}

Returns: Import summary with success/failure counts."""
)
async def import_memories(
    file_path: str,
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    skip_existing: bool = True,
    infer: bool = False
,
    verbose: bool = False
) -> str:
    """Import memories from exported JSON file."""
    try:
        mem0_client = _get_mem0_client()
        
        # Read the export file
        if not os.path.exists(file_path):
            return json.dumps({
                "error": f"File not found: {file_path}",
                "hint": "Check the file path and try again"
            }, indent=2)
        
        with open(file_path, "r", encoding="utf-8") as f:
            export_data = json.load(f)
        
        # Validate format
        if "memories" not in export_data:
            return json.dumps({
                "error": "Invalid export format",
                "hint": "File must contain 'memories' array"
            }, indent=2)
        
        memories = export_data["memories"]
        export_info = export_data.get("export_info", {})
        
        # Use provided user/agent or fall back to export file values
        import_user_id = user_id or export_info.get("user_id") or _get_user_id()
        import_agent_id = agent_id or export_info.get("agent_id") or _get_agent_id()
        
        # Get existing memories if skip_existing is True
        existing_ids = set()
        if skip_existing:
            all_memories = _fetch_all_memories(mem0_client, import_user_id, import_agent_id)
            existing_ids = {m.get("id") for m in all_memories}
        
        # Import memories
        imported = []
        skipped = []
        errors = []
        
        for memory in memories:
            memory_id = memory.get("id")
            
            # Skip if already exists
            if skip_existing and memory_id in existing_ids:
                skipped.append(memory_id)
                continue
            
            try:
                content = memory.get("memory", "")
                metadata = memory.get("metadata")
                
                messages = [{"role": "user", "content": content}]
                
                result = mem0_client.add(
                    messages,
                    user_id=import_user_id,
                    agent_id=import_agent_id,
                    metadata=metadata,
                    infer=infer
                )
                
                imported.append({
                    "original_id": memory_id,
                    "new_id": result.get("results", [{}])[0].get("id") if isinstance(result, dict) else None
                })
            except Exception as e:
                errors.append({
                    "memory_id": memory_id,
                    "error": str(e)
                })
        
        return json.dumps({
            "status": "completed",
            "summary": {
                "total_in_file": len(memories),
                "imported": len(imported),
                "skipped": len(skipped),
                "errors": len(errors)
            },
            "imported_to": {
                "user_id": import_user_id,
                "agent_id": import_agent_id
            },
            "imported_memories": imported[:10],  # Show first 10
            "errors": errors if errors else None
        }, indent=2)
    except Exception as e:
        logger.exception("Error importing memories")
        return f"Error importing memories: {str(e)}"


@mcp.tool(
    description="""Ingest documents into memory as a knowledge base using LlamaIndex.

Supports: PDF, DOCX, TXT, MD, HTML, and more. Automatically chunks and stores content.

REQUIRED: 'path' - file path or directory path to ingest
OPTIONAL: 'user_id' OR 'agent_id' (if neither provided, auto-detects current user)
OPTIONAL: 'run_id' - session/run identifier for partitioning
OPTIONAL: 'recursive' - recursively process subdirectories (default: False)
OPTIONAL: 'chunk_size' - max characters per chunk (default: 1024, min: 100, max: 8192)
OPTIONAL: 'chunk_overlap' - overlap between chunks (default: 200, min: 0, max: chunk_size-1)
OPTIONAL: 'file_metadata' - additional metadata to attach to all chunks
OPTIONAL: 'infer' - use LLM for fact extraction (default: False for speed)

Examples:
- Ingest single file: {"path": "/path/to/document.pdf"}
- Ingest directory: {"path": "/path/to/docs", "recursive": true}
- With metadata: {"path": "manual.pdf", "file_metadata": {"type": "documentation", "version": "2.0"}}
- Custom chunking: {"path": "large.pdf", "chunk_size": 2048, "chunk_overlap": 400}

Returns: Summary of ingested documents with chunk counts and memory IDs."""
)
async def ingest_documents(
    path: str,
    user_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    run_id: Optional[str] = None,
    recursive: bool = False,
    chunk_size: int = 1024,
    chunk_overlap: int = 200,
    file_metadata: Optional[Dict[str, Any]] = None,
    infer: bool = False
,
    verbose: bool = False
) -> str:
    """Ingest documents into memory using LlamaIndex."""
    try:
        # Validate chunk parameters
        if chunk_size < 100 or chunk_size > 8192:
            return json.dumps({
                "error": "Invalid chunk_size",
                "hint": "chunk_size must be between 100 and 8192",
                "provided": chunk_size
            }, indent=2)
        
        if chunk_overlap < 0 or chunk_overlap >= chunk_size:
            return json.dumps({
                "error": "Invalid chunk_overlap",
                "hint": f"chunk_overlap must be between 0 and {chunk_size - 1}",
                "provided": chunk_overlap
            }, indent=2)
        
        # Validate file_metadata
        if file_metadata:
            if not isinstance(file_metadata, dict):
                return json.dumps({"error": "file_metadata must be a JSON object"}, indent=2)
            
            for key in file_metadata.keys():
                if not isinstance(key, str) or not key.replace('_', '').replace('-', '').isalnum():
                    return json.dumps({
                        "error": f"Invalid metadata key: {key}",
                        "hint": "Keys must be alphanumeric with underscores/hyphens only"
                    }, indent=2)
        
        # Lazy import to avoid startup overhead
        from llama_index.core import SimpleDirectoryReader
        from llama_index.core.node_parser import SentenceSplitter
        
        mem0_client = _get_mem0_client()
        
        if not user_id and not agent_id:
            user_id = _get_user_id()
            agent_id = _get_agent_id()
        
        if run_id is None:
            run_id = _get_run_id()
        
        # Validate and sanitize path (prevent directory traversal)
        path_obj = Path(path).resolve()
        if not path_obj.exists():
            return json.dumps({
                "error": "Path does not exist",
                "path": str(path_obj)
            }, indent=2)
        
        # Check file size limits (50MB per file, 500MB total)
        MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
        MAX_TOTAL_SIZE = 500 * 1024 * 1024  # 500MB
        
        if path_obj.is_file():
            file_size = path_obj.stat().st_size
            if file_size > MAX_FILE_SIZE:
                return json.dumps({
                    "error": "File too large",
                    "max_size": "50MB",
                    "file_size": f"{file_size / 1024 / 1024:.2f}MB"
                }, indent=2)
            documents = SimpleDirectoryReader(input_files=[str(path_obj)]).load_data()
        else:
            # Check total directory size
            total_size = sum(f.stat().st_size for f in path_obj.rglob('*') if f.is_file())
            if total_size > MAX_TOTAL_SIZE:
                return json.dumps({
                    "error": "Directory too large",
                    "max_size": "500MB",
                    "total_size": f"{total_size / 1024 / 1024:.2f}MB",
                    "hint": "Process subdirectories separately or use smaller batches"
                }, indent=2)
            
            documents = SimpleDirectoryReader(
                input_dir=str(path_obj),
                recursive=recursive
            ).load_data()
        
        if not documents:
            return json.dumps({
                "error": "No documents found",
                "path": str(path_obj),
                "hint": "Check file format is supported (PDF, DOCX, TXT, MD, HTML)"
            }, indent=2)
        
        # Split into chunks
        splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        results: List[Dict[str, Any]] = []
        total_chunks = 0
        errors: List[Dict[str, str]] = []
        
        for doc in documents:
            try:
                chunks = splitter.split_text(doc.text)
                file_name = doc.metadata.get("file_name", "unknown")
                
                for idx, chunk in enumerate(chunks):
                    # Skip empty chunks
                    if not chunk.strip():
                        continue
                    
                    # Build metadata
                    metadata = {
                        "type": "knowledge_base",
                        "source_file": file_name,
                        "chunk_index": idx,
                        "total_chunks": len(chunks)
                    }
                    
                    # Add file metadata if provided
                    if file_metadata:
                        metadata.update(file_metadata)
                    
                    # Add document metadata
                    for key, value in doc.metadata.items():
                        if key not in metadata:
                            metadata[f"doc_{key}"] = value
                    
                    # Store in mem0
                    messages = [{"role": "user", "content": chunk}]
                    kwargs: Dict[str, Any] = {
                        "user_id": user_id,
                        "agent_id": agent_id,
                        "metadata": metadata,
                        "infer": infer
                    }
                    if run_id:
                        kwargs["run_id"] = run_id
                    
                    result = mem0_client.add(messages, **kwargs)
                    total_chunks += 1
                    
                    # Track first chunk of each file
                    if idx == 0:
                        results.append({
                            "file": file_name,
                            "chunks": len(chunks),
                            "first_memory_id": result.get("results", [{}])[0].get("id") if isinstance(result, dict) else None
                        })
            except Exception as e:
                errors.append({
                    "file": doc.metadata.get("file_name", "unknown"),
                    "error": str(e)
                })
                logger.warning(f"Failed to process document {doc.metadata.get('file_name')}: {e}")
        
        summary = {
            "status": "success" if not errors else "partial_success",
            "total_documents": len(documents),
            "total_chunks": total_chunks,
            "successful_files": len(results),
            "failed_files": len(errors),
            "files": results,
            "errors": errors if errors else None,
            "settings": {
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "infer": infer
            }
        }
        
        return json.dumps(summary, indent=2)
        
    except ImportError as e:
        return (
            f"Error: LlamaIndex not installed. Install with:\n"
            f"pip install llama-index llama-index-core pypdf python-docx\n"
            f"Details: {str(e)}"
        )
    except Exception as e:
        logger.exception("Error ingesting documents")
        return f"Error ingesting documents: {str(e)}"


@mcp.tool(
    description="""Setup the memory-first steering file for Kiro.

Creates a steering file at .kiro/steering/memory-first.md that instructs the AI
to always check memory before starting tasks and store important outcomes.

OPTIONAL: 'workspace_path' - path to workspace root (default: current directory)

Call this once after adding the MCP server to enable memory-first workflows.

Returns: Success message with file path created."""
)
async def setup_steering(workspace_path: str = ".") -> str:
    """Create the memory-first steering file in the workspace."""
    try:
        steering_dir = os.path.join(workspace_path, ".kiro", "steering")
        os.makedirs(steering_dir, exist_ok=True)
        
        filepath = os.path.join(steering_dir, "memory-first.md")
        
        if os.path.exists(filepath):
            return f"Steering file already exists at {filepath}"
        
        content = _get_steering_content()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"✓ Steering file created at {filepath}\n\nThe AI will now follow memory-first protocols in this workspace."
    except Exception as e:
        logger.exception("Error creating steering file")
        return f"Error creating steering file: {str(e)}"


def run_server():
    """Run the MCP server."""
    mcp.run()
