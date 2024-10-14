import sys

def readFST(filename):
    """Reads an FST description from a file and returns it as a dictionary."""
    with open(filename, 'r') as f: #reads from the file passed above
        # Read the number of states and the alphabet
        first_line = f.readline().strip().split() #reads the next line of the file (which would be the first line in this case), strips any leading or trailing whitespace, and then splits the string into a list of substrings separated by whitespace. then stores the list in first_line. for example, " a b " becomes "a b" and then ["a", "b"]
        num_states = int(first_line[0]) # the first element of the first line will be the number of states.
        alphabet = first_line[1]# the second element of the first tline will be all the upper and lowercase characters in the FST.

        
        fst = {} # lines 12-14 create a dictionary for the FST, with the states as the keys and empty dictionaries as the values.
        for i in range(1, num_states + 1):
            fst[i] = {} 
        # Read each state and its transitions
        for _ in range(num_states):
            state_info = f.readline().strip().split() # reads the next line of the file, strips leading and trailing whitespace, then creates a list of elements separated by whitespace.
            state_num = int(state_info[0]) #the first element of state_info will be the number of the state.
            is_final = state_info[1] == 'F' #if the second element of state_info is an F, this state is final.
            
            # Read transitions for this state
            while True:
                position = f.tell()
                line = f.readline().strip()
                if line == '':
                    break
                parts = line.split()
                if len(parts) != 3:
                    f.seek(position)
                    break  # Skip this line if it doesn't have 3 parts
                l_symbol, u_symbol, next_state = parts
                next_state = int(next_state)
                
                # Add the transition to the FST
                if (l_symbol, u_symbol) not in fst[state_num]:
                    fst[state_num][(l_symbol, u_symbol)] = []
                fst[state_num][(l_symbol, u_symbol)].append(next_state)
                
        return fst

def composeFST(F1, F2):
    """Composes two FSTs and returns the resulting FST."""
    composed_fst = {}
    for state1 in F1:
        for l_u in F1[state1]:
            l_symbol, u_symbol = l_u
            next_states1 = F1[state1][l_u]
            for state2 in F2:
                for l_u2 in F2[state2]:
                    if l_u2[0] == l_symbol:  # Match lower symbol
                        next_states2 = F2[state2][l_u2]
                        for next_state1 in next_states1:
                            for next_state2 in next_states2:
                                # Create a new state in the composed FST
                                if (next_state1, u_symbol) not in composed_fst:
                                    composed_fst[(next_state1, u_symbol)] = []
                                composed_fst[(next_state1, u_symbol)].append(next_state2)
    
    # Format composed FST as a dictionary of dictionaries
    result = {}
    for (next_state, u_symbol), next_states in composed_fst.items():
        if next_state not in result:
            result[next_state] = {}
        result[next_state][(next_state, u_symbol)] = next_states

    return result

def reconstructUpper(l, F):
    """Reconstructs upper strings associated with a lower string."""
    current_states = [1]  # Start from state 1
    results = set()
    
    for symbol in l:
        next_states = []
        for state in current_states:
            if state in F:
                transitions = F[state]
                for (l_symbol, u_symbol), next in transitions.items():
                    if l_symbol == symbol or l_symbol == "-":  # Match symbol or epsilon
                        next_states.extend(next)
                        results.add(u_symbol)  # Collect upper string
        current_states = next_states
    
    print(', '.join(results) if results else "No matches found.")

def reconstructLower(u, F):
    """Reconstructs lower strings associated with an upper string."""
    current_states = [1]  # Start from state 1
    results = set()
    
    for symbol in u:
        next_states = []
        for state in current_states:
            if state in F:
                transitions = F[state]
                for (l_symbol, u_symbol), next in transitions.items():
                    if u_symbol == symbol or u_symbol == "-":  # Match symbol or epsilon
                        next_states.extend(next)
                        results.add(l_symbol)  # Collect lower string
        current_states = next_states
    
    print(', '.join(results) if results else "No matches found.")

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
    print(f"Number of states: {num_states}, Number of transitions: {num_transitions}")

    # Read the forms from the specified file and perform the reconstruction
    with open(form_file, 'r') as f:
        for line in f:
            form = line.strip()
            if mode == 'surface':
                print(f"{form}: ", end='')
                reconstructUpper(form, combined_fst)
            elif mode == 'lexical':
                print(f"{form}: ", end='')
                reconstructLower(form, combined_fst)

if __name__ == "__main__":
    main()




