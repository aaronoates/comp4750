import sys

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

def composeFST(F1, F2):
    """Composes two FSTs and returns the resulting FST."""
    composed_fst = {}
    states1 = list(F1.keys())
    states2 = list(F2.keys())

    # Initialize composed states
    for state_of_F1 in states1:
        for state_of_F2 in states2:
            composed_state = (state_of_F1, state_of_F2)
            composed_fst[composed_state] = {}

    start_state = (states1[0], states2[0])
    final_states = []

    # Iterate through transitions in F1 and F2
    for state_of_F1 in F1.keys():
        for (l_symbol1, u_symbol1), next_state1 in F1[state_of_F1].items():
            for state_of_F2 in F2.keys():
                for (l_symbol2, u_symbol2), next_state2 in F2[state_of_F2].items():
                    # Compose transitions where upper symbol of F1 matches lower symbol of F2
                    if u_symbol1 == l_symbol2:
                        composed_state = (state_of_F1, state_of_F2)
                        next_composed_state = (next_state1, next_state2)
                        if (l_symbol1, u_symbol2) not in composed_fst[composed_state]:
                            composed_fst[composed_state][(l_symbol1, u_symbol2)] = []
                        composed_fst[composed_state][(l_symbol1, u_symbol2)].append(next_composed_state)

    # Handle final states
    for state_of_F1 in F1.keys():
        if F1[state_of_F1] == 'F':
            for state_of_F2 in F2.keys():
                if F2[state_of_F2] == 'F':
                    final_states.append((state_of_F1, state_of_F2))

    # Print composed FST for debugging
    print("Composed FST:", composed_fst)

    return composed_fst, final_states

def reconstructUpper(l, F):
    current_states = [1]  # Starting at (1, 1)
    position = 0
    result = []

    while current_states and position < len(l):
        l_symbol = l[position]
        next_states = []
        found = False
        
        # Iterate over all current states and find valid transitions
        for state in current_states:
            if state in F:
                transitions = F[state]
                for (l_symbol_fst, u_symbol), states in transitions.items():
                    if l_symbol_fst == l_symbol:
                        found = True
                        result.append(u_symbol)
                        next_states.extend(states)
                        break
            if found:
                break

        if not found:
            for state in current_states:
                if state in F:
                    transitions = F[state]
                    for (l_symbol_fst, u_symbol), states in transitions.items():
                        result.append(u_symbol)
                        next_states.extend(states)
                        break

        if found:
            position += 1

        current_states = next_states

    print("".join(result))

def reconstructLower(u, f):
    state = (1, 1)  # start at state (1, 1)
    lower_string = ""
    i = 0  # index to traverse the upper string

    while i < len(u):
        upper_symbol = u[i]
        found = False
        
        # Check all transitions for the current state
        if state in f:
            for (lower_symbol, transition_upper), next_states in f[state].items():
                if transition_upper == upper_symbol:
                    lower_string += lower_symbol
                    state = next_states[0]  # move to the next state
                    found = True
                    break
        
        if not found:
            lower_string += upper_symbol
        
        i += 1  # move to the next symbol in the upper string

    return lower_string


def main():
    if len(sys.argv) < 4:
        print("Usage: reconstruct.py <surface|lexical> <file> <FST files...>")
        return

    mode = sys.argv[1]
    form_file = sys.argv[2]
    fst_files = sys.argv[3:]

    # Read FSTs from files
    fst_list = [readFST(fst_file) for fst_file in fst_files]
    
    # Combine FSTs
    combined_fst = fst_list[0]
    for fst in fst_list[1:]:
        combined_fst, final_states = composeFST(combined_fst, fst)

    num_states = len(combined_fst)
    num_transitions = sum(len(transitions) for state in combined_fst for transitions in combined_fst[state].values())

    print(f"Composed FST has {num_states} states and {num_transitions} transitions")

    # Read the forms from the specified file and perform the reconstruction
    with open(form_file, 'r') as f:
        for line in f:
            form = line.strip()
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
