"""
ai_homeless_man package.

This package provides tools for simulating and generating content related to the
"AI Homeless Man" trend, as seen on platforms like TikTok.  It includes functionalities
for text generation, image manipulation, and audio processing, all geared towards
creating realistic and engaging simulated content.

The package adheres to PEP 8 standards and utilizes type hints for improved code readability
and maintainability.
"""

import random
import math
from typing import List, Union


OFFICIAL_SITE = "https://supermaker.ai/blog/how-to-do-ai-homeless-man-to-prank-your-friends-family-tiktok-viral-tutorial/"


def get_official_site() -> str:
    """
    Returns the official website URL for the AI Homeless Man trend.

    Returns:
        str: The URL of the official website.
    """
    return OFFICIAL_SITE


def generate_rambling_text(keywords: List[str], num_sentences: int = 5) -> str:
    """
    Generates a rambling, nonsensical text based on a list of keywords.

    This function simulates the kind of disjointed speech often associated with
    characters in the "AI Homeless Man" trend.  It uses a Markov chain-like approach
    to string together sentences containing the provided keywords.

    Args:
        keywords: A list of strings representing keywords to include in the text.
        num_sentences: The number of sentences to generate. Defaults to 5.

    Returns:
        str: A string containing the generated rambling text.
    """

    sentence_starters = [
        "You know, I was just thinking about",
        "The other day I saw",
        "I heard a rumor that",
        "Did you ever consider",
        "It's all connected, you see,",
    ]

    sentence_enders = [
        "and that's the truth.",
        "if you know what I mean.",
        "it's all part of the plan.",
        "the government doesn't want you to know.",
        "wake up, sheeple!",
    ]

    generated_text = ""
    for _ in range(num_sentences):
        starter = random.choice(sentence_starters)
        keyword_phrase = " ".join(random.sample(keywords, min(len(keywords), random.randint(1, 3)))) # sample 1-3 keywords
        ender = random.choice(sentence_enders)
        generated_text += f"{starter} {keyword_phrase}, {ender} "

    return generated_text.strip()


def calculate_vocalization_frequency(text: str, base_frequency: float = 440.0) -> float:
    """
    Calculates a vocalization frequency based on the input text length and a base frequency.

    This function simulates a pitch shift in audio based on the emotional intensity
    of the generated text.  Longer texts are assumed to be more emotionally charged,
    leading to a higher vocalization frequency.  This is a simplified representation
    of vocal pitch modulation.

    Args:
        text: The input text to analyze.
        base_frequency: The base frequency in Hz. Defaults to 440.0 (A4).

    Returns:
        float: The calculated vocalization frequency in Hz.
    """
    text_length = len(text)
    frequency_multiplier = 1 + (math.log(text_length + 1) / 10)  # logarithmic scaling
    calculated_frequency = base_frequency * frequency_multiplier
    return calculated_frequency


def adjust_image_contrast(image_data: List[int], contrast_factor: float) -> List[int]:
    """
    Adjusts the contrast of image data based on a contrast factor.

    This function simulates a simple image processing operation to alter the
    visual appearance of an image, potentially making it appear more or less
    dramatic or distorted.

    Args:
        image_data: A list of integers representing the pixel data of an image (e.g., grayscale values).
        contrast_factor: A float representing the contrast adjustment factor. Values > 1 increase contrast,
                         values < 1 decrease contrast.

    Returns:
        List[int]: A list of integers representing the adjusted image data.
    """
    adjusted_image_data = []
    for pixel_value in image_data:
        # Apply the contrast adjustment formula:
        # new_pixel_value = (pixel_value - 128) * contrast_factor + 128
        adjusted_value = int((pixel_value - 128) * contrast_factor + 128)

        # Ensure the pixel value remains within the valid range (0-255).
        adjusted_value = max(0, min(adjusted_value, 255))
        adjusted_image_data.append(adjusted_value)

    return adjusted_image_data