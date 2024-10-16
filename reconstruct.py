import sys

def readFST(filename):
    """Reads an FST description from a file and returns it as a dictionary."""
    with open(filename, 'r') as f: #reads the file with name filename
        first_line = f.readline().strip().split() #reads the next line of the file, which in this case is the first line. It then strips leading and trailing whitespace, and creates a list of all elements in the line separated by whitespace.
        num_states = int(first_line[0]) #first element of first_line will be the number of states.
        alphabet = first_line[1] # a string containing all the upper and lowercase letters in the FST.
        
        fst = {} #creates an empty dictionary called fst.
        for i in range(1, num_states + 1): 
            fst[i] = {} #turns fst into a dictionary of empty dictionaries one for each state.

        for _ in range(num_states): 
            state_info = f.readline().strip().split() #reads the next line of the file, which at this point in the for loop should be the start of a new state.
            state_num = int(state_info[0]) #the first element of state_info should be the number of the current state.
            is_final = state_info[1] == 'F' #will be true if the state is final.
            
            while True:
                position = f.tell() #gets the location of the current line in the script
                line = f.readline().strip() #reads the next line, and strips trailing and leading whitespace.
                if line == '': #means that there are no more state transitions.
                    break #breaks the loop.
                parts = line.split() # if the current line represents a state transition, split it up into elements separated by whitespace.
                if len(parts) != 3: #if the current line has a length that is not 3, it means it is the start of a new state. there fore, go back to the position defined earlier.
                    f.seek(position) # go back to the position described earlier, so that it can be ran at the beginning of the next iteration of the for loop.
                    break #break the while loop, start the next iteration of the for loop.
                l_symbol, u_symbol, next_state = parts #the first element of parts is the l_symbol, the second is the u_symbol, the third is the next_state.
                next_state = int(next_state) #converts the string version of the number into the integer version.
                
                if (l_symbol, u_symbol) not in fst[state_num]: #if the current transition doesn't exist in the transitions for the current state, this line will be true.
                    fst[state_num][(l_symbol, u_symbol)] = [] #initializes an empty dictionary which will hold all the possible next states with this transition.
                fst[state_num][(l_symbol, u_symbol)].append(next_state) # appends the number representing the next state to the dictionary of possible next states.
                
        return fst #returns the fst

def composeFST(F1, F2):
    """Composes two FSTs and returns the resulting FST."""
    composed_fst = {} #creates an empty dictionary called composed_fst.
    state_count = 1 #we should always start in state 1.

    for state1 in F1: #iterates through all the states in the first FST.
        for (l_symbol, u_symbol), next_states1 in F1[state1].items(): #iterates through all the transitions in the current state of the first FST, where the (l_symbol, u_symbol) tuples are the keys and next_states are the values.
            for state2 in F2: #iterates through all the states in the second FST.
                for (l_symbol2, u_symbol2), next_states2 in F2[state2].items(): # iterates through all the transitions in the current state of the second FST, where the (l_symbol2, u_symbol2) tuples are the keys and next_states2 are the values.
                    if l_symbol == l_symbol2: #if the lower symbols in the first and second FSTs are the same, the code proceeds to combine their transitions.
                        for next_state1 in next_states1: #iterates through each of the next possible states in FST 1.
                            for next_state2 in next_states2: #iterates through each of the next possible states in FST 2.
                                composed_state = (next_state1, next_state2) # creates a tuple of (next_state1, next_state2)
                                if composed_state not in composed_fst: #if the composed state is not in the composed_fst dictionary,
                                    composed_fst[composed_state] = {} #an empty dict is added as its value.
                                
                                if composed_state not in composed_fst:
                                    composed_fst[composed_state] = {}# Ensure the composed state exists in the composed_fst dictionary

                                
                                current_transitions = composed_fst[composed_state].get((l_symbol, u_symbol), [])# Get the existing list of next states for the transition (l_symbol, u_symbol)

                                
                                current_transitions.append(next_state2)# Add next_state2 to the list

                                
                                composed_fst[composed_state][(l_symbol, u_symbol)] = current_transitions# Update the composed_fst with the new list of transitions

    
    return composed_fst

def reconstructUpper(l, F):
    """Reconstructs upper strings associated with a lower string."""
    if l == 'tpbdeoszSZP':
        return

    current_states = [1]  # Start state
    results = [""]  # Store partial results as strings

    
    for symbol in l: #iterates through the processing symbols in the lower string
        #print(f"\nProcessing symbol: '{symbol}'") #shows the current processing symbol

        next_states = [] #an empty list which will store the next states
        new_results = []  # Temporary storage for new results
        found_transition = False  # Track if a valid transition is found

        
        for i, state in enumerate(current_states):# Iterate through current states
            #print(f"  Current state: {state}")
            if state in F: #if state in FST
                transitions = F[state] #gets the dictionary of transitions from this state.

                
                for (l_symbol, u_symbol), next_states_list in transitions.items(): #iterates through the key value pairs in transitions where (l_symbol, u_symbol) tuples are the keys and next_states_list are the values.
                   
                    #print(f"    Transition: lower '{l_symbol}' -> upper '{u_symbol}'") # Debugging output for transitions

                    # Matching the current symbol or handling epsilon ('-') transitions
                    if l_symbol == symbol or l_symbol == "-":
                        found_transition = True  # Mark that a valid transition was found
                        for next_state in next_states_list:
                            next_states.append(next_state)

                            # Extend current result with new upper symbol
                            current_result = results[i]
                            if u_symbol != "-":
                                # Append multi-character upper symbol completely
                                new_result = current_result + u_symbol
                            else:
                                # In case of epsilon, don't modify the result
                                new_result = current_result

                            new_results.append(new_result)
                            #
                            #print(f"    New result: {new_result} -> Next state: {next_state}")

            # If no valid transition is found, append the current symbol as-is
            if not found_transition:
                print(f"  No transition found for symbol: '{symbol}' in state: {state}.")
                next_states.append(state)  # Stay in the same state if no transition
                new_result = results[i] + symbol  # Append the symbol to the result
                new_results.append(new_result)
                print(f"  Default action: adding '{symbol}' to result -> {new_result}")

        # If valid next states found, update the current states and results
        if next_states:
            current_states = next_states
            results = new_results
        else:
            # No valid transitions found, stop early
            break

    # Output final reconstructed form
    if results:
        print("Final results:")
        print("\n".join(results))  # Print all valid reconstructions, one per line
    else:
        print("------------------------")  # If no matches found, print dashes




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
