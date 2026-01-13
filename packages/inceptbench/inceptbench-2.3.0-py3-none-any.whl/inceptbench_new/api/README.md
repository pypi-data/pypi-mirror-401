# InceptBench REST API

FastAPI application for evaluating educational content via HTTP.

## Quick Start

```bash
# Install dependencies
pip install -r inceptbench_new/requirements.txt

# Configure environment
export OPENAI_API_KEY=your-key
export INCEPT_API_KEY=your-incept-api-key
export INCEPTBENCH_API_KEY=your-api-key
export GEMINI_API_KEY=your-gemini-key          # optional
export ANTHROPIC_API_KEY=your-anthropic-key    # optional

# Start server
uvicorn inceptbench_new.api.main:app --reload
```

Access:

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Endpoints

### `POST /evaluate`

Evaluate educational content.

**Request:**

```json
{
  "generated_content": [
    {
      "id": "q1",
      "curriculum": "common_core",
      "request": {
        "grade": "7",
        "subject": "mathematics",
        "type": "mcq",
        "difficulty": "medium",
        "locale": "en-US",
        "skills": {
          "lesson_title": "Solving Linear Equations",
          "substandard_id": "CCSS.MATH.7.EE.A.1"
        },
        "instruction": "Create a linear equation problem"
      },
      "content": {
        "question": "What is x in 3x + 7 = 22?",
        "answer": "C",
        "options": ["3", "4", "5", "6"]
      }
    }
  ]
}
```

**Content Item Fields:**

| Field        | Required | Default        | Description                          |
| ------------ | -------- | -------------- | ------------------------------------ |
| `content`    | Yes      | -              | Content to evaluate (string or JSON) |
| `id`         | No       | Auto-generated | Unique identifier                    |
| `curriculum` | No       | `common_core`  | Curriculum for alignment             |
| `request`    | No       | `null`         | Generation metadata (see below)      |

**Request Metadata Fields (all optional):**

| Field         | Description                                       |
| ------------- | ------------------------------------------------- |
| `grade`       | Grade level (e.g., "7", "K", "12")                |
| `subject`     | Subject area (e.g., "mathematics", "english")     |
| `type`        | Content type (e.g., "mcq", "fill-in", "article")  |
| `difficulty`  | Difficulty level (e.g., "easy", "medium", "hard") |
| `locale`      | Locale/language code (e.g., "en-US", "es-MX")     |
| `skills`      | Skills info (JSON object or string)               |
| `instruction` | Generation instruction/prompt                     |

**Images in Content:**

Images are automatically detected from the content string (no separate field needed):

```json
{
  "content": "![triangle](https://example.com/triangle.png)\n\nWhat is the area?"
}
```

Supported: Direct URLs, Markdown `![](url)`, HTML `<img src="url">`.

**Response:**

```json
{
  "request_id": "uuid",
  "evaluations": {
    "q1": {
        "content_type": "question",
        "overall": {
          "score": 0.85,
          "reasoning": "...",
          "suggested_improvements": "..."
        },
      "factual_accuracy": { "score": 1.0, "reasoning": "..." },
      "educational_accuracy": { "score": 1.0, "reasoning": "..." },
      "weighted_score": 0.82
    }
  },
  "evaluation_time_seconds": 12.34,
  "inceptbench_version": "2.1.0",
  "failed_items": null
}
```

**Partial Success:**

```json
{
  "evaluations": {"q1": {...}},
  "failed_items": [{"item_id": "q2", "error": "Evaluation failed: timeout"}]
}
```

### `GET /health`

```json
{
  "status": "healthy",
  "version": "2.1.0",
  "service": "Educational Content Evaluator"
}
```

### `GET /curriculums`

```json
{ "curriculums": ["common_core"], "default": "common_core" }
```

### `GET /`

API info and endpoint listing.

## Authentication

Bearer token authentication:

```bash
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/evaluate
```

Configure API keys:

```bash
# Single key
export INCEPTBENCH_API_KEY=your-api-key

# Multiple keys
export INCEPTBENCH_API_KEY=key1,key2,key3
```

Generate a secure key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Configuration

| Variable                     | Default  | Description                          |
| ---------------------------- | -------- | ------------------------------------ |
| `OPENAI_API_KEY`             | Required | OpenAI API key (powers evaluations)  |
| `INCEPT_API_KEY`             | Required | For curriculum search API            |
| `INCEPTBENCH_API_KEY`        | Required | API authentication key(s)            |
| `GEMINI_API_KEY`             | Optional | For image analysis                   |
| `ANTHROPIC_API_KEY`          | Optional | For image analysis (fallback)        |
| `MAX_CONCURRENT_EVALUATIONS` | `10`     | Max parallel evaluations per request |

## Examples

**curl:**

```bash
# Simple evaluation
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"generated_content": [{"content": "What is 2+2?"}]}'

# With metadata
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "generated_content": [{
      "id": "q1",
      "curriculum": "common_core",
      "request": {"grade": "5", "subject": "math"},
      "content": {"question": "What is 2+2?", "answer": "4"}
    }]
  }'

# Batch
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"generated_content": [{"content": "Q1"}, {"content": "Q2"}]}'
```

**Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/evaluate",
    headers={"Authorization": "Bearer your-api-key"},
    json={"generated_content": [{"content": "What is 2+2?"}]}
)

result = response.json()
evaluation = result["evaluations"][list(result["evaluations"].keys())[0]]
print(f"Score: {evaluation['overall']['score']:.2f}")
```

## Deployment

### Docker

```bash
docker-compose up --build
```

### Google Cloud Run

```bash
./deploy_to_cloudrun.sh
```

Options:

| Flag              | Default           | Description             |
| ----------------- | ----------------- | ----------------------- |
| `--project`       | -                 | Google Cloud project ID |
| `--region`        | `us-central1`     | Deployment region       |
| `--service`       | `inceptbench-api` | Service name            |
| `--memory`        | `2Gi`             | Memory allocation       |
| `--cpu`           | `2`               | CPU allocation          |
| `--min-instances` | `0`               | Minimum instances       |
| `--max-instances` | `10`              | Maximum instances       |

```bash
./deploy_to_cloudrun.sh --memory 4Gi --cpu 4 --min-instances 1
```

## Limits

- Maximum **100 items** per request
- Parallel processing with configurable concurrency (default: 10)
- Failed items don't block successful evaluations

## Error Codes

| Status | Description                                         |
| ------ | --------------------------------------------------- |
| 200    | Success (check `failed_items` for partial failures) |
| 400    | Invalid input                                       |
| 401    | Missing/invalid API key                             |
| 422    | Schema validation failed                            |
| 500    | Internal server error                               |
| 503    | Service unavailable (API keys not configured)       |
