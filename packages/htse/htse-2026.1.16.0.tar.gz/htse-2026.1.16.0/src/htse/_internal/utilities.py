import os

import stko


def get_guest_conformer(guest_id, run_id, stk_mol, guest_dir):
    opt_file = os.path.join(guest_dir, f"g{guest_id}_{run_id}_opt.mol")
    if os.path.exists(opt_file):
        stk_mol = stk_mol.with_structure_from_file(opt_file)
    else:
        opt = stko.ETKDG(random_seed=run_id * 25)
        stk_mol = opt.optimize(stk_mol)
        stk_mol.write(opt_file)

    return stk_mol
