import sys
import re

class Grammar:
    def __init__(self):
        self.rules = {}
    
    def add_rule(self, lhs, rhs):
        if lhs not in self.rules:
            self.rules[lhs] = []
        self.rules[lhs].append(rhs)
    
    def get_rhs(self, symbol):
        return self.rules.get(symbol, [])

def parse_grammar(grammar_file):
    grammar = Grammar()
    with open(grammar_file, 'r') as file:
        for line in file:
            match = re.match(r'(\S+) -> ("[^"]+"|\S+ \S+|\S+)', line.strip())
            if match:
                lhs, rhs = match.groups()
                rhs_symbols = rhs.strip('"').split()
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
        for lhs, rhs in grammar.rules.items():
            for r in rhs:
                if len(r) == 1 and r[0] == word:
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