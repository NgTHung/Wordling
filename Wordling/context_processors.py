"""
Context processors for Wordling templates.
Makes game constants available in all templates.
"""

from api.constants import get_game_constants


def game_constants(request):
    """
    Add all game constants to the template context.
    
    Usage in templates:
        {{ WORD_LENGTH }}
        {{ MAX_GUESSES }}
        {{ ANIMATION_SHAKE_MS }}
        etc.
    """
    return get_game_constants()
