import numpy as np

from pyvoro2 import Box, PlaneFromRadii, PlaneMatrix, PlanePairs, compute


def _two_point_box():
    pts = np.array(
        [
            [0.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    box = Box(bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0)))
    return pts, box


def test_plane_pairs_shifts_split_as_expected():
    pts, box = _two_point_box()

    # For points at x=0 and x=2, the separating plane is at x = 2*t.
    t = 0.25
    plane = PlanePairs(pairs=[(0, 1, t)], default=0.5, symmetric=True)

    cells = compute(
        pts,
        domain=box,
        mode='plane',
        plane=plane,
        return_vertices=False,
        return_adjacency=False,
        return_faces=False,
    )

    vols = {c['id']: c['volume'] for c in cells}
    # Box is 10 x 10 x 10. Area of y-z cross-section is 100.
    # xmin=-5, xmax=5, plane at x=0.5 -> left length 5.5, right length 4.5.
    assert np.isclose(vols[0], 550.0, atol=1e-6)
    assert np.isclose(vols[1], 450.0, atol=1e-6)


def test_plane_from_radii_matches_pairs_formula():
    pts, box = _two_point_box()

    # R=[1, 3] -> t = 1/(1+3) = 0.25
    plane_r = PlaneFromRadii(radii=np.array([1.0, 3.0]), default=0.5)
    cells_r = compute(
        pts,
        domain=box,
        mode='plane',
        plane=plane_r,
        return_vertices=False,
        return_adjacency=False,
        return_faces=False,
    )

    plane_p = PlanePairs(pairs=[(0, 1, 0.25)], default=0.5, symmetric=True)
    cells_p = compute(
        pts,
        domain=box,
        mode='plane',
        plane=plane_p,
        return_vertices=False,
        return_adjacency=False,
        return_faces=False,
    )

    v_r = sorted([c['volume'] for c in cells_r])
    v_p = sorted([c['volume'] for c in cells_p])
    assert np.allclose(v_r, v_p)


def test_plane_matrix_matches_pairs():
    pts, box = _two_point_box()
    t = 0.25
    m = np.array([[0.5, t], [1.0 - t, 0.5]], dtype=float)
    plane_m = PlaneMatrix(fractions=m, symmetrize=False, validate=True)
    cells_m = compute(
        pts,
        domain=box,
        mode='plane',
        plane=plane_m,
        return_vertices=False,
        return_adjacency=False,
        return_faces=False,
    )

    plane_p = PlanePairs(pairs=[(0, 1, t)], default=0.5, symmetric=True)
    cells_p = compute(
        pts,
        domain=box,
        mode='plane',
        plane=plane_p,
        return_vertices=False,
        return_adjacency=False,
        return_faces=False,
    )

    v_m = sorted([c['volume'] for c in cells_m])
    v_p = sorted([c['volume'] for c in cells_p])
    assert np.allclose(v_m, v_p)


def test_plane_pairs_id_mode():
    pts, box = _two_point_box()

    ids = [10, 20]
    plane = PlanePairs(pairs=[(10, 20, 0.25)], default=0.5, symmetric=True, index_mode='id')
    cells = compute(
        pts,
        domain=box,
        ids=ids,
        mode='plane',
        plane=plane,
        return_vertices=False,
        return_adjacency=False,
        return_faces=False,
    )
    vols = {c['id']: c['volume'] for c in cells}
    assert set(vols) == {10, 20}
    assert np.isclose(vols[10], 550.0, atol=1e-6)
    assert np.isclose(vols[20], 450.0, atol=1e-6)
