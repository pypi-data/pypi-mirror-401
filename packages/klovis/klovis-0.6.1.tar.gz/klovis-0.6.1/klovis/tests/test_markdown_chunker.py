from klovis.chunking.markdown_chunker import MarkdownChunker
from klovis.models import Chunk, Document
import pytest

def test_markdown_chunker_basic():
    """Test basic markdown chunking by headings."""
    content = """# Title 1
Content for title 1.

## Subtitle 1.1
Content for subtitle 1.1.

## Subtitle 1.2
Content for subtitle 1.2.

# Title 2
Content for title 2.
"""
    doc = Document(source="test.md", content=content)
    
    chunker = MarkdownChunker(max_chunk_size=1000, overlap=50)
    chunks = chunker.chunk([doc])
    
    assert len(chunks) > 0
    assert all(isinstance(c, Chunk) for c in chunks)
    
    # Verify content structure
    # AST parser usually strips original markdown symbols or keeps them depending on implementation
    # Our implementation reconstructs title + body
    
    # Check if chunks correspond to sections
    chunk_texts = [c.text for c in chunks]
    # We expect roughly:
    # "# Title 1\nContent for title 1."
    # "## Subtitle 1.1\nContent for subtitle 1.1."
    # ...
    
    assert any("Title 1" in t for t in chunk_texts)
    assert any("Subtitle 1.1" in t for t in chunk_texts)


def test_markdown_chunker_ignore_code_comments():
    """
    Test that # inside code blocks are NOT treated as headings.
    This was a failure case for the Regex implementation.
    """
    content = """# Main Title

Here is some python code:

```python
# This is a comment, not a header
def hello():
    print("world")
```

## Next Section
"""
    doc = Document(source="test_code.md", content=content)
    chunker = MarkdownChunker(max_chunk_size=1000)
    chunks = chunker.chunk([doc])
    
    # With Regex, this might have split at "# This is a comment"
    # With AST, "Main Title" section should contain the code block fully
    
    # We expect 2 chunks: "Main Title" (with code) and "Next Section"
    # Or 3 if "Main Title" is split due to size, but here size is small.
    
    assert len(chunks) == 2
    
    main_chunk = chunks[0]
    assert "Main Title" in main_chunk.text
    assert "def hello():" in main_chunk.text
    assert "# This is a comment" in main_chunk.text
    
    next_chunk = chunks[1]
    assert "Next Section" in next_chunk.text


def test_markdown_chunker_large_section():
    """Test that large sections are split (hard split fallback)."""
    content = """# Title
""" + "Content " * 500  # Very long content
    
    doc = Document(source="test.md", content=content)
    
    # Force split by setting small max size
    chunker = MarkdownChunker(max_chunk_size=100, overlap=20)
    chunks = chunker.chunk([doc])
    
    assert len(chunks) > 1
    # Check hard split logic
    assert all(len(c.text) <= 120 for c in chunks) # 100 + overlap roughly


def test_markdown_chunker_no_headings():
    """Test chunking content without markdown headings."""
    content = "This is plain text without any markdown headings."
    doc = Document(source="test.md", content=content)
    
    chunker = MarkdownChunker(max_chunk_size=1000)
    chunks = chunker.chunk([doc])
    
    assert len(chunks) >= 1
    # Our logic defaults to "# Section" or "# Preamble" depending on where text is
    # Here it's all text without header -> likely returns "# Section" + text
    assert "# Section" in chunks[0].text
    assert content in chunks[0].text
