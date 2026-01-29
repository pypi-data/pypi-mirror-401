import molellipsize as mes  # type: ignore[import-not-found]
from scipy.spatial import ConvexHull


class Ellipsize:
    """
    Uses Mol-Ellipsize [1]_ to calculare size properties.

    References
    ----------
    .. [1] https://github.com/andrewtarzia/mol-ellipsize/

    """

    @staticmethod
    def get_volume(stk_mol):
        mes_mol = mes.Molecule(stk_mol.to_rdkit_mol(), conformers=[0])
        conformer = stk_mol.to_rdkit_mol().GetConformer(0)
        box, sideLen, shape = mes_mol.get_molecule_shape(
            conformer=conformer,
            cid=0,
            boxmargin=4.0,
            vdwscale=0.9,
            spacing=0.5,
        )

        hit_points = mes_mol.get_hitpoints(shape)
        return ConvexHull(hit_points).volume

    @staticmethod
    def get_intermed(stk_mol):
        mes_mol = mes.Molecule(stk_mol.to_rdkit_mol(), conformers=[0])
        conf_ellipsoids = mes_mol.get_ellipsoids(1.0, 4.0, 0.5)
        diameters = conf_ellipsoids[0][1]
        return diameters[1]
