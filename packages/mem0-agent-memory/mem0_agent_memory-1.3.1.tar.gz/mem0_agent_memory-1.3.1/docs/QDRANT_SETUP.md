# Qdrant Setup Guide

Qdrant is a high-performance vector database that provides native metadata filtering, eliminating the need for Python-side workarounds. This guide covers both embedded and server modes.

## Why Qdrant?

**Advantages over FAISS:**
- ✅ Native metadata filtering (no `limit=10000` workaround needed)
- ✅ Better performance for metadata-heavy queries
- ✅ Scalable for large datasets
- ✅ Production-ready with clustering support
- ✅ Can run embedded (no Docker) or as a server

**Advantages over OpenSearch:**
- ✅ Simpler setup (no AWS credentials needed)
- ✅ Lighter weight
- ✅ Better for local development

## Mode 1: Embedded Mode (Recommended for Development)

**No Docker required!** Qdrant runs as a pure Python library.

### Setup

```bash
# Install qdrant-client
pip install qdrant-client

# Set environment variable
export QDRANT_PATH=".mem0/qdrant"
```

### Configuration

```python
# In your MCP settings or environment
{
  "QDRANT_PATH": ".mem0/qdrant",
  "OLLAMA_HOST": "http://localhost:11434",
  "OLLAMA_EMBED_MODEL": "nomic-embed-text:latest",
  "OLLAMA_LLM_MODEL": "qwen3:latest"
}
```

### Test

```bash
python test_qdrant_embedded.py
```

### How It Works

- Uses `QdrantLocal` class from qdrant-client
- Stores data in local directory (like FAISS)
- Each workspace gets its own collection: `mem0_<workspace_name>`
- No server process needed
- Perfect for development and testing

## Mode 2: Server Mode (Recommended for Production)

**Requires Docker** but provides better performance and scalability.

### Setup

```bash
# Install qdrant-client
pip install qdrant-client

# Start Qdrant server with Docker
docker run -d \
  -p 6333:6333 \
  -v $(pwd)/.mem0/qdrant_server:/qdrant/storage \
  --name qdrant \
  qdrant/qdrant

# Set environment variables
export QDRANT_HOST="localhost"
export QDRANT_PORT="6333"
```

### Configuration

```python
# In your MCP settings or environment
{
  "QDRANT_HOST": "localhost",
  "QDRANT_PORT": "6333",
  "OLLAMA_HOST": "http://localhost:11434",
  "OLLAMA_EMBED_MODEL": "nomic-embed-text:latest",
  "OLLAMA_LLM_MODEL": "qwen3:latest"
}
```

### Test

```bash
python test_qdrant_server.py
```

### How It Works

- Connects to Qdrant server via HTTP
- Single Qdrant instance serves all workspaces
- Each workspace gets its own collection: `mem0_<workspace_name>`
- Better for production deployments
- Supports clustering and replication

## Workspace Isolation

Both modes provide workspace isolation:

```
Workspace: my-project
Collection: mem0_my_project

Workspace: another-project  
Collection: mem0_another_project
```

Collections are automatically created based on the current working directory name.

## Metadata Filtering

Qdrant supports native metadata filtering (future enhancement):

```python
# Future: Native Qdrant filtering
mem0_client.search(
    "query",
    user_id="user",
    filters={
        "AND": [
            {"type": "decision"},
            {"priority": {"gte": 5}}
        ]
    }
)
```

Currently, the server uses Python-side filtering (same as FAISS) but the infrastructure is ready for native filtering.

## Migration from FAISS

### Option 1: Fresh Start (Recommended)

```bash
# Just switch the environment variable
export QDRANT_PATH=".mem0/qdrant"
# Old FAISS data remains in .mem0/memory
```

### Option 2: Export/Import

```bash
# Export from FAISS
python -c "
from mem0_agent_memory.server import _get_mem0_client
import os
os.environ['FAISS_PATH'] = '.mem0/memory'
client = _get_mem0_client()
# Export logic here
"

# Import to Qdrant
export QDRANT_PATH=".mem0/qdrant"
# Import logic here
```

## Troubleshooting

### Embedded Mode

**Issue:** `ImportError: No module named 'qdrant_client'`
```bash
pip install qdrant-client
```

**Issue:** Permission denied creating directory
```bash
# Check directory permissions
ls -la .mem0/
# Or use a different path
export QDRANT_PATH="/tmp/qdrant"
```

### Server Mode

**Issue:** Cannot connect to Qdrant server
```bash
# Check if Docker is running
docker ps | grep qdrant

# Check Qdrant logs
docker logs qdrant

# Restart Qdrant
docker restart qdrant
```

**Issue:** Port 6333 already in use
```bash
# Use a different port
docker run -d -p 6334:6333 -v $(pwd)/.mem0/qdrant_server:/qdrant/storage qdrant/qdrant
export QDRANT_PORT="6334"
```

## Performance Comparison

| Backend | Setup | Metadata Filtering | Scale | Best For |
|---------|-------|-------------------|-------|----------|
| FAISS | Easy | Python-side | Small | Quick start |
| Qdrant Embedded | Easy | Native (future) | Medium | Development |
| Qdrant Server | Docker | Native (future) | Large | Production |
| OpenSearch | AWS | Native | Very Large | Enterprise |

## Next Steps

1. Try embedded mode for development
2. Use server mode for production
3. Monitor performance with `health_check` tool
4. Consider native metadata filtering in future updates

## References

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Python Client](https://python-client.qdrant.tech/)
- [mem0 Qdrant Integration](https://docs.mem0.ai/components/vectordbs/dbs/qdrant)
