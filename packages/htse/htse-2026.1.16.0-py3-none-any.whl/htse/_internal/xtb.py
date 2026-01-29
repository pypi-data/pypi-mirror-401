import os

import numpy as np
import stko


class XtbChargeError(Exception): ...


def get_xtb_charges(molecule, xtb_path):
    output_directory = "temp_directory"
    total_charge = 0

    spe = stko.XTBEnergy(
        xtb_path=xtb_path,
        unlimited_memory=True,
        charge=total_charge,
        output_dir=output_directory,
    )
    _ = spe.get_results(molecule)
    charge_file = os.path.join(output_directory, "charges")
    charges = []
    with open(charge_file, "r") as f:
        for line in f.readlines():
            charges.append(float(line.strip()))

    if not np.isclose(sum(charges), total_charge, atol=1e-4):
        raise XtbChargeError(f"{sum(charges)} != {total_charge}")
    if not len(charges) == molecule.get_num_atoms():
        raise XtbChargeError("length of charges != num. atoms")

    os.system(f"rm -r {output_directory}")
    return charges
