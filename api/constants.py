"""
Game constants loaded from environment variables.
This centralizes all magic numbers used throughout the application.
"""

import environ
import os

# Load environment variables
env = environ.Env()
env.read_env()

# ===== Game Rules =====
"""Core game mechanics that define how Wordle gameplay works"""
WORD_LENGTH = int(env('GAME_WORD_LENGTH', default=5))
MAX_GUESSES = int(env('GAME_MAX_GUESSES', default=6))

# ===== Animation Timings (milliseconds) =====
"""Frontend animation timing values for smooth UX"""
ANIMATION_SHAKE_MS = int(env('ANIMATION_SHAKE_MS', default=600))
ANIMATION_TILE_FLIP_STAGGER_MS = int(env('ANIMATION_TILE_FLIP_STAGGER_MS', default=350))
ANIMATION_BOUNCE_STAGGER_MS = int(env('ANIMATION_BOUNCE_STAGGER_MS', default=100))
ANIMATION_WIN_MODAL_DELAY_MS = int(env('ANIMATION_WIN_MODAL_DELAY_MS', default=1200))
ANIMATION_MODAL_DELAY_MS = int(env('ANIMATION_MODAL_DELAY_MS', default=200))
ANIMATION_TOAST_TIMEOUT_MS = int(env('ANIMATION_TOAST_TIMEOUT_MS', default=7000))

# ===== UI Dimensions =====
"""Frontend styling values passed to templates"""
UI_TILE_GAP_PX = int(env('UI_TILE_GAP_PX', default=5))
UI_BOARD_MAX_WIDTH_PX = int(env('UI_BOARD_MAX_WIDTH_PX', default=350))
UI_BOARD_COLUMNS = int(env('UI_BOARD_COLUMNS', default=5))

# ===== Pagination =====
"""Pagination settings for list views"""
LEADERBOARD_PAGE_SIZE = int(env('LEADERBOARD_PAGE_SIZE', default=50))

# ===== Guess Distribution =====
"""Array size for tracking wins per guess count (1 to MAX_GUESSES)"""
GUESS_DISTRIBUTION_SIZE = MAX_GUESSES

# ===== Color Codes for Guess Results =====
"""Feedback colors for user guesses"""
COLOR_CORRECT = 'G'      # Green - letter in correct position
COLOR_PRESENT = 'Y'      # Yellow - letter in word but wrong position
COLOR_ABSENT = 'B'       # Black/Absent - letter not in word

# ===== Statistics Multipliers =====
WIN_PERCENTAGE_MULTIPLIER = 100


def get_game_constants():
    """
    Return a dictionary of all game constants for template context.
    Useful for passing to templates to access constants in JavaScript/frontend.
    """
    return {
        # Game rules
        'WORD_LENGTH': WORD_LENGTH,
        'MAX_GUESSES': MAX_GUESSES,
        'WORD_LENGTH_RANGE': range(1, WORD_LENGTH + 1),
        'MAX_GUESSES_RANGE': range(1, MAX_GUESSES + 1),
        
        # Animation timings
        'ANIMATION_SHAKE_MS': ANIMATION_SHAKE_MS,
        'ANIMATION_TILE_FLIP_STAGGER_MS': ANIMATION_TILE_FLIP_STAGGER_MS,
        'ANIMATION_BOUNCE_STAGGER_MS': ANIMATION_BOUNCE_STAGGER_MS,
        'ANIMATION_WIN_MODAL_DELAY_MS': ANIMATION_WIN_MODAL_DELAY_MS,
        'ANIMATION_MODAL_DELAY_MS': ANIMATION_MODAL_DELAY_MS,
        'ANIMATION_TOAST_TIMEOUT_MS': ANIMATION_TOAST_TIMEOUT_MS,
        
        # UI dimensions
        'UI_TILE_GAP_PX': UI_TILE_GAP_PX,
        'UI_BOARD_MAX_WIDTH_PX': UI_BOARD_MAX_WIDTH_PX,
        'UI_BOARD_COLUMNS': UI_BOARD_COLUMNS,
        
        # Pagination
        'LEADERBOARD_PAGE_SIZE': LEADERBOARD_PAGE_SIZE,
    }
