# pyvoro2

Python bindings to **Voro++**, a fast, cell-based library for computing **3D Voronoi / Laguerre (radical) tessellations**.

In addition to classic Voronoi modes, **pyvoro2** adds an experimental **plane-positioning policy** (`mode='plane'`) that lets you shift the separating plane between points away from the midpoint (useful for “soft radii”, biased boundaries, and chemistry-oriented heuristics).

> Status: **alpha**. The API is intentionally small and may evolve until the first stable release.

---

## What is Voro++?

Voro++ is a C++ library designed for efficient *three-dimensional* Voronoi cell computations using a **cell-based** approach (compute each cell independently), which is particularly convenient for statistics over large particle systems and materials-science workflows.

pyvoro2 vendors Voro++ in `vendor/voro++`.

---

## Why not `pyvoro`?

`pyvoro` is a widely-used wrapper, but its last upstream PyPI release dates to **2014** and it has accumulated long-standing build/import issues across newer Python toolchains and platforms. If you need a modern, small, and easily hackable wrapper (especially on Windows) — or you want the **plane-positioning policies** — `pyvoro2` is meant to be that base.

If you only need 2D tessellation, `pyvoro` may still be a better fit (see below).

### Newer forks of `pyvoro`

The original `pyvoro` project has several community forks that focus on making installation easier and keeping the codebase usable on modern Python toolchains.
These forks can be a great option if you want the classic `pyvoro` API surface (including its 2D workflow).

`pyvoro2` exists for a different set of requirements:
- modern build tooling (pybind11 + scikit-build-core) and reliable Windows builds,
- explicit support for fully periodic triclinic unit cells,
- a new "plane" mode that allows shifting the separating plane between selected point pairs.

### Triclinic periodic cells (tilted unit cells)

`pyvoro2` supports fully periodic **triclinic** unit cells (tilted lattice vectors) via a coordinate transform.
This is convenient for crystal structures and any simulation cell with non-90° angles.

`pyvoro` focuses on simpler domain types and does not natively expose a triclinic periodic cell interface
(i.e., periodic boxes are typically orthorhombic / axis-aligned), so triclinic systems require workarounds.

---

## Installation

From source (recommended while the project is young):

```bash
pip install -e .
pytest -q
```

From PyPI:

```bash
pip install pyvoro2
```

You'll need a C++ compiler and CMake (scikit-build-core will drive the build).

---

## Quickstart

```python
import numpy as np
from pyvoro2 import Box, compute

pts = np.array([[0, 0, 0], [2, 0, 0]], dtype=float)
box = Box(bounds=((-5, 5), (-5, 5), (-5, 5)))

cells = compute(
    pts,
    domain=box,
    mode="standard",
    return_vertices=True,
    return_faces=True,
    return_adjacency=False,
)

print(cells[0].keys())
```

See the notebook: **`examples/pyvoro2_examples.ipynb`**.

---

## Modes

### Standard Voronoi (`mode='standard'`)
Classic Voronoi tessellation (midplanes between points).

### Radical / Laguerre (power diagram) (`mode='power'`)
Weighted Voronoi where each point has a "radius/weight" (`radii=`).

### Plane-fraction Voronoi (`mode='plane'`)
Like standard Voronoi, but the bisector plane between points *i* and *j* can be shifted.

For each pair *(i, j)* we use a plane fraction `t_ij`:
- `t_ij = 0.5` → classic midpoint plane
- `t_ij < 0.5` → plane moves toward **i**
- `t_ij > 0.5` → plane moves toward **j**

pyvoro2 supports three ways to specify `t_ij`:

1) **`PlaneFromRadii(radii)`**  
   A simple radii-based policy:
   `t_ij = R_i / (R_i + R_j)` (with a configurable fallback if `R_i + R_j == 0`).

2) **`PlaneMatrix(matrix)`**  
   Dense `n×n` matrix of pairwise fractions.

3) **`PlanePairs(pairs=[...], default=...)`**  
   Sparse overrides for selected pairs plus a global default.

---

## Output

`compute(...)` returns a list of per-point cell dictionaries. Depending on flags, a cell can include:
- `id`, `volume`
- `vertices` (optional)
- `faces` with `adjacent_cell` (optional)
- `adjacency` (optional)

The exact fields are demonstrated in the examples notebook.

---

## 2D tessellation support

pyvoro2 is **3D-only** (it wraps a 3D library).  
If you need 2D Voronoi tessellations, consider:
- `scipy.spatial.Voronoi` (2D/ND, not cell-based), or
- `pyvoro` (supports 2D and 3D).

---

## Future ideas

Some directions that fit naturally with Voro++ and could be added later:

- Additional Voro++ container types (e.g. polyhedral container variants).
- Wall primitives (plane/sphere/cylinder/cone) exposed in Python.
- Performance/ergonomics improvements for very large point sets (batching/streaming/parallel workflows).
- Optional geometry extras (face areas/normals, etc.) as needed by downstream projects.

---

## License

- **pyvoro2**: MIT (see `LICENSE.md`)
- Includes **Voro++** under its original license (see `vendor/voro++/LICENSE` and `THIRD_PARTY_NOTICES.md`)

---

## References

- Voro++: https://math.lbl.gov/voro++/
- pyvoro: https://github.com/joe-jordan/pyvoro
- pyvoro-mmalahe: https://github.com/mmalahe/pyvoro
- scipy.spatial.Voronoi: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html
