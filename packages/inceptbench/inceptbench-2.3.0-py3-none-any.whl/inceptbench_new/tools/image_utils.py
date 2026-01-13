"""
Image utility functions for educational content evaluation.

This module provides utilities for extracting image URLs from content,
downloading images, and encoding them for API use.
"""

import base64
import logging
import re
from typing import List

import requests

logger = logging.getLogger(__name__)


def _clean_image_url(url: str) -> str:
    """
    Clean an extracted image URL by removing any trailing description or garbage.
    
    Handles formats like:
    - 'https://example.com/image.png "description"' -> 'https://example.com/image.png'
    - 'https://example.com/image.png \\"description\\"' -> 'https://example.com/image.png'
    - 'https://example.com/image.png)' -> 'https://example.com/image.png'
    """
    if not url:
        return url
    
    # Strip leading/trailing whitespace
    url = url.strip()
    
    # Find where the actual URL ends - look for image extension followed by optional query string
    # Pattern: .ext or .ext?query but nothing after that except valid URL chars
    extension_match = re.search(
        r'(\.(?:jpg|jpeg|png|gif|bmp|svg|webp))(\?[^\s"\'\\]*)?',
        url, 
        re.IGNORECASE
    )
    
    if extension_match:
        # URL ends at the extension (plus any query string)
        end_pos = extension_match.end()
        url = url[:end_pos]
    
    # Also handle Supabase URLs that might not have extensions visible
    # Stop at common "end of URL" indicators
    for stop_char in [' "', ' \\"', ' \\\"', '\t', ' \'', '\\n', '\n']:
        if stop_char in url:
            url = url.split(stop_char)[0]
    
    # Remove trailing punctuation that's not part of URLs
    url = url.rstrip('"\'\\ \t\n,;:)>')
    
    # URL-encode spaces (common issue with S3 URLs that have spaces in filenames)
    url = url.replace(' ', '%20')
    
    return url


def extract_image_urls(content: str) -> List[str]:
    """
    Extract image URLs from content.
    
    Args:
        content: The content to extract URLs from
        
    Returns:
        List of unique image URLs found in the content
    """
    # Pattern to match common image URL formats
    # Matches URLs ending in common image extensions
    # Note: [^\s<>"\\] excludes backslash to handle escaped quotes like \"
    url_pattern = r'https?://[^\s<>"\\]+?\.(?:jpg|jpeg|png|gif|bmp|svg|webp)(?:\?[^\s<>"\\]*)?'
    
    # Also match Supabase storage URLs (common in this codebase)
    # Be more restrictive - stop at spaces, quotes, or backslashes
    supabase_pattern = r'https://[^\s<>"\\]*supabase[^\s<>"\\]*storage[^\s<>"\\]*\.(?:jpg|jpeg|png|gif|bmp|svg|webp)'
    
    urls = []
    urls.extend(re.findall(url_pattern, content, re.IGNORECASE))
    urls.extend(re.findall(supabase_pattern, content, re.IGNORECASE))

    # Extract markdown image syntax: ![alt](url)
    markdown_image_matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
    urls.extend(markdown_image_matches)

    # Extract HTML image tags
    html_image_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    urls.extend(html_image_matches)

    # Clean all extracted URLs and remove any that are now invalid
    cleaned_urls = []
    for url in urls:
        cleaned = _clean_image_url(url)
        if cleaned and cleaned.startswith('http'):
            cleaned_urls.append(cleaned)
        else:
            logger.debug(f"Discarded invalid URL after cleaning: {url} -> {cleaned}")

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in cleaned_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    logger.debug(f"Extracted {len(unique_urls)} unique image URLs from content")
    return unique_urls


def download_and_encode_image(image_url: str, timeout: int = 30) -> str:
    """
    Download an image and encode it as a base64 data URL.
    
    This helps avoid timeout issues when OpenAI's servers try to download
    external URLs directly. Falls back to the original URL if download fails.
    
    Args:
        image_url: The URL of the image to download and encode
        timeout: Request timeout in seconds (default: 30)
        
    Returns:
        Either a base64-encoded data URL (data:image/...;base64,...) or
        the original URL if download failed
    """
    # Clean the URL to remove any trailing description text
    cleaned_url = _clean_image_url(image_url)
    if cleaned_url != image_url:
        logger.debug(f"Cleaned image URL before download: {image_url} -> {cleaned_url}")
    
    try:
        response = requests.get(cleaned_url, timeout=timeout)
        response.raise_for_status()
        image_bytes = response.content
        
        if image_bytes:
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            content_type = response.headers.get('content-type', 'image/png')
            
            # Determine the appropriate MIME type
            if 'jpeg' in content_type or 'jpg' in content_type:
                return f"data:image/jpeg;base64,{image_base64}"
            elif 'png' in content_type:
                return f"data:image/png;base64,{image_base64}"
            elif 'gif' in content_type:
                return f"data:image/gif;base64,{image_base64}"
            elif 'webp' in content_type:
                return f"data:image/webp;base64,{image_base64}"
            else:
                # Default to PNG for unknown types
                return f"data:image/png;base64,{image_base64}"
        else:
            logger.warning(
                f"Empty response when downloading {cleaned_url}, using direct URL"
            )
            return cleaned_url
            
    except Exception as e:
        logger.warning(
            f"Could not download image {cleaned_url}, using direct URL: {e}"
        )
        return cleaned_url


def prepare_images_for_api(image_urls: List[str]) -> List[dict]:
    """
    Prepare a list of image URLs for API consumption.
    
    Downloads and encodes each image, then returns them in the format
    expected by the OpenAI Vision API.
    
    Args:
        image_urls: List of image URLs to prepare
        
    Returns:
        List of dictionaries in the format:
        [{"type": "input_image", "image_url": "data:image/...;base64,..."}]
    """
    prepared_images = []
    
    for image_url in image_urls:
        encoded_url = download_and_encode_image(image_url)
        prepared_images.append({
            "type": "input_image",
            "image_url": encoded_url
        })
        
        if encoded_url.startswith("data:"):
            logger.info(f"Prepared image (base64 encoded): {image_url}")
        else:
            logger.info(f"Prepared image (direct URL): {image_url}")
    
    return prepared_images


def build_llm_content_with_images(text: str, image_urls: List[str], encode_base64: bool = False) -> List[dict]:
    """
    Build LLM message content array with text and images for vision-capable models.

    Args:
        text: The text content to include
        image_urls: List of image URLs to include
        encode_base64: If True, download and encode images as base64

    Returns:
        List of content blocks in OpenAI message format
    """
    content = [{"type": "text", "text": text}]

    for url in image_urls:
        # Clean the URL to remove any trailing description text
        cleaned_url = _clean_image_url(url)
        
        if encode_base64:
            encoded_url = download_and_encode_image(cleaned_url)
        else:
            encoded_url = cleaned_url
        content.append({
            "type": "image_url",
            "image_url": {"url": encoded_url}
        })

    return content
