# API Usage Examples

Real-world examples of using the Educational Content Evaluator API.

## Table of Contents

- [Simple Question](#simple-question)
- [Math Problem with Metadata](#math-problem-with-metadata)
- [Structured MCQ](#structured-mcq)
- [Reading Passage](#reading-passage)
- [Batch Evaluation](#batch-evaluation)
- [Content with Images](#content-with-images)
- [Error Handling](#error-handling)

---

## Simple Question

The simplest form - just provide content as a string.

**Request:**

```json
POST /evaluate
{
  "generated_content": [
    {
      "content": "What is the capital of France?"
    }
  ]
}
```

**Response:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "evaluations": {
    "auto-generated-uuid": {
      "content_type": "question",
      "overall": {
        "score": 0.62,
        "reasoning": "This is a simple factual recall question...",
        "suggested_improvements": "Consider adding misconception-revealing distractors"
      },
      "factual_accuracy": {
        "score": 1.0,
        "reasoning": "Paris is indeed the capital of France.",
        "suggested_improvements": null
      },
      "educational_accuracy": {
        "score": 1.0,
        "reasoning": "The question is factually correct.",
        "suggested_improvements": null
      },
      "weighted_score": 0.75
    }
  },
  "evaluation_time_seconds": 8.5,
  "inceptbench_version": "x.y.z",
  "failed_items": null
}
```

---

## Math Problem with Metadata

Include request metadata for context-aware evaluation.

**Request:**

```json
POST /evaluate
{
  "generated_content": [
    {
      "id": "algebra-q1",
      "curriculum": "common_core",
      "request": {
        "grade": "7",
        "subject": "mathematics",
        "type": "mcq",
        "difficulty": "medium",
        "instructions": "Create a two-step linear equation"
      },
      "content": "Solve for x: 2x + 5 = 15\nA) x = 5\nB) x = 10\nC) x = 7.5\nD) x = 2.5"
    }
  ]
}
```

**Response:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440001",
  "evaluations": {
    "algebra-q1": {
      "content_type": "question",
      "overall": {
        "score": 0.92,
        "reasoning": "Well-constructed algebra problem with appropriate difficulty.",
        "suggested_improvements": null
      },
      "factual_accuracy": {
        "score": 1.0,
        "reasoning": "Correct answer is A) x = 5. (2*5 + 5 = 15)",
        "suggested_improvements": null
      },
      "curriculum_alignment": {
        "score": 1.0,
        "reasoning": "Aligns with Common Core standard 7.EE.B.4",
        "suggested_improvements": null
      },
      "distractor_quality": {
        "score": 1.0,
        "reasoning": "Distractors represent common student errors.",
        "suggested_improvements": null
      },
      "weighted_score": 0.94
    }
  },
  "evaluation_time_seconds": 12.3,
  "inceptbench_version": "x.y.z",
  "failed_items": null
}
```

---

## Structured MCQ

Pass content as a structured JSON object.

**Request:**

```json
POST /evaluate
{
  "generated_content": [
    {
      "id": "mcq-001",
      "curriculum": "common_core",
      "request": {
        "grade": "7",
        "subject": "mathematics",
        "type": "mcq",
        "skills": {
          "lesson_title": "Solving Linear Equations",
          "substandard_id": "CCSS.MATH.7.EE.A.1"
        }
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
}
```

**Response:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440002",
  "evaluations": {
    "mcq-001": {
      "content_type": "question",
      "overall": {
        "score": 0.88,
        "reasoning": "Good question with clear wording.",
        "suggested_improvements": "Distractors could target specific misconceptions."
      },
      "factual_accuracy": {
        "score": 1.0,
        "reasoning": "The correct answer C (x=5) is mathematically accurate.",
        "suggested_improvements": null
      },
      "weighted_score": 0.85
    }
  },
  "evaluation_time_seconds": 10.2,
  "inceptbench_version": "x.y.z",
  "failed_items": null
}
```

---

## Reading Passage

Evaluate reading passages with comprehension questions.

**Request:**

```json
POST /evaluate
{
  "generated_content": [
    {
      "id": "reading-001",
      "request": {
        "grade": "4",
        "subject": "english",
        "type": "fiction_reading"
      },
      "content": "The Story of the Tortoise and the Hare\n\nOnce upon a time, a speedy hare made fun of a slow tortoise. The tortoise, tired of being laughed at, challenged the hare to a race.\n\nWhen the race began, the hare sprinted ahead. Feeling confident, the hare decided to take a nap under a tree. Meanwhile, the tortoise kept moving slowly but steadily.\n\nWhen the hare woke up, he saw the tortoise crossing the finish line.\n\nMoral: Slow and steady wins the race.\n\nQuestions:\n1. Why did the tortoise challenge the hare?\n2. What did the hare do during the race?\n3. What is the moral of this story?"
    }
  ]
}
```

**Response:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440003",
  "evaluations": {
    "reading-001": {
      "content_type": "fiction_reading",
      "overall": {
        "score": 0.87,
        "reasoning": "Classic fable with clear moral lesson.",
        "suggested_improvements": "Consider adding more descriptive language."
      },
      "reading_level_match": {
        "score": 1.0,
        "reasoning": "Appropriate vocabulary for grade 4.",
        "suggested_improvements": null
      },
      "engagement": {
        "score": 1.0,
        "reasoning": "Classic story with clear conflict and resolution.",
        "suggested_improvements": null
      },
      "weighted_score": 0.89
    }
  },
  "evaluation_time_seconds": 15.4,
  "inceptbench_version": "x.y.z",
  "failed_items": null
}
```

---

## Batch Evaluation

Evaluate multiple items in a single request.

**Request:**

```json
POST /evaluate
{
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
    },
    {
      "id": "q3",
      "content": "Who wrote Romeo and Juliet?",
      "request": {"subject": "english", "grade": "8"}
    }
  ]
}
```

**Response:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440004",
  "evaluations": {
    "q1": {
      "content_type": "question",
      "overall": { "score": 0.75, "reasoning": "..." },
      "weighted_score": 0.78
    },
    "q2": {
      "content_type": "question",
      "overall": { "score": 0.82, "reasoning": "..." },
      "weighted_score": 0.8
    },
    "q3": {
      "content_type": "question",
      "overall": { "score": 0.7, "reasoning": "..." },
      "weighted_score": 0.72
    }
  },
  "evaluation_time_seconds": 18.5,
  "inceptbench_version": "x.y.z",
  "failed_items": null
}
```

---

## Content with Images

The API automatically detects and analyzes images in content.

**Request:**

```json
POST /evaluate
{
  "generated_content": [
    {
      "id": "visual-math-001",
      "request": {
        "grade": "3",
        "subject": "mathematics",
        "type": "mcq"
      },
      "content": "Look at the image showing baskets of apples:\nhttps://example.com/images/apple-baskets.jpg\n\nQuestion: If each basket contains 4 apples and there are 3 baskets, how many apples are there in total?\nA) 7\nB) 12\nC) 16\nD) 9"
    }
  ]
}
```

**Response:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440005",
  "evaluations": {
    "visual-math-001": {
      "content_type": "question",
      "overall": {
        "score": 0.95,
        "reasoning": "Excellent visual math problem with real-world context.",
        "suggested_improvements": null
      },
      "stimulus_quality": {
        "score": 1.0,
        "reasoning": "Image shows clear, countable objects. Object counting confirms 3 baskets with 4 apples each.",
        "suggested_improvements": null
      },
      "factual_accuracy": {
        "score": 1.0,
        "reasoning": "Correct answer is B) 12. 3 × 4 = 12 total apples.",
        "suggested_improvements": null
      },
      "weighted_score": 0.96
    }
  },
  "evaluation_time_seconds": 22.1,
  "inceptbench_version": "x.y.z",
  "failed_items": null
}
```

**Note:** The API automatically:

1. Detects image URLs in content
2. Downloads and encodes images
3. Performs object counting and visual analysis
4. Includes analysis data in evaluation context

---

## Error Handling

### Partial Success

When some items fail, successful items are still returned:

**Response:**

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440006",
  "evaluations": {
    "q1": {
      "content_type": "question",
      "overall": { "score": 0.85, "reasoning": "..." },
      "weighted_score": 0.87
    }
  },
  "evaluation_time_seconds": 15.0,
  "inceptbench_version": "x.y.z",
  "failed_items": [
    { "item_id": "q2", "error": "Evaluation failed: timeout" },
    { "item_id": "q3", "error": "Invalid curriculum: xyz" }
  ]
}
```

### Validation Errors

**Missing content:**

```json
HTTP 422 Unprocessable Entity
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "generated_content", 0, "content"],
      "msg": "Field required"
    }
  ]
}
```

**Empty array:**

```json
HTTP 422 Unprocessable Entity
{
  "detail": [
    {
      "type": "too_short",
      "loc": ["body", "generated_content"],
      "msg": "List should have at least 1 item"
    }
  ]
}
```

### Authentication Errors

**Missing API key:**

```json
HTTP 401 Unauthorized
{
  "detail": "Invalid or missing API key"
}
```

### Service Errors

**API keys not configured:**

```json
HTTP 503 Service Unavailable
{
  "detail": "Service initialization failed: OPENAI_API_KEY required"
}
```

---

## Using the Interactive Documentation

1. Start the API: `uvicorn inceptbench_new.api.main:app --reload`
2. Visit: http://localhost:8000/docs
3. Click **Authorize** and enter your API key
4. Click **Try it out** on the `/evaluate` endpoint
5. Enter your request JSON and click **Execute**

The interactive docs include:

- Request/response schemas
- Example values
- Validation rules
- Real-time testing
