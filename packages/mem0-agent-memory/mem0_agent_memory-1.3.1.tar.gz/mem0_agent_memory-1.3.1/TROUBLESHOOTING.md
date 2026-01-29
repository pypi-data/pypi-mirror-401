# Troubleshooting Guide

## Embedding Dimension Mismatch Error

### Error Message
```
Error storing memory: could not broadcast input array from shape (768,) into shape (1536,)
```
or
```
Error searching memories: shapes (0,1536) and (768,) not aligned: 1536 (dim 1) != 768 (dim 0)
```

### Root Cause

The Qdrant/FAISS collection was created with a different embedding dimension than what your current embedding model generates.

**Common scenarios**:
- Collection created with Bedrock (1024D or 1536D) → switched to Ollama (768D)
- Collection created with one Ollama model → switched to different model
- Testing different backends without resetting storage

### Embedding Dimensions by Model

| Backend | Model | Dimensions |
|---------|-------|------------|
| AWS Bedrock | Titan Embed v1 | 1024 |
| AWS Bedrock | Titan Embed v2 | 1024 |
| AWS Bedrock | Cohere Embed | 1536 |
| Ollama | nomic-embed-text | 768 |
| Ollama | mxbai-embed-large | 1024 |
| Ollama | all-minilm | 384 |

### Solution

**Option 1: Reset the collection** (deletes all memories)

Using MCP tool:
```python
reset_memory()
```

Using bash:
```bash
# For Qdrant
rm -rf .mem0/qdrant_embedded/

# For FAISS
rm -rf .mem0/bedrock_memory/
rm -rf .mem0/ollama_memory/
```

**Option 2: Use a different storage path**

Update your MCP config to use a new path:
```json
{
  "env": {
    "QDRANT_PATH": ".mem0/qdrant_ollama_768",  // New path
    "OLLAMA_EMBED_MODEL": "nomic-embed-text:latest"
  }
}
```

**Option 3: Switch back to the original model**

If you want to keep existing memories, switch back to the embedding model that created them.

### Prevention

1. **Use separate storage paths** for different embedding models:
   ```
   .mem0/qdrant_bedrock/     # For Bedrock embeddings
   .mem0/qdrant_ollama/      # For Ollama embeddings
   .mem0/qdrant_nomic/       # For nomic-embed-text specifically
   ```

2. **Document your configuration** in a README or config file

3. **Export memories before switching** models:
   ```python
   export_memories(format="json", output_path="backup.json")
   ```

### How the Code Determines Dimensions

From `src/mem0_agent_memory/server.py`:

```python
# For Qdrant
embedding_dims = 768 if "ollama" in merged_config["embedder"]["provider"] else 1024

# For FAISS
embedding_model_dims = 1024 if "bedrock" in merged_config["embedder"]["provider"] else 768
```

**Note**: This assumes:
- Ollama = 768D (nomic-embed-text default)
- Bedrock = 1024D (Titan default)

If using different models, you may need to adjust the code or ensure your model matches these dimensions.

### Verifying Current Setup

Check your health status:
```python
health_check()
```

Look for:
- `vector_store_backend`: Shows which backend (Qdrant/FAISS)
- `model_backend`: Shows which embedding provider (Ollama/Bedrock)

### Related Issues

- **"Collection already exists"**: Qdrant won't recreate a collection with different dimensions
- **"Index dimension mismatch"**: FAISS has the same issue
- **Silent failures**: Some operations may fail silently if dimensions don't match
- **Wrong backend in reset_memory response**: Fixed in latest version - `reset_memory()` now correctly reports Qdrant backend

---

## Bug Fix: reset_memory() Backend Detection

**Issue**: The `reset_memory()` function reported `"backend": "FAISS"` even when using Qdrant.

**Root Cause**: Missing Qdrant detection in backend determination logic (line 1677-1686).

**Fixed**: Updated to match `health_check()` pattern:
```python
# Before (incorrect)
if os.environ.get("MEM0_API_KEY"):
    backend = "Mem0 Platform"
elif os.environ.get("OPENSEARCH_HOST"):
    backend = "OpenSearch"
else:
    backend = "FAISS"  # ❌ Missing Qdrant check

# After (correct)
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
```

**Impact**: Cosmetic only - the reset operation worked correctly, just reported wrong backend name.

