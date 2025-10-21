"""
Utility functions for the Wordling game API.
"""

from api.constants import COLOR_CORRECT, COLOR_PRESENT, COLOR_ABSENT


def color_word(word, correct_letters):
    """
    Compare a guessed word against the correct answer and return color codes.
    
    Args:
        word (str): The word that was guessed
        correct_letters (str): The correct answer word
    
    Returns:
        str: A string of color codes where:
            - 'G' (Green) = Letter in correct position
            - 'Y' (Yellow) = Letter in word but wrong position
            - 'B' (Black/Absent) = Letter not in word
    
    Example:
        >>> color_word('SPEED', 'ERASE')
        'YBGBY'
    """
    # Initialize all tiles as absent (black)
    colored = [COLOR_ABSENT] * len(word)
    letter_count = {}
    
    # Count available letters in the correct answer
    for char in correct_letters:
        letter_count[char] = letter_count.get(char, 0) + 1
    
    # First pass: Mark all correct letters (green)
    for idx in range(len(word)):
        if word[idx] == correct_letters[idx]:
            letter_count[word[idx]] -= 1
            colored[idx] = COLOR_CORRECT
    
    # Second pass: Mark present but wrong position letters (yellow)
    for idx in range(len(word)):
        if colored[idx] == COLOR_ABSENT and word[idx] in letter_count and letter_count[word[idx]] > 0:
            letter_count[word[idx]] -= 1
            colored[idx] = COLOR_PRESENT
    
    return ''.join(colored)
