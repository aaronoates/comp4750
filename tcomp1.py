#########################################################
##  CS 4750 (Fall 2024), Assignment #1, Question #1    ##
##   Script File Name: tcomp1.py                       ##
##       Student Name: Aaron Oates                     ##
##         Login Name: ajoates                         ##
##              MUN #: 202105417                       ##
#########################################################
import sys

def read_filepath(filepath):
    with open(filepath, 'r') as f:  #Opens and reads from the designated filepath
        return ''.join(f.read().split()) #reads the contents of the file as a single string, removes whitespaces etc., splits the contents of the file into a list of words, and then concatenates all the list elements together.
    
def ngram_frequency(text, n):
    total_ngrams = len(text) - n + 1 #The total number of n-grams you can extract from the string is the number of positions in the string where you can start forming an n-gram. #In a string of length L, the last possible starting position for an n-gram of length n is at position L - n. So, the number of possible starting positions is L - n + 1, because you have to account for the 0th index.
    #print("total ngrams for ", text, " is", total_ngrams)
    frequencies = {} #defines an empty dictionary. The keys will be the different ngrams, and the values will be the frequencies at which they appear.
    for i in range(total_ngrams):
        ngram = text[i:i+n] #if i = 0, and n = 3, then the first n gram in the text starts at the first index and comprises it and the next two indeces.
        if ngram in frequencies: #if the ngram is a key in the frequencies dictionary, then this block runs.
            frequencies[ngram] += 1 #increments the value assigned to the ngram key by 1.
        else:
            frequencies[ngram] = 1 #If the else block runs, this implies that a new ngram has been discovered, so we create a new key to represent it and assign it the value of 1 initially.

    for ngram in frequencies:
        frequencies[ngram] /= total_ngrams #if an ngram appears 2 times, and there are 7 total ngrams, then the frequency is 2/7.
    #print(f"the frequencies of the different n-grams in {text} is {frequencies}")
    return frequencies

def diff_ngrams(freq1, freq2):
    all_ngrams = set(freq1.keys()).union(set(freq2.keys())) # converts two dictionaries of ngram frequencies into sets so that they can be united into a single set containing all ngram frequencies in either set.
    #print(all_ngrams)
    diff_sum = 0.0 #default value assignment

    for n_gram in all_ngrams:
        diff_sum += abs(freq1.get(n_gram, 0) - freq2.get(n_gram, 0))
        #print(diff_sum)

    #print("diff sum between ", freq1, "and ", freq2, " is ", diff_sum)
    return diff_sum

def similarity_score(master_freq, comparison_freq):
    diff_sum = diff_ngrams(master_freq, comparison_freq) #gets the diff_sum 
    similarity = 1.0 - (diff_sum/2.0) #based on the formula given in the assignment text.
    #print("sim score between ", master_freq, "and ", comparison_freq, "is, ", similarity)
    return similarity

def main():
    if len(sys.argv) < 4: #ensures that there are at least 4 command line arguments
        print("usage: python3 tcomp1.py filename n file1name file2name...")
        return
    
    master_file = sys.argv[1] #the master file will be the second command line argument.
    n = int(sys.argv[2]) # the number of the n-gram will be the third command line argument.
    comparison_files = sys.argv[3:] #All command line arguments from the fourth one onwards are the comparsion files.
    master_text = read_filepath(master_file) #reads the text from the master_file
    master_freq = ngram_frequency(master_text,n) #gets the ngram frequency of the master text.

    best_sim = 0 #default variable assignment, because the similarity will obviously never be -1. Must be at least 0.
    most_similar_file = None #creates an empty variable assignment to be assigned once the most similar file is decided
    for comp_file in comparison_files: # iterates through the comparison files
        comp_text = read_filepath(comp_file) #reads the contents of the current comparison file
        comp_freq = ngram_frequency(comp_text, n) #gets the ngram frequency of the comp_text
        sim_score = similarity_score(master_freq, comp_freq) #calculates the similarity score
        print(f'>>> Sim("{master_file}","{comp_file}") = {sim_score:.3f}') # prints the similarity score to 3 floating point decimals
        if sim_score > best_sim: #if the sim score in the current iteration is higher than the current best, then the current sim score replaces the current best.
            best_sim = sim_score # best sim is now the current sim.
            most_similar_file = comp_file #most similar file is now the current file.

    print(f' File"{most_similar_file}" is most similar to file "{master_file}"') #prints it to the console.

if __name__ == "__main__":
    main()