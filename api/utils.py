import random
from api.constants import COLOR_CORRECT, COLOR_BROKEN, COLOR_PRESENT, COLOR_ABSENT, COLOR_VAMPIRE_CORRECT, COLOR_VAMPIRE_PRESENT


def color_word(word, pallet_colors):
    
    colored = [[COLOR_ABSENT for _ in range(len(word))] for _ in range(len(pallet_colors))]
    letter_count = [{} for _ in range(len(pallet_colors))]
    
    for idx, color in enumerate(pallet_colors):
        for char in color:
            letter_count[idx][char] = letter_count[idx].get(char, 0) + 1
    
    for idx, color in enumerate(pallet_colors):
        for cidx, char in enumerate(color):
            if char == word[cidx]:
                colored[idx][cidx] = COLOR_CORRECT
                letter_count[idx][char] -= 1
    
    for idx, color in enumerate(pallet_colors):
        for cidx, char in enumerate(word):
            if char in color and letter_count[idx].get(char, 0) > 0:
                if colored[idx][cidx] != COLOR_CORRECT:
                    colored[idx][cidx] = COLOR_PRESENT
                    letter_count[idx][char] -= 1
    return [ ''.join(row) for row in colored ]

def nightmare_color_word(word, pallet_colors, challenge, challenge_value):
    color = color_word(word, pallet_colors)
    if challenge == 'LIAR':
        if not bool(challenge_value):
            return color
        tile_to_flip = random.randint(0, len(word) - 1)
        for icolor in range(len(color)):
            possible_colors = [COLOR_CORRECT, COLOR_PRESENT, COLOR_ABSENT]
            possible_colors.remove(color[icolor][tile_to_flip])
            random_choice = random.choice(possible_colors)
            color[icolor] = color[icolor][:tile_to_flip] + random_choice + color[icolor][tile_to_flip + 1:]
    elif challenge == 'BROKEN':
        pass
    elif challenge == 'AMNESIA':
        pass
    elif challenge == 'GLITCH':
        for idx,char in enumerate(color[challenge_value]):
            if char == COLOR_ABSENT:
                color[challenge_value] = color[challenge_value][:idx] + COLOR_PRESENT + color[challenge_value][idx + 1:]
            elif char == COLOR_PRESENT:
                color[challenge_value] = color[challenge_value][:idx] + COLOR_ABSENT + color[challenge_value][idx + 1:]
    elif challenge == 'VAMPIRE':
        drained_color_idx = challenge_value
        for idx, char in enumerate(color[drained_color_idx]):
            if char == COLOR_CORRECT:
                color[drained_color_idx] = color[drained_color_idx][:idx] + COLOR_VAMPIRE_CORRECT + color[drained_color_idx][idx + 1:]
            elif char == COLOR_PRESENT:
                color[drained_color_idx] = color[drained_color_idx][:idx] + COLOR_VAMPIRE_PRESENT + color[drained_color_idx][idx + 1:]
    return color