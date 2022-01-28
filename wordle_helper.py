import argparse
from collections import defaultdict
from pathlib import Path
import os
import urllib.request


def load_words(fp):
    with open(fp, "r") as f:
        words = [word.strip() for word in f.readlines()]
    return words


def fail_gray(word, gray):
    for letter in gray:
        if letter in word:
            return True
    return False


def parse_guesses(guesses):
    game_state = {
        "gray": [],
        "yellow": defaultdict(list),
        "green": defaultdict(list),
    }

    for guess in guesses:
        word, colors = guess.split("/")
        for i, (letter, color) in enumerate(zip(word, colors)):
            if color == "g":
                game_state["gray"].append(letter)
            elif color == "y":
                game_state["yellow"][letter].append(i)
            elif color == "n":
                game_state["green"][letter].append(i)
            else:
                raise ValueError(f'"{color}" is not a valid color')

    return game_state


def check_gray(word, game_state):
    for letter in game_state["gray"]:
        if letter in word:
            return False
    return True


def check_yellow(word, game_state):
    for letter, positions in game_state["yellow"].items():
        if not letter in word:
            return False

        for i in positions:
            if word[i] == letter:
                return False

    return True


def check_green(word, game_state):
    for letter, positions in game_state["green"].items():
        if not letter in word:
            return False

        for i in positions:
            if word[i] != letter:
                return False

    return True


def filter_words(words, game_state):
    valid_words = []
    for word in words:
        if check_gray(word, game_state):
            if check_yellow(word, game_state):
                if check_green(word, game_state):
                    valid_words.append(word)
    return valid_words


def get_word_list(url, keep_full_list=False):

    with urllib.request.urlopen(url) as f:
        lines = [line.decode("utf-8") for line in f.readlines()]

    words = []
    for line in lines:
        word, _ = line.strip().split(" ")
        if len(word) == 5:
            words.append(word)
    with open("five_letter_words_by_freq.txt", "w") as f:
        for word in words:
            f.write(word + "\n")


if __name__ == "__main__":
    if "five_letter_words_by_freq.txt" not in os.listdir(
        Path(__file__).parent.resolve()
    ):
        print("words not found, downloading word list...")
        get_word_list(
            "https://raw.githubusercontent.com/IlyaSemenov/wikipedia-word-frequency/master/results/enwiki-20190320-words-frequency.txt"
        )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--n-results", help="max number of words to display", default=10, type=int
    )
    parser.add_argument(
        "guesses", type=str, nargs="+", help="wordle guesses (wwwww/ccccc)"
    )
    args = parser.parse_args()
    game_state = parse_guesses(args.guesses)
    words = load_words("five_letter_words_by_freq.txt")
    valid_words = filter_words(words, game_state)

    print("most frequent valid words")
    for valid_word in valid_words[: args.n_results]:
        print(valid_word)
