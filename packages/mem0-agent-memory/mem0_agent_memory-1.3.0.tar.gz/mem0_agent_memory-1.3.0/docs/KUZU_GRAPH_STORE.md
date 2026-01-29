# KuzuDB Graph Store Integration

**Date**: January 15, 2026  
**Status**: ✅ Supported  
**Feature**: Graph Memory with KuzuDB embedded database

---

## Overview

KuzuDB is an embedded graph database that adds relationship tracking to mem0's vector-based memory system. It stores entities and their relationships alongside embeddings, enabling context-aware memory retrieval.

### Benefits

- **Relationship Awareness**: Understands connections between people, places, events
- **Embedded**: No separate database server required
- **Fast**: In-process queries with no network overhead
- **Persistent**: File-based storage survives restarts
- **Lightweight**: Minimal dependencies and resource usage

---

## How It Works

```
User Input → mem0 → Extract Entities & Relationships (always when graph_store enabled)
                 ↓
         ┌───────┴────────┐
         ↓                ↓
    Vector Store      Graph Store
    (Qdrant/FAISS)    (KuzuDB)
    - Embeddings      - Entities (nodes)
    - Semantic search - Relationships (edges)
         ↓                ↓
         └───────┬────────┘
                 ↓
         Combined Results
         (Vector + Graph context)
```

**Important**: Graph extraction happens **independently** of the `infer` parameter:
- `infer=true`: LLM extracts facts + LLM extracts graph relationships (2 LLM calls)
- `infer=false`: Content stored as-is + LLM extracts graph relationships (1 LLM call)

The `infer` parameter only controls whether mem0 breaks down content into atomic facts. Graph extraction always requires an LLM call when `graph_store` is configured, so `infer=false` reduces cost but doesn't eliminate it entirely.

### Example

**Input**: "John works at Amazon and prefers Python for backend development"

**Vector Store** (Qdrant):
- Embedding: [0.123, -0.456, ...]
- Memory: "Prefers Python for backend development"

**Graph Store** (KuzuDB):
- Node: Person(name="John")
- Node: Company(name="Amazon")
- Node: Language(name="Python")
- Edge: John --[WORKS_AT]--> Amazon
- Edge: John --[PREFERS]--> Python

**Retrieval**: Query "What does John like?" returns both the vector match AND related graph context (works at Amazon, prefers Python).

---

## Configuration

### Environment Variables

Set `KUZU_DB_PATH` to enable KuzuDB graph store:

```bash
# File-based storage (persistent)
export KUZU_DB_PATH=".mem0/kuzu/graph.kuzu"

# In-memory storage (temporary, cleared on restart)
export KUZU_DB_PATH=":memory:"
```

### MCP Server Configuration

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "mem0-nova-qdrant-kuzu": {
      "command": "uv",
      "args": ["run", "--python", "3.13", "--directory", "/path/to/mem0-agent-memory", "python", "-m", "mem0_agent_memory"],
      "env": {
        "QDRANT_PATH": ".mem0/qdrant_nova_kuzu",
        "KUZU_DB_PATH": ".mem0/kuzu/nova_graph.kuzu",
        "BEDROCK_LLM_MODEL": "us.amazon.nova-micro-v1:0",
        "MEM0_USER_ID": "your_user_id",
        "MEM0_AGENT_ID": "mem0-agent-memory",
        "MEM0_INFER_DEFAULT": "true"
      },
      "disabled": false
    }
  }
}
```

### Python Configuration

```python
from mem0 import Memory

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": ".mem0/qdrant",
            "collection_name": "memories",
            "embedding_model_dims": 1024
        }
    },
    "graph_store": {
        "provider": "kuzu",
        "config": {
            "db": ".mem0/kuzu/graph.kuzu"  # or ":memory:" for temporary
        }
    },
    "llm": {
        "provider": "aws_bedrock",
        "config": {
            "model": "us.amazon.nova-micro-v1:0"
        }
    }
}

memory = Memory.from_config(config)
```

---

## Usage Examples

### Basic Storage with Graph

```python
# Store memory - automatically extracts entities and relationships
memory.add(
    "Alice is a software engineer at Google. She loves Python and mentors Bob.",
    user_id="user123"
)

# Graph automatically creates:
# - Nodes: Alice (Person), Google (Company), Python (Language), Bob (Person)
# - Edges: Alice --[WORKS_AT]--> Google
#          Alice --[LOVES]--> Python
#          Alice --[MENTORS]--> Bob
```

### Retrieval with Graph Context

```python
# Search returns vector matches + graph relationships
results = memory.search(
    "What does Alice do?",
    user_id="user123"
)

# Returns:
# - Vector match: "Alice is a software engineer"
# - Graph context: Works at Google, loves Python, mentors Bob
```

### Relationship Queries

```python
# Find all people Alice knows
results = memory.search(
    "Who does Alice know?",
    user_id="user123"
)

# Graph traversal finds: Bob (mentee), colleagues at Google
```

---

## Storage Modes

### File-Based (Recommended for Production)

```bash
export KUZU_DB_PATH=".mem0/kuzu/graph.kuzu"
```

**Pros**:
- Persistent across restarts
- Can be backed up
- Supports large graphs

**Cons**:
- Requires disk space
- Slightly slower than in-memory

### In-Memory (Recommended for Testing)

```bash
export KUZU_DB_PATH=":memory:"
```

**Pros**:
- Fastest performance
- No disk usage
- Clean state on restart

**Cons**:
- Data lost on restart
- Limited by RAM

---

## Performance Considerations

### Graph Store Overhead

- **Storage**: ~10-20% increase vs vector-only
- **Write latency**: 
  - `infer=true`: +100-150ms (fact extraction + graph extraction)
  - `infer=false`: +50-100ms (graph extraction only)
- **Read latency**: +10-50ms for graph traversal
- **Memory**: Minimal (embedded, in-process)
- **LLM calls**: Graph extraction always requires 1 LLM call, even with `infer=false`

### When to Use Graph Store

**Use Graph Store When**:
- Tracking relationships between entities
- Need context-aware retrieval
- Building knowledge graphs
- Multi-hop reasoning required

**Skip Graph Store When**:
- Simple keyword search sufficient
- No entity relationships
- Latency critical (< 100ms)
- Minimal storage preferred

---

## Comparison: Vector-Only vs Vector + Graph

| Feature | Vector Only | Vector + Graph |
|---------|-------------|----------------|
| Semantic search | ✅ Excellent | ✅ Excellent |
| Relationship tracking | ❌ No | ✅ Yes |
| Context awareness | ⚠️ Limited | ✅ Strong |
| Storage overhead | Low | Medium |
| Write latency | Fast (~100ms) | Medium (~150-200ms) |
| Read latency | Fast (~50ms) | Medium (~60-100ms) |
| Use case | Simple Q&A | Knowledge graphs |

---

## Installation

KuzuDB is included in mem0's dependencies:

```bash
# Already installed with mem0
pip install mem0ai

# Or install separately
pip install kuzu
```

---

## Troubleshooting

### Issue: "kuzu module not found"

```bash
pip install kuzu
```

### Issue: Permission denied creating database file

```bash
# Use temp directory
export KUZU_DB_PATH="/tmp/mem0_kuzu.kuzu"

# Or use in-memory
export KUZU_DB_PATH=":memory:"
```

### Issue: Database file corrupted

```bash
# Delete and recreate
rm -rf .mem0/kuzu/
# Restart server - will recreate database
```

### Issue: Slow graph queries

- Use file-based storage (not :memory:) for large graphs
- Ensure SSD storage for database files
- Consider indexing frequently queried relationships

---

## Advanced Configuration

### Custom Graph Schema

```python
config = {
    "graph_store": {
        "provider": "kuzu",
        "config": {
            "db": ".mem0/kuzu/graph.kuzu",
            # Custom node types
            "node_types": ["Person", "Company", "Technology"],
            # Custom relationship types
            "edge_types": ["WORKS_AT", "USES", "KNOWS"]
        }
    }
}
```

### Multiple Graphs

```python
# Separate graphs for different contexts
user_graph = Memory.from_config({
    "graph_store": {"provider": "kuzu", "config": {"db": ".mem0/kuzu/users.kuzu"}}
})

project_graph = Memory.from_config({
    "graph_store": {"provider": "kuzu", "config": {"db": ".mem0/kuzu/projects.kuzu"}}
})
```

---

## References

- [KuzuDB Documentation](https://kuzudb.com/)
- [mem0 Graph Memory](https://docs.mem0.ai/open-source/features/graph-memory)
- [Graph Database Concepts](https://en.wikipedia.org/wiki/Graph_database)

---

## Related Documentation

- `README.md` - Main project documentation
- `docs/QDRANT_SETUP.md` - Qdrant configuration guide
