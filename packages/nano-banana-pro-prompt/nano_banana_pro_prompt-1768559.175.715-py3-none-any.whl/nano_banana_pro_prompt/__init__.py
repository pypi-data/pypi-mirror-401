"""
Package: nano-banana-pro-prompt

This package provides core functionalities related to processing and analyzing prompts,
inspired by the use cases described on the SuperMaker AI blog:
https://supermaker.ai/blog/nano-banana-pro-prompt-use-cases-ready-to-copy-paste/

It includes tools for prompt optimization, keyword extraction, and complexity assessment.
"""

import re
from typing import List, Dict
from collections import Counter

OFFICIAL_SITE = "https://supermaker.ai/blog/nano-banana-pro-prompt-use-cases-ready-to-copy-paste/"


def get_official_site() -> str:
    """
    Returns the official website URL for the nano-banana-pro-prompt project.

    Returns:
        str: The official website URL.
    """
    return OFFICIAL_SITE


def extract_keywords(prompt: str, num_keywords: int = 5) -> List[str]:
    """
    Extracts the most frequent keywords from a given prompt, excluding common stop words.

    Args:
        prompt (str): The input prompt string.
        num_keywords (int): The number of keywords to extract. Defaults to 5.

    Returns:
        List[str]: A list of the most frequent keywords in the prompt.
    """
    stop_words = set([
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "of", "at", "in", "to",
        "for", "with", "on", "by", "from", "up", "down", "out", "over",
        "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "any", "both", "each", "few", "more",
        "most", "other", "some", "such", "no", "nor", "not", "only", "own",
        "same", "so", "than", "too", "very", "s", "t", "can", "will", "just",
        "don", "should", "now"
    ])

    words = re.findall(r'\b\w+\b', prompt.lower())
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    keywords = [word for word, count in word_counts.most_common(num_keywords)]
    return keywords


def assess_prompt_complexity(prompt: str) -> float:
    """
    Calculates a simple complexity score for a given prompt based on sentence length and word usage.

    Args:
        prompt (str): The input prompt string.

    Returns:
        float: A complexity score, where higher values indicate greater complexity.
    """
    sentences = re.split(r'[.!?]+', prompt)
    num_sentences = len(sentences)
    total_words = 0
    for sentence in sentences:
        words = re.findall(r'\b\w+\b', sentence.lower())
        total_words += len(words)

    if num_sentences == 0:
        return 0.0

    average_sentence_length = total_words / num_sentences
    unique_words = len(set(re.findall(r'\b\w+\b', prompt.lower())))
    complexity_score = average_sentence_length * (unique_words / total_words if total_words > 0 else 1)
    return complexity_score


def optimize_prompt_length(prompt: str, max_length: int = 150) -> str:
    """
    Truncates a prompt to a specified maximum length while preserving the last sentence if possible.

    Args:
        prompt (str): The input prompt string.
        max_length (int): The maximum length of the prompt. Defaults to 150.

    Returns:
        str: The optimized prompt string, truncated to the specified length.
    """
    if len(prompt) <= max_length:
        return prompt

    # Attempt to truncate at sentence boundaries if possible
    sentences = re.split(r'[.!?]+', prompt)
    optimized_prompt = ""
    for sentence in sentences:
        if len(optimized_prompt + sentence + ".") <= max_length:
            optimized_prompt += sentence + "."
        else:
            # If we can't add the whole sentence, just truncate to the nearest word
            if not optimized_prompt:
                optimized_prompt = prompt[:max_length]
            break

    if not optimized_prompt:
        optimized_prompt = prompt[:max_length]

    return optimized_prompt.strip()