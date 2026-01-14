import numpy as np

from pyvoro2 import Box, PeriodicCell, PlaneFromRadii, PlanePairs, PlaneMatrix, compute


def test_box_standard_two_points_volume_partition():
    pts = np.array([[0.0, 0.0, 0.0],
                    [2.0, 0.0, 0.0]], dtype=float)
    box = Box(bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0)))
    cells = compute(pts, domain=box, mode='standard', return_adjacency=False, return_faces=False)
    vols = sorted([c['volume'] for c in cells])
    assert len(vols) == 2
    assert abs(sum(vols) - 1000.0) < 1e-6  # 10*10*10


def test_box_plane_default_matches_standard():
    pts = np.array([[0.0, 0.0, 0.0],
                    [2.0, 0.0, 0.0]], dtype=float)
    box = Box(bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0)))

    cells_std = compute(pts, domain=box, mode='standard', return_vertices=False, return_adjacency=False, return_faces=False)
    pairs = PlanePairs(pairs=[], default=0.5)
    cells_plane = compute(pts, domain=box, mode='plane', plane=pairs, return_vertices=False, return_adjacency=False, return_faces=False)

    v0 = sorted([c['volume'] for c in cells_std])
    v1 = sorted([c['volume'] for c in cells_plane])
    assert np.allclose(v0, v1)


def test_box_plane_from_radii_equal():
    pts = np.array([[0.0, 0.0, 0.0],
                    [2.0, 0.0, 0.0]], dtype=float)
    box = Box(bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0)))

    cells_std = compute(pts, domain=box, mode='standard', return_vertices=False, return_adjacency=False, return_faces=False)
    plane = PlaneFromRadii(radii=np.array([1.0, 1.0]))
    cells_plane = compute(pts, domain=box, mode='plane', plane=plane, return_vertices=False, return_adjacency=False, return_faces=False)

    v0 = sorted([c['volume'] for c in cells_std])
    v1 = sorted([c['volume'] for c in cells_plane])
    assert np.allclose(v0, v1)
