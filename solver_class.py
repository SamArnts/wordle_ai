import pandas as pd
import re

class solver:

    def __init__(self, og_list, common_word_score):
        self.og_list = og_list
        self.common_word_score = common_word_score


    def score_words(self, word_list, common_word_score, round):

        score_dict_letter = {
            "e" : 11.1607, "a" : 8.4966, "r" : 7.5809, "i" : 7.5448, "o" : 7.1635,
            "t" : 6.9509, "n" : 6.6544, "s" : 5.7351, "l" : 5.4893, "c" : 4.5388,
            "u" : 3.6308, "d" : 3.3844, "p" : 3.1671, "m" : 3.0129, "h" : 3.0034,
            "g" : 2.4705, "b" : 2.0720, "f" : 1.8121, "y" : 1.7779, "w" : 1.2899,
            "k" : 1.1016, "v" : 1.0074, "x" : 0.2902, "z" : 0.2722, "j" : 0.1965,
            "q" : 0.1962
        }

        scored_words = {}

        for word in word_list:
            letters_used = []
            score = 0
            repeats = 0
            for i in word:
                if (str.isalpha(i)):
                    if not((i in(letters_used))):
                        score += score_dict_letter[i]
                        letters_used.append(i)
                    else:
                        repeats += 1

            #penalizing words for having the same letters
            score = score * ((5- repeats) / 5)

            #adding the commonality multiplier
            #commonality (how common the word is) is taken into account 
            #more towards later rounds
            if (word in common_word_score):
                score = score + ((round / 6) * (score * common_word_score[word]))

            scored_words[word] = score

        df = pd.DataFrame(data={"Word": scored_words.keys(), "Score": scored_words.values()})

        df_sorted = df.sort_values(by="Score", ascending=False)

        return df_sorted["Word"].to_numpy(), df_sorted["Score"].to_numpy()
    
    

    def adjust_list(self, old_list, guess, right):

        x_index = []
        green_index = []
        yellow_index = []

        new_list = []


        #getting the indexes that were right
        #or had the right letters
        for i in range(0, 5):
            if right[i] == "g":
                green_index.append(i)
            
            elif right[i] == "y":
                yellow_index.append(i)

            else:
                x_index.append(i)
            


        for word in range(len(old_list)):
            
            
            greens_good = True
            yellows_good = True
            x_good = True

            #this is for situations where people guess a word
            #with two of the same letter, one is green and one
            #not
            green_letters = []
            for j in green_index:
                green_letters.append(old_list[word][j])

            for w in x_index:
                if ((guess[w] in old_list[word]) and (guess[w] not in(green_letters))):

                    x_good = False
                    break

            #if word doesn't contain any of the letters marked as x
            #checking to see if the word has the letters marked green
            #in the correct indexes
            if (x_good):
                for j in green_index:
                    if (old_list[word][j] != guess[j]):
                        greens_good = False
                        break
            
            #if the greens are all good
            #check to make sure that word has all the letters marked yellow
            #but not at the same index
            if (greens_good and x_good):
                for k in yellow_index:
                    if ((old_list[word][k] == guess[k]) or not((guess[k] in(old_list[word])))):
                        yellows_good = False
                        break
            
            if (x_good and greens_good and yellows_good):
                new_list.append(old_list[word])


        return new_list
