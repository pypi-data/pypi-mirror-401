# InceptBench - Educational Content Evaluator

A production-ready system for evaluating educational content quality using LLM-based analysis.

## Overview

InceptBench evaluates educational content across multiple quality dimensions:

- **Automated Classification** - Determines content type (question, quiz, reading passage, etc.)
- **Hierarchical Evaluation** - Decomposes complex content (e.g., quiz → questions) and evaluates bottom-up
- **Comprehensive Metrics** - Assesses 8-11 metrics per content type with scores and reasoning
- **Curriculum-Aware** - Integrates curriculum standards via vector store search
- **Image Analysis** - Counts objects and analyzes visual stimuli

## Installation

### Prerequisites

- Python 3.11+
- API keys: OpenAI (required), Gemini (for images), Anthropic (for images), Incept API key (for curriculum search)

### Setup

```bash
# Install dependencies
pip install -r inceptbench_new/requirements.txt

# Configure environment
cat > .env << EOF
OPENAI_API_KEY=your-openai-key
INCEPT_API_KEY=your-incept-api-key
INCEPTBENCH_API_KEY=your-api-key
GEMINI_API_KEY=your-gemini-key
ANTHROPIC_API_KEY=your-anthropic-key
EOF
```

## Usage

> **Important:** Before using InceptBench (CLI, API, or programmatic), ensure environment variables are set. See [Configuration](#configuration) for details.

InceptBench offers three ways to evaluate content:

### 1. Programmatic (Python)

```python
import asyncio
from inceptbench_new.service import EvaluationService

async def main():
    service = EvaluationService()
    
    # Evaluate content
    result = await service.evaluate(
        content="What is 2+2? A) 3 B) 4 C) 5 D) 6",
        curriculum="common_core",
        generation_prompt="Create a basic addition question for grade 2"
    )
    
    print(f"Content Type: {result.content_type}")
    print(f"Overall Score: {result.overall.score:.2f}")
    print(f"Reasoning: {result.overall.reasoning}")
    
    # Or get JSON directly
    json_result = await service.evaluate_json(content="Your content here")
    print(json_result)

asyncio.run(main())
```

**Convenience imports:**

```python
from inceptbench_new.service import EvaluationService
from inceptbench_new.core import ContentItem, BatchProcessor
```

### 2. Command Line (CLI)

```bash
# Create sample input file
python -m inceptbench_new example

# Evaluate from JSON file
python -m inceptbench_new evaluate content.json

# Evaluate raw content
python -m inceptbench_new evaluate --raw "What is 2+2?"

# Save results
python -m inceptbench_new evaluate content.json -o results.json
```

See [cli/README.md](cli/README.md) for complete CLI documentation.

### 3. REST API

```bash
# Start server
uvicorn inceptbench_new.api.main:app --reload

# Evaluate via HTTP
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"generated_content": [{"content": "What is 2+2?"}]}'
```

See [api/README.md](api/README.md) for complete API documentation.

## Input Format

All interfaces (programmatic, CLI, API) use the same content structure:

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

## Images in Content

Images are **automatically detected** from the content string. No separate `image_url` field is needed.

**Supported formats:**

| Format | Example |
| ------ | ------- |
| Direct URL | `https://example.com/image.png` |
| Markdown | `![description](https://example.com/image.png)` |
| HTML | `<img src="https://example.com/image.png">` |

**Example content with image:**

```json
{
  "content": "Look at the triangle below:\n\n![triangle](https://example.com/triangle.png)\n\nWhat is the area of the triangle?"
}
```

When images are detected:
- They are sent to vision-capable models (GPT-4o, Claude) for analysis
- Object counting is performed automatically
- Visual properties are analyzed for educational relevance

## Content Types

The evaluator automatically classifies content into one of these types:

| Type                 | Description                  | Metrics |
| -------------------- | ---------------------------- | ------- |
| `question`           | Single educational question  | 11      |
| `quiz`               | Multiple questions together  | 8       |
| `fiction_reading`    | Fictional narrative passages | 9       |
| `nonfiction_reading` | Informational passages       | 9       |
| `other`              | General educational content  | 8       |

> **Note:** The `type` field in request metadata can be any string (e.g., "mcq", "fill-in", "article"). The evaluator will classify the actual content and map it to one of the above types internally.

## Metrics

### Universal Metrics

| Metric                 | Type    | Description                 |
| ---------------------- | ------- | --------------------------- |
| `overall`              | 0.0-1.0 | Holistic quality score      |
| `factual_accuracy`     | Binary  | Factually correct           |
| `educational_accuracy` | Binary  | Fulfills educational intent |

### Content-Specific Metrics

**Question:** curriculum_alignment, clarity_precision, reveals_misconceptions, difficulty_alignment, passage_reference, distractor_quality, stimulus_quality, mastery_learning_alignment

**Quiz:** concept_coverage, difficulty_distribution, non_repetitiveness, test_preparedness, answer_balance

**Reading:** reading_level_match, length_appropriateness, topic_focus, engagement, accuracy_and_logic, question_quality

**Other:** educational_value, direct_instruction_alignment, content_appropriateness, clarity_and_organization, engagement

## Architecture

```
Content → Classifier → Decomposer → Orchestrator → Evaluators → Result
                                         ↓
                                   [Tools: curriculum search, image analysis]
```

### Components

```
inceptbench_new/
├── service.py          # Main EvaluationService
├── core/               # Shared models and processor
│   ├── input_models.py # ContentItem, RequestMetadata
│   └── processor.py    # BatchProcessor
├── classifier/         # Content type classification
├── decomposer/         # Hierarchical decomposition
├── orchestrator/       # Bottom-up evaluation coordination
├── evaluators/         # Type-specific evaluators
├── models/             # Pydantic output models
├── tools/              # Utilities (curriculum, images)
├── prompts/            # LLM prompt templates
├── config/             # Settings
├── api/                # REST API (FastAPI)
└── cli/                # Command-line interface
```

## Configuration

### Environment Variables

| Variable                     | Required | Description                          |
| ---------------------------- | -------- | ------------------------------------ |
| `OPENAI_API_KEY`             | Yes      | OpenAI API key (powers evaluations)  |
| `INCEPT_API_KEY`             | Yes      | For curriculum search API            |
| `INCEPTBENCH_API_KEY`        | Yes      | API authentication key(s)            |
| `GEMINI_API_KEY`             | No       | For image analysis                   |
| `ANTHROPIC_API_KEY`          | No       | For image analysis (fallback)        |
| `MAX_CONCURRENT_EVALUATIONS` | No       | Parallel limit (default: 10)         |
| `LOG_LEVEL`                  | No       | Logging level (default: INFO)        |

### Curriculum

```python
# Use default (common_core)
result = await service.evaluate(content)

# Specify curriculum
result = await service.evaluate(content, curriculum="common_core")
```

## Extending

### Adding a New Evaluator

1. Create model in `models/new_type.py`
2. Create prompt in `prompts/new_type/evaluation.txt`
3. Create evaluator in `evaluators/new_type.py`
4. Update classifier prompt in `prompts/classifier.txt`
5. Register in orchestrator

## Performance

| Stage          | Time                   |
| -------------- | ---------------------- |
| Classification | 1-3 seconds            |
| Evaluation     | 10-30 seconds          |
| **Total**      | 15-35 seconds per item |

## License

See LICENSE file in repository root.
