import sys

def readFST(filename):
    """Reads an FST description from a file and returns it as a dictionary."""
    with open(filename, 'r') as f: #reads the file with name filename
        first_line = f.readline().strip().split() #reads the next line of the file, which in this case is the first line. It then strips leading and trailing whitespace, and creates a list of all elements in the line separated by whitespace.
        num_states = int(first_line[0]) #first element of first_line will be the number of states.
        alphabet = first_line[1] # a string containing all the upper and lowercase letters in the FST.
        
        fst = {} #creates an empty dictionary called fst.
        for i in range(1,num_states + 1): 
            fst[i] = {} #turns fst into a dictionary of empty dictionaries one for each state.

        for _ in range(1,num_states + 1): 
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
                    fst[state_num][(l_symbol, u_symbol)] = [] #enters the dictionary at the value of the state_num key in fst, and then assigns the [(lsymbol,usymbol)] key in this dictionary the value of an empty list.
                fst[state_num][(l_symbol, u_symbol)].append(next_state) # same as above, but appends the next state to this key's existing value. 
                
        #print(fst)        
        return fst #returns the fst


def composeFST(F1, F2):
    #print(F1)
    #print(F2)
    composed_FST = {} #initialize an empty dictionary which will eventually represent the composed FST.
    transition_count = 0  # Counter for transitions.
    for state_of_F1 in F1.keys(): #The states of the first FST
        for state_of_F2 in F2.keys(): #Thw states of the second FST.
            composed_state = (state_of_F1, state_of_F2) #a tuple representing a new composed state in the FST.
            composed_FST[composed_state] = {} #Initialize transitions for the new state.

            for (lower_1, upper_1), next_state_of_F1 in F1[state_of_F1].items():
                for(lower_2, upper_2), next_state_of_F2 in F2[state_of_F2].items():
                    #print(F2[state_of_F2])
                    if upper_1 == lower_2: #in a composed FST, the upper string in the first FST should become the lower string in the second FST in order to make a valid transition.
                        composed_ul_pair = (lower_1, upper_2)
                        composed_next_state = (next_state_of_F1, next_state_of_F2)
                        if composed_ul_pair not in composed_FST[composed_state]:
                            composed_FST[composed_state][composed_ul_pair] = []
                        composed_FST[composed_state][composed_ul_pair].append(composed_next_state)
    return composed_FST




# Example FSTs

def reconstructUpper(l, F):
    #print(F)
    if isinstance(list(F.keys())[0], tuple):  # Check if states are tuples (composed FST)
        current_states = [(1, 1)]  # Starting at state (1, 1)
    else:  # Uncomposed FST # Starting at state 1, assuming state numbering starts from 1
        current_states = [1]
    position = 0
    result = []

    while current_states and position < len(l):
        l_symbol = l[position]  # Read the current symbol from the lexical form
        next_states = []
        found = False  # Tracks if a valid transition was found

        # Iterate over all current states and find valid transitions
        for state in current_states:
            #print(state)
            if state in list(F.keys()):
                transitions = F[state]
                for (l_symbol_fst, u_symbol), states in transitions.items():
                    if l_symbol_fst == l_symbol:
                        found = True
                        result.append(u_symbol)  # Append the upper symbol to the result
                        next_states.extend(states)  # Add the next possible states
                        break
            if found:
                break

        if not found:
            # If no valid transition is found, output the upper symbol as is and don't consume the lower symbol
            for state in current_states:
                if state in list(F.keys()):
                    transitions = F[state]
                    # Find any transition in the current state and output its upper symbol
                    for (l_symbol_fst, u_symbol), states in transitions.items():
                        result.append(u_symbol)  # Append the upper symbol to the result
                        next_states.extend(states)  # Move to the next states
                        break

        # If a valid transition was found, consume the lower symbol
        if found:
            position += 1

        current_states = next_states

    # Output the result
    print("".join(result))

def reconstructLower(u, F):
    if isinstance(list(F.keys())[0], tuple):  # Check if states are tuples (composed FST)
        current_states = [(1, 1)]  # Starting at state (1, 1)
    else:  # Uncomposed FST # Starting at state 1, assuming state numbering starts from 1
        current_states = [1]
    position = 0
    result = []

    while current_states and position < len(u):
        u_symbol = u[position]  # Read the current symbol from the lexical form
        next_states = []
        found = False  # Tracks if a valid transition was found
        
        # Iterate over all current states and find valid transitions
        for state in current_states:
            if state in F:
                transitions = F[state]
                for (l_symbol, u_symbol_fst), states in transitions.items():
                    if u_symbol_fst == u_symbol:
                        found = True
                        result.append(l_symbol)  # Append the upper symbol to the result
                        next_states.extend(states)  # Add the next possible states
                        break
            if found:
                break

        if not found:
            # If no valid transition is found, output the upper symbol as is and don't consume the lower symbol
            for state in current_states:
                if state in F:
                    transitions = F[state]
                    # Find any transition in the current state and output its upper symbol
                    for (l_symbol, u_symbol_fst), states in transitions.items():
                        result.append(l_symbol)  # Append the upper symbol to the result
                        next_states.extend(states)  # Move to the next states
                        break

        # If a valid transition was found, consume the lower symbol
        if found:
            position += 1

        current_states = next_states

    # Output the result
    print("".join(result))


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
    combined_fst = fst_list[0] #fst_list[0] would be fst_file at sys.argv[3]
    #print("here is the fst for sys.argv[3]")
    #print(combined_fst)
    #print("here is the combined FST for sys.argv[4] and onwards if they exist")
    for fst in fst_list[1:]: # if there are arguments beyond sys.argv[3] we run this for loop until all fsts are accounted for.
        combined_fst = composeFST(combined_fst, fst) # after this loop ends, the combined_fst will be a combined fst of all the fsts.

    #print(combined_fst)
    #if there is only one element in fst_list, then the for loop doesn't execute. This makes sense, because if we call compose_FST and pass an empty list to F2, the combined_fst will just be F1.
    # Output number of states and transitions
    num_states = len(combined_fst) #the number of inner dictionaries in the outer dictionary should give the number of states.
    # Initialize a variable to store the total number of transitions
    num_transitions = 0 #initializes the count for the number of transitions.

# Loop over each state in the FST
    for state in combined_fst:
    # Get all the transitions for the current state
        #print(state)
        transitions_dict = combined_fst[state]
    
    # Loop over each transition (values) in the transition dictionary
        for transitions in transitions_dict.values():
        # Add the number of transitions (could be 1 or more) to the total
            num_transitions += len(transitions)

    print(f"Composed FST has {num_states} states and {num_transitions} transitions") #outputs the number of states and transitions in the composed FST.

    # Read the forms from the specified file and perform the reconstruction
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
