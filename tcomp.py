#########################################################
##  CS 4750 (Fall 2024), Assignment #1, Question #1    ##
##   Script File Name: tcomp1.py                       ##
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

def ngram_frequency(words, n):
    """
    Calculate n-gram frequencies for a list of words.
    :param words: List of words to process.
    :param n: The n-gram size.
    :return: A dictionary with n-gram frequencies.
    """
    frequencies = defaultdict(int)  # Dictionary to hold n-gram frequencies

    for word in words:
        total_ngrams = len(word) - n + 1  # Calculate the number of n-grams in the word
        if total_ngrams > 0:  # Only process words that are long enough for the given n
            for i in range(total_ngrams):
                ngram = word[i:i+n]  # Get the n-gram from the current position
                frequencies[ngram] += 1  # Increment the frequency of the n-gram

    total_ngrams_in_text = sum(frequencies.values())  # sums up all the values in the frequencies dictionary to produce the total number of n_grams in the text.
    for ngram in frequencies:
        frequencies[ngram] /= total_ngrams_in_text  # divides each of the values in frequencies by the total ngrams in the text to get the frequency ratios.

    return frequencies

def diff_ngrams(freq1, freq2):
    """
    Calculate the difference between two n-gram frequency distributions.
    :param freq1: First n-gram frequency distribution.
    :param freq2: Second n-gram frequency distribution.
    :return: The sum of differences in frequencies.
    """
    all_ngrams = set(freq1.keys()).union(set(freq2.keys()))  # Union of all n-grams in either set.
    diff_sum = 0.0 #default value assignment

    for ngram in all_ngrams:
        diff_sum += abs(freq1.get(ngram, 0) - freq2.get(ngram, 0))  # Sum absolute differences

    return diff_sum

def similarity_score(master_freq, comparison_freq):
    """
    Calculate the similarity score between two frequency distributions.
    :param master_freq: Frequency distribution of the master file.
    :param comparison_freq: Frequency distribution of the comparison file.
    :return: The similarity score.
    """
    diff_sum = diff_ngrams(master_freq, comparison_freq)
    similarity = 1.0 - (diff_sum / 2.0)  # Formula for similarity score
    return similarity

def main():
    if len(sys.argv) < 4:  # Ensure there are at least 4 command-line arguments
        print("usage: python3 tcomp1.py filename n file1name file2name...")
        return
    
    master_file = sys.argv[1]  # Master file is the second command-line argument
    n = int(sys.argv[2])  # n-gram size is the third command-line argument
    comparison_files = sys.argv[3:]  # Remaining arguments are comparison files

    master_words = read_words(master_file)  # Get words from the master file
    master_freq = ngram_frequency(master_words, n)  # Get n-gram frequencies of master text

    best_sim = 0.0  # Default value for best similarity score
    most_similar_file = None  # Variable to hold the most similar file

    for comp_file in comparison_files:  # Iterate through comparison files
        comp_words = read_words(comp_file)  # Get words from the comparison file
        comp_freq = ngram_frequency(comp_words, n)  # Get n-gram frequencies of comparison text
        sim_score = similarity_score(master_freq, comp_freq)  # Calculate similarity score
        print(f'>>> Sim("{master_file}", "{comp_file}") = {sim_score:.3f}')  # Output similarity score to 3 decimal places

        if sim_score > best_sim:  # If the current similarity score is higher than the best one
            best_sim = sim_score # best score gets updated to current score.
            most_similar_file = comp_file  # Update the most similar file

    print(f'File "{most_similar_file}" is most similar to file "{master_file}"')  # Output the most similar file

if __name__ == "__main__":
    main()
