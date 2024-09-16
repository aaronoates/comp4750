#########################################################
##  CS 4750 (Fall 2024), Assignment #1, Question #2    ##
##   Script File Name: tcomp2.py                       ##
##       Student Name: Aaron Oates                     ##
##         Login Name: ajoates                         ##
##              MUN #: 202105417                       ##
#########################################################
import sys

def read_words(filepath):
    """
    Reads the contents of the file and splits them into words based on whitespace.
    """
    with open(filepath, 'r') as f:  # Opens and reads from the designated filepath
        return set(f.read().split())  # Reads the contents of the file and splits by whitespace
    
def num_Of_Words(words):
    

    num_of_words = len(words)

    return num_of_words

def SD(X,Y):
    
    all_words = X.symmetric_difference(Y) #creates a set of all the words that are in X or Y but not both.   

    

    sd = len(all_words) #Gets the number of words in the above set.
    return sd

def sim(X,Y):
    Sim = 1.0 - (SD(X,Y)/(num_Of_Words(X) + num_Of_Words(Y))) #based on the formula in the assignment text.
    return Sim



def main():
    if len(sys.argv) < 3:  # Ensure there are at least 3 command-line arguments
        print("usage: python3 tcomp2.py filename file1name file2name...")
        return
    
    most_similar_file = None #To be assigned later
    best_sim_score = 0.0 #Default value assignment
    master_file = sys.argv[1] #The master file is the second command line argument
    comparison_files = sys.argv[2:] #All arguments from the third one onwards are the comparison files.
    master_words = read_words(master_file) 
    for comparison_file in comparison_files:
        comparison_words = read_words(comparison_file) 
        sim_score = sim(master_words, comparison_words)
        print(f'>>> Sim("{master_file}", "{comparison_file}") = {sim_score:.3f}') #Prints the Sim score of the master file and the current comparison file to 3 decimal places
        if sim_score > best_sim_score:
            best_sim_score = sim_score #this sim score becomes the new current best.
            most_similar_file = comparison_file # this comparison file becomes the new most similar.
    print(f'File "{most_similar_file}" is most similar to "{master_file}"')
    

if __name__ == "__main__":
    main()
