import pandas as pd
import numpy as np


def read_words():

    #list of most common words
    freq_df = pd.read_csv("unigram_freq.csv")
    all_words = freq_df["word"].to_numpy()

    words_len5 = []


    #words are already sorted by frequecy so we don't
    #need to worry about sorting
    for i in range(len(all_words)):
        if (len(str(all_words[i])) == 5):
            words_len5.append(all_words[i])
    

    #getting the wordle words
    wordle_list = {}
    f = open("words.txt", "r")
    for x in f:
        wordle_list[x.replace("\n", "")] = 0

    #if the word is a wordle word, add it to the list
    wordle_len5 = []
    for i in range(len(words_len5)):
        if (words_len5[i] in wordle_list):
            wordle_len5.append(words_len5[i])

    return wordle_len5

def write_len5_words(words):
    
    f = open("words_len5.txt", "w")

    for i in words:
        f.write(i + "\n")

    f.close()
    return

def main():
    wordle_len5 = read_words()
    write_len5_words(wordle_len5)

if __name__ == "__main__":
    main()
