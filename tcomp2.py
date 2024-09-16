#########################################################
##  CS 4750 (Fall 2024), Assignment #1, Question #2    ##
##   Script File Name: tcomp2.py                       ##
##       Student Name: Aaron Oates                     ##
##         Login Name: ajoates                         ##
##              MUN #: 202105417                       ##
#########################################################
import sys
from collections import defaultdict

def read_words(filepath):
    """
    Reads the contents of the file and splits them into words based on whitespace.
    """
    with open(filepath, 'r') as f:  # Opens and reads from the designated filepath
        return f.read().split()  # Reads the contents of the file and splits by whitespace
    
def num_Of_Words(words):
    """
    gets the number of different words in a text
    """
    different_words = []
    for word in words:
        if word not in different_words:
            different_words.append(word)# if a new word is discovered, a new key for this word is created in the dictionary and the count is initialized as 1.
       

    num_of_words = len(different_words)

    return num_of_words

def SD(X,Y):
    x_list = []
    y_list = []
    for word in X:
        if word not in X:
            x_list.append(word)
    
    for word in Y:
        if word not in Y:
            y_list.append(word)
        

    all_words = set(x_list).union(set(y_list))

    sd = len(all_words)
    return sd

def sim(X,Y):
    Sim = 1.0 - (SD(X,Y)/(num_Of_Words(X) + num_Of_Words(Y)))
    print(f'Sim("{X}","{Y}") = {Sim}')



def main():
    if len(sys.argv) < 3:  # Ensure there are at least 4 command-line arguments
        print("usage: python3 tcomp3.py filename file1name file2name...")
        return
    
    
