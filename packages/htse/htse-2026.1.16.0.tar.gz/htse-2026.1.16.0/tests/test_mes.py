import numpy as np
import stk

import htse


def test_mes_get_volume():
    bb = stk.BuildingBlock("NCCCN")
    volume = htse.Ellipsize.get_volume(bb)
    assert np.isclose(volume, 78.39583333333333)
