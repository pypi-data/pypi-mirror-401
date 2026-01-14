#!/usr/bin/env python3
"""
Color utilities.
"""
import colorsys
import re
import typing

REGEX_HEX_COLOR = r"#[a-zA-Z0-9]{6,8}"
MIN_LIGHTNESS = 0.0000000000001


def fg(hex_color, msg):
    """Decorate msg with hex_color in foreground."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[38;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def bg(hex_color, msg):
    """Decorate msg with hex_color in background."""
    _rgb = hex2rgb(hex_color)
    return f"\x01\x1b[48;2;{_rgb[0]};{_rgb[1]};{_rgb[2]}m\x02{msg}\x01\x1b[0m"


def hex2rgb(hex_color):
    """Convert hex color to RGB tuple.

    Args:
        hex_color (str): Hex color code (e.g., '#FF0000')

    Returns:
        tuple: RGB values as (r, g, b) where each value is 0-255

    Raises:
        AssertionError: If hex_color is not a valid hex color format
    """
    assert re.match(REGEX_HEX_COLOR, hex_color), f"{hex_color} is not a valid hex color."
    hex_color = hex_color.lstrip("#")
    rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return rgb_color


def hex2hls(hex_color):
    """Convert hex color to HLS tuple.

    Args:
        hex_color (str): Hex color code (e.g., '#FF0000')

    Returns:
        tuple: HLS values as (hue, lightness, saturation) where each value is 0-1
    """
    rgb_color = hex2rgb(hex_color)
    normalized_rgb = (
        rgb_color[0] / 255.0,
        rgb_color[1] / 255.0,
        rgb_color[2] / 255.0,
    )
    hls_color = colorsys.rgb_to_hls(normalized_rgb[0], normalized_rgb[1], normalized_rgb[2])
    return hls_color


def hls2hex(hls_color):
    """
    Convert HSL color to HEX code.

    Parameter:
    hls_color - tuple containing hue, lightness, and saturation color codes
    such as (0.5277777777777778, 0.04, 1).
    """
    rgb_color = colorsys.hls_to_rgb(hls_color[0], hls_color[1], hls_color[2])
    scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    return rgb2hex(scaled_rgb)


def rgb2hex(rgb_color):
    """Convert RGB tuple to hex color.

    Args:
        rgb_color (tuple): RGB values as (r, g, b), can be int (0-255) or float (0-1)

    Returns:
        str: Hex color code (e.g., '#FF0000')
    """
    scaled_rgb = rgb_color
    if isinstance(rgb_color[0], float):
        scaled_rgb = tuple(int(c * 255) for c in rgb_color)
    hex_color = f"#{scaled_rgb[0]:02X}{scaled_rgb[1]:02X}{scaled_rgb[2]:02X}"
    return hex_color


def rgb2hls(rgb_color):
    """Convert RGB tuple to HLS tuple.

    Args:
        rgb_color (tuple): RGB values as (r, g, b)

    Returns:
        tuple: HLS values as (hue, lightness, saturation)
    """
    return hex2hls(rgb2hex(rgb_color))


def display_palette_in_plain_text_file(plain_text_file):
    """Display palette colors from a plain text file.

    Args:
        plain_text_file (str): Path to the plain text palette file
    """
    with open(plain_text_file, "r") as p_file:
        palette_plain_text = p_file.readlines()
        color_palette_plain_text("".join(palette_plain_text))


def color_palette_plain_text(palette_plain_text):
    """Show palette."""
    for line in palette_plain_text.splitlines():
        try:
            _, hex_color = line.strip().split(":")
        except ValueError:
            raise ValueError("Invalid line in palette file: {line}")
        hex_color = hex_color.replace('"', "")
        print(bg(hex_color, line))


# TODO: use ONE display function to display colors from different sources:
# string, plain text file, plain text, list, Palette, palette_colors
def display_palette_colors(palette_colors: typing.List[typing.List[str]]):
    """Display palette colors."""
    if isinstance(palette_colors, list):
        for graduation_colors in palette_colors:
            for hex_color in graduation_colors:
                print(bg(hex_color, hex_color))
    if isinstance(palette_colors, dict):
        for color_id, hex_color in list(palette_colors.items()):
            print(bg(hex_color, f"{color_id}:{hex_color}"))


def display_list_colors(colors: typing.List[str]):
    """Display a list of colors with their HLS and RGB values.

    Args:
        colors (List[str] or str): List of hex color codes or single hex color
    """
    if isinstance(colors, str):
        colors = [colors]
    if isinstance(colors, list):
        for color in colors:
            print(bg(color, color + str(hex2hls(color)) + str(hex2rgb(color))))


def is_black_or_gray(hex_color):
    """Check if the given hex_color is black or gray."""
    if hex_color is None:
        return False
    rgb_color = hex2rgb(hex_color)
    return max(rgb_color) == min(rgb_color)


def set_hue(hex_color, hue):
    """Set hue value of a hex color.

    Args:
        hex_color (str): Original hex color code
        hue (float or None): New hue value (0-1), None to keep original

    Returns:
        str: Hex color with updated hue
    """
    if hue is None:
        return hex_color
    hls_color = hex2hls(hex_color)
    new_hls_color = (hue, hls_color[1], hls_color[2])
    return hls2hex(new_hls_color)


def set_saturation(hex_color, saturation):
    """Set saturation value of a hex color.

    Args:
        hex_color (str): Original hex color code
        saturation (float or None): New saturation value (0-1), None to keep original

    Returns:
        str: Hex color with updated saturation
    """
    if saturation is None:
        return hex_color
    hls_color = hex2hls(hex_color)
    new_hls_color = (hls_color[0], hls_color[1], saturation)
    return hls2hex(new_hls_color)


def set_lightness(hex_color, lightness):
    """Set lightness value of a hex color.

    Args:
        hex_color (str): Original hex color code
        lightness (float or None): New lightness value (0-1), None to keep original

    Returns:
        str: Hex color with updated lightness
    """
    if lightness is None:
        return hex_color

    hls_color = hex2hls(hex_color)
    new_hls_color = (hls_color[0], lightness, hls_color[2])
    result = hls2hex(new_hls_color)
    return result


def set_hls_values(hex_color, hue, saturation, lightness):
    """Set hue, lightness, and saturation."""
    if hue is None and saturation is None and lightness is None:
        return hex_color
    hls_color = hex2hls(hex_color)
    new_hls_color = (
        hue or hls_color[0],
        lightness or hls_color[1],
        saturation or hls_color[2],
    )
    return hls2hex(new_hls_color)


def darken(hex_color, rate: float):
    """Darken a hex color by reducing its lightness.

    Args:
        hex_color (str): Original hex color code
        rate (float): Darkening rate (0-1), where 0.5 makes it 50% darker

    Returns:
        str: Darkened hex color
    """
    hls_color = hex2hls(hex_color)
    lightness = max(hls_color[1], MIN_LIGHTNESS)
    new_lightness = max(lightness * rate, 0)
    return set_lightness(hex_color, new_lightness)


def lighten(hex_color, rate: float):
    """Lighten a hex color by increasing its lightness.

    Args:
        hex_color (str): Original hex color code
        rate (float): Lightening rate (>1), where 1.5 makes it 50% lighter

    Returns:
        str: Lightened hex color
    """
    if rate < 1:
        rate = 1 + rate
    hls_color = hex2hls(hex_color)
    lightness = max(hls_color[1], MIN_LIGHTNESS)
    new_lightness = min(1, lightness * rate)
    return set_lightness(hex_color, new_lightness)
