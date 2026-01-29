# Memory-First Development Guidance

## Core Principle
**ALWAYS search memory first** before starting tasks, making decisions, or creating new content.

## Quick Start Workflow

### Session Start
```python
get_recent_memories(days=3, limit=5)  # Recent context
search_memories("project status")      # Current state
```

### Before Any Task
```python
search_memories("<task_topic>")        # Check previous work
search_memories("decisions")           # Avoid re-deciding
```

### After Completing Work
```python
store_memory(
    content="Completed: <task> - Outcome: <result>",
    metadata={"type": "task_completion", "priority": "medium"}
)
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `store_memory(content, metadata?)` | Save information |
| `update_memory(memory_id, content, metadata?)` | Update existing memory |
| `search_memories(query, limit?)` | Find relevant memories |
| `search_by_metadata(type?, priority?, status?)` | Filter by metadata |
| `get_recent_memories(days?, limit?)` | Get recent context |
| `list_memories(page?, page_size?)` | Browse all memories |
| `get_memory(memory_id)` | Get specific memory |
| `delete_memory(memory_id)` | Remove memory |
| `bulk_delete_memories(metadata_type?, older_than_days?)` | Delete multiple |
| `get_memory_history(memory_id)` | View change history |
| `get_memory_stats()` | Get usage statistics |
| `export_memories(format?)` | Export to JSON/Markdown |
| `health_check()` | Verify backend status |
| `setup_steering(workspace_path?)` | Create Kiro steering file |

## Recommended Metadata

```json
{
  "type": "decision|task_completion|preference|note",
  "priority": "high|medium|low",
  "status": "complete|in_progress|blocked"
}
```

## Best Practices

1. **Search before creating** - Check if similar work exists
2. **Store decisions** - Record why choices were made
3. **Use metadata** - Makes searching easier later
4. **Session summaries** - Store progress before ending long sessions
5. **Be specific** - Clear content is easier to find

## Example Queries

```python
# Find user preferences
search_memories("user prefers")

# Find past decisions
search_memories("decision architecture")

# Find implementation patterns
search_memories("how to implement")

# Find blockers
search_memories("blocked issue")
```

## Performance: The `infer` Parameter

The `store_memory` tool has an optional `infer` parameter that controls speed vs intelligence:

### `infer=true` (Default) - Smart but Slower (~10-15s)
- LLM extracts key facts from your content
- Automatically deduplicates and updates existing memories
- Best for: Important decisions, preferences, complex information
- **Note**: Works best with AWS Bedrock/Claude. Local models (Ollama) may return empty results due to JSON formatting issues.

```python
store_memory(
    content="User prefers React over Vue for frontend development",
    metadata={"type": "preference"}
)  # LLM extracts: "User prefers React over Vue"
```

### `infer=false` - Fast Raw Storage (~1-2s)
- Stores content exactly as provided
- No deduplication or fact extraction
- Best for: Quick notes, logs, well-structured content
- **Recommended for Ollama/local models** - reliable and fast

```python
store_memory(
    content="Completed: API refactoring - Outcome: 30% faster response times",
    metadata={"type": "task_completion"},
    infer=False
)  # Stored verbatim, very fast
```

### When to Use Each

| Scenario | Recommended `infer` | Reason |
|----------|-------------------|---------|
| User preferences | `true` | Extracts key facts, deduplicates |
| Important decisions | `true` | Prevents redundant storage |
| Task completions | `true` | Extracts outcomes, avoids duplicates |
| Project milestones | `true` | Consolidates related information |
| Quick temporary notes | `false` | Speed matters more than deduplication |
| Logs needing exact wording | `false` | Preserve exact content |
| Rapid iteration/testing | `false` | 5-10x faster writes |

**Backend Considerations:**
- **AWS Bedrock/Claude**: `infer=true` works reliably
- **Ollama + Qwen3**: `infer=true` works well ✓
- **Ollama + llama3.1/mistral**: Use `infer=false` (JSON formatting issues)

**Key Insight:** The steering guidance previously recommended `infer=false` for task completions, but `infer=true` is actually better for most use cases because it prevents storing duplicate information and extracts only new facts. Use `infer=false` primarily when you need speed or exact content preservation.

### Ollama Model Recommendation

Use **`qwen3:latest`** for full `infer=true` support with Ollama. Qwen3 outputs clean JSON without markdown wrapping, enabling proper fact extraction.

Other models (llama3.1, mistral) wrap JSON in markdown code blocks, which breaks mem0's parsing - use `infer=false` with them.
