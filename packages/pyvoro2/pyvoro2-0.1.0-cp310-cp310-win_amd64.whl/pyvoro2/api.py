"""High-level API for computing Voronoi tessellations."""

from __future__ import annotations

from typing import Any, Sequence

import numpy as np

from . import _core
from .domains import Box, PeriodicCell
from .planes import PlaneFromRadii, PlaneMatrix, PlanePairs


def _remap_ids_inplace(cells: list[dict[str, Any]], ids_user: np.ndarray) -> None:
    """Remap internal IDs (0..n-1) to user IDs in-place."""
    for c in cells:
        pid = int(c.get('id', -1))
        if 0 <= pid < ids_user.size:
            c['id'] = int(ids_user[pid])

        faces = c.get('faces')
        if faces is None:
            continue

        for f in faces:
            adj = int(f.get('adjacent_cell', -999999))
            # In Voro++, negative neighbor IDs can encode walls; keep them unchanged.
            if 0 <= adj < ids_user.size:
                f['adjacent_cell'] = int(ids_user[adj])


def compute(
    points: Sequence[Sequence[float]] | np.ndarray,
    *,
    domain: Box | PeriodicCell,
    ids: Sequence[int] | None = None,
    block_size: float | None = None,
    blocks: tuple[int, int, int] | None = None,
    init_mem: int = 8,
    mode: str = 'standard',
    radii: Sequence[float] | np.ndarray | None = None,
    plane: PlaneFromRadii | PlaneMatrix | PlanePairs | None = None,
    return_vertices: bool = True,
    return_adjacency: bool = True,
    return_faces: bool = True,
) -> list[dict[str, Any]]:
    """Compute Voronoi tessellation cells.

    Notes:
        Internally, the C++ layer always uses point indices 0..n-1 as particle IDs
        (this is required for vector/matrix-based plane policies). If `ids` is provided,
        results are remapped back to those user IDs on return.

    Args:
        points: Point coordinates, shape (n, 3).
        domain: `Box` (0D bounded) or `PeriodicCell` (3D periodic).
        ids: Optional integer IDs returned in output. Defaults to `range(n)`.
        block_size: Approximate grid block size. If provided, `blocks` is derived.
        blocks: Explicit (nx, ny, nz) grid blocks. Overrides `block_size`.
        init_mem: Initial per-block particle memory in Voro++.
        mode: 'standard' (midplanes), 'power' (Voro++ radical Voronoi),
            or 'plane' (pairwise plane fractions).
        radii: Per-point radii for `mode='power'`.
        plane: Plane-fraction specification for `mode='plane'`.
        return_vertices: Include vertex coordinates.
        return_adjacency: Include vertex adjacency.
        return_faces: Include faces with adjacent cell IDs.

    Returns:
        List of cell dictionaries, one per point.

    Raises:
        ValueError: If inputs are inconsistent or an unknown mode is provided.
    """
    pts = np.asarray(points, dtype=np.float64)
    if pts.ndim != 2 or pts.shape[1] != 3:
        raise ValueError('points must have shape (n, 3)')
    n = int(pts.shape[0])

    # Internal IDs are always 0..n-1 for compatibility with array/matrix plane policies.
    ids_internal = np.arange(n, dtype=np.int32)

    ids_user: np.ndarray | None
    if ids is None:
        ids_user = None
    else:
        if len(ids) != n:
            raise ValueError('ids must have length n')
        ids_user = np.asarray(ids, dtype=np.int64)

    # Determine blocks
    if blocks is not None:
        nx, ny, nz = blocks
    else:
        if block_size is None:
            # Simple heuristic: 2.5 * mean spacing inferred from density.
            if isinstance(domain, Box):
                (xmin, xmax), (ymin, ymax), (zmin, zmax) = domain.bounds
                vol = (xmax - xmin) * (ymax - ymin) * (zmax - zmin)
                spacing = (vol / max(n, 1)) ** (1.0 / 3.0)
            else:
                bx, _bxy, by, _bxz, _byz, bz = domain.to_internal_params()
                vol = bx * by * bz
                spacing = (vol / max(n, 1)) ** (1.0 / 3.0)
            block_size = max(1e-6, 2.5 * spacing)

        if isinstance(domain, Box):
            (xmin, xmax), (ymin, ymax), (zmin, zmax) = domain.bounds
            nx = max(1, int((xmax - xmin) / block_size))
            ny = max(1, int((ymax - ymin) / block_size))
            nz = max(1, int((zmax - zmin) / block_size))
        else:
            bx, _bxy, by, _bxz, _byz, bz = domain.to_internal_params()
            nx = max(1, int(bx / block_size))
            ny = max(1, int(by / block_size))
            nz = max(1, int(bz / block_size))

    opts = (bool(return_vertices), bool(return_adjacency), bool(return_faces))

    if isinstance(domain, Box):
        bounds = domain.bounds

        if mode == 'standard':
            cells = _core.compute_box_standard(pts, ids_internal, bounds, (nx, ny, nz), init_mem, opts)

        elif mode == 'power':
            if radii is None:
                raise ValueError('radii is required for mode="power"')
            rr = np.asarray(radii, dtype=np.float64)
            if rr.shape != (n,):
                raise ValueError('radii must have shape (n,)')
            cells = _core.compute_box_power(pts, ids_internal, rr, bounds, (nx, ny, nz), init_mem, opts)

        elif mode == 'plane':
            if plane is None:
                raise ValueError('plane is required for mode="plane"')

            if isinstance(plane, PlaneFromRadii):
                rr = plane.as_array()
                if rr.shape != (n,):
                    raise ValueError('plane radii must have shape (n,)')
                cells = _core.compute_box_plane_from_radii(
                    pts, ids_internal, rr, float(plane.default), bounds, (nx, ny, nz), init_mem, opts
                )

            elif isinstance(plane, PlaneMatrix):
                t = plane.as_array()
                if t.shape != (n, n):
                    raise ValueError('plane matrix must have shape (n, n)')
                cells = _core.compute_box_plane_matrix(
                    pts, ids_internal, t, float(plane.default), bounds, (nx, ny, nz), init_mem, opts
                )

            elif isinstance(plane, PlanePairs):
                pairs = plane.as_tuples()
                if plane.index_mode == 'id':
                    if ids_user is None:
                        raise ValueError('PlanePairs(index_mode="id") requires ids=... to be provided')
                    inv = {int(ids_user[i]): int(i) for i in range(n)}
                    try:
                        pairs = [(inv[int(i)], inv[int(j)], float(tt)) for i, j, tt in pairs]
                    except KeyError as e:
                        raise ValueError(f'PlanePairs refers to unknown id: {e}') from e
                else:
                    pairs = [(int(i), int(j), float(tt)) for i, j, tt in pairs]

                cells = _core.compute_box_plane_pairs(
                    pts, ids_internal, pairs, float(plane.default), bounds, (nx, ny, nz), init_mem, opts
                )
            else:
                raise ValueError('unknown plane specification')

        else:
            raise ValueError(f'unknown mode: {mode}')

        if ids_user is not None:
            _remap_ids_inplace(cells, ids_user)
        return cells

    # Periodic cell: transform to internal coordinates for Voro++
    cell = domain
    bx, bxy, by, bxz, byz, bz = cell.to_internal_params()
    pts_i = cell.wrap_internal(cell.cart_to_internal(pts))

    if mode == 'standard':
        cells = _core.compute_periodic_standard(
            pts_i, ids_internal, (bx, bxy, by, bxz, byz, bz), (nx, ny, nz), init_mem, opts
        )

    elif mode == 'power':
        if radii is None:
            raise ValueError('radii is required for mode="power"')
        rr = np.asarray(radii, dtype=np.float64)
        if rr.shape != (n,):
            raise ValueError('radii must have shape (n,)')
        cells = _core.compute_periodic_power(
            pts_i, ids_internal, rr, (bx, bxy, by, bxz, byz, bz), (nx, ny, nz), init_mem, opts
        )

    elif mode == 'plane':
        if plane is None:
            raise ValueError('plane is required for mode="plane"')

        if isinstance(plane, PlaneFromRadii):
            rr = plane.as_array()
            if rr.shape != (n,):
                raise ValueError('plane radii must have shape (n,)')
            cells = _core.compute_periodic_plane_from_radii(
                pts_i,
                ids_internal,
                rr,
                float(plane.default),
                (bx, bxy, by, bxz, byz, bz),
                (nx, ny, nz),
                init_mem,
                opts,
            )

        elif isinstance(plane, PlaneMatrix):
            t = plane.as_array()
            if t.shape != (n, n):
                raise ValueError('plane matrix must have shape (n, n)')
            cells = _core.compute_periodic_plane_matrix(
                pts_i,
                ids_internal,
                t,
                float(plane.default),
                (bx, bxy, by, bxz, byz, bz),
                (nx, ny, nz),
                init_mem,
                opts,
            )

        elif isinstance(plane, PlanePairs):
            pairs = plane.as_tuples()
            if plane.index_mode == 'id':
                if ids_user is None:
                    raise ValueError('PlanePairs(index_mode="id") requires ids=... to be provided')
                inv = {int(ids_user[i]): int(i) for i in range(n)}
                try:
                    pairs = [(inv[int(i)], inv[int(j)], float(tt)) for i, j, tt in pairs]
                except KeyError as e:
                    raise ValueError(f'PlanePairs refers to unknown id: {e}') from e
            else:
                pairs = [(int(i), int(j), float(tt)) for i, j, tt in pairs]

            cells = _core.compute_periodic_plane_pairs(
                pts_i,
                ids_internal,
                pairs,
                float(plane.default),
                (bx, bxy, by, bxz, byz, bz),
                (nx, ny, nz),
                init_mem,
                opts,
            )
        else:
            raise ValueError('unknown plane specification')

    else:
        raise ValueError(f'unknown mode: {mode}')

    # Remap ids (and face neighbor ids) to user ids if requested
    if ids_user is not None:
        _remap_ids_inplace(cells, ids_user)

    # Transform vertices back to Cartesian if requested
    if return_vertices:
        for c in cells:
            verts = np.asarray(c.get('vertices', []), dtype=np.float64)
            if verts.size:
                c['vertices'] = cell.internal_to_cart(verts).tolist()

    return cells
