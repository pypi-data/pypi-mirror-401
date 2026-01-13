# InceptBench CLI

Command-line interface for evaluating educational content.

## Prerequisites

Before using the CLI, set the required environment variables:

```bash
export OPENAI_API_KEY=your-openai-key        # Required
export INCEPT_API_KEY=your-incept-api-key    # Required
export GEMINI_API_KEY=your-gemini-key        # Optional (for images)
export ANTHROPIC_API_KEY=your-anthropic-key  # Optional (for images)
```

| Variable | Required | Description |
| -------- | -------- | ----------- |
| `OPENAI_API_KEY` | Yes | Powers LLM evaluations |
| `INCEPT_API_KEY` | Yes | For curriculum search API |
| `GEMINI_API_KEY` | No | For image analysis |
| `ANTHROPIC_API_KEY` | No | For image analysis (fallback) |

## Quick Start

```bash
# Create sample input file
python -m inceptbench_new example

# Evaluate content
python -m inceptbench_new evaluate content.json
```

## Commands

### `example`

Creates a sample `content.json` file with example content items.

```bash
python -m inceptbench_new example
```

Output:

```
Created content.json

Edit the file, then run:
  inceptbench evaluate content.json
```

### `evaluate`

Evaluate educational content. Supports two mutually exclusive input modes:

#### Mode 1: JSON File (Batch Mode)

```bash
python -m inceptbench_new evaluate <content.json>
```

The JSON file uses the same format as the API. Only `content` is required; all other fields are optional:

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

**Field Reference:**

- `content` (required): String or JSON object to evaluate
- `id` (optional): Unique identifier (auto-generated if omitted)
- `curriculum` (optional): Curriculum for alignment (default: `common_core`)
- `request` (optional): Generation metadata with all optional fields: `grade`, `subject`, `type`, `difficulty`, `locale`, `skills`, `instruction`

#### Mode 2: Raw Content

```bash
# Direct string
python -m inceptbench_new evaluate --raw "What is 2+2? A) 3 B) 4 C) 5"

# From file (.txt or .md)
python -m inceptbench_new evaluate --raw content.txt
```

**Raw mode options:**

| Option                | Description                                      |
| --------------------- | ------------------------------------------------ |
| `--curriculum NAME`   | Curriculum for evaluation (default: common_core) |
| `--generation-prompt` | Generation prompt (string or .txt/.md file)      |

```bash
# With curriculum and prompt
python -m inceptbench_new evaluate --raw question.txt \
  --curriculum common_core \
  --generation-prompt "Create a grade 5 math question"

# Prompt from file
python -m inceptbench_new evaluate --raw question.txt \
  --generation-prompt prompt.md
```

## Common Options

| Option          | Short | Description               |
| --------------- | ----- | ------------------------- |
| `--output FILE` | `-o`  | Save results to JSON file |
| `--verbose`     | `-v`  | Show verbose/debug output |

```bash
# Save results to file
python -m inceptbench_new evaluate content.json -o results.json

# Verbose mode
python -m inceptbench_new evaluate content.json -v
```

## Input Validation

- **JSON mode**: File must have `.json` extension and valid JSON format
- **Raw mode**: String argument or file with `.txt`/`.md` extension
- `--curriculum` and `--generation-prompt` only allowed with `--raw`
- Cannot use both positional JSON file and `--raw` together

## Images in Content

Images are automatically detected from content (no separate field needed):

```bash
# Image URL in raw content
python -m inceptbench_new evaluate --raw "![triangle](https://example.com/img.png) What is the area?"

# Or in JSON file content field
# {"content": "![img](url)\n\nQuestion text..."}
```

Supported formats: Direct URLs, Markdown `![](url)`, HTML `<img src="url">`.

## Output Format

Results are printed to stdout (and saved to file with `-o`):

```
Evaluation Results
==================
Total: 2 | Success: 2 | Failed: 0

Item: q1
  Type: question
  Overall: 0.85
  Weighted: 0.82
  Metrics:
    factual_accuracy: 1.00
    educational_accuracy: 1.00
    curriculum_alignment: 0.80
    ...
```

JSON output format:

```json
{
  "evaluations": {
    "q1": {
      "content_type": "question",
      "overall": {
        "score": 0.85,
        "reasoning": "...",
        "suggested_improvements": "..."
      },
      "factual_accuracy": {"score": 1.0, "reasoning": "..."},
      ...
    }
  },
  "failed_items": [],
  "success_count": 1,
  "failure_count": 0,
  "total_count": 1
}
```

## Examples

```bash
# Evaluate a quiz
python -m inceptbench_new evaluate quiz.json -o quiz_results.json

# Evaluate raw question with context
python -m inceptbench_new evaluate --raw "Solve for x: 2x + 5 = 15" \
  --curriculum common_core \
  --generation-prompt "Grade 7 algebra, solving linear equations"

# Verbose mode for debugging
python -m inceptbench_new evaluate content.json -v

# Process and save results
python -m inceptbench_new evaluate content.json -o results.json
```

## Exit Codes

| Code | Description                                     |
| ---- | ----------------------------------------------- |
| 0    | Success                                         |
| 1    | Error (invalid input, evaluation failure, etc.) |

## Troubleshooting

### "No content to evaluate"

Either provide a JSON file or use `--raw`:

```bash
python -m inceptbench_new evaluate content.json
# or
python -m inceptbench_new evaluate --raw "Your content"
```

### "Cannot use both content_json and --raw"

These are mutually exclusive. Use one or the other:

```bash
# ✓ Correct
python -m inceptbench_new evaluate content.json
python -m inceptbench_new evaluate --raw "content"

# ✗ Wrong
python -m inceptbench_new evaluate content.json --raw "content"
```

### "--curriculum and --generation-prompt require --raw"

These options are only for raw content mode:

```bash
# ✓ Correct
python -m inceptbench_new evaluate --raw "content" --curriculum common_core

# ✗ Wrong (JSON mode doesn't need these - put them in the JSON)
python -m inceptbench_new evaluate content.json --curriculum common_core
```
