import numpy as np

# Atomic number to element symbol mapping (partial, add more if needed)
atomic_number_to_symbol = {
    1: 'H', 2: 'He', 6: 'C', 7: 'N', 8: 'O', 17:'Cl', 19:'K'
    # Add more mappings based on your data
}

def parse_line(line):
    return [float(x) if is_number(x) else x for x in line.split()]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_trajectory(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    number_of_atoms = int(lines[0].strip())
    box_data = []
    coord_data = []
    dipole_data = []
    atom_types = set()
    type_indices_first_snapshot = []
    first_snapshot_processed = False

    for line in lines[1:]:
        if line.startswith('# Step') and first_snapshot_processed:
            # Skip processing other snapshots after the first one is done
            break
        elif line.startswith('# Step'):
            first_snapshot_processed = True
        elif line.startswith('# Cell'):
            box_data.append(parse_line(line))
        elif not line.startswith('#') and first_snapshot_processed:
            line_data = parse_line(line)
            if len(line_data) > 10:
                atomic_charge = int(line_data[1])
                element_symbol = atomic_number_to_symbol.get(atomic_charge, 'Unknown')
                atom_types.add(element_symbol)
                if first_snapshot_processed:
                    type_indices_first_snapshot.append(element_symbol)
                coord_data.append(line_data[3:6])  # Extracting position data
                dipole_data.append(line_data[9:12])  # Extracting dipole data

    # Creating type map
    type_map = {element: idx for idx, element in enumerate(sorted(atom_types))}

    # Converting type indices for the first snapshot
    type_indices_first_snapshot = [type_map[element] for element in type_indices_first_snapshot]

    box_array = np.array(box_data)
    coord_array = np.array(coord_data).reshape(-1, 3*number_of_atoms)
    dipole_array = np.array(dipole_data).reshape(-1, 3*number_of_atoms)

    return box_array, coord_array, dipole_array, type_map, type_indices_first_snapshot

# Replace 'your_file.txt' with your actual file name
box, coord, dipole, type_map, type_indices_first_snapshot = read_trajectory('your_file.txt')

np.save('box.npy', box)
np.save('coord.npy', coord)
np.save('atomic_dipole.npy', dipole)

# Saving type map
with open('type_map.raw', 'w') as file:
    for element, idx in type_map.items():
        file.write(f'{element}: {idx}\n')

# Saving type indices of the first snapshot
np.savetxt('type.raw', [type_indices_first_snapshot], fmt='%d')
