# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2026-01-15

### Fixed
- **Critical stdio transport fix**: Disabled logging output that was interfering with JSON-RPC protocol
  - Resolves "Invalid JSON: EOF while parsing" errors when using stdio transport (default mode)
  - Affects all MCP clients using stdio (Kiro, Claude Desktop, etc.)
  - Logging still enabled for `--help` flag for debugging purposes
  - No impact on HTTP/SSE transport modes

## [1.3.0] - 2026-01-15

### Added
- **Response Optimization**: New `verbose` parameter for all 15 MCP tools to optimize agent context window usage
  - Default compact mode reduces response size by 55% (180 tokens → 80 tokens per memory)
  - Compact responses include only essential fields: `id`, `memory`, `metadata`, `score`
  - **Graph relations preserved**: Kuzu graph store relations included in compact mode for context-aware reasoning
  - Verbose mode available via parameter override or `MEM0_VERBOSE` environment variable
  - Simplified pagination in compact mode (only shown when multiple pages exist)
  - Backward compatible - existing code continues to work without changes

### Performance Improvements
- **Token savings**: 
  - 10 memories: ~1,000 tokens saved (1,800 → 800)
  - 50 memories: ~5,000 tokens saved (9,000 → 4,000)
- **Faster agent processing**: Less data to parse and process
- **Context efficiency**: 2.25x more memories fit in same context window
- **Graph context**: Entity relationships preserved without verbose overhead

### Configuration
- `MEM0_VERBOSE` environment variable for global verbose mode control (default: `false`)
- `MEM0_MAX_RELATIONS` environment variable to limit relations in compact mode (default: `20`)
- Per-call `verbose` parameter for fine-grained control on individual tool calls

### Tools Updated
All 15 tools now support compact/verbose modes:
- `store_memory`, `search_memories`, `list_memories`, `get_memory`, `get_recent_memories`
- `delete_memory`, `update_memory`, `delete_all_memories`, `get_memory_history`
- `get_memory_stats`, `search_by_metadata`, `bulk_delete_memories`
- `export_memories`, `import_memories`, `ingest_documents`

### Graph Store Enhancement
- Graph relations (entities and relationships) now preserved in compact mode
- **Smart truncation**: Relations limited to 20 by default in compact mode to prevent token bloat
- Truncation metadata included when relations exceed limit: `relations_truncated`, `relations_total`, `relations_showing`
- Configurable via `MEM0_MAX_RELATIONS` environment variable
- Verbose mode always returns all relations without truncation
- Relations include: `source`, `relationship`, `destination` for related entities
- Available in both `store_memory` and `search_memories` responses when Kuzu graph store is enabled
- Search returns graph context alongside vector matches for enriched retrieval
- **Important**: Relations in search results are query-level context (entities extracted from the query), not per-memory. All pages of paginated results receive the same graph context.

## [1.2.0] - 2026-01-13

### Added
- **Document Ingestion**: New `ingest_documents` tool using LlamaIndex for knowledge base creation
  - Supports PDF, DOCX, TXT, MD, HTML, and more file formats
  - Automatic text extraction and intelligent chunking
  - Configurable chunk size and overlap
  - Recursive directory processing
  - Metadata preservation from source documents
  - Custom metadata attachment per ingestion
- **Dependencies**: Added LlamaIndex, pypdf, and python-docx for document processing

### Features
- Ingest single files or entire directories into memory as searchable knowledge base
- Automatic chunking with configurable size (default: 1024 chars) and overlap (default: 200 chars)
- Source tracking with file name, chunk index, and total chunks in metadata
- Works with all backends (FAISS, OpenSearch, Mem0 Platform)
- Optional LLM inference for fact extraction (default: off for speed)

## [1.1.1] - 2026-01-13

### Performance Improvements
- **Environment variable caching**: Cached `MEM0_USER_ID`, `MEM0_AGENT_ID`, `MEM0_RUN_ID`, and `MEM0_INFER_DEFAULT` at module load to eliminate repeated `os.environ.get()` calls
- **Code deduplication**: Implemented `_fetch_all_memories()` helper function to reduce code duplication and ensure consistent response handling across all tools
- **Response optimization**: `search_memories` now removes redundant fields (`hash`, `user_id`, `agent_id`) when returning more than 5 results to reduce payload size
- **Configurable relevance**: Made relevance score threshold configurable via `MEM0_MIN_RELEVANCE_SCORE` environment variable (default: 0.7)
- **Bedrock optimizations**:
  - Reduced temperature from 0.1 to 0.0 for deterministic, faster responses
  - Reduced default `max_tokens` from 2000 to 1500 (configurable via `BEDROCK_MAX_TOKENS`)
  - Added boto3 connection pooling with 50 max connections
  - Configured adaptive retry mode with 3 max attempts
  - Set explicit timeouts: 5s connection, 30s read
  - Added `top_p=0.9` for better quality with lower temperature
- **OpenSearch optimizations**: Added explicit timeout (30s) and retry configuration (3 attempts)

### Fixed
- **search_memories limit parameter**: Fixed `limit` parameter to properly control number of results returned. Now `page_size` defaults to `limit` value when not explicitly specified, making `{"query": "...", "limit": 5}` correctly return 5 results instead of 10

### Added
- `BEDROCK_MAX_TOKENS` environment variable for controlling response length
- `MEM0_MIN_RELEVANCE_SCORE` environment variable for search result filtering
- boto3 `Config` with connection pooling and adaptive retries

### Changed
- Bedrock temperature: 0.1 → 0.0 (faster, deterministic)
- Bedrock max_tokens: 2000 → 1500 (configurable)
- All tools now use cached environment variables
- Response handling consolidated into single helper function
- `search_memories` `page_size` parameter now optional, defaults to `limit` value

### Documentation
- Added "Performance Tuning" section to README with Bedrock and search optimization tips
- Documented built-in performance optimizations
- Added performance comparison tips (FAISS vs OpenSearch, infer=true vs false)
- **Updated AGENT_GUIDANCE.md**: Corrected `infer` parameter recommendations - now recommends `infer=true` for task completions and decisions (prevents duplicates, extracts facts) and `infer=false` primarily for speed-critical operations or exact content preservation
- **Clarified score interpretation**: Added documentation explaining FAISS uses L2 distance where lower scores indicate higher similarity (0-100 = very similar, 600+ = dissimilar), not cosine similarity (which would be -1 to 1)

## [1.1.0] - 2025-01-13

### Added
- `delete_all_memories` tool for deleting all memories in a specific scope (user/agent/run)
- `reset_memory` tool for clearing the entire memory store (destructive operation)
- `import_memories` tool for importing memories from JSON export files
- Memory partitioning support: `run_id` parameter added to:
  - `store_memory`
  - `search_memories`
  - `list_memories`
  - `get_recent_memories`
  - `bulk_delete_memories`
  - `delete_all_memories`

### Changed
- Enhanced all partitioning-aware tools to use environment variable default (`MEM0_RUN_ID`)
- Improved tool descriptions with clearer examples and warnings for destructive operations

### Removed
- `app_id` parameter (Platform-only feature not supported in local backends)
- `chat_with_memory` tool (Platform-only feature)

### Documentation
- Updated README.md with new tools and enhanced tool table
- Added comprehensive examples for memory partitioning with `run_id`
- Documented Platform-only features that are not implemented

### Notes
- This release focuses on backend-agnostic features that work across FAISS, OpenSearch, and Platform
- Platform-only features (app_id, chat, custom_instructions, custom_categories, expiration_date) are not implemented
- Users can access Platform-specific features through the Mem0 dashboard when using Platform mode

## [1.0.9] - 2025-01-13

### Added
- `update_memory` tool for direct memory updates without LLM processing
- `get_memory_stats` tool for memory usage statistics
- `bulk_delete_memories` tool for batch deletion with filters
- `export_memories` tool for JSON/Markdown export (writes to `.mem0/exports/` by default)
- `search_by_metadata` tool for metadata-based filtering
- `health_check` tool for backend connectivity verification
- `app_id` and `run_id` parameters for memory partitioning
- `custom_instructions` parameter for per-call ingestion control
- `MEM0_APP_ID` and `MEM0_RUN_ID` environment variables

### Changed
- Improved error handling with specific exception logging in steering file setup
- Added lazy client initialization with clear error messages on failure
- Enhanced type hints with TypedDict for model configuration

### Fixed
- Fixed CONTRIBUTING.md incorrect entry point reference

## [1.0.8] - 2025-01-10

### Changed
- Updated default Ollama LLM model to `qwen3:latest` for better JSON output compatibility

## [1.0.7] - 2025-01-08

### Added
- LM Studio backend support via `LMSTUDIO_HOST` environment variable

## [1.0.6] - 2025-01-05

### Added
- `infer` parameter for `store_memory` to control LLM fact extraction vs raw storage
- `MEM0_INFER_DEFAULT` environment variable to configure default infer behavior

## [1.0.5] - 2025-01-02

### Added
- Ollama backend support via `OLLAMA_HOST` environment variable
- Configurable embedding dimensions for different model backends

## [1.0.4] - 2024-12-28

### Added
- `setup_steering` tool for Kiro memory-first workflow integration
- Bundled AGENT_GUIDANCE.md documentation

## [1.0.3] - 2024-12-20

### Changed
- Improved FAISS path handling with configurable `FAISS_PATH` environment variable
- Better fallback to temp directory when default path is not writable

## [1.0.2] - 2024-12-15

### Fixed
- Fixed pagination in `search_memories` and `list_memories`
- Improved date filtering in `get_recent_memories`

## [1.0.1] - 2024-12-10

### Added
- `get_recent_memories` tool for session continuity
- Pagination support for `list_memories` and `search_memories`

## [1.0.0] - 2024-08-31

### Added
- Initial release of Mem0 Agent Memory MCP server
- Multi-backend support (FAISS, OpenSearch, Mem0 Platform)
- Auto user detection via system username
- Complete memory operations (store, search, list, get, delete, history)
- Pagination support for large memory collections
- Recent memory tracking for session continuity
- Relevance filtering (score > 0.7)
- Robust error handling with graceful fallbacks
- Comprehensive tool descriptions and examples
