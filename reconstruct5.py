import sys
from collections import defaultdict

def readFST(filename):
    """Reads an FST description from a file and returns it as a dictionary."""
    with open(filename, 'r') as f:
        first_line = f.readline().strip().split()
        num_states = int(first_line[0])
        alphabet = first_line[1]

        fst = {}
        for i in range(1, num_states + 1):
            fst[i] = {}

        for _ in range(1, num_states + 1):
            state_info = f.readline().strip().split()
            state_num = int(state_info[0])
            is_final = state_info[1] == 'F'
            
            while True:
                position = f.tell()
                line = f.readline().strip()
                if line == '':
                    break
                parts = line.split()
                if len(parts) != 3:
                    f.seek(position)
                    break
                l_symbol, u_symbol, next_state = parts
                next_state = int(next_state)

                if (l_symbol, u_symbol) not in fst[state_num]:
                    fst[state_num][(l_symbol, u_symbol)] = []
                fst[state_num][(l_symbol, u_symbol)].append(next_state)

        return fst

# Compose two FSTs
def composeFST(fst1, fst2):
    composed_fst = defaultdict(lambda: defaultdict(list))
    for state1, transitions1 in fst1.items():
        for (input_symbol1, output_symbol1), next_states1 in transitions1.items():
            for state2, transitions2 in fst2.items():
                for (input_symbol2, output_symbol2), next_states2 in transitions2.items():
                    if output_symbol1 == input_symbol2:  # Check for matching output/input
                        for next_state1 in next_states1:
                            for next_state2 in next_states2:
                                composed_fst[state1][(input_symbol1, output_symbol2)].append(next_state2)
    return composed_fst

# Reconstruct surface forms for uppercase lexical forms
def reconstructUpper(fst, lexical_form):
    state = 1  # Assuming the start state is 1
    reconstructed_forms = []
    for char in lexical_form:
        found = False
        for (input_symbol, output_symbol), next_states in fst[state].items():
            if input_symbol == char:
                for next_state in next_states:
                    reconstructed_forms.append(output_symbol)
                    state = next_state  # Move to next state
                    found = True
                    break
        if not found:
            return []  # No valid reconstruction
    return [''.join(reconstructed_forms)]  # Return as a single string

# Reconstruct surface forms for lowercase lexical forms
def reconstructLower(fst, lexical_form):
    state = 1  # Assuming the start state is 1
    reconstructed_forms = []
    for char in lexical_form:
        found = False
        for (input_symbol, output_symbol), next_states in fst[state].items():
            if input_symbol == char:
                for next_state in next_states:
                    reconstructed_forms.append(output_symbol)
                    state = next_state  # Move to next state
                    found = True
                    break
        if not found:
            return []  # No valid reconstruction
    return [''.join(reconstructed_forms)]  # Return as a single string

# Main function
def main():
    if len(sys.argv) < 4:
        print("Usage: python3 reconstruct4.py surface word.lex vcePlu.fst addVowPlu.fst")
        return

    mode = sys.argv[1]
    form_file = sys.argv[2]
    fst_files = sys.argv[3:]

    

    # Compose the FSTs
    fst_list = [readFST(fst_file) for fst_file in fst_files]

    combined_fst = fst_list[0]
    for fst in fst_list[1:]:
        combined_fst = composeFST(combined_fst,fst)
    # Print the number of states and transitions
    num_states = len(combined_fst)
    num_transitions = sum(len(transitions) for transitions in combined_fst.values())
    print(f"Composed FST has {num_states} states and {num_transitions} transitions")

    with open(form_file, 'r') as f: #opens the form file, either word.lex for surface reconstructiond or word.srf for lexical reconstructions.
        for line in f:
            form = line.strip() # for example, in word.lex the first iteration of form would be tpbdeoszSZP
            if mode == 'surface':
                print(f"Lexical form: {form}")
                print("Reconstructed surface forms:")
                reconstructUpper(form, combined_fst)
                print("------------------------")
            elif mode == 'lexical':
                print(f"Surface form: {form}")
                print("Reconstructed lexical forms:")
                reconstructLower(form, combined_fst)
                print("------------------------")

if __name__ == "__main__":
    main()
