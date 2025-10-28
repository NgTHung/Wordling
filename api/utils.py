"""
Utility functions for the Wordling game API.
"""

from api.constants import COLOR_CORRECT, COLOR_PRESENT, COLOR_ABSENT


def color_word(word, pallet_colors):
    
    # Initialize all tiles as absent (black)
    colored = [[COLOR_ABSENT for _ in range(len(word))] for _ in range(len(pallet_colors))]
    letter_count = [{} for _ in range(len(pallet_colors))]
    
    # Count available letters in the correct answer
    for idx, color in enumerate(pallet_colors):
        for char in color:
            letter_count[idx][char] = letter_count[idx].get(char, 0) + 1
    
    # First pass: Mark all correct letters (green)
    for idx, color in enumerate(pallet_colors):
        for cidx, char in enumerate(color):
            if char == word[cidx]:
                colored[idx][cidx] = COLOR_CORRECT
                letter_count[idx][char] -= 1
    
    # Second pass: Mark present but wrong position letters (yellow)
    for idx, color in enumerate(pallet_colors):
        for cidx, char in enumerate(word):
            if char in color and letter_count[idx].get(char, 0) > 0:
                if colored[idx][cidx] != COLOR_CORRECT:
                    colored[idx][cidx] = COLOR_PRESENT
                    letter_count[idx][char] -= 1
    return [ ''.join(row) for row in colored ]