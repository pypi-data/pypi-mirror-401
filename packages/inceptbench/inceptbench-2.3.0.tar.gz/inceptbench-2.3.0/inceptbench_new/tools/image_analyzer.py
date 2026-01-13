"""
Image analysis functionality for educational content evaluation.

This module provides accurate visual analysis by combining:
1. Computer Vision (OpenCV) for precise geometric measurements
2. LLM vision for semantic understanding and classification

The CV layer extracts accurate measurements (angles, side lengths, etc.)
which are then provided to the LLM for interpretation and classification.
This separation leverages each technology's strengths.
"""

import asyncio
import base64
import logging
import math
import random
import time
from typing import List, Optional, Tuple

import cv2
import numpy as np
import requests
from pydantic import BaseModel, Field

from inceptbench_new.llm import LLMFactory, LLMImage, LLMMessage
from inceptbench_new.tools.image_utils import _clean_image_url
from inceptbench_new.utils.failure_tracker import AttemptError, FailureTracker

logger = logging.getLogger(__name__)

# Retry configuration for image downloads
IMAGE_DOWNLOAD_MAX_RETRIES = 3
IMAGE_DOWNLOAD_BASE_DELAY = 4.0


# =============================================================================
# Computer Vision Analysis - Extracts accurate measurements from images
# =============================================================================

class DetectedVertex(BaseModel):
    """A vertex (corner) of a detected shape."""
    x: float = Field(description="X coordinate in pixels")
    y: float = Field(description="Y coordinate in pixels")
    interior_angle: float = Field(description="Interior angle at this vertex in degrees")


class DetectedShape(BaseModel):
    """A shape detected by computer vision with computed measurements."""
    shape_id: int = Field(description="Unique identifier for this shape")
    num_vertices: int = Field(description="Number of vertices/corners")
    vertices: List[DetectedVertex] = Field(description="List of vertices with coordinates and angles")
    side_lengths: List[float] = Field(description="Length of each side in pixels, ordered by vertex")
    centroid: Tuple[float, float] = Field(description="Center point (x, y) of the shape")
    area: float = Field(description="Area in square pixels")
    perimeter: float = Field(description="Perimeter in pixels")
    bounding_box: Tuple[float, float, float, float] = Field(description="Bounding box (x, y, width, height)")
    is_convex: bool = Field(description="Whether the shape is convex")
    
    # Computed properties for classification
    side_length_ratios: List[float] = Field(description="Ratio of each side to the longest side")
    angle_variance: float = Field(description="Variance in interior angles (0 = all equal)")
    min_angle: float = Field(description="Smallest interior angle")
    max_angle: float = Field(description="Largest interior angle")


class CVAnalysisResult(BaseModel):
    """Results from computer vision analysis."""
    success: bool
    image_width: int
    image_height: int
    shapes: List[DetectedShape]
    error_message: Optional[str] = None


def compute_angle(p1: np.ndarray, vertex: np.ndarray, p2: np.ndarray) -> float:
    """
    Compute the interior angle at 'vertex' formed by points p1-vertex-p2.
    
    Returns angle in degrees.
    """
    v1 = p1 - vertex
    v2 = p2 - vertex
    
    # Normalize vectors
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)
    
    if v1_norm == 0 or v2_norm == 0:
        return 0.0
    
    v1 = v1 / v1_norm
    v2 = v2 / v2_norm
    
    # Compute angle using dot product
    dot = np.clip(np.dot(v1, v2), -1.0, 1.0)
    angle_rad = math.acos(dot)
    angle_deg = math.degrees(angle_rad)
    
    return angle_deg


def analyze_contour(contour: np.ndarray, shape_id: int, epsilon_factor: float = 0.02) -> Optional[DetectedShape]:
    """
    Analyze a single contour and extract geometric measurements.
    
    Args:
        contour: OpenCV contour
        shape_id: Unique identifier for this shape
        epsilon_factor: Approximation accuracy (lower = more vertices)
    
    Returns:
        DetectedShape with computed measurements, or None if invalid
    """
    # Approximate polygon
    perimeter = cv2.arcLength(contour, True)
    epsilon = epsilon_factor * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    num_vertices = len(approx)
    if num_vertices < 3:
        return None
    
    # Extract vertices
    vertices_array = approx.reshape(-1, 2).astype(float)
    
    # Compute side lengths
    side_lengths = []
    for i in range(num_vertices):
        p1 = vertices_array[i]
        p2 = vertices_array[(i + 1) % num_vertices]
        length = np.linalg.norm(p2 - p1)
        side_lengths.append(float(length))
    
    # Compute interior angles at each vertex
    angles = []
    for i in range(num_vertices):
        p_prev = vertices_array[(i - 1) % num_vertices]
        p_curr = vertices_array[i]
        p_next = vertices_array[(i + 1) % num_vertices]
        angle = compute_angle(p_prev, p_curr, p_next)
        angles.append(angle)
    
    # Build vertex list
    detected_vertices = []
    for i, (coord, angle) in enumerate(zip(vertices_array, angles)):
        detected_vertices.append(DetectedVertex(
            x=float(coord[0]),
            y=float(coord[1]),
            interior_angle=round(angle, 1)
        ))
    
    # Compute other properties
    area = cv2.contourArea(contour)
    moments = cv2.moments(contour)
    if moments['m00'] != 0:
        cx = moments['m10'] / moments['m00']
        cy = moments['m01'] / moments['m00']
    else:
        cx, cy = np.mean(vertices_array, axis=0)
    
    x, y, w, h = cv2.boundingRect(contour)
    is_convex = cv2.isContourConvex(approx)
    
    # Compute ratios and variance
    max_side = max(side_lengths) if side_lengths else 1
    side_ratios = [s / max_side for s in side_lengths]
    angle_variance = float(np.var(angles)) if angles else 0.0
    
    return DetectedShape(
        shape_id=shape_id,
        num_vertices=num_vertices,
        vertices=detected_vertices,
        side_lengths=[round(s, 1) for s in side_lengths],
        centroid=(round(cx, 1), round(cy, 1)),
        area=round(area, 1),
        perimeter=round(perimeter, 1),
        bounding_box=(float(x), float(y), float(w), float(h)),
        is_convex=is_convex,
        side_length_ratios=[round(r, 3) for r in side_ratios],
        angle_variance=round(angle_variance, 1),
        min_angle=round(min(angles), 1) if angles else 0.0,
        max_angle=round(max(angles), 1) if angles else 0.0
    )



def deduplicate_shapes(shapes: List[DetectedShape], centroid_threshold: float = 50.0) -> List[DetectedShape]:
    """
    Deduplicate shapes that have similar centroids (likely the same shape detected multiple times
    due to thick outlines or concentric contours).
    
    For each group of similar shapes, keeps only the largest one.
    
    Args:
        shapes: List of detected shapes
        centroid_threshold: Maximum distance between centroids to consider shapes as duplicates
    
    Returns:
        Deduplicated list of shapes
    """
    if not shapes:
        return shapes
    
    # Group shapes by proximity of centroids
    groups: List[List[DetectedShape]] = []
    used = set()
    
    for i, shape in enumerate(shapes):
        if i in used:
            continue
            
        # Start a new group with this shape
        group = [shape]
        used.add(i)
        
        # Find all shapes with similar centroids and same number of vertices
        for j, other_shape in enumerate(shapes):
            if j in used:
                continue
            
            # Only group shapes with the same number of vertices
            if shape.num_vertices != other_shape.num_vertices:
                continue
                
            # Check centroid distance
            dist = math.sqrt(
                (shape.centroid[0] - other_shape.centroid[0]) ** 2 +
                (shape.centroid[1] - other_shape.centroid[1]) ** 2
            )
            
            if dist < centroid_threshold:
                group.append(other_shape)
                used.add(j)
        
        groups.append(group)
    
    # Keep only the largest shape from each group
    deduplicated = []
    for group in groups:
        # Sort by area (largest first) and keep the first one
        group.sort(key=lambda s: s.area, reverse=True)
        deduplicated.append(group[0])
    
    # Re-assign IDs
    for i, shape in enumerate(deduplicated):
        shape.shape_id = i
    
    return deduplicated


def run_cv_analysis(image_bytes: bytes, min_area_ratio: float = 0.001) -> CVAnalysisResult:
    """
    Run computer vision analysis on an image to detect shapes and compute measurements.
    
    Args:
        image_bytes: Raw image data
        min_area_ratio: Minimum shape area as ratio of image area (filters noise)
    
    Returns:
        CVAnalysisResult with detected shapes and measurements
    """
    try:
        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return CVAnalysisResult(
                success=False,
                image_width=0,
                image_height=0,
                shapes=[],
                error_message="Failed to decode image"
            )
        
        height, width = img.shape[:2]
        min_area = width * height * min_area_ratio
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding to handle varying lighting
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Also try Canny edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Combine both approaches
        combined = cv2.bitwise_or(thresh, edges)
        
        # Find contours
        contours, hierarchy = cv2.findContours(
            combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Analyze each contour
        shapes = []
        shape_id = 0
        
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            
            # Filter by area (skip tiny contours and image-border-sized contours)
            if area < min_area:
                continue
            if area > width * height * 0.95:  # Skip if nearly full image
                continue
            
            # Analyze the contour
            shape = analyze_contour(contour, shape_id)
            if shape is not None and shape.num_vertices >= 3:
                shapes.append(shape)
                shape_id += 1
        
        # Sort shapes by area (largest first)
        shapes.sort(key=lambda s: s.area, reverse=True)
        
        # Deduplicate shapes with similar centroids (removes duplicates from thick outlines)
        shapes = deduplicate_shapes(shapes)
        
        return CVAnalysisResult(
            success=True,
            image_width=width,
            image_height=height,
            shapes=shapes,
            error_message=None
        )
        
    except Exception as e:
        logger.error(f"CV analysis failed: {e}")
        return CVAnalysisResult(
            success=False,
            image_width=0,
            image_height=0,
            shapes=[],
            error_message=str(e)
        )


def _group_similar_shapes(shapes: List[DetectedShape]) -> dict:
    """
    Group shapes by their geometric signature (num vertices, angle pattern, etc.)
    for more efficient summarization.
    """
    groups: dict[str, List[DetectedShape]] = {}
    
    for shape in shapes:
        # Create a signature based on key properties
        # Round angles to nearest 5 degrees for grouping
        angle_pattern = tuple(round(v.interior_angle / 5) * 5 for v in shape.vertices)
        min_ratio = min(shape.side_length_ratios)
        side_equality = "equal" if min_ratio > 0.9 else ("similar" if min_ratio > 0.7 else "varied")
        
        key = f"{shape.num_vertices}v_{side_equality}_{angle_pattern}"
        if key not in groups:
            groups[key] = []
        groups[key].append(shape)
    
    return groups


def format_cv_measurements_for_llm(cv_result: CVAnalysisResult, max_detailed_shapes: int = 10) -> str:
    """
    Format CV measurements into a clear text description for the LLM.
    
    This provides the LLM with accurate geometric data it can use
    for classification, without requiring it to measure from the image.
    
    Args:
        cv_result: Computer vision analysis result
        max_detailed_shapes: Maximum number of shapes to show in full detail.
                            Beyond this, shapes are summarized by type.
    """
    if not cv_result.success:
        return f"[CV Analysis Failed: {cv_result.error_message}]"
    
    if not cv_result.shapes:
        return "[No shapes detected by computer vision]"
    
    lines = [
        "## COMPUTER VISION MEASUREMENTS",
        "",
        "The following measurements were computed programmatically from the image.",
        "These measurements are ACCURATE - use them for classification decisions.",
        f"Image dimensions: {cv_result.image_width} x {cv_result.image_height} pixels",
        f"Detected {len(cv_result.shapes)} unique shape(s):",
        ""
    ]
    
    # If few shapes, show full detail for each
    if len(cv_result.shapes) <= max_detailed_shapes:
        for shape in cv_result.shapes:
            lines.extend(_format_shape_detail(shape))
    else:
        # Group similar shapes and summarize
        groups = _group_similar_shapes(cv_result.shapes)
        
        lines.append("### Shape Summary (grouped by type):")
        lines.append("")
        
        for key, group_shapes in groups.items():
            count = len(group_shapes)
            representative = group_shapes[0]  # Use first as example
            
            if count == 1:
                lines.extend(_format_shape_detail(representative))
            else:
                # Summarize the group
                lines.append(f"**{count}x {representative.num_vertices}-sided polygons** (similar geometry)")
                lines.append(f"  - Example: Shape {representative.shape_id + 1}")
                lines.append(f"  - Convex: {'Yes' if representative.is_convex else 'No'}")
                
                min_ratio = min(representative.side_length_ratios)
                if min_ratio > 0.9:
                    lines.append(f"  - Sides: All approximately EQUAL ({min_ratio:.0%}+ ratio)")
                else:
                    lines.append(f"  - Side ratios: {representative.side_length_ratios}")
                
                lines.append(f"  - Angle range: {representative.min_angle:.1f}° to {representative.max_angle:.1f}°")
                
                # Show angle pattern
                angles = [v.interior_angle for v in representative.vertices]
                lines.append(f"  - Interior angles: {[round(a, 0) for a in angles]}")
                
                angle_diff = representative.max_angle - representative.min_angle
                if angle_diff > 30:
                    lines.append("  - Note: Alternating acute/obtuse angles (star pattern)")
                
                lines.append("")
        
        # Also show first few shapes in detail for reference
        lines.append("### Detailed measurements for first 3 shapes:")
        lines.append("")
        for shape in cv_result.shapes[:3]:
            lines.extend(_format_shape_detail(shape))
    
    return "\n".join(lines)


def _format_shape_detail(shape: DetectedShape) -> List[str]:
    """Format detailed measurements for a single shape."""
    lines = []
    lines.append(f"### Shape {shape.shape_id + 1}: {shape.num_vertices}-sided polygon")
    lines.append(f"- Area: {shape.area:.0f} sq pixels | Perimeter: {shape.perimeter:.0f} px")
    lines.append(f"- Convex: {'Yes' if shape.is_convex else 'No'} | Centroid: ({shape.centroid[0]:.0f}, {shape.centroid[1]:.0f})")
    
    # Compact side lengths
    side_str = ', '.join(f"{s:.0f}" for s in shape.side_lengths)
    lines.append(f"- Side lengths (px): [{side_str}]")
    
    min_ratio = min(shape.side_length_ratios)
    if min_ratio > 0.9:
        lines.append(f"  → All sides approximately EQUAL ({min_ratio:.0%})")
    elif min_ratio > 0.7:
        lines.append(f"  → Sides similar ({min_ratio:.0%} min ratio)")
    else:
        lines.append(f"  → Sides vary significantly ({min_ratio:.0%} min ratio)")
    
    # Compact angles
    angles = [v.interior_angle for v in shape.vertices]
    angle_str = ', '.join(f"{a:.0f}°" for a in angles)
    lines.append(f"- Interior angles: [{angle_str}]")
    
    angle_diff = shape.max_angle - shape.min_angle
    if angle_diff < 10:
        lines.append(f"  → Angles approximately EQUAL (range {angle_diff:.0f}°)")
    elif angle_diff < 30:
        lines.append(f"  → Angles somewhat similar (range {angle_diff:.0f}°)")
    else:
        lines.append(f"  → Angles vary significantly (range {angle_diff:.0f}°)")
    
    # Quadrilateral-specific analysis
    if shape.num_vertices == 4:
        lines.append("- Quadrilateral analysis:")
        
        right_angles = sum(1 for v in shape.vertices if 85 <= v.interior_angle <= 95)
        if right_angles == 4:
            lines.append("  → All 4 angles ~90° (rectangle/square)")
        elif right_angles > 0:
            lines.append(f"  → {right_angles} angle(s) ~90°")
        
        # Parallel/supplementary angle check
        sum_02 = angles[0] + angles[2]
        sum_13 = angles[1] + angles[3]
        
        if 170 <= sum_02 <= 190 and 170 <= sum_13 <= 190:
            lines.append("  → Opposite angles supplementary (parallelogram property)")
        
        # Side pairing
        sides = shape.side_lengths
        opp_ratio_1 = min(sides[0], sides[2]) / max(sides[0], sides[2]) if max(sides[0], sides[2]) > 0 else 0
        opp_ratio_2 = min(sides[1], sides[3]) / max(sides[1], sides[3]) if max(sides[1], sides[3]) > 0 else 0
        
        if opp_ratio_1 > 0.9 and opp_ratio_2 > 0.9:
            lines.append("  → Opposite sides equal (parallelogram/rect/rhombus/square)")
        
        # Kite pattern check
        adj_ratio_03 = min(sides[0], sides[3]) / max(sides[0], sides[3]) if max(sides[0], sides[3]) > 0 else 0
        adj_ratio_12 = min(sides[1], sides[2]) / max(sides[1], sides[2]) if max(sides[1], sides[2]) > 0 else 0
        adj_ratio_01 = min(sides[0], sides[1]) / max(sides[0], sides[1]) if max(sides[0], sides[1]) > 0 else 0
        
        if adj_ratio_03 > 0.9 and adj_ratio_12 > 0.9 and adj_ratio_01 < 0.85:
            lines.append("  → KITE PATTERN: Adjacent pairs equal, pairs different")
        
        # Angle pairing for kite
        angle_02_diff = abs(angles[0] - angles[2])
        angle_13_diff = abs(angles[1] - angles[3])
        
        if angle_02_diff < 10 and angle_13_diff > 30:
            lines.append(f"  → KITE: Angles 1&3 equal (~{angles[0]:.0f}°), 2&4 different")
        elif angle_13_diff < 10 and angle_02_diff > 30:
            lines.append(f"  → KITE: Angles 2&4 equal (~{angles[1]:.0f}°), 1&3 different")
    
    lines.append("")
    return lines


# =============================================================================
# LLM Analysis - Interprets CV measurements and provides semantic understanding
# =============================================================================

SYSTEM_PROMPT = """You are an expert at analyzing images and classifying geometric shapes.

You will receive:
1. An image to analyze
2. ACCURATE MEASUREMENTS computed by computer vision (side lengths, angles, etc.)

Your job is to:
1. Describe what you see in the image
2. Use the provided CV measurements to CLASSIFY shapes accurately
3. Provide any additional visual observations the CV might have missed

## CRITICAL: Use the CV measurements for classification decisions

The computer vision measurements are ACCURATE. Do NOT try to estimate angles or side lengths yourself.
Instead, USE the provided measurements to determine shape classifications.

## Shape Classification Rules

For TRIANGLES (3 sides):
- EQUILATERAL: All sides equal (ratio > 0.95), all angles ~60°
- ISOSCELES: Exactly 2 sides equal
- SCALENE: No sides equal
- Also classify by angles: ACUTE (all < 90°), RIGHT (one = 90°), OBTUSE (one > 90°)

For QUADRILATERALS (4 sides):
- SQUARE: All 4 sides equal AND all 4 angles = 90°
- RECTANGLE: Opposite sides equal AND all 4 angles = 90°
- RHOMBUS: All 4 sides equal, angles NOT 90°
- PARALLELOGRAM: Opposite sides equal, opposite angles equal, angles NOT 90°
- TRAPEZOID: Exactly ONE pair of parallel sides
- KITE: Two pairs of ADJACENT sides equal (not opposite), typically angles at two vertices are equal
- IRREGULAR: None of the above

## How to identify shape types from CV measurements:

**Parallelogram family** (parallelogram, rectangle, rhombus, square):
- Opposite sides are equal (check side ratios)
- Opposite angles are supplementary (sum to ~180°)

**Trapezoid:**
- Only ONE pair of opposite sides has similar angles to horizontal
- NOT a parallelogram (opposite sides not equal OR opposite angles not supplementary)

**Kite:**
- Adjacent pairs of sides are equal (sides 0,3 equal AND sides 1,2 equal)
- BUT the two pairs are DIFFERENT lengths (sides 0 ≠ sides 1)
- One pair of opposite angles are equal, the other pair are different
- CV will flag "KITE pattern" if detected

## Output Format

For each shape detected, provide:
1. Shape classification (e.g., "rhombus", "isosceles triangle", "kite")
2. Key measurements that support your classification
3. Any additional visual observations

Be concise but accurate. Trust the CV measurements."""

ANALYSIS_USER_PROMPT = """Please analyze the shapes in this image.

{cv_measurements}

Based on the computer vision measurements above and what you can see in the image:

1. For each detected shape, provide a classification (e.g., "square", "kite", "scalene triangle")
2. Explain which measurements support your classification
3. Note any shapes or details the CV might have missed

Remember: The CV measurements are accurate - use them for classification decisions."""


class ShapeClassification(BaseModel):
    """Classification result for a single shape."""
    shape_id: int = Field(description="ID of the shape (from CV detection)")
    classification: str = Field(description="Shape classification (e.g., 'kite', 'rhombus', 'isosceles right triangle')")
    confidence: str = Field(description="HIGH, MEDIUM, or LOW confidence")
    supporting_measurements: List[str] = Field(description="Key measurements that support this classification")
    reasoning: str = Field(description="Brief explanation of why this classification was chosen")


class ImageAnalysisData(BaseModel):
    """Complete analysis data for a single image."""
    image_url: str
    image_index: int
    overall_description: str = Field(description="General description of what the image shows")
    cv_shapes_detected: int = Field(description="Number of shapes detected by computer vision")
    shape_classifications: List[ShapeClassification] = Field(description="Classification for each detected shape")
    additional_observations: List[str] = Field(description="Any additional visual observations not captured by CV")
    overall_confidence: str = Field(description="HIGH, MEDIUM, or LOW overall confidence")


class ImageAnalysisToolResult(BaseModel):
    """Tool response format for image analysis."""
    image_analyses: List[ImageAnalysisData]


class ImageAnalysisResult(BaseModel):
    """Result from analyzing one or more images."""
    success: bool
    image_analyses: List[ImageAnalysisData]
    cv_results: List[CVAnalysisResult] = Field(default_factory=list, description="Raw CV analysis results")
    error_message: Optional[str] = None


async def analyze_images(image_urls: List[str]) -> ImageAnalysisResult:
    """
    Analyze images using computer vision for measurements + LLM for classification.
    
    This two-stage approach:
    1. Uses OpenCV to extract accurate geometric measurements
    2. Provides those measurements to an LLM for semantic understanding and classification
    
    Parameters
    ----------
    image_urls : List[str]
        List of image URLs to analyze
        
    Returns
    -------
    ImageAnalysisResult
        Analysis results including CV measurements and LLM classifications
    """
    if not image_urls:
        return ImageAnalysisResult(
            success=True,
            image_analyses=[],
            cv_results=[],
            error_message=None
        )
    
    start_time = time.time()
    cv_results = []
    images_for_llm = []
    cv_texts = []
    
    try:
        # Stage 1: Download images and run CV analysis
        logger.info(f"Running CV analysis on {len(image_urls)} image(s)...")
        
        for i, image_url in enumerate(image_urls):
            # Clean the URL to remove any trailing description text
            cleaned_url = _clean_image_url(image_url)
            if cleaned_url != image_url:
                logger.debug(f"Cleaned image URL: {image_url} -> {cleaned_url}")
            
            # Download with retry logic
            image_bytes = None
            content_type = 'image/png'
            download_success = False
            attempt_errors: List[AttemptError] = []
            
            for attempt in range(IMAGE_DOWNLOAD_MAX_RETRIES + 1):
                try:
                    await asyncio.sleep(0.2)  # Small delay between requests
                    response = requests.get(cleaned_url, timeout=30)
                    response.raise_for_status()
                    image_bytes = response.content
                    content_type = response.headers.get('content-type', 'image/png')
                    download_success = True
                    
                    # Record recovery if this wasn't the first attempt
                    if attempt > 0:
                        FailureTracker.record_recovered(
                            component="image_analyzer.download",
                            message=f"Succeeded on attempt {attempt + 1}/{IMAGE_DOWNLOAD_MAX_RETRIES + 1}",
                            context={"image_index": i + 1, "url": cleaned_url[:100]},
                            attempt_errors=attempt_errors if attempt_errors else None
                        )
                        logger.info(f"Image {i+1} download succeeded on attempt {attempt + 1}")
                    break
                    
                except Exception as e:
                    attempt_errors.append(AttemptError(
                        attempt=attempt + 1,
                        error_message=str(e)
                    ))
                    
                    if attempt < IMAGE_DOWNLOAD_MAX_RETRIES:
                        delay = IMAGE_DOWNLOAD_BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(
                            f"Image {i+1} download failed (attempt {attempt + 1}/"
                            f"{IMAGE_DOWNLOAD_MAX_RETRIES + 1}): {e}. Retrying in {delay:.1f}s..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        # All retries exhausted
                        logger.error(f"Image {i+1} download failed after all retries: {e}")
                        FailureTracker.record_exhausted(
                            component="image_analyzer.download",
                            error_message=str(e),
                            context={"image_index": i + 1, "url": cleaned_url[:100], "attempts": attempt + 1},
                            attempt_errors=attempt_errors
                        )
            
            if download_success and image_bytes:
                # Run CV analysis
                cv_result = run_cv_analysis(image_bytes)
                cv_results.append(cv_result)
                
                # Format CV results for LLM
                cv_text = format_cv_measurements_for_llm(cv_result)
                cv_texts.append(cv_text)
                logger.info(f"Image {i+1}: CV detected {len(cv_result.shapes)} shape(s)")
                
                # Prepare image for LLM
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                media_type = "image/jpeg" if 'jpeg' in content_type or 'jpg' in content_type else "image/png"
                images_for_llm.append(LLMImage(base64_data=image_base64, media_type=media_type))
            else:
                # Download failed - use fallback
                logger.warning(f"Image {i+1}: Using URL fallback after download failure")
                cv_results.append(CVAnalysisResult(
                    success=False,
                    image_width=0,
                    image_height=0,
                    shapes=[],
                    error_message="Download failed after retries"
                ))
                cv_texts.append(f"[Error downloading image after {IMAGE_DOWNLOAD_MAX_RETRIES + 1} attempts]")
                images_for_llm.append(LLMImage(url=cleaned_url))
        
        # Stage 2: LLM analysis with CV measurements
        logger.info("Running LLM analysis with CV measurements...")
        
        llm = LLMFactory.create("image_analyzer")
        
        # Combine all CV measurements into the prompt
        combined_cv_text = "\n\n---\n\n".join([
            f"## Image {i+1}\n\n{text}" for i, text in enumerate(cv_texts)
        ])
        
        user_prompt = ANALYSIS_USER_PROMPT.format(cv_measurements=combined_cv_text)
        
        # Call LLM with images and CV measurements
        tool_result = await llm.generate_with_vision(
            messages=[
                LLMMessage(role="system", content=SYSTEM_PROMPT),
                LLMMessage(role="user", content=user_prompt)
            ],
            images=images_for_llm,
            response_schema=ImageAnalysisToolResult
        )
        
        logger.info(
            f"Analysis complete in {time.time() - start_time:.2f}s. "
            f"Analyzed {len(tool_result.image_analyses)} image(s)."
        )
        
        return ImageAnalysisResult(
            success=True,
            image_analyses=tool_result.image_analyses,
            cv_results=cv_results,
            error_message=None
        )
        
    except Exception as e:
        logger.error(f"Analysis failed after {time.time() - start_time:.2f}s: {e}")
        return ImageAnalysisResult(
            success=False,
            image_analyses=[],
            cv_results=cv_results,
            error_message=str(e)
        )


def _summarize_shape_classifications(classifications: List[ShapeClassification]) -> str:
    """
    Summarize shape classifications by grouping similar shapes together.
    
    Instead of listing each shape individually, groups them by type.
    E.g., "24 5-pointed stars" instead of listing all 24.
    """
    if not classifications:
        return ""
    
    # Group by classification type
    groups: dict[str, List[ShapeClassification]] = {}
    for sc in classifications:
        key = sc.classification.lower()
        if key not in groups:
            groups[key] = []
        groups[key].append(sc)
    
    lines = []
    for classification, items in groups.items():
        count = len(items)
        # Get representative measurements from first item
        first = items[0]
        
        if count == 1:
            lines.append(f"- **{classification.upper()}** (Shape {first.shape_id + 1})")
            lines.append(f"  - Confidence: {first.confidence}")
            if first.supporting_measurements:
                lines.append(f"  - Key measurements: {', '.join(first.supporting_measurements[:3])}")
            if first.reasoning:
                lines.append(f"  - Reasoning: {first.reasoning}")
        else:
            # Summarize multiple shapes of the same type
            lines.append(f"- **{count}x {classification.upper()}** (Shapes {', '.join(str(s.shape_id + 1) for s in items[:5])}{'...' if count > 5 else ''})")
            # Use the highest confidence as representative
            confidences = [s.confidence for s in items]
            if 'HIGH' in confidences:
                lines.append("  - Confidence: HIGH (all shapes)")
            elif 'MEDIUM' in confidences:
                lines.append("  - Confidence: MEDIUM to HIGH")
            else:
                lines.append("  - Confidence: varies")
            # Show representative measurements
            if first.supporting_measurements:
                lines.append(f"  - Typical measurements: {', '.join(first.supporting_measurements[:3])}")
    
    return '\n'.join(lines)


def format_analysis_for_prompt(analysis_result: ImageAnalysisResult) -> str:
    """
    Format analysis results into a readable string for inclusion in evaluation prompts.
    
    This version is optimized for conciseness:
    - Groups similar shapes instead of listing each one
    - Omits raw CV measurements (LLM has already interpreted them)
    - Focuses on actionable information for evaluation
    
    Parameters
    ----------
    analysis_result : ImageAnalysisResult
        The analysis results to format
        
    Returns
    -------
    str
        Formatted string describing the analysis
    """
    if not analysis_result.success:
        return f"\n\nImage Analysis Failed: {analysis_result.error_message}"
    
    if not analysis_result.image_analyses:
        return ""
    
    output_parts = ["\n\n## IMAGE ANALYSIS (CV + LLM)"]
    output_parts.append("\nComputer vision measurements + LLM classification.")
    output_parts.append("AUTHORITATIVE FOR: Geometric shape counts, shape classifications, angle measurements.")
    output_parts.append("NOT AUTHORITATIVE FOR: Non-geometric objects (use OBJECT COUNT DATA instead).\n")
    
    for i, (img_data, cv_result) in enumerate(zip(
        analysis_result.image_analyses, 
        analysis_result.cv_results
    )):
        if len(analysis_result.image_analyses) > 1:
            output_parts.append(f"\n### Image {i + 1}")
        
        output_parts.append(f"**Description**: {img_data.overall_description}")
        
        # Summary stats
        cv_count = len(cv_result.shapes) if cv_result.success else 0
        output_parts.append(f"**Shapes detected**: {cv_count}")
        output_parts.append(f"**Confidence**: {img_data.overall_confidence}")
        
        # Summarized shape classifications
        if img_data.shape_classifications:
            output_parts.append("\n**Shape Classifications**:")
            summary = _summarize_shape_classifications(img_data.shape_classifications)
            output_parts.append(summary)
        
        # Additional observations (keep these, they might be important)
        if img_data.additional_observations:
            output_parts.append("\n**Additional Observations**:")
            for obs in img_data.additional_observations:
                output_parts.append(f"  - {obs}")
    
    return "\n".join(output_parts)
