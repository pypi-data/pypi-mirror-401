"""Image utilities for clipboard image handling and encoding.

Provides functions to:
- Read images from system clipboard
- Encode images to base64 data URLs
- Check clipboard image availability
- Resize large images for LLM processing
"""

import base64
import io
import os
import platform
import sys
from enum import Enum
from typing import Optional


class ImageFormat(str, Enum):
    """Supported image formats."""
    PNG = "png"
    JPEG = "jpeg"
    GIF = "gif"


# Maximum image size for LLM processing (5MB)
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024

# Default max dimensions for resized images
MAX_IMAGE_DIMENSION = 2048

# Tokens per image for context estimation
ESTIMATED_TOKENS_PER_IMAGE = 500


class ClipboardImageError(Exception):
    """Error reading image from clipboard."""
    pass


class ImageProcessingError(Exception):
    """Error processing image data."""
    pass


def _import_pillow():
    """Try to import PIL, return None if not available."""
    try:
        from PIL import Image
        return Image
    except ImportError:
        return None


def _import_windows_clipboard():
    """Try to import Windows clipboard modules."""
    try:
        import win32clipboard
        import win32con
        return win32clipboard, win32con
    except ImportError:
        return None, None


def _import_mac_clipboard():
    """Try to import macOS clipboard modules."""
    try:
        import AppKit
        import objc
        return AppKit, objc
    except ImportError:
        return None, None


def is_clipboard_image_available() -> bool:
    """Check if the clipboard contains image data.

    Returns:
        True if clipboard has image data, False otherwise.
    """
    system = platform.system()

    if system == "Windows":
        return _check_windows_clipboard()
    elif system == "Darwin":  # macOS
        return _check_macos_clipboard()
    elif system == "Linux":
        return _check_linux_clipboard()
    else:
        return False


def _check_windows_clipboard() -> bool:
    """Check Windows clipboard for image data."""
    win32clipboard, win32con = _import_windows_clipboard()
    if win32clipboard is None:
        return False

    try:
        win32clipboard.OpenClipboard(0)
        try:
            return win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB)
        finally:
            win32clipboard.CloseClipboard()
    except Exception:
        return False


def _check_macos_clipboard() -> bool:
    """Check macOS clipboard for image data."""
    AppKit, objc = _import_mac_clipboard()
    if AppKit is None:
        return False

    try:
        pasteboard = AppKit.NSPasteboard.generalPasteboard()
        return bool(pasteboard.dataForType_("public.png"))
    except Exception:
        return False


def _check_linux_clipboard() -> bool:
    """Check Linux clipboard for image data (via wl-paste or xclip)."""
    # Try wl-paste (Wayland)
    result = os.system("which wl-paste > /dev/null 2>&1") == 0
    if result:
        # Check if clipboard has image
        return os.system("wl-paste -t image/png > /dev/null 2>&1") == 0

    # Try xclip (X11)
    result = os.system("which xclip > /dev/null 2>&1") == 0
    if result:
        return os.system("xclip -selection clipboard -t image/png -o > /dev/null 2>&1") == 0

    return False


def read_clipboard_image() -> Optional[bytes]:
    """Read an image from the system clipboard.

    Returns:
        Raw image bytes (PNG format), or None if no image available.

    Raises:
        ClipboardImageError: If clipboard access fails unexpectedly.
    """
    system = platform.system()

    if system == "Windows":
        return _read_windows_clipboard()
    elif system == "Darwin":  # macOS
        return _read_macos_clipboard()
    elif system == "Linux":
        return _read_linux_clipboard()
    else:
        raise ClipboardImageError(
            f"Unsupported platform: {system}. "
            "Image paste is supported on Windows, macOS, and Linux (with wl-paste or xclip)."
        )


def _read_windows_clipboard() -> Optional[bytes]:
    """Read image from Windows clipboard."""
    win32clipboard, win32con = _import_windows_clipboard()
    if win32clipboard is None:
        raise ClipboardImageError(
            "pywin32 is required for clipboard access on Windows. "
            "Install with: pip install pywin32"
        )

    try:
        win32clipboard.OpenClipboard(0)
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
                data = win32clipboard.GetClipboardData(win32con.CF_DIB)
                return _dib_to_png(data)
            elif win32clipboard.IsClipboardFormatAvailable(win32con.CF_BITMAP):
                bitmap = win32clipboard.GetClipboardData(win32con.CF_BITMAP)
                return _bitmap_to_png(bitmap)
            return None
        finally:
            win32clipboard.CloseClipboard()
    except Exception as e:
        raise ClipboardImageError(f"Failed to read Windows clipboard: {e}")


def _dib_to_png(dib_data: bytes) -> bytes:
    """Convert DIB data to PNG bytes."""
    Image = _import_pillow()
    if Image is None:
        raise ClipboardImageError("PIL/Pillow is required for image processing")

    import struct

    # Parse DIB header
    if len(dib_data) < 40:
        raise ClipboardImageError("Invalid DIB data")

    header_size = struct.unpack('<I', dib_data[0:4])[0]

    if header_size == 40:  # BITMAPINFOHEADER
        width = struct.unpack('<I', dib_data[4:8])[0]
        height = struct.unpack('<I', dib_data[8:12])[0]
        planes = struct.unpack('<H', dib_data[12:14])[0]
        bit_count = struct.unpack('<H', dib_data[14:16])[0]
    else:
        # Use PIL to handle it
        with io.BytesIO(dib_data) as bio:
            img = Image.open(bio)
            return _image_to_png_bytes(img)

    with io.BytesIO(dib_data) as bio:
        img = Image.open(bio)
        return _image_to_png_bytes(img)


def _bitmap_to_png(bitmap: int) -> bytes:
    """Convert Windows bitmap handle to PNG bytes."""
    Image = _import_pillow()
    if Image is None:
        raise ClipboardImageError("PIL/Pillow is required for image processing")

    raise ClipboardImageError("Bitmap handle conversion not implemented")


def _read_macos_clipboard() -> Optional[bytes]:
    """Read image from macOS clipboard."""
    AppKit, objc = _import_mac_clipboard()
    if AppKit is None:
        raise ClipboardImageError(
            "pyobjc is required for clipboard access on macOS. "
            "Install with: pip install pyobjc"
        )

    try:
        pasteboard = AppKit.NSPasteboard.generalPasteboard()

        # Try PNG first
        data = pasteboard.dataForType_("public.png")
        if data:
            return bytes(data)

        # Try other image types
        for img_type in ["public.jpeg", "public.tiff", "com.compuserve.gif"]:
            data = pasteboard.dataForType_(img_type)
            if data:
                img_data = bytes(data)
                return _convert_to_png(img_data)

        return None
    except Exception as e:
        raise ClipboardImageError(f"Failed to read macOS clipboard: {e}")


def _read_linux_clipboard() -> Optional[bytes]:
    """Read image from Linux clipboard (wl-paste or xclip)."""
    # Try wl-paste first (Wayland)
    result = os.system("which wl-paste > /dev/null 2>&1") == 0
    if result:
        try:
            import subprocess
            proc = subprocess.run(
                ["wl-paste", "-t", "image/png"],
                capture_output=True,
                timeout=5
            )
            if proc.returncode == 0 and proc.stdout:
                return proc.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # Try xclip (X11)
    result = os.system("which xclip > /dev/null 2>&1") == 0
    if result:
        try:
            import subprocess
            proc = subprocess.run(
                ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
                capture_output=True,
                timeout=5
            )
            if proc.returncode == 0 and proc.stdout:
                return proc.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    raise ClipboardImageError(
        "No clipboard image tools found. Install wl-paste (Wayland) or xclip (X11):\n"
        "  Wayland: sudo apt install wl-clipboard  (Debian/Ubuntu)\n"
        "  X11:     sudo apt install xclip        (Debian/Ubuntu)"
    )


def _convert_to_png(image_data: bytes) -> bytes:
    """Convert image data to PNG format."""
    Image = _import_pillow()
    if Image is None:
        raise ClipboardImageError("PIL/Pillow is required for image processing")

    with io.BytesIO(image_data) as bio:
        img = Image.open(bio)
        return _image_to_png_bytes(img)


def _image_to_png_bytes(img) -> bytes:
    """Convert PIL Image to PNG bytes."""
    output = io.BytesIO()
    img.convert("RGB")  # Ensure RGB mode
    img.save(output, format="PNG")
    return output.getvalue()


def encode_image_to_base64(image_data: bytes, format: ImageFormat = ImageFormat.PNG) -> str:
    """Encode image bytes to base64 data URL.

    Args:
        image_data: Raw image bytes.
        format: Image format (PNG, JPEG, GIF).

    Returns:
        Base64 data URL string: data:image/{format};base64,{encoded_data}
    """
    encoded = base64.b64encode(image_data).decode("utf-8")
    mime_type = f"image/{format.value}"
    return f"data:{mime_type};base64,{encoded}"


def encode_image_for_llm(image_data: bytes, format: ImageFormat = ImageFormat.PNG) -> dict:
    """Encode image for LLM vision API (OpenAI/Anthropic format).

    Args:
        image_data: Raw image bytes.
        format: Image format.

    Returns:
        Dict with base64 image data and media type for LLM APIs.
    """
    encoded = base64.b64encode(image_data).decode("utf-8")
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/{format.value};base64,{encoded}"
        }
    }


def resize_image_if_needed(
    image_data: bytes,
    max_size: int = MAX_IMAGE_SIZE_BYTES,
    max_dimension: int = MAX_IMAGE_DIMENSION
) -> bytes:
    """Resize image if it exceeds size or dimension limits.

    Args:
        image_data: Raw image bytes.
        max_size: Maximum image size in bytes.
        max_dimension: Maximum width/height dimension.

    Returns:
        Resized image bytes (always PNG format).
    """
    Image = _import_pillow()
    if Image is None:
        # Can't resize without Pillow, but if it's small enough, return as-is
        if len(image_data) <= max_size:
            return image_data
        raise ImageProcessingError(
            "PIL/Pillow is required to resize large images. "
            "Install with: pip install pillow"
        )

    with io.BytesIO(image_data) as bio:
        img = Image.open(bio)

        # Check if resizing is needed
        needs_resize = False

        if len(image_data) > max_size:
            needs_resize = True

        width, height = img.size
        if width > max_dimension or height > max_dimension:
            needs_resize = True

        if not needs_resize:
            # Return original as PNG
            return _image_to_png_bytes(img)

        # Calculate new dimensions maintaining aspect ratio
        if width > height:
            new_width = min(width, max_dimension)
            new_height = int(height * (new_width / width))
        else:
            new_height = min(height, max_dimension)
            new_width = int(width * (new_height / height))

        # Resize image
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Optimize quality if still too large
        output = io.BytesIO()
        quality = 95
        resized.save(output, format="PNG", quality=quality, optimize=True)

        # If still too large, reduce quality
        while len(output.getvalue()) > max_size and quality > 50:
            quality -= 10
            output = io.BytesIO()
            resized.save(output, format="PNG", quality=quality, optimize=True)
            if quality <= 50:
                break

        return output.getvalue()


def get_image_info(image_data: bytes) -> dict:
    """Get information about an image.

    Args:
        image_data: Raw image bytes.

    Returns:
        Dict with image info: width, height, size, format.
    """
    Image = _import_pillow()
    if Image is None:
        return {
            "width": None,
            "height": None,
            "size_bytes": len(image_data),
            "format": "unknown",
            "error": "PIL/Pillow not available"
        }

    with io.BytesIO(image_data) as bio:
        img = Image.open(bio)
        return {
            "width": img.width,
            "height": img.height,
            "size_bytes": len(image_data),
            "format": img.format or "unknown"
        }


def estimate_image_tokens(image_data: bytes) -> int:
    """Estimate token count for an image.

    This is a rough estimate based on image size and dimensions.
    Actual token count varies by model.

    Args:
        image_data: Raw image bytes.

    Returns:
        Estimated token count.
    """
    info = get_image_info(image_data)

    # Base token estimate
    tokens = ESTIMATED_TOKENS_PER_IMAGE

    # Adjust based on size (larger images have more detail)
    size_factor = len(image_data) / (1024 * 1024)  # MB
    tokens += int(tokens * size_factor * 0.5)

    # Adjust based on dimensions
    if info["width"] and info["height"]:
        dimension_factor = (info["width"] * info["height"]) / (1024 * 1024)  # megapixels
        tokens += int(tokens * dimension_factor * 0.3)

    return tokens


def read_and_prepare_image(
    max_size: int = MAX_IMAGE_SIZE_BYTES,
    raise_errors: bool = True
) -> Optional[bytes]:
    """Read image from clipboard and prepare for LLM.

    Combines checking, reading, and resizing into one call.

    Args:
        max_size: Maximum image size in bytes.
        raise_errors: If True, raises errors on failure. If False, returns None.

    Returns:
        Prepared image bytes, or None if no image available.
    """
    try:
        if not is_clipboard_image_available():
            return None

        image_data = read_clipboard_image()
        if image_data is None:
            return None

        return resize_image_if_needed(image_data, max_size)

    except ClipboardImageError as e:
        if raise_errors:
            raise
        return None
