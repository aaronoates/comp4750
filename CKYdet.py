import sys  # Import the sys module for command-line argument handling.

# Define the Grammar class to store and manage grammar rules.
class Grammar:
    def __init__(self):
        # Initialize a dictionary to store grammar rules, where each left-hand side (lhs) points to a list of possible right-hand sides (rhs).
        self.rules = {}
    
    def add_rule(self, lhs, rhs):
        # If the lhs is not already a key in rules, add it with an empty list.
        if lhs not in self.rules:
            self.rules[lhs] = []
        # Append the rhs to the list of rules for this lhs.
        self.rules[lhs].append(rhs)
    
    def get_rhs(self, symbol):
        # Return the list of rhs associated with a given lhs symbol, or an empty list if none exists.
        return self.rules.get(symbol, [])
    
    def print_rules(self):
        # Print all grammar rules for debugging purposes.
        for lhs, rhs_list in self.rules.items():
            for rhs in rhs_list:
                rhs_str = ' '.join(rhs)  # Join rhs symbols into a single string.
                print(f"{lhs} -> {rhs_str}")

# Function to parse a grammar file and return a Grammar object.
def parse_grammar(grammar_file):
    grammar = Grammar()  # Create a new Grammar instance.
    with open(grammar_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading and trailing whitespace.
            if '->' in line:  # Process lines that contain '->' to indicate a rule.
                lhs, rhs = line.split('->', 1)  # Split into lhs and rhs by '->'.
                lhs = lhs.strip()  # Clean lhs.
                rhs = rhs.strip()  # Clean rhs.

                # Check if rhs is a terminal symbol (enclosed in quotes).
                if rhs.startswith('"') and rhs.endswith('"'):
                    rhs_symbols = [rhs[1:-1]]  # Remove quotes and store as a single symbol.
                else:
                    rhs_symbols = rhs.split()  # Split rhs into a list of symbols if not terminal.
                grammar.add_rule(lhs, rhs_symbols)  # Add the rule to the grammar.
    return grammar  # Return the parsed Grammar object.

# Function to parse utterances from a file, returning a list of strings (utterances).
def parse_utterances(utterance_file):
    with open(utterance_file, 'r') as file:
        return [line.strip() for line in file]  # Return a list of stripped lines.

# CKY parsing function that takes a Grammar object and an utterance string and returns a list of possible parses.
def cky_parse(grammar, utterance):
    words = utterance.split()  # Split the utterance into individual words.
    n = len(words)  # Number of words in the utterance.
    # Initialize an (n x n+1) parse table, where each cell holds a dictionary of potential parses for each lhs.
    parse_table = [[{} for _ in range(n+1)] for _ in range(n)]
    
    # Populate the table with terminal productions.
    for j in range(1, n+1):
        word = words[j-1]  # Get the j-th word (1-based index).
        for lhs, rhs_list in grammar.rules.items():
            for rhs in rhs_list:
                # If rhs matches the word as a terminal production, add it to the parse table.
                if len(rhs) == 1 and rhs[0] == word:
                    parse_table[j-1][j][lhs] = f'[{lhs} "{word}"]'
        
        # Handle unary productions in each cell.
        unary_updates = True
        while unary_updates:
            unary_updates = False
            for lhs, rhs_list in grammar.rules.items():
                for rhs in rhs_list:
                    # If rhs has a single symbol and it exists in the parse table, add the unary production.
                    if len(rhs) == 1 and rhs[0] in parse_table[j-1][j] and lhs not in parse_table[j-1][j]:
                        parse_table[j-1][j][lhs] = f'[{lhs} {parse_table[j-1][j][rhs[0]]}]'
                        unary_updates = True
    
    # Fill in the table for non-terminal rules.
    for span in range(2, n+1):  # Span length starts from 2 to n (since we handle terminals separately).
        for i in range(n - span + 1):
            j = i + span  # Endpoint of the span.
            for k in range(i+1, j):  # Split point within the span.
                for lhs, rhs_list in grammar.rules.items():
                    for rhs in rhs_list:
                        # If rhs has two symbols, check if they can be combined from sub-spans.
                        if len(rhs) == 2:
                            B, C = rhs
                            if B in parse_table[i][k] and C in parse_table[k][j]:
                                B_parse = parse_table[i][k][B]  # Get parse for B.
                                C_parse = parse_table[k][j][C]  # Get parse for C.
                                # Combine B and C into lhs parse and add to the table.
                                parse_table[i][j][lhs] = f'[{lhs} {B_parse} {C_parse}]'
            
            # Handle unary productions in each cell for the current span.
            unary_updates = True
            while unary_updates:
                unary_updates = False
                for lhs, rhs_list in grammar.rules.items():
                    for rhs in rhs_list:
                        # Check for unary productions and add to table if new.
                        if len(rhs) == 1 and rhs[0] in parse_table[i][j] and lhs not in parse_table[i][j]:
                            parse_table[i][j][lhs] = f'[{lhs} {parse_table[i][j][rhs[0]]}]'
                            unary_updates = True

    # Return all parses for the start symbol 'S', or indicate no valid parse if none exist.
    if 'S' in parse_table[0][n]:
        return [parse_table[0][n]['S']]
    else:
        return ["No valid parse"]

# Main function to read grammar and utterance files, then parse each utterance.
def main():
    # Check if the correct number of command-line arguments is provided.
    if len(sys.argv) != 3:
        print("Usage: python CKYdet.py <grammar_file> <utterance_file>")
        sys.exit(1)  # Exit if arguments are incorrect.

    # Read the grammar and utterance file paths from command-line arguments.
    grammar_file = sys.argv[1]
    utterance_file = sys.argv[2]

    # Parse the grammar and utterances.
    grammar = parse_grammar(grammar_file)
    utterances = parse_utterances(utterance_file)

    # Process each utterance and print the parse results.
    for idx, utterance in enumerate(utterances, 1):
        print(f"Utterance #{idx}: {utterance}")
        parses = cky_parse(grammar, utterance)  # Parse the utterance.
        for parse_idx, parse in enumerate(parses, 1):
            if parse == "No valid parse":
                print(f"  {parse}")
            else:
                print(f"  Parse #{parse_idx}: {parse}")
        print()

# Execute main function if script is run directly.
if __name__ == "__main__":
    main()
