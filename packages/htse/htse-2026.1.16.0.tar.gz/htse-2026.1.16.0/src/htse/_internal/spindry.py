import logging
from dataclasses import dataclass
from itertools import combinations

import numpy as np
import spindry as spd  # type: ignore[import-untyped]
import stk
from scipy.spatial.distance import cdist

from htse._internal.properties import (
    calculate_centroid_distance,
    calculate_min_atom_distance,
)


def get_supramolecule(hgcomplex, host_charges, guest_charges):
    charges = host_charges + guest_charges

    return spd.SupraMolecule(
        atoms=(
            ChargedAtom(
                id=atom.get_id(),
                element_string=atom.__class__.__name__,
                charge=charges[atom.get_id()],
            )
            for atom in hgcomplex.get_atoms()
        ),
        bonds=(
            spd.Bond(
                id=i,
                atom_ids=(
                    bond.get_atom1().get_id(),
                    bond.get_atom2().get_id(),
                ),
            )
            for i, bond in enumerate(hgcomplex.get_bonds())
        ),
        position_matrix=hgcomplex.get_position_matrix(),
    )


@dataclass
class SpindryConformer:
    name: str
    conformer: spd.SupraMolecule
    host_conf: spd.Molecule
    guest_conf: spd.Molecule
    potential: float


class Laundrette:
    def __init__(
        self,
        num_dockings,
        naming_prefix,
        output_dir,
        potential=None,
        seed=None,
        verbose=True,
    ):
        self._num_dockings = num_dockings
        self._naming_prefix = naming_prefix
        self._output_dir = output_dir

        if potential is None:
            self._potential = spd.SpdPotential(5)

        self._verbose = verbose
        if seed is None:
            self._rng = np.random.default_rng(seed=42)
        else:
            self._rng = np.random.default_rng(seed=seed)

    def run_dockings(
        self,
        host_bb,
        host_charges,
        guest_bb,
        guest_charges,
    ):
        for docking_id in range(self._num_dockings):
            if self._verbose:
                logging.info(f"docking run: {docking_id + 1}")

            guest = stk.host_guest.Guest(
                building_block=guest_bb,
                start_vector=guest_bb.get_direction(),
                end_vector=self._rng.random((1, 3))[0],
                # Change the displacement of the guest.
                displacement=self._rng.random((1, 3))[0],
            )
            # TODO: Optimise the host-guest complex with UFF.
            hgcomplex = stk.ConstructedMolecule(
                topology_graph=stk.host_guest.Complex(
                    host=stk.BuildingBlock.init_from_molecule(host_bb),
                    guests=guest,
                ),
            )
            supramolecule = get_supramolecule(
                hgcomplex=hgcomplex,
                host_charges=host_charges,
                guest_charges=guest_charges,
            )
            comps = list(supramolecule.get_components())

            cg = spd.Spinner(
                step_size=1.0,
                rotation_step_size=2.0,
                num_conformers=200,
                max_attempts=500,
                potential_function=self._potential,
                beta=1.0,
                random_seed=None,
            )
            cid = 1
            for conformer in cg.get_conformers(supramolecule):
                comps = list(conformer.get_components())
                yield SpindryConformer(
                    name=f"{self._naming_prefix}_{docking_id}_{cid}",
                    conformer=conformer,
                    host_conf=comps[0],
                    guest_conf=comps[1],
                    potential=conformer.get_potential(),
                )
                cid += 1


def run_spinner(supramolecule, guest_bb, output_dir):
    cg = spd.Spinner(
        step_size=1.0,
        rotation_step_size=2.0,
        num_conformers=20,
        max_attempts=50,
        potential_function=QSpdPotential(nonbond_epsilon=10),
        # potential_function=UFFPotential(hgcomplex),
        # beta=0.4,
        beta=10,  # Lower tempterature to make high energy cases harder
        random_seed=None,
    )

    spd_energies = {}
    collisions = {}
    comcom = {}
    for conformer in cg.get_conformers(supramolecule):
        # spd_energies[conformer.get_cid()] = conformer.get_potential()

        comps = list(conformer.get_components())
        if conformer.get_cid() == 0:
            comps[0].write_xyz_file(f"{output_dir}/h_conf.xyz")
        guest_mol = guest_bb.with_position_matrix(
            comps[1].get_position_matrix(),
        )
        guest_mol.write(f"{output_dir}/conf_{conformer.get_cid()}.xyz")

    collisions[conformer.get_cid()] = calculate_min_atom_distance(conformer)
    comcom[conformer.get_cid()] = calculate_centroid_distance(conformer)
    spd_energies[conformer.get_cid()] = conformer.get_potential()

    return collisions, spd_energies, comcom


class ChargedAtom(spd.Atom):
    def __init__(self, id, element_string, charge):
        super().__init__(id, element_string)
        self._charge = charge

    def get_charge(self):
        return self._charge


class QSpdPotential(spd.SpdPotential):
    def _get_charges(self, charges1, charges2):
        charges = np.outer(charges1, charges2)
        return charges

    def _electrostatic_potential(self, distance, charges):
        # E = k_e * q1*q2 / r
        # k_e in eV A e^-2
        _constant = 14.3996
        # k_e in kJ/mol A e^-2
        _constant *= 96.4869
        # In kJ/mol.
        potential = _constant * charges / distance
        return potential

    def _compute_nonbonded_potential(
        self,
        position_matrices,
        radii,
        charges,
    ):
        nonbonded_potential = 0
        for pos_mat_pair, radii_pair, qs_pair in zip(
            combinations(position_matrices, 2),
            combinations(radii, 2),
            combinations(charges, 2),
        ):
            pair_dists = cdist(pos_mat_pair[0], pos_mat_pair[1])
            sigmas = self._combine_sigma(radii_pair[0], radii_pair[1])
            charges = self._get_charges(qs_pair[0], qs_pair[1])
            nonbonded_potential += np.sum(
                self._nonbond_potential(
                    distance=pair_dists.flatten(),
                    sigmas=sigmas.flatten(),
                )
            )
            nonbonded_potential += np.sum(
                self._electrostatic_potential(
                    distance=pair_dists.flatten(),
                    charges=charges.flatten(),
                )
            )

        return nonbonded_potential

    def compute_potential(self, supramolecule):
        component_position_matrices = (
            i.get_position_matrix() for i in supramolecule.get_components()
        )
        component_radii = (
            tuple(j.get_radius() for j in i.get_atoms())
            for i in supramolecule.get_components()
        )
        component_charges = (
            tuple(j.get_charge() for j in i.get_atoms())
            for i in supramolecule.get_components()
        )
        return self._compute_nonbonded_potential(
            position_matrices=component_position_matrices,
            radii=component_radii,
            charges=component_charges,
        )
