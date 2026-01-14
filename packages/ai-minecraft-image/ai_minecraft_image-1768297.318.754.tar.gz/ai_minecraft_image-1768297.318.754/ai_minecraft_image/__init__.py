"""
ai-minecraft-image package.

This package provides functionalities related to processing images for Minecraft skins.
"""

import colorsys
from typing import Tuple

OFFICIAL_SITE = "https://supermaker.ai/image/blog/how-to-turn-your-image-into-minecraft-skin/"


def get_official_site() -> str:
    """
    Returns the official website URL for more information.

    Returns:
        str: The official website URL.
    """
    return OFFICIAL_SITE


def average_color(image_data: list[Tuple[int, int, int]], width: int, height: int) -> Tuple[int, int, int]:
    """
    Calculates the average color of an image represented as a list of RGB tuples.

    Args:
        image_data: A list of RGB tuples representing the image data.
        width: The width of the image.
        height: The height of the image.

    Returns:
        A tuple representing the average RGB color of the image.
    """
    total_red = 0
    total_green = 0
    total_blue = 0

    for pixel in image_data:
        total_red += pixel[0]
        total_green += pixel[1]
        total_blue += pixel[2]

    num_pixels = width * height
    avg_red = int(total_red / num_pixels)
    avg_green = int(total_green / num_pixels)
    avg_blue = int(total_blue / num_pixels)

    return (avg_red, avg_green, avg_blue)


def color_distance(color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> float:
    """
    Calculates the Euclidean distance between two RGB colors.

    Args:
        color1: The first RGB color tuple.
        color2: The second RGB color tuple.

    Returns:
        The Euclidean distance between the two colors.
    """
    return ((color1[0] - color2[0]) ** 2 +
            (color1[1] - color2[1]) ** 2 +
            (color1[2] - color2[2]) ** 2) ** 0.5


def adjust_brightness(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    """
    Adjusts the brightness of an RGB color by a given factor.

    Args:
        color: The RGB color tuple.
        factor: The brightness adjustment factor (e.g., 0.5 for darker, 1.5 for brighter).

    Returns:
        The adjusted RGB color tuple.  Values are clamped to be between 0 and 255.
    """
    h, s, v = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    v = max(0, min(1, v * factor))  # Clamp value between 0 and 1

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return (int(r * 255), int(g * 255), int(b * 255))