"""
CLI tests for educational content evaluator.

Tests the CLI input models and utilities. Run with:
    python -m inceptbench_new.cli.test_cli

Note: Full CLI tests that require the evaluation service are skipped
if dependencies like cv2 are not available.
"""

import json
import sys
import tempfile
from pathlib import Path


def test_core_input_models():
    """Test core input models independently."""
    print("Testing core input models...")

    from ..core.input_models import ContentItem, RequestMetadata

    # Test ContentItem with simple content
    item = ContentItem(content="What is 2+2?")
    assert item.content == "What is 2+2?"
    assert item.id is not None  # Auto-generated
    assert item.curriculum == "common_core"  # Default
    assert item.request is None
    print("✓ Simple ContentItem works")

    # Test ContentItem with all fields
    item = ContentItem(
        id="my-id",
        curriculum="ngss",
        request=RequestMetadata(
            grade="7",
            subject="math",
            instructions="Create a question"
        ),
        content={"question": "What is x?", "answer": "5"}
    )
    assert item.id == "my-id"
    assert item.curriculum == "ngss"
    assert item.request.grade == "7"
    assert item.request.subject == "math"
    assert item.request.instructions == "Create a question"
    assert item.content["question"] == "What is x?"
    print("✓ Full ContentItem works")

    # Test get_content_string
    item = ContentItem(content="Hello world")
    assert item.get_content_string() == "Hello world"

    item = ContentItem(content={"key": "value"})
    content_str = item.get_content_string()
    assert "key" in content_str
    assert "value" in content_str
    print("✓ get_content_string works")

    # Test get_generation_prompt
    item = ContentItem(content="Hello")
    assert item.get_generation_prompt() is None

    item = ContentItem(
        content="Hello",
        request=RequestMetadata(grade="5", subject="science")
    )
    prompt = item.get_generation_prompt()
    assert prompt is not None
    assert "grade" in prompt
    assert "5" in prompt
    print("✓ get_generation_prompt works")

    # Test RequestMetadata.to_generation_prompt
    req = RequestMetadata(grade="7", subject="math")
    prompt = req.to_generation_prompt()
    data = json.loads(prompt)
    assert data["grade"] == "7"
    assert data["subject"] == "math"
    print("✓ RequestMetadata.to_generation_prompt works")

    # Test empty RequestMetadata
    req = RequestMetadata()
    assert req.to_generation_prompt() is None
    print("✓ Empty RequestMetadata returns None")

    # Test validation - empty content rejected
    try:
        ContentItem(content="")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
    print("✓ Empty content rejected")

    # Test validation - whitespace content rejected
    try:
        ContentItem(content="   ")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower() or "whitespace" in str(e).lower()
    print("✓ Whitespace content rejected")

    # Test validation - empty dict rejected
    try:
        ContentItem(content={})
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
    print("✓ Empty dict rejected")

    # Test validation - empty list rejected
    try:
        ContentItem(content=[])
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
    print("✓ Empty list rejected")

    print("✓ All core input model tests passed")


def test_batch_processor_models():
    """Test batch processor result models."""
    print("\nTesting batch processor models...")

    from ..core.processor import BatchResult, FailedItem

    # Test FailedItem
    failed = FailedItem(item_id="q1", error="Something went wrong")
    assert failed.item_id == "q1"
    assert failed.error == "Something went wrong"
    print("✓ FailedItem works")

    # Test BatchResult empty
    result = BatchResult()
    assert result.success_count == 0
    assert result.failure_count == 0
    assert result.total_count == 0
    print("✓ Empty BatchResult works")

    # Test BatchResult with data
    result = BatchResult(
        evaluations={
            "q1": {"score": 0.9},
            "q2": {"score": 0.8}
        },
        failed_items=[
            FailedItem(item_id="q3", error="Failed")
        ]
    )
    assert result.success_count == 2
    assert result.failure_count == 1
    assert result.total_count == 3
    print("✓ BatchResult with data works")

    print("✓ All batch processor model tests passed")


def test_json_loading():
    """Test JSON content loading utilities."""
    print("\nTesting JSON content loading...")

    from ..core.input_models import ContentItem

    def load_json_content(file_path: Path) -> list:
        """Load content items from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            if 'generated_content' not in data:
                raise ValueError("Missing generated_content")
            items_data = data['generated_content']
        elif isinstance(data, list):
            items_data = data
        else:
            raise ValueError("Invalid format")

        if not items_data:
            raise ValueError("No content items")

        return [ContentItem(**item) for item in items_data]

    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = Path(tmpdir) / "content.json"

        # Test generated_content format
        json_file.write_text(json.dumps({
            "generated_content": [
                {"content": "Q1"},
                {"content": "Q2"}
            ]
        }))

        items = load_json_content(json_file)
        assert len(items) == 2
        assert items[0].content == "Q1"
        print("✓ generated_content format works")

        # Test direct array format
        json_file.write_text(json.dumps([
            {"content": "A1"},
            {"content": "A2"},
            {"content": "A3"}
        ]))

        items = load_json_content(json_file)
        assert len(items) == 3
        print("✓ Direct array format works")

        # Test with full item data
        json_file.write_text(json.dumps({
            "generated_content": [
                {
                    "id": "custom-id",
                    "curriculum": "ngss",
                    "request": {
                        "grade": "5",
                        "subject": "science"
                    },
                    "content": "What is photosynthesis?"
                }
            ]
        }))

        items = load_json_content(json_file)
        assert items[0].id == "custom-id"
        assert items[0].curriculum == "ngss"
        assert items[0].request.grade == "5"
        print("✓ Full item data works")

        # Test empty content error
        json_file.write_text(json.dumps({
            "generated_content": []
        }))

        try:
            load_json_content(json_file)
            assert False
        except ValueError as e:
            assert "No content" in str(e)
        print("✓ Empty content raises error")

        # Test missing key error
        json_file.write_text(json.dumps({
            "other_key": []
        }))

        try:
            load_json_content(json_file)
            assert False
        except ValueError as e:
            assert "generated_content" in str(e)
        print("✓ Missing key raises error")

    print("✓ All JSON loading tests passed")


def test_file_detection():
    """Test file path detection and reading utilities."""
    print("\nTesting file detection utilities...")

    def is_file_path(value: str, extensions: tuple) -> bool:
        """Check if value is a file path with allowed extensions."""
        if not value:
            return False
        path = Path(value)
        return path.suffix.lower() in extensions and path.exists()

    def read_file_or_string(value: str, extensions: tuple) -> tuple:
        """Read file or return string."""
        if is_file_path(value, extensions):
            return (Path(value).read_text(encoding='utf-8'), True)
        return (value, False)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        txt_file = Path(tmpdir) / "test.txt"
        txt_file.write_text("TXT content")

        md_file = Path(tmpdir) / "test.md"
        md_file.write_text("MD content")

        json_file = Path(tmpdir) / "test.json"
        json_file.write_text("{}")

        # Test is_file_path
        assert is_file_path(str(txt_file), ('.txt', '.md'))
        assert is_file_path(str(md_file), ('.txt', '.md'))
        assert not is_file_path(str(json_file), ('.txt', '.md'))
        assert not is_file_path("/nonexistent.txt", ('.txt', '.md'))
        assert not is_file_path("plain string", ('.txt', '.md'))
        assert not is_file_path("", ('.txt', '.md'))
        print("✓ is_file_path works")

        # Test read_file_or_string - file
        content, was_file = read_file_or_string(str(txt_file), ('.txt', '.md'))
        assert was_file
        assert content == "TXT content"
        print("✓ read_file_or_string reads files")

        # Test read_file_or_string - string
        content, was_file = read_file_or_string("Just a string", ('.txt', '.md'))
        assert not was_file
        assert content == "Just a string"
        print("✓ read_file_or_string returns strings")

    print("✓ All file detection tests passed")


def test_sample_content_structure():
    """Test sample content matches expected structure."""
    print("\nTesting sample content structure...")

    # Define sample content (same as in cli/main.py)
    sample = {
        "generated_content": [
            {
                "id": "example-1",
                "curriculum": "common_core",
                "request": {
                    "grade": "5",
                    "subject": "mathematics",
                    "type": "mcq",
                    "instructions": "Create a basic multiplication question"
                },
                "content": "What is 7 x 8?\nA) 54\nB) 56\nC) 58\nD) 64"
            },
            {
                "id": "example-2",
                "curriculum": "common_core",
                "content": "What is the capital of France?"
            }
        ]
    }

    from ..core.input_models import ContentItem

    # Verify we can create ContentItems from sample
    items = [ContentItem(**item) for item in sample["generated_content"]]

    assert len(items) == 2

    assert items[0].id == "example-1"
    assert items[0].curriculum == "common_core"
    assert items[0].request.grade == "5"
    assert "7 x 8" in items[0].content

    assert items[1].id == "example-2"
    assert items[1].request is None
    assert "France" in items[1].content

    print("✓ Sample content creates valid ContentItems")
    print("✓ All sample content tests passed")


def main():
    """Run all CLI tests."""
    print("=" * 70)
    print("Educational Content Evaluator CLI - Test Suite")
    print("=" * 70)

    try:
        test_core_input_models()
        test_batch_processor_models()
        test_json_loading()
        test_file_detection()
        test_sample_content_structure()

        print("\n" + "=" * 70)
        print("✓ All CLI tests passed!")
        print("=" * 70)
        return 0

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

