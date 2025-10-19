def color_word(word, correct_letters):
    colored = ''
    letter_count = {}
    for char in correct_letters:
        letter_count[char] = letter_count.get(char, 0) + 1
    for idx in range(len(word)):
        if word[idx] == correct_letters[idx]:
            colored += 'G'  # Green
            letter_count[word[idx]] -= 1
        elif word[idx] in correct_letters:
            if letter_count[word[idx]] > 0:
                colored += 'Y'  # Yellow
                letter_count[word[idx]] -= 1
            else:
                colored += 'B'  # Black
        else:
            colored += 'B'  # Black
    return colored