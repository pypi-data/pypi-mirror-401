from itertools import combinations

import numpy as np
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from scipy.spatial.distance import cdist


def calculate_rot_bonds(stk_molecule):
    rdk_mol = stk_molecule.to_rdkit_mol()
    Chem.SanitizeMol(rdk_mol)
    return rdMolDescriptors.CalcNumRotatableBonds(rdk_mol)


def calculate_centroid_distance(supramolecule):
    comps = list(supramolecule.get_components())
    if len(comps) != 2:
        raise ValueError("more than one guest there buddy!")

    return np.linalg.norm(comps[0].get_centroid() - comps[1].get_centroid())


def calculate_min_atom_distance(supramolecule):
    component_position_matrices = (
        i.get_position_matrix() for i in supramolecule.get_components()
    )

    min_distance = 1e24
    for pos_mat_pair in combinations(component_position_matrices, 2):
        pair_dists = cdist(pos_mat_pair[0], pos_mat_pair[1])
        min_distance = min([min_distance, min(pair_dists.flatten())])

    return min_distance
