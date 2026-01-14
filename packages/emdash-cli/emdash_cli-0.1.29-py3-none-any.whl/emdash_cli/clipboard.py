"""Clipboard utilities for image handling."""

import base64
import io
from typing import Optional, Tuple


def get_clipboard_image() -> Optional[Tuple[str, str]]:
    """Get image from clipboard if available.

    Returns:
        Tuple of (base64_data, format) if image found, None otherwise.
    """
    try:
        from PIL import ImageGrab, Image

        # Try to grab image from clipboard
        image = ImageGrab.grabclipboard()

        if image is None:
            return None

        # Handle list of file paths (Windows)
        if isinstance(image, list):
            # It's a list of file paths
            if image and isinstance(image[0], str):
                try:
                    image = Image.open(image[0])
                except Exception:
                    return None
            else:
                return None

        # Convert to PNG bytes
        if isinstance(image, Image.Image):
            buffer = io.BytesIO()
            # Convert to RGB if necessary (for RGBA images)
            if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                # Keep as PNG to preserve transparency
                image.save(buffer, format='PNG')
                img_format = 'png'
            else:
                # Convert to JPEG for smaller size
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(buffer, format='JPEG', quality=85)
                img_format = 'jpeg'

            buffer.seek(0)
            base64_data = base64.b64encode(buffer.read()).decode('utf-8')
            return base64_data, img_format

    except ImportError:
        # PIL not available
        return None
    except Exception:
        # Any other error (no clipboard access, etc.)
        return None

    return None


def get_image_from_path(path: str) -> Optional[Tuple[str, str]]:
    """Load image from file path.

    Args:
        path: Path to image file

    Returns:
        Tuple of (base64_data, format) if successful, None otherwise.
    """
    try:
        from PIL import Image

        image = Image.open(path)
        buffer = io.BytesIO()

        # Determine format from file extension
        ext = path.lower().split('.')[-1]
        if ext in ('jpg', 'jpeg'):
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(buffer, format='JPEG', quality=85)
            img_format = 'jpeg'
        elif ext == 'png':
            image.save(buffer, format='PNG')
            img_format = 'png'
        elif ext == 'gif':
            image.save(buffer, format='GIF')
            img_format = 'gif'
        elif ext == 'webp':
            image.save(buffer, format='WEBP')
            img_format = 'webp'
        else:
            # Default to PNG
            image.save(buffer, format='PNG')
            img_format = 'png'

        buffer.seek(0)
        base64_data = base64.b64encode(buffer.read()).decode('utf-8')
        return base64_data, img_format

    except Exception:
        return None


def get_image_dimensions(base64_data: str) -> Optional[Tuple[int, int]]:
    """Get dimensions of base64-encoded image.

    Args:
        base64_data: Base64-encoded image data

    Returns:
        Tuple of (width, height) if successful, None otherwise.
    """
    try:
        from PIL import Image

        image_bytes = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_bytes))
        return image.size
    except Exception:
        return None
