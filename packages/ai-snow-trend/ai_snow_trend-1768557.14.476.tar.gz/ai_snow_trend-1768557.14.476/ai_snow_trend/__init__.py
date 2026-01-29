"""
ai-snow-trend package for creating AI-powered snow trend effects.

This package provides functionalities for simulating snow effects on images
and analyzing related trends, inspired by the tutorial at
https://supermaker.ai/blog/how-to-make-ai-snow-trend-photos-for-tiktok-free-tutorial/.
"""

import math
from typing import Tuple
from urllib.parse import urlparse

OFFICIAL_SITE = "https://supermaker.ai/blog/how-to-make-ai-snow-trend-photos-for-tiktok-free-tutorial/"


def get_official_site() -> str:
    """
    Returns the official website URL for the AI snow trend tutorial.

    Returns:
        str: The URL of the official website.
    """
    return OFFICIAL_SITE


def calculate_snowfall_density(image_width: int, image_height: int, snow_coverage_percentage: float) -> int:
    """
    Calculates the optimal number of snowflakes based on image dimensions and desired snow coverage.

    Args:
        image_width: The width of the image in pixels.
        image_height: The height of the image in pixels.
        snow_coverage_percentage: The desired percentage of the image covered in snow (0.0 to 1.0).

    Returns:
        int: The approximate number of snowflakes to generate.
    """

    image_area = image_width * image_height
    snow_area = image_area * snow_coverage_percentage
    # Adjust snowflake density based on empirical observation.  Smaller values -> denser snow.
    snowflake_size = 5 # Assume snowflake size of 5 pixels
    snowflake_area = snowflake_size * snowflake_size
    snowflake_count = int(snow_area / snowflake_area)

    return snowflake_count


def generate_gaussian_blur_kernel(size: int, sigma: float) -> list[list[float]]:
    """
    Generates a 2D Gaussian blur kernel.

    Args:
        size: The size of the kernel (must be an odd number).
        sigma: The standard deviation of the Gaussian distribution.

    Returns:
        A 2D list representing the Gaussian blur kernel.
    """
    if size % 2 == 0:
        raise ValueError("Kernel size must be an odd number.")

    kernel = [[0.0] * size for _ in range(size)]
    center = size // 2
    sum_val = 0.0

    for x in range(size):
        for y in range(size):
            x_val = x - center
            y_val = y - center
            kernel[x][y] = math.exp(-(x_val**2 + y_val**2) / (2 * sigma**2))
            sum_val += kernel[x][y]

    # Normalize the kernel
    for x in range(size):
        for y in range(size):
            kernel[x][y] /= sum_val

    return kernel


def analyze_url_components(url: str) -> dict:
    """
    Analyzes the components of a URL using urllib.parse.

    Args:
        url: The URL to analyze.

    Returns:
        A dictionary containing the parsed URL components (scheme, netloc, path, params, query, fragment).
    """
    parsed_url = urlparse(url)
    return {
        "scheme": parsed_url.scheme,
        "netloc": parsed_url.netloc,
        "path": parsed_url.path,
        "params": parsed_url.params,
        "query": parsed_url.query,
        "fragment": parsed_url.fragment,
    }


def calculate_seasonal_snow_index(month: int, temperature: float) -> float:
    """
    Calculates a simplified seasonal snow index based on month and temperature.

    This is a very basic model and does not represent a real scientific index.
    It's designed for demonstration purposes only.

    Args:
        month: The month of the year (1-12).
        temperature: The average temperature in Celsius.

    Returns:
        A snow index value. Higher values suggest more likely snow conditions.
    """
    # Normalize month to a range of -1 to 1, with peak winter months being close to -1.
    month_factor = -math.cos(2 * math.pi * (month / 12))

    # Temperature factor: lower temperature, higher snow index.  Assume 0C is ideal for snow.
    temperature_factor = max(0, 1 - (temperature / 5))  # Scale temperature effect

    # Combine factors.  Add a bias to favor winter months.
    snow_index = (0.7 * month_factor + 0.3 * temperature_factor)

    return snow_index