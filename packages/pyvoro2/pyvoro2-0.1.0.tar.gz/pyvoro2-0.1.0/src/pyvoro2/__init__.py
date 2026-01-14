"""pyvoro2 package.

This package provides Python bindings to the Voro++ cell-based Voronoi tessellation
library, plus optional extensions used by chemistry-oriented workflows.

Public API:
    - Box, PeriodicCell
    - PlaneFromRadii, PlaneMatrix, PlanePairs
    - compute
"""

from __future__ import annotations

from .domains import Box, PeriodicCell
from .planes import PlaneFromRadii, PlaneMatrix, PlanePairs
from .api import compute

__all__ = [
    'Box',
    'PeriodicCell',
    'PlaneFromRadii',
    'PlaneMatrix',
    'PlanePairs',
    'compute',
]
