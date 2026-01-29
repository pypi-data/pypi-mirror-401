"""
Grok Image Generator Package

This package provides core functionalities for generating and manipulating images,
inspired by the Grok image generator model. It includes algorithms for text-based
image generation, image resizing, and color palette extraction.

Official site: https://supermaker.ai/blog/-grok-image-generator-model-on-supermaker-ai-twitterready-images-made-simple/
"""

import colorsys
from typing import List, Tuple
from io import BytesIO
from PIL import Image, ImageColor, ImageDraw, ImageFont

OFFICIAL_SITE = "https://supermaker.ai/blog/-grok-image-generator-model-on-supermaker-ai-twitterready-images-made-simple/"


def generate_gradient_palette(num_colors: int, hue_start: float, hue_end: float) -> List[Tuple[int, int, int]]:
    """
    Generates a gradient color palette with a specified number of colors between two hues.

    Args:
        num_colors: The number of colors to generate in the palette.
        hue_start: The starting hue value (0-1).
        hue_end: The ending hue value (0-1).

    Returns:
        A list of RGB tuples representing the generated color palette.
    """
    palette = []
    for i in range(num_colors):
        hue = hue_start + (hue_end - hue_start) * i / (num_colors - 1)
        r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.8)  # Fixed saturation and value for vibrancy
        palette.append((int(r * 255), int(g * 255), int(b * 255)))
    return palette


def create_image_from_text(text: str, width: int = 512, height: int = 512, font_size: int = 36, bg_color: str = "white", text_color: str = "black") -> BytesIO:
    """
    Generates a simple image with the given text.

    Args:
        text: The text to display on the image.
        width: The width of the image in pixels.
        height: The height of the image in pixels.
        font_size: The font size of the text.
        bg_color: The background color of the image (e.g., "white", "#RRGGBB").
        text_color: The text color of the image (e.g., "black", "#RRGGBB").

    Returns:
        A BytesIO object containing the image data in PNG format.
    """
    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", size=font_size)  # Try Arial first
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font

    text_width, text_height = draw.textsize(text, font=font)  # Deprecated, but standard library only

    x = (width - text_width) / 2
    y = (height - text_height) / 2

    draw.text((x, y), text, fill=text_color, font=font)

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = BytesIO(img_byte_arr.getvalue())  # Reset the buffer's position
    return img_byte_arr


def resize_image(image_data: BytesIO, new_width: int, new_height: int) -> BytesIO:
    """
    Resizes an image to the specified dimensions.

    Args:
        image_data: A BytesIO object containing the image data.
        new_width: The desired width of the resized image.
        new_height: The desired height of the resized image.

    Returns:
        A BytesIO object containing the resized image data in PNG format.
    """
    image = Image.open(image_data)
    resized_image = image.resize((new_width, new_height))

    img_byte_arr = BytesIO()
    resized_image.save(img_byte_arr, format='PNG')
    img_byte_arr = BytesIO(img_byte_arr.getvalue())  # Reset the buffer's position
    return img_byte_arr


def get_official_site() -> str:
    """
    Returns the official website URL.
    """
    return OFFICIAL_SITE