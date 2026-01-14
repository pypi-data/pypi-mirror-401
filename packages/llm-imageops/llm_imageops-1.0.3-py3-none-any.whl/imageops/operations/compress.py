"""Compression operations with fallback strategies."""

import asyncio
import logging
import os
import tempfile
from typing import Optional
import cv2

from ..exceptions import ImageProcessingError

logger = logging.getLogger("imageops")


async def compress_to_size(
    image_path: str,
    max_size_mb: float,
    output_folder: Optional[str] = None,
    quality_start: int = 95,
    quality_step: int = 5,
    min_quality: int = 10
) -> str:
    """
    Compress image to target size with fallback strategies.
    
    Strategies:
    1. Iterative quality reduction (95 → 10)
    2. If still too large: Resize dimensions by 85%
    3. Repeat until under limit or error
    
    Args:
        image_path: Path to image
        max_size_mb: Maximum size in MB
        output_folder: Optional custom folder name for temp files
        quality_start: Starting quality
        quality_step: Quality reduction step
        min_quality: Minimum quality
        
    Returns:
        Path to compressed image
        
    Raises:
        ImageProcessingError: If cannot compress below limit
    """
    def _compress():
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot read image: {image_path}")
        
        height, width = img.shape[:2]
        current_quality = quality_start
        resize_factor = 1.0
        max_size_bytes = max_size_mb * 1024 * 1024
        
        # Create temp path
        if output_folder:
            os.makedirs(output_folder, exist_ok=True)
            temp_path = os.path.join(output_folder, f"compressed_{os.path.basename(image_path)}")
        else:
            temp_path = tempfile.mktemp(suffix=".jpg")
        
        attempt = 0
        max_attempts = 150  # Increase limit for very small target sizes
        
        while attempt < max_attempts:
            attempt += 1
            
            # Apply resize if factor changed
            if resize_factor < 1.0:
                new_width = int(width * resize_factor)
                new_height = int(height * resize_factor)
                resized_img = cv2.resize(
                    img,
                    (new_width, new_height),
                    interpolation=cv2.INTER_AREA
                )
            else:
                resized_img = img
            
            # Compress with current quality
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), current_quality]
            success = cv2.imwrite(temp_path, resized_img, encode_param)
            
            if not success:
                raise ImageProcessingError("Failed to write compressed image")
            
            current_size = os.path.getsize(temp_path)
            
            # Check if we're under the limit
            if current_size <= max_size_bytes:
                return temp_path
            
            # Strategy 1: Reduce quality
            if current_quality > min_quality:
                current_quality = max(min_quality, current_quality - quality_step)
                continue
            
            # Strategy 2: Resize dimensions (more aggressive 85% step)
            resize_factor *= 0.85
            current_quality = quality_start  # Reset quality
            
            # Check if we've resized too much
            if resize_factor < 0.05:  # Don't go below 5%
                raise ImageProcessingError(
                    f"Cannot compress image below {max_size_mb}MB even at "
                    f"{resize_factor:.1%} size and quality {min_quality}"
                )
        
        raise ImageProcessingError(f"Compression failed after {max_attempts} attempts")
    
    try:
        return await asyncio.to_thread(_compress)
    except Exception as e:
        logger.error(f"Compression failed: {e}")
        raise ImageProcessingError(f"Compression failed: {e}") from e

