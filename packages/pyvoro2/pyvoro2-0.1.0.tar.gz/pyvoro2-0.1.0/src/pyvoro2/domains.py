"""Domain specifications for Voronoi tessellation.

pyvoro2 currently supports:
- Box: orthogonal bounding box (non-periodic, for 0D systems)
- PeriodicCell: fully periodic triclinic cell (3D crystals), implemented via
  a coordinate transform into Voro++'s lower-triangular representation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np


@dataclass(frozen=True, slots=True)
class Box:
    """Orthogonal bounding box domain.

    Args:
        bounds: Three (min, max) pairs for x, y, z.

    Raises:
        ValueError: If bounds are malformed or degenerate.
    """

    bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]

    def __post_init__(self) -> None:
        if len(self.bounds) != 3:
            raise ValueError('bounds must have length 3')
        for lo, hi in self.bounds:
            if not np.isfinite(lo) or not np.isfinite(hi):
                raise ValueError('bounds must be finite')
            if not hi > lo:
                raise ValueError('each bound must satisfy hi > lo')

    @classmethod
    def from_points(cls, points: np.ndarray, padding: float = 2.0) -> 'Box':
        """Create a box that encloses points with optional padding.

        Args:
            points: Array of shape (n, 3).
            padding: Padding added on each side, in the same units as points.

        Returns:
            Box: Bounding box.

        Raises:
            ValueError: If points shape is invalid.
        """
        pts = np.asarray(points, dtype=float)
        if pts.ndim != 2 or pts.shape[1] != 3:
            raise ValueError('points must have shape (n, 3)')
        mins = pts.min(axis=0) - padding
        maxs = pts.max(axis=0) + padding
        return cls(bounds=((float(mins[0]), float(maxs[0])),
                           (float(mins[1]), float(maxs[1])),
                           (float(mins[2]), float(maxs[2]))))


@dataclass(frozen=True, slots=True)
class PeriodicCell:
    """Fully periodic triclinic cell for 3D crystals.

    The user provides three lattice vectors in Cartesian coordinates. Internally,
    pyvoro2 converts them into the Voro++ periodic container representation:
        a = (bx, 0, 0)
        b = (bxy, by, 0)
        c = (bxz, byz, bz)

    and transforms points into that coordinate system before tessellation.

    Args:
        vectors: Three lattice vectors (a, b, c), each length-3.
        origin: Origin of the unit cell in Cartesian coordinates.

    Raises:
        ValueError: If vectors are malformed or degenerate.
    """

    vectors: tuple[tuple[float, float, float],
                   tuple[float, float, float],
                   tuple[float, float, float]]
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def __post_init__(self) -> None:
        vec = np.asarray(self.vectors, dtype=float)
        if vec.shape != (3, 3):
            raise ValueError('vectors must have shape (3, 3)')
        if np.linalg.det(vec) == 0:
            raise ValueError('cell vectors are degenerate (det == 0)')

    def _rotation_to_internal(self) -> np.ndarray:
        """Return the 3x3 rotation that maps Cartesian -> internal basis."""
        a, b, _c = np.asarray(self.vectors, dtype=float)
        e1 = a / np.linalg.norm(a)
        b_perp = b - np.dot(b, e1) * e1
        nb = np.linalg.norm(b_perp)
        if nb == 0:
            raise ValueError('vectors a and b are colinear')
        e2 = b_perp / nb
        e3 = np.cross(e1, e2)
        r = np.vstack([e1, e2, e3])
        return r

    def to_internal_params(self) -> tuple[float, float, float, float, float, float]:
        """Convert lattice vectors into Voro++ periodic cell parameters.

        Returns:
            Tuple of (bx, bxy, by, bxz, byz, bz).
        """
        r = self._rotation_to_internal()
        a, b, c = (r @ np.asarray(self.vectors, dtype=float).T).T
        bx = float(a[0])
        bxy = float(b[0])
        by = float(b[1])
        bxz = float(c[0])
        byz = float(c[1])
        bz = float(c[2])
        if bx <= 0 or by <= 0 or bz <= 0:
            raise ValueError('internal cell parameters must be positive (check handedness)')
        return bx, bxy, by, bxz, byz, bz

    def cart_to_internal(self, points: np.ndarray) -> np.ndarray:
        """Transform Cartesian points into the internal coordinate system."""
        r = self._rotation_to_internal()
        origin = np.asarray(self.origin, dtype=float)
        pts = np.asarray(points, dtype=float) - origin[None, :]
        return (r @ pts.T).T

    def internal_to_cart(self, points_internal: np.ndarray) -> np.ndarray:
        """Transform internal points back into Cartesian coordinates."""
        r = self._rotation_to_internal()
        origin = np.asarray(self.origin, dtype=float)
        pts = (r.T @ np.asarray(points_internal, dtype=float).T).T + origin[None, :]
        return pts

    def wrap_internal(self, points_internal: np.ndarray) -> np.ndarray:
        """Wrap internal coordinates into the primary cell.

        Note:
            This wraps only by bx/by/bz in the internal basis. This is consistent
            with Voro++'s periodic container representation.

        Returns:
            Wrapped coordinates, shape (n, 3).
        """
        bx, _bxy, by, _bxz, _byz, bz = self.to_internal_params()
        pts = np.asarray(points_internal, dtype=float).copy()
        pts[:, 0] = np.mod(pts[:, 0], bx)
        pts[:, 1] = np.mod(pts[:, 1], by)
        pts[:, 2] = np.mod(pts[:, 2], bz)
        return pts
