from klovis.models import Document, Chunk, KlovisBaseModel, Relationship
import json


def test_document_creation():
    """Test Document model creation."""
    doc = Document(
        source="test.txt",
        content="Test content",
        metadata={"key": "value"}
    )
    
    assert doc.source == "test.txt"
    assert doc.content == "Test content"
    assert doc.metadata == {"key": "value"}


def test_chunk_creation_advanced():
    """Test Chunk model with new RAG fields."""
    chunk = Chunk(
        text="Chunk text",
        metadata={"chunk_id": 0},
        vector=[0.1, 0.2, 0.3],
        parent_id="parent_doc_1",
        relationships=[
            Relationship(target_id="chunk_2", type="next"),
            Relationship(target_id="entity_1", type="mentions")
        ]
    )
    
    assert chunk.text == "Chunk text"
    assert chunk.vector == [0.1, 0.2, 0.3]
    assert chunk.parent_id == "parent_doc_1"
    assert len(chunk.relationships) == 2
    assert chunk.relationships[0].type == "next"


def test_document_to_dict():
    """Test Document serialization to dict."""
    doc = Document(source="test.txt", content="Content")
    doc_dict = doc.to_dict()
    
    assert isinstance(doc_dict, dict)
    assert doc_dict["source"] == "test.txt"
    assert doc_dict["content"] == "Content"


def test_chunk_to_json():
    """Test Chunk serialization to JSON including new fields."""
    chunk = Chunk(
        text="Text", 
        metadata={"id": 1},
        vector=[0.9],
        parent_id="p1"
    )
    json_str = chunk.to_json()
    
    assert isinstance(json_str, str)
    parsed = json.loads(json_str)
    assert parsed["text"] == "Text"
    assert parsed["metadata"]["id"] == 1
    assert parsed["vector"] == [0.9]
    assert parsed["parent_id"] == "p1"


def test_document_default_metadata():
    """Test Document with default empty metadata."""
    doc = Document(source="test.txt", content="Content")
    
    assert doc.metadata == {}


def test_chunk_default_metadata():
    """Test Chunk with default empty metadata."""
    chunk = Chunk(text="Text")
    
    assert chunk.metadata == {}
    assert chunk.vector is None
    assert chunk.parent_id is None
    assert chunk.relationships == []
