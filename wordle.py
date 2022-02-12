import sys
import random
import numpy


# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


# https://stackoverflow.com/questions/15993447/python-data-structure-for-efficient-add-remove-and-random-choice
class ListDict(object):
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def add_item(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items)-1

    def remove_item(self, item):
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def choose_random_item(self):
        return random.choice(self.items)

    def contains(self, item):
        return item in self.item_to_position


# Returns a random word from the word set
def getWord(word_set):
    return word_set.choose_random_item()


# Returns a histogram of the word
def getWordHist(word):
    word_hist = {}
    for c in word:
        if c in word_hist:
            word_hist[c] += 1
        else:
            word_hist[c] = 1
    return word_hist


# Returns an the game grid as an array
def initializeGrid():
    return numpy.full((6, 5, 2), ('_', 'w'))


# Sets the character and color for a grid cell
def markColor(arr, row, col, c, color):
    arr[row][col][0] = c.upper()
    arr[row][col][1] = color


# End game on correct guess
def win(arr, count):
    printGrid(arr)
    print(f"You have won!\n{count+1}/6")
    sys.exit()


# Compares guess to word
def compareWords(word, guess, arr, counter):
    word_hist = getWordHist(word)
    correct_count = 0
    # First pass to check for correct letters in correct positions
    for i in range(0, 5):
        if guess[i] == word[i]:
            markColor(arr, counter, i, guess[i], 'g')
            correct_count += 1
            word_hist[word[i]] -= 1
        else:
            markColor(arr, counter, i, guess[i], 'r')
    if correct_count == 5: # End game if correct word is guessed
        win(arr, counter)
    else:
        # Second pass to check for correct letters in wrong positions
        for i in range(5):
            c = guess[i]
            if c in word and word_hist[c] != 0 and c != word[i]:
                if guess[i] != word[i]:
                    markColor(arr, counter, i, guess[i], 'y')
                    word_hist[c] -= 1


def printGrid(arr):
    for row in arr:
        for col in row:
            if col[1] == 'g':
                print(f"{bcolors.GREEN}{col[0]}{bcolors.ENDC} ", end='')
            elif col[1] == 'y':
                print(f"{bcolors.YELLOW}{col[0]}{bcolors.ENDC} ", end='')
            elif col[1] == 'r':
                print(f"{bcolors.RED}{col[0]}{bcolors.ENDC} ", end='')
            else:
                print(f"{col[0]} ", end='')
        print()


# Game start and guessing loop
def game(word_set, guess_set):
    word = getWord(word_set)
    arr = initializeGrid()
    for count in range(6):
        print()
        while True:
            guess = input("Guess a 5 letter word: ")
            if len(guess) != 5 or not guess.isalpha() or not (guess_set.contains(guess) or word_set.contains(guess)):
                continue
            else:
                break
        print()
        compareWords(word, guess, arr, count)
        printGrid(arr)
    print(f"\nWord was {word.upper()}")


def main():
    filename1 = "wordle_word_list.txt"
    filename2 = "wordle_allowed_guesses.txt"
    word_set = ListDict()
    guess_set = ListDict()
    try:
        with open(filename1, 'r') as f:
            for line in f:
                word_set.add_item(line.strip())
        with open(filename2, 'r') as f:
            for line in f:
                guess_set.add_item(line.strip())
        game(word_set, guess_set)
    except FileNotFoundError:
        print(f"File {filename1} or {filename2} was not found")


if __name__ == "__main__":
    main()