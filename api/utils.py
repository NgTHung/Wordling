def color_word(word, correct_letters):
    colored = ['B'] * len(word)
    letter_count = {}
    for char in correct_letters:
        letter_count[char] = letter_count.get(char, 0) + 1
    for idx in range(len(word)):
        if word[idx] == correct_letters[idx]:
            letter_count[word[idx]] -= 1
            colored[idx] = 'G'
    for idx in range(len(word)):
        if colored[idx] == 'B' and word[idx] in letter_count and letter_count[word[idx]] > 0:
            letter_count[word[idx]] -= 1
            colored[idx] = 'Y'
    return ''.join(colored)