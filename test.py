import pandas as pd
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
    return common_words[0:100]


def determine_xyg(guess, true):
    
    right = ['y'] * 5
    print(right)

    yellow_count = {}
    for i in range(len(guess)):
        #if the letter is in the right place
        if guess[i] == true[i]:
            right[i] = 'g'
    print(right)       
    for i in range(len(guess)):
        #if the letter is not in the word
        if (guess[i] not in true):
            right[i] = 'x'
            
    print(right)
    right = ''.join(right)
    return right



def look_ahead(curr_word_list):

    total_scores = {}
    for i in curr_word_list:
        total_scores[i] = 0

    #for this we need to iterate through every word in the word list
    for i in range(len(curr_word_list)):

        #assuming every word could be the correct answer
        true_answer = curr_word_list[i]

        #going through the whole word list, seeing
        #how many guesses it would take to reach the 
        #"true" answer giving our methodology
        for j in range(len(curr_word_list)):
            num_guesses = 1

            guess = curr_word_list[j]
            #og_list = curr_word_list

            while ("guess" != true_answer):


                #new_list = solve_puzzle.adjust_list(og_list, guess, right)

                num_guesses += 1

            total_scores[curr_word_list[j]] += num_guesses

def main():
    print(determine_xyg("green", "nuieq"))
    return
    
if __name__ == "__main__":
    main()