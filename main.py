import requests
import random
import requests
import random


#this is all code to create the wordle game, if you want to just play my version of wordle, change the if name == main to just play_wordle()


def fetch_word():
    url = "https://gist.githubusercontent.com/shmookey/b28e342e1b1756c4700f42f17102c2ff/raw/ed4c33a168027aa1e448c579c8383fe20a3a6225/WORDS"
    try:
        response = requests.get(url)
        response.raise_for_status()
        words = [word for word in response.text.splitlines() if len(word) == 5]
        return random.choice(words)
    except requests.RequestException:
        print("Failed to fetch the word list. Please try again later.")
        return None

def wordle_feedback(word, guess):
    response = ["_" for _ in range(5)]
    for i, letter in enumerate(guess):
        if word[i] == letter:
            response[i] = letter
        elif letter in word:
            response[i] = f"{letter}~"
    return response

def play_wordle():
    word = fetch_word()
    if not word:
        return

    print("Welcome to Wordle!")
    print("Instructions: Guess the 5-letter word. Feedback will guide you.")
    print("  - Correct letters in the correct position are shown as is.")
    print("  - Correct letters in the wrong position are shown as 'a~'.")
    print("  - You have 5 attempts.")

    current_progress = ["_"] * 5
    attempts = 0

    while attempts < 5:
        print(f"Attempt {attempts + 1}: {''.join(current_progress)}")
        guess = input("Enter your guess: ").strip().lower()

        if len(guess) != 5 or not guess.isalpha():
            print("Invalid guess. Please enter a 5-letter word.")
            continue

        if guess == word:
            print(f"Congratulations! You've guessed the word: {word}")
            return

        current_progress = wordle_feedback(word, guess)
        attempts += 1

    print(f"Too many attempts! The word was: {word}")



# this is where the solver code starts

def fetch_word_list():
    url = "https://gist.githubusercontent.com/shmookey/b28e342e1b1756c4700f42f17102c2ff/raw/ed4c33a168027aa1e448c579c8383fe20a3a6225/WORDS"
    try:
        response = requests.get(url)
        response.raise_for_status()
        words = [word for word in response.text.splitlines() if len(word) == 5]
        return words
    except requests.RequestException:
        print("Failed to fetch the word list.")
        return []

def filter_words(possible_words, guess, feedback):
    filtered = []
    for word in possible_words:
        match = True
        for i, char in enumerate(feedback):
            if char == "_":
                if guess[i] in word:
                    match = False
                    break
            elif char.endswith("~"):
                if guess[i] not in word or word[i] == guess[i]:
                    match = False
                    break
            else:
                if word[i] != char:
                    match = False
                    break
        if match:
            filtered.append(word)
    return filtered

def get_feedback(word, guess):
    feedback = ["_" for _ in range(5)]
    for i in range(5):
        if guess[i] == word[i]:
            feedback[i] = guess[i]
        elif guess[i] in word:
            feedback[i] = f"{guess[i]}~"
    return feedback

def solve_wordle():
    word_list = fetch_word_list()
    if not word_list:
        return

    correct_word = random.choice(word_list)
    print(f"Hidden word (for testing): {correct_word}")

    possible_words = word_list
    attempts = 0

    while possible_words:
        guess = random.choice(possible_words)
        print(f"Attempt {attempts + 1}: {guess}")
        feedback = get_feedback(correct_word, guess)
        print(f"Feedback: {feedback}")

        if guess == correct_word:
            print(f"Solved! The word is '{correct_word}' in {attempts + 1} attempts.")
            break

        possible_words = filter_words(possible_words, guess, feedback)
        attempts += 1




if __name__ == "__main__":
    # play_wordle() to play
    solve_wordle()



