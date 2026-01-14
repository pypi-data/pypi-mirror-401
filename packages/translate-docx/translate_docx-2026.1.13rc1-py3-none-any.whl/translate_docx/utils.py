"""Utility functions for color and unit conversions."""

from typing import Optional

from docx.shared import RGBColor


def color_to_hex(color_obj) -> Optional[str]:
    """Convert python-docx color object to hex string.

    Args:
        color_obj: python-docx color object (typically run.font.color)

    Returns:
        Hex color string (e.g., "#FF0000") or None if no color is set
    """
    if color_obj is None:
        return None

    # Check if it has RGB attribute
    if hasattr(color_obj, "rgb") and color_obj.rgb is not None:
        # RGBColor object has a value attribute that is a 3-tuple
        return f"#{color_obj.rgb}"

    # Check if it's a theme color (not handled for now)
    if hasattr(color_obj, "theme_color") and color_obj.theme_color is not None:
        # Theme colors would need special handling
        return None

    return None


def hex_to_rgb_color(hex_color: Optional[str]) -> Optional[RGBColor]:
    """Convert hex color string to python-docx RGBColor object.

    Args:
        hex_color: Hex color string (e.g., "#FF0000" or "FF0000")

    Returns:
        RGBColor object or None if hex_color is None
    """
    if hex_color is None:
        return None

    # Remove '#' if present
    hex_color = hex_color.lstrip("#")

    # Ensure it's 6 characters
    if len(hex_color) != 6:
        return None

    try:
        return RGBColor.from_string(hex_color)
    except (ValueError, TypeError):
        return None


def points_to_twips(points: int) -> int:
    """Convert points to twips (1/20th of a point).

    Args:
        points: Value in points

    Returns:
        Value in twips
    """
    return points * 20


def twips_to_points(twips: int) -> int:
    """Convert twips to points.

    Args:
        twips: Value in twips

    Returns:
        Value in points
    """
    return twips // 20


def inches_to_twips(inches: float) -> int:
    """Convert inches to twips.

    Args:
        inches: Value in inches

    Returns:
        Value in twips
    """
    return int(inches * 1440)


def twips_to_inches(twips: int) -> float:
    """Convert twips to inches.

    Args:
        twips: Value in twips

    Returns:
        Value in inches
    """
    return twips / 1440


def normalize_alignment(alignment) -> Optional[str]:
    """Convert alignment enum to string representation.

    Args:
        alignment: python-docx alignment enum or string

    Returns:
        String representation or None
    """
    if alignment is None:
        return None

    alignment_str = str(alignment)

    # Handle enum objects
    if "LEFT" in alignment_str or "left" in alignment_str:
        return "left"
    elif "CENTER" in alignment_str or "center" in alignment_str:
        return "center"
    elif "RIGHT" in alignment_str or "right" in alignment_str:
        return "right"
    elif "JUSTIFY" in alignment_str or "justify" in alignment_str:
        return "justify"
    elif "DISTRIBUTE" in alignment_str or "distribute" in alignment_str:
        return "distribute"

    # Return as-is if already a simple string
    if alignment_str in ["left", "center", "right", "justify", "distribute"]:
        return alignment_str

    return None
