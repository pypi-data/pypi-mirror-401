# Models API Reference

Complete API documentation for data models.

## Document

Represents a raw or loaded document.

### Class Definition

```python
class Document(KlovisBaseModel):
    source: Any
    content: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `source` | `Any` | Document source (path, URL, or identifier) |
| `content` | `str` | Document text content |
| `metadata` | `Dict[str, Any]` | Additional metadata (default: `{}`) |

### Methods

#### `to_dict() -> Dict[str, Any]`

Converts the document to a dictionary.

**Returns:**
- `Dict[str, Any]`: Dictionary representation

**Example:**
```python
doc = Document(source="test.txt", content="Content")
doc_dict = doc.to_dict()
```

#### `to_json(indent: int = 2) -> str`

Converts the document to a JSON string.

**Parameters:**
- `indent` (`int`): Number of spaces for indentation (default: 2)

**Returns:**
- `str`: JSON string representation

**Example:**
```python
json_str = doc.to_json(indent=4)
```

### Example

```python
from klovis.models import Document

doc = Document(
    source="example.txt",
    content="Document content here",
    metadata={"author": "John Doe", "date": "2024-01-01"}
)

print(doc.source)  # "example.txt"
print(doc.content)  # "Document content here"
print(doc.metadata)  # {"author": "John Doe", "date": "2024-01-01"}
```

---

## Chunk

Represents a processed chunk of text ready for RAG pipelines. Supports advanced features like vector storage and graph relationships.

### Class Definition

```python
class Chunk(KlovisBaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    vector: Optional[List[float]] = None
    parent_id: Optional[str] = None
    relationships: List[Relationship] = Field(default_factory=list)
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | `str` | Chunk text content |
| `metadata` | `Dict[str, Any]` | Processing metadata (default: `{}`) |
| `vector` | `Optional[List[float]]` | Vector embedding of the chunk text |
| `parent_id` | `Optional[str]` | ID of the parent document or chunk (for hierarchical RAG) |
| `relationships` | `List[Relationship]` | List of relationships to other entities/chunks (GraphRAG) |

### Relationship Object

Structure for `relationships` list items:

```python
class Relationship(BaseModel):
    target_id: str
    type: str
    metadata: Optional[Dict[str, Any]] = {}
```

### Methods

#### `to_dict() -> Dict[str, Any]`

Converts the chunk to a dictionary.

**Returns:**
- `Dict[str, Any]`: Dictionary representation

#### `to_json(indent: int = 2) -> str`

Converts the chunk to a JSON string.

**Parameters:**
- `indent` (`int`): Number of spaces for indentation (default: 2)

**Returns:**
- `str`: JSON string representation

### Common Metadata Fields

Chunks typically include:
- `chunk_id`: Sequential identifier
- `source`: Source document path
- `length`: Character count
- `type`: Chunk type (e.g., "simple", "markdown", "semantic")

### Example

```python
from klovis.models import Chunk, Relationship

chunk = Chunk(
    text="Chunk content here",
    metadata={"chunk_id": 0, "source": "doc.txt"},
    vector=[0.12, 0.45, 0.88],
    parent_id="doc_123",
    relationships=[
        Relationship(target_id="chunk_5", type="next"),
        Relationship(target_id="entity_python", type="mentions")
    ]
)

print(chunk.vector)  # [0.12, 0.45, 0.88]
```

---

## KlovisBaseModel

Base class for all Klovis models (Document, Chunk).

### Features

- Pydantic-based validation
- Type safety
- Serialization methods (`to_dict()`, `to_json()`)
- Metadata preservation

### Configuration

- `arbitrary_types_allowed = True`
- `validate_assignment = True`
- `extra = "forbid"` (prevents extra fields)
- `frozen = False` (mutable models)
- `str_strip_whitespace = True`
