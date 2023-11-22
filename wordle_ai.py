
import pandas as pd
import re
from solver_class import solver

def read_words():
    word_list = []
    f = open("words.txt", "r")
    for x in f:
        word_list.append(x.replace("\n", ""))

    common_words = []

    f2 = open("words_len5.txt", "r")
    for y in f2:
        common_words.append(y.replace("\n", ""))
    return word_list, common_words

    

def score_common_words(common_word_list):

    score_dict_common = {}

    for i in range(len(common_word_list)):
        score_dict_common[common_word_list[i]] = ((len(common_word_list) - i ) / len(common_word_list))

    return score_dict_common


def contains_only_gyx(input_string):
    # Define the regular expression pattern
    pattern = re.compile("^[gyx]+$")
    
    # Use the pattern to match the input string
    match = pattern.match(input_string)
    
    # If there is a match, the string contains only 'g', 'y', and 'x'
    return bool(match)               
    

def main():

    
    print("\nRound 1: ")
    
    #reading the words, scoring words by commonality
    og_list, common_words = read_words()
    common_words_score = score_common_words(common_words)

    #calling our solver
    solve_puzzle = solver(og_list, common_words_score)

    full_list = og_list
    print("Possible choices: " , len(og_list))
    print("Here are some starter words:")
    #starter_words(og_list, common_words_score)

    #printing out some starter words
    best_words, best_scores = solve_puzzle.score_words(og_list, common_words_score, 0)
    for i in range(len(best_words)):
            print(best_words[i], " : ", best_scores[i])


    trys = 1
    win = ""

    while (trys < 7 and win != "y"):
        print("Go ahead and guess!\n")

        win = ""
        while (win != "y" and win != "n"):
            win = str(input("Did you win? (y/n) ")).lower()
            
            if (win != "y" and win != "n"):
                print("Make sure to type in y or n")
                    

        if (win == "y"):
            print("Congrats!")
            break

        if (win != "y" and trys == 6):
            print("Sorry :/")
            break


        #making sure the guess is valid
        guess = ""
        while (not(guess in(full_list))):
            guess = str(input("What was your guess?   ")).lower()

            if (not(guess in(full_list))):
                print("This word is not in the list, please try again")


        #making sure the input of whats right and wrong in the word is 
        #in the correct format
        right = ""
        while (not(len(right)==5) or (not(contains_only_gyx(right)))):
            right = str(input("Type locations of g, y, x   ")).lower()

            if (not(len(right)==5) or not(contains_only_gyx(right))):
                print("Make sure you only type in 5 characters of g,y, or x")

        new_list = solve_puzzle.adjust_list(og_list, guess, right)
        print("--------------")
        print("Round ", trys + 1, ": ")
        print("New possible choices: ", len(new_list))

        best_words, best_scores = solve_puzzle.score_words(new_list, common_words_score, trys)
    
        print("Here are new words to try: \n")
        for i in range(len(best_words)):
            print(best_words[i], " : ", best_scores[i])

        og_list = new_list
        trys += 1

    return


if __name__ == "__main__":
    main()