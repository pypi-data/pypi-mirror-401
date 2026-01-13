# InceptBench

[![PyPI version](https://img.shields.io/pypi/v/inceptbench?logo=pypi)](https://pypi.org/project/inceptbench/)
[![Python Version](https://img.shields.io/pypi/pyversions/inceptbench?logo=python)](https://www.python.org/)
![License](https://img.shields.io/badge/License-Proprietary-orange.svg)
[![Swagger](https://img.shields.io/badge/Swagger-API_Docs-85EA2D?logo=swagger)](https://api.inceptbench.com/docs)

Educational content evaluation framework using LLM-based analysis.

[Website](https://www.inceptbench.com/) • [Benchmarks](https://benchmark.inceptbench.com/) • [API Endpoint](https://api.inceptbench.com/) • [API Docs](https://api.inceptbench.com/docs) • [GitHub](https://github.com/trilogy-group/inceptbench)

## Overview

InceptBench evaluates educational content across multiple quality dimensions:

- **Automated Classification** - Determines content type (question, quiz, reading, etc.)
- **Hierarchical Evaluation** - Decomposes complex content and evaluates bottom-up
- **Comprehensive Metrics** - 8-11 metrics per content type with scores and reasoning
- **Curriculum-Aware** - Integrates curriculum standards via vector store search

## Installation

```bash
pip install inceptbench
```

## CLI Usage

```bash
# Create sample input file
inceptbench example

# Evaluate from JSON file
inceptbench evaluate content.json

# Evaluate raw content
inceptbench evaluate --raw "What is 2+2? A) 3 B) 4 C) 5 D) 6"

# Save results to file
inceptbench evaluate content.json -o results.json

# Check version
inceptbench --version
```

## REST API

The production API is available at **https://api.inceptbench.com**

```bash
# Health check
curl https://api.inceptbench.com/health

# Interactive docs
# Visit: https://api.inceptbench.com/docs

# Evaluate content
curl -X POST https://api.inceptbench.com/evaluate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"generated_content": [{"content": "What is 2+2? A) 3 B) 4 C) 5 D) 6"}]}'
```

## Programmatic Usage (Python)

```python
import asyncio
from inceptbench_new import EvaluationService

async def main():
    service = EvaluationService()
    result = await service.evaluate(
        content="What is 2+2? A) 3 B) 4 C) 5 D) 6",
        curriculum="common_core"
    )
    print(f"Score: {result.overall.score:.2f}")

asyncio.run(main())
```

## Input Format

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
      "content": "What is 2+2? A) 3 B) 4 C) 5 D) 6"
    }
  ]
}
```

### Content Item Fields

| Field        | Required | Default        | Description                          |
| ------------ | -------- | -------------- | ------------------------------------ |
| `content`    | Yes      | -              | Content to evaluate (string or JSON) |
| `id`         | No       | Auto-generated | Unique identifier                    |
| `curriculum` | No       | `common_core`  | Curriculum for alignment             |
| `request`    | No       | `null`         | Generation metadata (see below)      |

### Request Metadata Fields (all optional)

| Field         | Description                                       |
| ------------- | ------------------------------------------------- |
| `grade`       | Grade level (e.g., "7", "K", "12")                |
| `subject`     | Subject area (e.g., "mathematics", "english")     |
| `type`        | Content type (e.g., "mcq", "fill-in", "article")  |
| `difficulty`  | Difficulty level (e.g., "easy", "medium", "hard") |
| `locale`      | Locale/language code (e.g., "en-US", "es-MX")     |
| `skills`      | Skills info (JSON object or string)               |
| `instruction` | Generation instruction/prompt                     |

### Images

Images are automatically detected from content. Include as:

- Direct URLs: `https://example.com/image.png`
- Markdown: `![alt](https://example.com/image.png)`
- HTML: `<img src="https://example.com/image.png">`

## Content Types

The evaluator automatically classifies content into:

| Type                 | Description                  |
| -------------------- | ---------------------------- |
| `question`           | Single educational question  |
| `quiz`               | Multiple questions together  |
| `fiction_reading`    | Fictional narrative passages |
| `nonfiction_reading` | Informational passages       |
| `other`              | General educational content  |

## Documentation

For complete documentation, input format details, and developer guides:

**[View Full Documentation on GitHub](https://github.com/trilogy-group/inceptbench)**

## License

Proprietary - Copyright Trilogy Education Services
