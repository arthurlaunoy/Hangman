import random
import os
import time

def getWordFromFile(filename):
    """
    Get a random word from a file containing a list of words.

    param: filename -> file to take the word from.

    return: string -> the word the game is going to use.
    """

    f = open(filename, "r")
    lines = f.readlines()
    index = random.randint(0, len(lines) - 1)
    word = lines[index]
    f.close()
    return word[:-1].lower()

def loadWord():
    """
    Get a word for the program to work. It either comes from user input or a random
    word from the words.txt file. The user may also input their own list of words
    to pick from.

    return: (string, string) -> word to play with and dummy word containing only '_'.
    """

    print("If you want to input your own word, type 1.")
    print("If you want to input your own list of words, type 2.")
    print("If you want to use our list of words, type 3.")
    res = input("\nEnter your number here: ")

    if res == '1':
        word = input("\nPlease input the word you want to use for the game: ")
    elif res == '2':
        filename = input("\nPlease input the name of the text file you want to use as a list of words: ")
        word = getWordFromFile(filename)
    elif res == '3':
        word = getWordFromFile("words.txt")
    else:
        print("Invalid number. Exiting game...")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()

    dummy = ['_' for letter in word]
    print('\nThe game begins !\n')
    printWord(dummy)
    return (word, dummy)

def printWord(dummy):
    """
    Displays the word that the user is trying to find.

    param: dummy -> list of characters containing '_' for letters that haven't been
    guessed yet.

    return: void
    """

    print('This is the current state of your word: ', end='')
    for c in dummy:
        print(c + ' ', end='')
    print('\n')


def isGameOver(dummy, limbsLost):
    """
    Checks whether the game is over.

    return: int -> 0 if the game is not is not over.
                   1 if the game is over and User won.
                   2 if the game is over and User lost.
    """
    if isWordGuessed(dummy):
        return 1
    elif limbsLost == 11:
        return 2
    else:
        return 0

def isWordGuessed(dummy):
    """
    Checks whether the word has been guessed by the user.

    return: bool -> True if word has been guessed.
                 -> False if word hasn't been guessed.
    """

    for c in dummy:
        if c == '_':
            return False

    return True

def updateWords(word, dummy, letter):
    """
    Checks whether the letter is present at least once in the word. If it is,
    update the dummy word so that this letter appears. If it is not present, add 1 to the number
    of limbs lost.

    param: word   -> The word to guess.
           dummy  -> Dummy word in which letters are supposed to appear.
           letter -> The letter the user just guessed.

    return: int -> 0 if the letter was present in the word.
                   1 if the letter was not present int the word.
    """

    flip = False
    i = 0
    for l in word:
        if l == letter:
            dummy[i] = l
            flip = True
        i += 1

    if flip:
        return 0
    else:
        return 1


def printGuessedLetters(l):
    """
    Displays the list of letters that has been guessed by the user.

    param: letters -> list of guessed letters, empty at the beginning of the game.

    return: void
    """

    letters = list(l)
    if len(l) > 1:
        print('The letters you have guessed so far are: ', end='')
    else:
        print('The letter you have guessed so far is: ', end='')

    for i in range(len(letters) - 1):
        print(letters[i] + ',', end='')

    print(letters[-1] + '\n')

def anotherOne(over, word):
    """
    Concludes the game and asks the user if they want to play another game.

    param: over -> exit code that indicates whether the user won the game.
           word -> solution of the game.
    return: void
    """

    if over == 1:
        print('Congratulations! You won! The word was indeed \'' + word + '\'.')
    else:
        print('Oh no! You lost! The word was \'' + word + '\'.')

    l = input("If you want to play again, enter 'y', otherwise, enter 'n': ")

    if l == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()



def main():
    print('\nWelcome to the hangman game !\n')
    word, dummy = loadWord()
    limbsLost = 0
    guessedLetters = set()
    over = isGameOver(dummy, limbsLost)

    while over == 0:
        letter = input("Please input a letter: ")
        print('------------------------------------------------------------')
        if letter in guessedLetters:
            limbsLost += 1
        guessedLetters.add(letter.lower())
        limbsLost += updateWords(word, dummy, letter)
        over = isGameOver(dummy, limbsLost)
        if over == 0:
            printWord(dummy)
            if 11 - limbsLost == 1:
                print('You have ' + str(11 - limbsLost) + ' attempt left.\n')
            else:
                print('You have ' + str(11 - limbsLost) + ' attempts left.\n')
            printGuessedLetters(guessedLetters)

    anotherOne(over, word)

main()
