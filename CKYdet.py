import sys # for allowing the use of command-line arguments

class Grammar: #Grammar class definition which will be used to store and retrieve grammar rules for parsing.
    def __init__(self): #constructor method of the grammar class that is automatically run when an instance of this class is created.
        self.rules = {} #initializes an empty dictionary named rules, which will hold grammar rules. The keys of this dictionary will be left-hand side (LHS) symbols, and the values will be lists of possible right-hand side (RHS) expansions.
    
    def add_rule(self, lhs, rhs): #add_rule method definition that takes 2 parameters: the left hand side symbol, and the right hand side symbol.
        if lhs not in self.rules: #if the lhs is not currently a key in the rules dictionary
            self.rules[lhs] = [] #create an empty list as its value
        self.rules[lhs].append(rhs) #append the rhs to the list of rules for lhs in the rules dictionary.
    
    def get_rhs(self, symbol): # get_rhs method that takes one parameter, symbol.
        return self.rules.get(symbol, []) #returns the list of RHS expansions for the given symbol. if symbol exists in the dictionary, returns its associated list of RHS expansions. else, returns an empty list.

def parse_grammar(grammar_file): #defines a method parse_grammar that takes a single parameter grammar file.
    grammar = Grammar() #creates an instance of the grammar class called grammar. this will store the grammar rules parsed from the file.
    with open(grammar_file, 'r') as file: #reads from the grammar file
        for line in file: #iterates through the lines of the file
            line = line.strip() #eliminates leading and trailing whitespace
            if '->' in line: # Will be true if this line contains a grammar rule.
                lhs, rhs = line.split('->', 1) #splits the line at the first occurence of -> , creating two parts: lhs and rhs.
                lhs = lhs.strip() #eliminates trailing and leading whitespace for lhs.
                rhs = rhs.strip() #eliminates trailing and leading whitespace for rhs.

                # Handle quoted strings and multiple symbols
                if rhs.startswith('"') and rhs.endswith('"'):
                    # Remove quotes around single words like "word"
                    rhs_symbols = [rhs[1:-1]]
                else:
                    # Split multi-symbol RHS (like 'Det N')
                    rhs_symbols = rhs.split()

                grammar.add_rule(lhs, rhs_symbols)
    return grammar

def parse_utterances(utterance_file):
    with open(utterance_file, 'r') as file:
        return [line.strip() for line in file]

def cky_parse(grammar, utterance):
    words = utterance.split()
    n = len(words)
    parse_table = [[{} for _ in range(n+1)] for _ in range(n)]

    for j in range(1, n+1):
        word = words[j-1]
        for lhs, rhs_list in grammar.rules.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] == word:
                    parse_table[j-1][j][lhs] = f'[{lhs} "{word}"]'
        
        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                for lhs, rhs_list in grammar.rules.items():
                    for rhs in rhs_list:
                        if len(rhs) == 2:
                            B, C = rhs
                            if B in parse_table[i][k] and C in parse_table[k][j]:
                                B_parse = parse_table[i][k][B]
                                C_parse = parse_table[k][j][C]
                                parse_table[i][j][lhs] = f'[{lhs} {B_parse} {C_parse}]'

    if 'S' in parse_table[0][n]:
        return [parse_table[0][n]['S']]
    else:
        return ["No valid parse"]

def main():
    if len(sys.argv) != 3:
        print("Usage: python CKYdet.py <grammar_file> <utterance_file>")
        sys.exit(1)

    grammar_file = sys.argv[1]
    utterance_file = sys.argv[2]

    grammar = parse_grammar(grammar_file)
    utterances = parse_utterances(utterance_file)

    for idx, utterance in enumerate(utterances, 1):
        print(f"Utterance #{idx}: {utterance}")
        parses = cky_parse(grammar, utterance)
        for parse_idx, parse in enumerate(parses, 1):
            if parse == "No valid parse":
                print(f"  {parse}")
            else:
                print(f"  Parse #{parse_idx}: {parse}")
        print()

if __name__ == "__main__":
    main()
