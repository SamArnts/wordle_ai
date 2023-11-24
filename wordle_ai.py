
import pandas as pd
import re
import random
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

def look_ahead(curr_word_list, common_words_score, round):

    total_scores = {}
    for i in curr_word_list:
        total_scores[i] = 0

    word_list = []

    #if the current word list is too big it will take a long time
    #will choose the most common words to increase our chances
    if (len(curr_word_list) > 200):
        remaining_common_words = {}
        for i in curr_word_list:
            if i in common_words_score:
                remaining_common_words[i] = common_words_score[i]
            else:
                remaining_common_words[i] = 0

        new_common_df = pd.DataFrame(data={"Word": remaining_common_words.keys(), 
                                        "Score": remaining_common_words.values()}).sort_values(by="Score", ascending=False)
        

        word_list = new_common_df["Word"].to_numpy()[0:200]
        
    else:
        word_list = curr_word_list

        
    print("Trying ", len(word_list), " combinations...")
    # #for this we need to iterate through every word in the word list
    for i in range(len(word_list)):
        print('**************************')
        print("Trying word ", i+1)
        print('**************************')
        

        #assuming every word could be the correct answer
        true_answer = word_list[i]
        # print("++++++++++++++++++++++++")
        # print("TRUE: ",  true_answer)
        # print("++++++++++++++++++++++++")

        #going through the whole word list, seeing
        #how many guesses it would take to reach the 
        #"true" answer giving our methodology
        for j in range(len(word_list)):
            # if ((j + 1) % 10 == 0):
            #     print("Combo ", j + 1)
            new_solver = solver()
            num_guesses = 1


            #seeing what would happen if we choose the current word
            #as our guess

            #how likely is it that we'd be successful
            guess = word_list[j]
            #print("First guess", guess)
            og_list = word_list

            while (guess != true_answer):
                # print("------------------------------------")
                # print("Num guess", num_guesses)
                # print("------------------------------------")

                right = new_solver.determine_xyg(guess=guess, true=true_answer)
                # print("right: ", right)
            

                #parsing down the list based on previous guess, getting new best scores
                #print("Length old list", len(og_list))
                new_list = new_solver.adjust_list(og_list, guess, right)
                #print("Length new list", len(new_list))
                best_words, best_scores = new_solver.score_words(new_list, common_words_score, round + num_guesses)
                #getting the best guess using the heuristic
                guess = best_words[0]
                #print("New guess: ", guess)

                og_list = new_list

                num_guesses += 1


            total_scores[word_list[j]] += num_guesses
            # print("***********************************")
            # print(curr_word_list[j], ": total score, ", total_scores[curr_word_list[j]])
            # print("***********************************")

    df = pd.DataFrame(data={"Word": total_scores.keys(), "Score": total_scores.values()})

    #everything that has 0 guesses is no longer in the list
    df = df[df["Score"] > 0]
    df_head = df.sort_values(by="Score").head()

    return df_head["Word"].to_numpy(), df_head["Score"].to_numpy()


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
    solve_puzzle = solver()

    full_list = og_list
    print("Possible choices: " , len(og_list))
    print("Here are the top 5 starter words:")
    print("irate terai tiare retia raine")

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
        print("Thinking of new words .....")
        words, scores = look_ahead(new_list, common_words_score, trys)

        
        
        print("Here are new words to try: \n")
        for i in range(len(words)):
            print(words[i], " : ", scores[i])

        og_list = new_list
        trys += 1

    return


if __name__ == "__main__":
    main()