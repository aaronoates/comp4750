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

def reconstruct_surface(lexical_form, fst):
    """Reconstruct surface forms from a given lexical form using the FST."""
    current_states = [1]  # Start from the initial state (1)
    results = []

    # Loop through each character in the lexical form
    for char in lexical_form:
        next_states = []
        for state in current_states:
            # Check for all transitions from current states
            for (l_symbol, u_symbol), next_state_list in fst.get(state, {}).items():
                if char == l_symbol:  # If the character matches the l_symbol
                    next_states.extend(next_state_list)
                    # Create new surface forms from u_symbol
                    new_surface = [u_symbol for _ in next_state_list]
                    results.extend(new_surface)

        current_states = next_states  # Update current states for the next iteration

    return results

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
        combined_fst = composeFST(combined_fst, fst)  # This function remains unchanged

    num_states = len(combined_fst)
    num_transitions = sum(len(transitions) for state in combined_fst for transitions in combined_fst[state].values())
    print(f"Composed FST has {num_states} states and {num_transitions} transitions")

    # Read the forms from the specified file and perform the reconstruction
    with open(form_file, 'r') as f:
        for line in f:
            form = line.strip()
            if mode == 'surface':
                print(f"Lexical form: {form}")
                surface_forms = reconstruct_surface(form, combined_fst)
                print("Reconstructed surface forms:")
                print(", ".join(surface_forms) if surface_forms else "None")
                print("------------------------")
            # Handle 'lexical' mode similarly if needed

if __name__ == "__main__":
    main()
