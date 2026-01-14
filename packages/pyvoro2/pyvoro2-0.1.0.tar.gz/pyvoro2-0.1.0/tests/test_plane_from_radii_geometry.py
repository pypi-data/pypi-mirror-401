import numpy as np

from pyvoro2 import Box, PlaneFromRadii, compute


def _polygon_area_3d(vertices):
    """Compute polygon area from ordered 3D vertices."""
    v = np.asarray(vertices, dtype=float)
    if v.shape[0] < 3:
        return 0.0
    area_vec = np.zeros(3, dtype=float)
    for i in range(v.shape[0]):
        area_vec += np.cross(v[i], v[(i + 1) % v.shape[0]])
    return 0.5 * float(np.linalg.norm(area_vec))


def _find_interface_face(cell, other_id):
    for f in cell.get('faces', []):
        if int(f.get('adjacent_cell', -999999)) == int(other_id):
            return f
    return None


def test_plane_from_radii_x_axis_volume_and_face_area():
    # Two points along +x, so interface is a YZ rectangle.
    pts = np.array([[0.0, 0.0, 0.0],
                    [2.0, 0.0, 0.0]], dtype=float)
    box = Box(bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0)))

    # t = 1/(1+3)=0.25 -> plane_x = 0 + 2*0.25 = 0.5
    plane = PlaneFromRadii(radii=[1.0, 3.0], default=0.5)

    cells = compute(
        pts, domain=box, mode='plane', plane=plane,
        return_vertices=True, return_faces=True, return_adjacency=False
    )

    c0 = {c['id']: c for c in cells}[0]
    c1 = {c['id']: c for c in cells}[1]

    cross_area = 10.0 * 10.0
    plane_x = 0.5
    v0_expected = (plane_x - (-5.0)) * cross_area  # 550
    v1_expected = (5.0 - plane_x) * cross_area     # 450

    assert np.isclose(c0['volume'], v0_expected, atol=1e-6)
    assert np.isclose(c1['volume'], v1_expected, atol=1e-6)

    iface = _find_interface_face(c0, 1)
    assert iface is not None
    verts = [c0['vertices'][i] for i in iface['vertices']]

    xs = np.array([v[0] for v in verts], dtype=float)
    assert np.allclose(xs, plane_x, atol=1e-7)

    area = _polygon_area_3d(verts)
    assert np.isclose(area, cross_area, atol=1e-6)


def test_plane_from_radii_y_axis_volume_and_face_area():
    # Two points along +y, so interface is an XZ rectangle.
    pts = np.array([[0.0, 0.0, 0.0],
                    [0.0, 2.0, 0.0]], dtype=float)
    box = Box(bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0)))

    # t = 1/(1+3)=0.25 -> plane_y = 0.5
    plane = PlaneFromRadii(radii=[1.0, 3.0], default=0.5)

    cells = compute(
        pts, domain=box, mode='plane', plane=plane,
        return_vertices=True, return_faces=True, return_adjacency=False
    )

    c0 = {c['id']: c for c in cells}[0]
    c1 = {c['id']: c for c in cells}[1]

    cross_area = 10.0 * 10.0
    plane_y = 0.5
    v0_expected = (plane_y - (-5.0)) * cross_area  # 550
    v1_expected = (5.0 - plane_y) * cross_area     # 450

    assert np.isclose(c0['volume'], v0_expected, atol=1e-6)
    assert np.isclose(c1['volume'], v1_expected, atol=1e-6)

    iface = _find_interface_face(c0, 1)
    assert iface is not None
    verts = [c0['vertices'][i] for i in iface['vertices']]

    ys = np.array([v[1] for v in verts], dtype=float)
    assert np.allclose(ys, plane_y, atol=1e-7)

    area = _polygon_area_3d(verts)
    assert np.isclose(area, cross_area, atol=1e-6)


def test_plane_from_radii_diagonal_plane_bisects_centered_cube():
    # For a centrally symmetric convex body (cube centered at origin),
    # any plane through the center bisects volume.
    box = Box(bounds=((-5.0, 5.0), (-5.0, 5.0), (-5.0, 5.0)))

    pts = np.array([[-1.0, -1.0, -1.0],
                    [ 1.0,  1.0,  1.0]], dtype=float)

    # Equal radii => t=0.5 => separating plane passes through midpoint (0,0,0).
    plane = PlaneFromRadii(radii=[1.0, 1.0], default=0.5)

    cells = compute(
        pts, domain=box, mode='plane', plane=plane,
        return_vertices=True, return_faces=True, return_adjacency=False
    )
    c0 = {c['id']: c for c in cells}[0]

    # Cube volume = 10^3 = 1000; bisected => 500 each
    assert np.isclose(cells[0]['volume'] + cells[1]['volume'], 1000.0, atol=1e-6)
    assert np.isclose(cells[0]['volume'], 500.0, atol=1e-6)
    assert np.isclose(cells[1]['volume'], 500.0, atol=1e-6)

    iface = _find_interface_face(c0, 1)
    assert iface is not None

    verts = np.asarray([c0['vertices'][i] for i in iface['vertices']], dtype=float)

    # For points [-1,-1,-1] and [1,1,1], normal is (2,2,2) ~ (1,1,1).
    # Plane at midpoint passes through origin => equation x + y + z = 0.
    s = verts[:, 0] + verts[:, 1] + verts[:, 2]
    assert np.allclose(s, 0.0, atol=1e-7)
