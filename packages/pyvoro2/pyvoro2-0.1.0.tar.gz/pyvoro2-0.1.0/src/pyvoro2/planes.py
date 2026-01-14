"""Plane-fraction specifications for `mode='plane'` tessellation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence

import numpy as np


@dataclass(frozen=True, slots=True)
class PlaneFromRadii:
    """Define pairwise plane fractions from per-point radii.

    For a pair (i, j), the plane fraction is:
        t_ij = R_i / (R_i + R_j)
    where R_i, R_j are radii for points i and j.

    Args:
        radii: Per-point radii, shape (n,).
        default: Used when (R_i + R_j) == 0.
    """

    radii: np.ndarray
    default: float = 0.5

    def as_array(self) -> np.ndarray:
        """Return radii as float64 array."""
        r = np.asarray(self.radii, dtype=np.float64)
        if r.ndim != 1:
            raise ValueError('radii must be 1D')
        return r


@dataclass(frozen=True, slots=True)
class PlaneMatrix:
    """Define pairwise plane fractions from a dense matrix.

    Args:
        fractions: Dense matrix T with shape (n, n) where T[i, j] is t_ij.
        default: Fallback when a value is missing (not used for dense).
        symmetrize: If True, enforce t_ji = 1 - t_ij.
        validate: If True, validate range [0, 1] and diagonal.
    """

    fractions: np.ndarray
    default: float = 0.5
    symmetrize: bool = True
    validate: bool = True

    def as_array(self) -> np.ndarray:
        """Return (possibly symmetrized) fractions as float64 array."""
        t = np.asarray(self.fractions, dtype=np.float64)
        if t.ndim != 2 or t.shape[0] != t.shape[1]:
            raise ValueError('fractions must have shape (n, n)')
        if self.symmetrize:
            t = 0.5 * (t + (1.0 - t.T))
        if self.validate:
            if not np.all(np.isfinite(t)):
                raise ValueError('fractions must be finite')
            if np.any(t < 0.0) or np.any(t > 1.0):
                raise ValueError('fractions must be in [0, 1]')
            # diagonal is unused; allow anything but keep it sensible
        return t


@dataclass(frozen=True, slots=True)
class PlanePairs:
    """Define pairwise plane fractions from sparse overrides.

    Args:
        pairs: Iterable of (i, j, t_ij) tuples. Indices or ids depending on `index_mode`.
        default: Default t for unspecified pairs.
        symmetric: If True, automatically add (j, i) = 1 - t.
        index_mode: 'index' uses 0..n-1 indices; 'id' uses provided ids.
        validate: If True, validate values are finite and in [0, 1].
    """

    pairs: Sequence[tuple[int, int, float]]
    default: float = 0.5
    symmetric: bool = True
    index_mode: Literal['index', 'id'] = 'index'
    validate: bool = True

    def as_tuples(self) -> list[tuple[int, int, float]]:
        """Return pairs as a list, expanding symmetry if requested."""
        out: list[tuple[int, int, float]] = []
        for i, j, t in self.pairs:
            tt = float(t)
            out.append((int(i), int(j), tt))
            if self.symmetric:
                out.append((int(j), int(i), 1.0 - tt))
        if self.validate:
            for i, j, t in out:
                if not np.isfinite(t) or t < 0.0 or t > 1.0:
                    raise ValueError('pair fractions must be finite and in [0, 1]')
        return out
