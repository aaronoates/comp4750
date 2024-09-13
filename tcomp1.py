import sys

def read_filepath(filepath):
    with open(filepath, 'r') as f:  #Opens and reads from the designated filepath
        return ''.join(f.read().split()) #reads the contents of the file as a single string, removes whitespaces etc., splits the contents of the file into a list of words, and then concatenates all the list elements together.
    
def ngram_frequency(text, n):
    total_ngrams = len(text) - n + 1 #The total number of n-grams you can extract from the string is the number of positions in the string where you can start forming an n-gram. #In a string of length L, the last possible starting position for an n-gram of length n is at position L - n. So, the number of possible starting positions is L - n + 1.
    frequencies = {} #defines an empty dictionary. The keys will be the different ngrams, and the values will be the frequencies at which they appear.
    for i in range(total_ngrams):
        ngram = text[i:i+n] #if i = 0, and n = 3, then the first n gram in the text starts at the first index and comprises it and the next two indeces.
        if ngram in frequencies: #if the ngram is a key in the frequencies dictionary, then this block runs.
            frequencies[ngram] += 1 #increments the value assigned to the ngram key by 1.
        else:
            frequencies[ngram] = 1 #If the else block runs, this implies that a new ngram has been discovered, so we create a new key to represent it and assign it the value of 1 initially.

    for ngram in frequencies:
        frequencies[ngram] /= total_ngrams #if an ngram appears 2 times, and there are 7 total ngrams, then the frequency is 2/7.
    return frequencies

def diff_ngrams(freq1, freq2):
    all_ngrams = set(freq1.keys()).union(set(freq2.keys())) # converts two dictionaries of ngram frequencies into sets so that they can be united into a single set containing all ngram frequencies in either set.
    diff_sum = 0.0
    for n_gram in all_ngrams:
        diff_sum += abs(freq1.get(n_gram,0) - freq2.get(n_gram,0)) # gets the frequency of the given ngram in dictionary 1 if it exists, defaults to 0 if not. Then it does the same thing for dictionary 2. we then subtract frequency1 from frequency 2, get the absolute value of the difference, and then the result is assigned to diff_sum.
    return diff_sum
def similarity_score(master_freq, comparison_freq):
    diff_sum = diff_ngrams(master_freq, comparison_freq)
    similarity = 1.0 - (diff_ngrams/2.0)
    return similarity

def main():
    if len(sys.argv) < 4: #ensures that there are at least 4 command line arguments
        print("usage: python3 tcomp1.py filename n file1name file2name...")
        return
    
    master_file = sys.argv[1] #the master file will be the second command line argument.
    n = int(sys.argv[2]) # the number of the n-gram will be the third command line argument.
    comparison_files = sys.argv[3:] #All command line arguments from the fourth one onwards are the comparsion files.
    master_text = read_filepath(master_file)
    master_freq = ngram_frequency(master_text,n)