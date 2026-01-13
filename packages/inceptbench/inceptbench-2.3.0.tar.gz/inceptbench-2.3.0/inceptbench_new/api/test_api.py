"""
Test script for the Educational Content Evaluator API.

Usage:
    python -m inceptbench_new.api.test_api

Tests the API endpoints with the new unified input format.
"""

import sys

from fastapi.testclient import TestClient

from .main import app

# Create test client
client = TestClient(app)


def test_health():
    """Test health check endpoint."""
    print("Testing /health endpoint...")
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    print(f"✓ Health check passed: {data}")


def test_curriculums():
    """Test curriculum listing endpoint."""
    print("\nTesting /curriculums endpoint...")
    response = client.get("/curriculums")
    assert response.status_code == 200
    data = response.json()
    assert "curriculums" in data
    assert "common_core" in data["curriculums"]
    print(f"✓ Curriculums endpoint passed: {data}")


def test_root():
    """Test root endpoint."""
    print("\nTesting / endpoint...")
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "endpoints" in data
    assert "input_format" in data
    print(f"✓ Root endpoint passed: {data['service']}")


def test_evaluate_validation():
    """Test evaluation endpoint input validation."""
    print("\nTesting /evaluate endpoint validation...")

    # Test missing generated_content
    response = client.post("/evaluate", json={})
    assert response.status_code == 422
    print("✓ Validation: Missing generated_content rejected")

    # Test empty generated_content array
    response = client.post("/evaluate", json={"generated_content": []})
    assert response.status_code == 422
    print("✓ Validation: Empty generated_content rejected")

    # Test missing content field
    response = client.post("/evaluate", json={
        "generated_content": [{"curriculum": "common_core"}]
    })
    assert response.status_code == 422
    print("  Validation: Missing content field rejected")

    # Test empty content string
    response = client.post("/evaluate", json={
        "generated_content": [{"content": ""}]
    })
    assert response.status_code == 422
    print("  Validation: Empty content string rejected")

    # Test whitespace-only content
    response = client.post("/evaluate", json={
        "generated_content": [{"content": "   "}]
    })
    assert response.status_code == 422
    print("  Validation: Whitespace-only content rejected")

    # Test empty content object
    response = client.post("/evaluate", json={
        "generated_content": [{"content": {}}]
    })
    assert response.status_code == 422
    print("  Validation: Empty content object rejected")

    # Test too many items (>100)
    many_items = [{"content": f"Question {i}"} for i in range(101)]
    response = client.post("/evaluate", json={
        "generated_content": many_items
    })
    assert response.status_code == 422
    print("  Validation: >100 items rejected")


def test_evaluate_valid_requests():
    """Test evaluation endpoint accepts valid request formats."""
    print("\nTesting /evaluate with valid request formats...")

    # Test minimal request (just content string)
    response = client.post("/evaluate", json={
        "generated_content": [
            {"content": "What is the capital of France?"}
        ]
    })
    # 200 if API keys configured, 503 if not
    assert response.status_code in [200, 503]
    print("  Valid: Minimal string content accepted")

    # Test content as JSON object
    response = client.post("/evaluate", json={
        "generated_content": [
            {
                "content": {
                    "question": "What is 2 + 2?",
                    "answer": "4"
                }
            }
        ]
    })
    assert response.status_code in [200, 503]
    print("✓ Valid: JSON content object accepted")

    # Test with all optional fields
    response = client.post("/evaluate", json={
        "generated_content": [
            {
                "id": "custom-id-123",
                "curriculum": "common_core",
                "request": {
                    "grade": "7",
                    "subject": "mathematics",
                    "type": "mcq",
                    "difficulty": "medium",
                    "locale": "en-US",
                    "skills": {
                        "lesson_title": "Algebra Basics",
                        "substandard_id": "CCSS.MATH.7.EE.A.1"
                    },
                    "instructions": "Create a basic algebra problem"
                },
                "content": "Solve for x: 2x + 5 = 15"
            }
        ]
    })
    assert response.status_code in [200, 503]
    print("  Valid: Full request with all fields accepted")

    # Test with skills as string
    response = client.post("/evaluate", json={
        "generated_content": [
            {
                "request": {
                    "grade": "5",
                    "skills": "Basic arithmetic operations"
                },
                "content": "What is 3 x 4?"
            }
        ]
    })
    assert response.status_code in [200, 503]
    print("✓ Valid: Skills as string accepted")

    # Test batch (multiple items)
    response = client.post("/evaluate", json={
        "generated_content": [
            {"content": "Question 1"},
            {"content": "Question 2"},
            {"content": "Question 3"}
        ]
    })
    assert response.status_code in [200, 503]
    print("  Valid: Batch request (3 items) accepted")


def test_evaluate_simple_content():
    """Test evaluation with simple string content."""
    print("\nTesting /evaluate with simple content...")
    print("  (This makes actual LLM API calls)")

    response = client.post("/evaluate", json={
        "generated_content": [
            {"content": "What is 2 + 2?"}
        ]
    })

    if response.status_code == 503:
        print("⚠️  Service unavailable (likely missing API keys)")
        print("  Set OPENAI_API_KEY and ANTHROPIC_API_KEY in .env file")
        return

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "request_id" in data
    assert "evaluations" in data
    assert "evaluation_time_seconds" in data
    assert "inceptbench_version" in data

    # Verify evaluations
    assert isinstance(data["evaluations"], dict)
    assert len(data["evaluations"]) == 1

    # Get the evaluation (key is auto-generated UUID)
    first_key = list(data["evaluations"].keys())[0]
    evaluation = data["evaluations"][first_key]

    # Verify evaluation has expected fields
    assert "content_type" in evaluation
    assert "overall" in evaluation
    assert "factual_accuracy" in evaluation

    print(f"✓ Evaluation successful:")
    print(f"    Request ID: {data['request_id']}")
    print(f"    Content type: {evaluation['content_type']}")
    print(f"    Overall score: {evaluation['overall']['score']:.2f}")
    print(f"    Time: {data['evaluation_time_seconds']:.2f}s")


def test_evaluate_structured_content():
    """Test evaluation with structured content and metadata."""
    print("\nTesting /evaluate with structured content...")
    print("  (This makes actual LLM API calls)")

    response = client.post("/evaluate", json={
        "generated_content": [
            {
                "id": "math-q1",
                "curriculum": "common_core",
                "request": {
                    "grade": "7",
                    "subject": "mathematics",
                    "type": "mcq"
                },
                "content": {
                    "question": "What is the value of x in 3x + 7 = 22?",
                    "answer": "C",
                    "answer_explanation": "Subtract 7: 3x = 15. Divide by 3: x = 5",
                    "answer_options": [
                        {"key": "A", "text": "3"},
                        {"key": "B", "text": "4"},
                        {"key": "C", "text": "5"},
                        {"key": "D", "text": "6"}
                    ]
                }
            }
        ]
    })

    if response.status_code == 503:
        print("⚠️  Service unavailable (likely missing API keys)")
        return

    assert response.status_code == 200
    data = response.json()

    # Verify the custom ID is preserved
    assert "math-q1" in data["evaluations"]

    evaluation = data["evaluations"]["math-q1"]

    print(f"✓ Structured evaluation successful:")
    print(f"    Item ID: math-q1")
    print(f"    Content type: {evaluation['content_type']}")
    print(f"    Score: {evaluation['overall']['score']:.2f}")


def test_evaluate_batch():
    """Test batch evaluation with multiple items."""
    print("\nTesting /evaluate with batch (multiple items)...")
    print("  (This makes actual LLM API calls)")

    response = client.post("/evaluate", json={
        "generated_content": [
            {
                "id": "q1",
                "content": "What causes water to evaporate?",
                "request": {"subject": "science", "grade": "5"}
            },
            {
                "id": "q2",
                "content": "What is 3.5 + 2.7?",
                "request": {"subject": "mathematics", "grade": "6"}
            }
        ]
    })

    if response.status_code == 503:
        print("⚠️  Service unavailable (likely missing API keys)")
        return

    assert response.status_code == 200
    data = response.json()

    # Verify both items evaluated
    assert "q1" in data["evaluations"]
    assert "q2" in data["evaluations"]

    print(f"✓ Batch evaluation successful:")
    print(f"    Total items: {len(data['evaluations'])}")
    print(f"    Time: {data['evaluation_time_seconds']:.2f}s")
    for item_id, eval_data in data["evaluations"].items():
        print(f"    {item_id}: {eval_data['overall']['score']:.2f}")


def main():
    """Run all tests."""
    print("=" * 70)
    print("Educational Content Evaluator API - Test Suite")
    print("=" * 70)

    try:
        # Basic endpoint tests (no LLM calls)
        test_health()
        test_curriculums()
        test_root()
        test_evaluate_validation()
        test_evaluate_valid_requests()

        # Full evaluation tests (requires API keys)
        print("\n" + "=" * 70)
        print("Full Evaluation Tests (requires API keys)")
        print("=" * 70)
        test_evaluate_simple_content()
        test_evaluate_structured_content()
        test_evaluate_batch()

        print("\n" + "=" * 70)
        print("✓ All tests passed!")
        print("=" * 70)
        return 0

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
