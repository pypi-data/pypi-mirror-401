from klovis.loaders.directory_loader import DirectoryLoader
from klovis.models import Document
from pathlib import Path
import json
import pytest

def test_directory_loader_with_multiple_formats(tmp_path):
    # --- Setup test directory
    subdir = tmp_path / "nested"
    subdir.mkdir()

    # Create text file
    txt_file = tmp_path / "doc1.txt"
    txt_file.write_text("Hello Klovis from text file.")

    # Create JSON file
    json_file = tmp_path / "data.json"
    json_file.write_text(json.dumps({"content": "JSON data for Klovis"}))

    # Create HTML file
    html_file = subdir / "page.html"
    html_file.write_text("<html><body><h1>Hello Klovis</h1></body></html>")

    # Create PDF file (mock content since we can't easily gen a valid PDF)
    # Note: PDFLoader might fail on invalid PDF content if not mocked, 
    # but let's see if it handles exceptions gracefully or if we need to mock.
    # For this test, we rely on the fact that it returns a list.
    # If PDFLoader is strict, we might see an error log but test continues.
    pdf_file = subdir / "empty.pdf"
    pdf_file.write_text("%PDF-1.4\n%Fake minimal PDF for testing\n")

    # --- Run loader (Standard Sync Mode)
    loader = DirectoryLoader(path=str(tmp_path), recursive=True)
    documents = loader.load()
    
    # --- Assertions
    assert isinstance(documents, list)
    assert all(isinstance(d, Document) for d in documents)
    assert len(documents) >= 3  # Should load at least txt, json, html
    sources = [str(d.source) for d in documents] # d.source might be Path or str
    
    # Normalize paths for assertion
    sources_str = " ".join(sources)
    assert "doc1.txt" in sources_str
    assert "data.json" in sources_str
    assert "page.html" in sources_str


def test_directory_loader_stream(tmp_path):
    """Test the new streaming capability."""
    # Setup
    (tmp_path / "file1.txt").write_text("Content 1")
    (tmp_path / "file2.txt").write_text("Content 2")
    
    loader = DirectoryLoader(path=str(tmp_path))
    
    # Execute stream
    stream_iterator = loader.load_stream()
    
    # Verify it is an iterator/generator
    import types
    assert isinstance(stream_iterator, types.GeneratorType) or hasattr(stream_iterator, '__next__')
    
    docs = list(stream_iterator)
    assert len(docs) == 2
    contents = sorted([d.content for d in docs])
    assert contents == ["Content 1", "Content 2"]


def test_directory_loader_parallel_workers(tmp_path):
    """Test that max_workers parameter is accepted and works."""
    # Create enough files to likely trigger multiple workers
    for i in range(10):
        (tmp_path / f"file_{i}.txt").write_text(f"Content {i}")
        
    loader = DirectoryLoader(path=str(tmp_path), max_workers=2)
    documents = loader.load()
    
    assert len(documents) == 10


def test_directory_loader_empty(tmp_path):
    loader = DirectoryLoader(path=str(tmp_path))
    docs = loader.load()
    assert docs == []
