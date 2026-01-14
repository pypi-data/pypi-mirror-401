import numpy as np

from pyvoro2 import PeriodicCell, PlaneFromRadii, PlanePairs, compute


def test_periodic_standard_volume_conservation():
    # Simple cubic cell 10x10x10
    cell = PeriodicCell(vectors=((10.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 0.0, 10.0)))
    pts = np.array(
        [
            [1.0, 1.0, 1.0],
            [5.0, 5.0, 5.0],
            [8.0, 2.0, 7.0],
            [3.0, 9.0, 4.0],
        ],
        dtype=float,
    )
    cells = compute(pts, domain=cell, mode='standard', return_vertices=False, return_adjacency=False, return_faces=False)
    vol = sum([c['volume'] for c in cells])
    assert np.isclose(vol, 1000.0, atol=1e-6)


def test_periodic_plane_default_matches_standard():
    cell = PeriodicCell(vectors=((10.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 0.0, 10.0)))
    pts = np.array(
        [
            [1.0, 1.0, 1.0],
            [5.0, 5.0, 5.0],
            [8.0, 2.0, 7.0],
            [3.0, 9.0, 4.0],
        ],
        dtype=float,
    )
    cells_std = compute(pts, domain=cell, mode='standard', return_vertices=False, return_adjacency=False, return_faces=False)
    plane = PlanePairs(pairs=[], default=0.5)
    cells_plane = compute(pts, domain=cell, mode='plane', plane=plane, return_vertices=False, return_adjacency=False, return_faces=False)
    v0 = sorted([c['volume'] for c in cells_std])
    v1 = sorted([c['volume'] for c in cells_plane])
    assert np.allclose(v0, v1)


def test_periodic_plane_from_radii_equal_matches_standard():
    cell = PeriodicCell(vectors=((10.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 0.0, 10.0)))
    pts = np.array(
        [
            [1.0, 1.0, 1.0],
            [5.0, 5.0, 5.0],
            [8.0, 2.0, 7.0],
            [3.0, 9.0, 4.0],
        ],
        dtype=float,
    )
    cells_std = compute(pts, domain=cell, mode='standard', return_vertices=False, return_adjacency=False, return_faces=False)
    plane = PlaneFromRadii(radii=np.ones(len(pts), dtype=float))
    cells_plane = compute(pts, domain=cell, mode='plane', plane=plane, return_vertices=False, return_adjacency=False, return_faces=False)
    v0 = sorted([c['volume'] for c in cells_std])
    v1 = sorted([c['volume'] for c in cells_plane])
    assert np.allclose(v0, v1)
