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

        for _ in range(num_states):
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
    state_count = 1

    for state1 in F1:
        for (l_symbol, u_symbol), next_states1 in F1[state1].items():
            for state2 in F2:
                for (l_symbol2, u_symbol2), next_states2 in F2[state2].items():
                    if l_symbol == l_symbol2:
                        for next_state1 in next_states1:
                            for next_state2 in next_states2:
                                composed_state = (next_state1, next_state2)
                                if composed_state not in composed_fst:
                                    composed_fst[composed_state] = {}
                                composed_fst[composed_state][(l_symbol, u_symbol)] = composed_fst.get(composed_state, {}).get((l_symbol, u_symbol), []) + [next_state2]
    
    return composed_fst

def reconstructUpper(l, F):
    """Reconstructs upper strings associated with a lower string."""
    current_states = [1]
    results = []

    for symbol in l:
        next_states = []
        new_results = []  # Store new results in a separate list for this iteration

        for state in current_states:
            if state in F:
                transitions = F[state]
                for (l_symbol, u_symbol), next in transitions.items():
                    if l_symbol == symbol or l_symbol == "-":
                        next_states.extend(next)
                        new_results.append(u_symbol)  # Collect outputs for this iteration

        # If we found any next states, update current_states and append results
        if next_states:
            current_states = next_states
            results.extend(new_results)  # Extend results with new results from this iteration
        else:
            break  # No next states, break early

    # Print the final reconstructed form
    if results:
        print(''.join(results))  # Join the list into a single string
    else:
        print("------------------------")  # Print dashes if no matches found


def reconstructLower(u, F):
    """Reconstructs lower strings associated with an upper string."""
    current_states = [1]
    results = []
    
    for symbol in u:
        next_states = []
        for state in current_states:
            if state in F:
                transitions = F[state]
                for (l_symbol, u_symbol), next in transitions.items():
                    if u_symbol == symbol or u_symbol == "-":
                        next_states.extend(next)
                        results.append(l_symbol)  # Append directly to the results list
        current_states = next_states
    
    if results:
        print(''.join(results))  # Join the list into a single string
    else:
        print("No matches found.")

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
        combined_fst = composeFST(combined_fst, fst)

    # Output number of states and transitions
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
