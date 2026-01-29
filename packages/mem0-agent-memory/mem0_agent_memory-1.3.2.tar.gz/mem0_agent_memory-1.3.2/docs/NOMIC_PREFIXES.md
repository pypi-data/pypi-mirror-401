# Nomic Embed Text with Task Prefixes

## Overview

Nomic Embed Text models are instruction-based embedders that require explicit task context to produce semantically aligned embeddings. Without proper prefixes, queries and documents exist in different vector spaces, resulting in poor similarity scores during search.

## The Problem

When using Ollama's `nomic-embed-text` without prefixes:
- ❌ Embeddings are generated successfully
- ❌ Similarity search returns irrelevant results or no results
- ❌ Scores are very high (>1000 with L2 distance)
- ❌ Semantic meaning is lost

## The Solution

Add task-specific prefixes to align embeddings:
- `search_document:` - for content being stored in the vector database
- `search_query:` - for user queries during search operations

## Configuration

### Enable Nomic Prefixes

Set the environment variable in your MCP config:

```json
{
  "env": {
    "OLLAMA_HOST": "http://localhost:11434",
    "OLLAMA_EMBED_MODEL": "nomic-embed-text:latest",
    "NOMIC_USE_PREFIXES": "true",
    "FAISS_PATH": ".mem0/ollama_memory_prefixed"
  }
}
```

### How It Works

The MCP server automatically patches mem0's Ollama embedder to:

1. **For document storage**: Prepends `search_document: ` to all text chunks
2. **For search queries**: Prepends `search_query: ` to user queries
3. **Detection**: Uses stack frame inspection to determine context

## Technical Details

### Nomic Model Specifications

- **Context Length**: 8,192 tokens (ideal for long technical docs)
- **Architecture**: Mixture of Experts (MoE) in v2
- **Dimensions**: 768 (default), supports Matryoshka: 512, 256, 128, 64
- **Similarity Metric**: Cosine similarity or dot product (normalized vectors)

### Model Variants

- `nomic-embed-text-v1.5/v2`: General-purpose text retrieval
- `nomic-embed-code`: Specialized for code retrieval (Python, Java, JS)
- `nomic-embed-multimodal`: For PDFs with charts/diagrams

### Performance Comparison

| Embedding Model | Prefix Required | Similarity Score Range | Technical Docs Quality |
|----------------|-----------------|------------------------|----------------------|
| Ollama nomic-embed-text (no prefix) | ❌ | >1000 (poor) | ❌ Poor |
| Ollama nomic-embed-text (with prefix) | ✅ | 0.5-0.7 (good) | ✅ Excellent |
| AWS Bedrock Titan | ❌ | 0.5-0.7 (good) | ✅ Excellent |

## Testing

### Before (No Prefixes)

```python
# Query: "COBOL programming language"
# Results: 0 matches (all filtered out with scores >1000)
```

### After (With Prefixes)

```python
# Query: "COBOL programming language"
# Results: 55 matches with scores 0.51-0.67
# Top result: "COBOL Programming... object-oriented programming..."
```

## Troubleshooting

### Still Getting Poor Results?

1. **Check prefix is enabled**: Look for log message "Patching Ollama embedder to add Nomic task prefixes"
2. **Verify model version**: Use `nomic-embed-text:latest` or `nomic-embed-text-v1.5`
3. **Check dimensions**: Ensure FAISS is configured for 768 dimensions
4. **Restart MCP server**: Changes require server restart

### Matryoshka Dimensions

If using truncated dimensions, use trained granularities:
- ✅ 768, 512, 256, 128, 64 (trained)
- ❌ 300, 400, 600 (arbitrary truncation degrades quality)

## References

- [Nomic Embed Text v1.5 on Hugging Face](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5)
- [Nomic Embed Code on Hugging Face](https://huggingface.co/nomic-ai/nomic-embed-code)
- [Nomic API Documentation](https://docs.nomic.ai/reference/endpoints/nomic-embed-text)
- [Matryoshka Representation Learning Paper](https://arxiv.org/abs/2205.13147)

## Implementation Details

The prefix injection is implemented via runtime patching of mem0's embedder:

```python
def patched_embed(text: str, **kwargs):
    # Detect context using stack frame inspection
    prefix = "search_document: "  # default for storage
    
    if is_search_operation():
        prefix = "search_query: "
    
    return original_embed(f"{prefix}{text}", **kwargs)
```

This approach:
- ✅ Works with existing mem0 code
- ✅ No mem0 library modifications needed
- ✅ Automatic context detection
- ✅ Backward compatible (disabled by default)
