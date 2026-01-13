"""
InceptBench REST API.

This module provides a REST API for evaluating educational content across
multiple dimensions including accuracy, curriculum alignment, and engagement.

Designed for Cloud Run and traditional server deployments (Docker, etc.).
"""

import logging
import os
import time
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from .dependencies import EvaluationServiceDep, APIKeyDep
from .models import (
    CurriculumsResponse,
    ErrorResponse,
    EvaluationRequest,
    EvaluationResponse,
    FailedItem,
    HealthResponse,
)
from ..core.processor import BatchProcessor
from ..config.settings import settings
from .. import __version__

logger = logging.getLogger(__name__)

# API Version - imported from package __init__.py
API_VERSION = __version__

# Concurrency control - max parallel evaluations per request
MAX_CONCURRENT_EVALUATIONS = int(
    os.getenv("MAX_CONCURRENT_EVALUATIONS", "10")
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting InceptBench API v{API_VERSION}")
    logger.info(f"Max concurrent evaluations: {MAX_CONCURRENT_EVALUATIONS}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down InceptBench API")


# Create FastAPI application
app = FastAPI(
    title="InceptBench API",
    description=(
        "AI-powered educational content evaluation service that assesses "
        "questions, quizzes, reading passages, and other educational "
        "materials across **11+ quality dimensions** including accuracy, "
        "curriculum alignment, clarity, misconception detection, and more."
        "\n\n"
        "## Useful Links\n\n"
        "- [Website](https://www.inceptbench.com/) - Official InceptBench site\n"
        "- [Benchmarks](https://benchmark.inceptbench.com/) - Benchmark results\n"
        "- [PyPI Package](https://pypi.org/project/inceptbench/) - Python package\n"
        "- [GitHub](https://github.com/trilogy-group/inceptbench) - Source code\n\n"
        "---\n\n"
        "## Authentication\n\n"
        "All evaluation endpoints require an API key. "
        "Click the **Authorize** button to enter your API key.\n\n"
        "---\n\n"
        "## Input Format\n\n"
        "All requests use a single array-based format:\n\n"
        "```json\n"
        '{\n'
        '  "generated_content": [\n'
        '    {\n'
        '      "id": "q1",\n'
        '      "curriculum": "common_core",\n'
        '      "request": {\n'
        '        "grade": "7",\n'
        '        "subject": "mathematics",\n'
        '        "type": "mcq",\n'
        '        "instructions": "Create a linear equation"\n'
        '      },\n'
        '      "content": "What is 2 + 2?"\n'
        '    }\n'
        '  ]\n'
        "}\n"
        "```\n\n"
        "### Content Item Fields\n\n"
        "| Field | Required | Default | Description |\n"
        "|-------|----------|---------|-------------|\n"
        "| `content` | Yes | - | Content to evaluate (string or JSON) |\n"
        "| `id` | No | Auto-generated | Unique identifier |\n"
        "| `curriculum` | No | `common_core` | Curriculum for alignment |\n"
        "| `request` | No | `null` | Generation metadata (see below) |\n\n"
        "### Request Metadata Fields (all optional)\n\n"
        "| Field | Description |\n"
        "|-------|-------------|\n"
        "| `grade` | Grade level (e.g., \"7\", \"K\", \"12\") |\n"
        "| `subject` | Subject area (e.g., \"mathematics\", \"english\") |\n"
        "| `type` | Content type (e.g., \"mcq\", \"fill-in\", \"article\") |\n"
        "| `difficulty` | Difficulty level (e.g., \"easy\", \"medium\", \"hard\") |\n"
        "| `locale` | Locale/language code (e.g., \"en-US\", \"es-MX\") |\n"
        "| `skills` | Skills info (JSON object or string) |\n"
        "| `instruction` | Generation instruction/prompt |\n\n"
        "The `content` field accepts any format - plain text, JSON object, "
        "or structured data. The evaluator automatically classifies and "
        "processes the content appropriately.\n\n"
        "### Images\n\n"
        "Images are automatically detected from content. Include as:\n"
        "- Direct URLs: `https://example.com/image.png`\n"
        "- Markdown: `![alt](https://example.com/image.png)`\n"
        "- HTML: `<img src=\"https://example.com/image.png\">`\n\n"
        "---\n\n"
        "## Performance\n\n"
        "- **Parallel Processing**: Items evaluated concurrently\n"
        "- **Concurrency Limit**: Max 10 items processed simultaneously\n"
        "- **Batch Support**: 1-100 items per request\n"
        "- **Partial Success**: Failed items don't block others"
    ),
    version=API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware (configure for your deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configure OpenAPI schema with security
def custom_openapi():
    """
    Customize OpenAPI schema to include Bearer token authentication.
    
    This adds the security scheme to the OpenAPI spec, which makes
    Swagger UI display the "Authorize" button.
    """
    if app.openapi_schema:
        return app.openapi_schema
       
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "API Key",
            "description": (
                "Enter your API key: `your-api-key-here`\n\n"
                "Sent as: `Authorization: Bearer <your-api-key>`"
            )
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    logger.warning(f"ValueError: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            error="ValidationError",
            message=str(exc)
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            detail=str(exc) if settings.LOG_LEVEL == "DEBUG" else None
        ).model_dump()
    )


# API Endpoints
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check endpoint",
    description="Check if the service is healthy and get version information"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns service health status and version information.
    """
    return HealthResponse(
        status="healthy",
        version=API_VERSION,
        service="InceptBench API"
    )


@app.get(
    "/curriculums",
    response_model=CurriculumsResponse,
    tags=["Metadata"],
    summary="List available curriculums",
    description=(
        "Get information about curriculum support. Returns the default "
        "curriculum. The API will return an error if an unsupported "
        "curriculum is requested."
    )
)
async def list_curriculums() -> CurriculumsResponse:
    """
    List curriculum information.
    
    Returns the default curriculum and available options.
    """
    return CurriculumsResponse(
        curriculums=[settings.DEFAULT_CURRICULUM],
        default=settings.DEFAULT_CURRICULUM
    )


@app.post(
    "/evaluate",
    response_model=EvaluationResponse,
    tags=["Evaluation"],
    summary="Evaluate educational content",
    description=(
        "Evaluate educational content across **11+ quality dimensions**.\n\n"
        "**Input Format:**\n"
        "```json\n"
        '{"generated_content": [{"content": "Your content here"}]}\n'
        "```\n\n"
        "**Response:**\n"
        "Returns evaluation results keyed by item ID, with scores and "
        "reasoning for each quality dimension.\n\n"
        "**Limits:** Maximum 100 items per request"
    ),
    response_description="Evaluation results with quality metrics"
)
async def evaluate_content(
    request: EvaluationRequest,
    service: EvaluationServiceDep,
    api_key: APIKeyDep
) -> EvaluationResponse:
    """
    Evaluate educational content.
    
    This endpoint accepts educational content and:
    1. Classifies content type (question, quiz, reading passage, etc.)
    2. Routes to the appropriate evaluator
    3. Processes items in parallel with concurrency control
    4. Returns evaluation results with scores and suggestions
    
    Args:
        request: EvaluationRequest with generated_content array
        service: Injected EvaluationService instance
        api_key: API key for authentication
    
    Returns:
        EvaluationResponse with evaluations keyed by item ID
    
    Raises:
        HTTPException: If evaluation fails or validation errors occur
    """
    start_time = time.time()
    request_id = str(uuid4())
    
    items = request.generated_content
    
    logger.info(
        f"[{request_id}] Evaluating {len(items)} item(s) "
        f"(max concurrent: {MAX_CONCURRENT_EVALUATIONS})"
    )

    try:
        # Use BatchProcessor for parallel evaluation
        processor = BatchProcessor(
            service=service,
            max_concurrent=MAX_CONCURRENT_EVALUATIONS
        )

        # Process all items (no progress callback for API)
        batch_result = await processor.process_batch(items)
        
        # Calculate total time
        evaluation_time = time.time() - start_time
        
        # Log summary
        if batch_result.failed_items:
            logger.warning(
                f"[{request_id}] Partial success. "
                f"Success: {batch_result.success_count}, "
                f"Failed: {batch_result.failure_count}, "
                f"Time: {evaluation_time:.2f}s"
            )
        else:
            logger.info(
                f"[{request_id}] Complete. "
                f"Items: {batch_result.success_count}, "
                f"Time: {evaluation_time:.2f}s"
            )
        
        # Build failed items list for API response
        failed_items_list = None
        if batch_result.failed_items:
            failed_items_list = [
                FailedItem(item_id=fi.item_id, error=fi.error)
                for fi in batch_result.failed_items
            ]
        
        # Return response
        return EvaluationResponse(
            request_id=request_id,
            evaluations=batch_result.evaluations,
            evaluation_time_seconds=evaluation_time,
            inceptbench_version=API_VERSION,
            failed_items=failed_items_list
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"[{request_id}] Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(
            f"[{request_id}] Error during evaluation: {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )


# Root endpoint
@app.get(
    "/",
    include_in_schema=False,
    tags=["Root"]
)
async def root():
    """Root endpoint - provides API information."""
    return {
        "service": "InceptBench API",
        "version": API_VERSION,
        "inceptbench_version": API_VERSION,
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "evaluate": "POST /evaluate",
            "curriculums": "GET /curriculums",
            "health": "GET /health"
        },
        "input_format": {
            "description": "Single array-based format for all content",
            "example": {
                "generated_content": [
                    {
                        "content": "What is 2 + 2?",
                        "curriculum": "common_core",
                        "request": {
                            "grade": "3",
                            "subject": "math"
                        }
                    }
                ]
            }
        },
        "limits": {
            "max_items_per_request": 100,
            "max_concurrent_evaluations": MAX_CONCURRENT_EVALUATIONS
        }
    }


# For local development and testing
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "inceptbench_new.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
