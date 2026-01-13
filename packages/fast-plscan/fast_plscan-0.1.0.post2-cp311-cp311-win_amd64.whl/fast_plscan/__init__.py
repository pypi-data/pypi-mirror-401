"""Public API for the plscan package."""


# start delvewheel patch
def _delvewheel_patch_1_11_2():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'fast_plscan.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_11_2()
del _delvewheel_patch_1_11_2
# end delvewheel patch

from .sklearn import PLSCAN
from .api import (
    clusters_from_spanning_forest,
    extract_mutual_spanning_forest,
    compute_mutual_spanning_tree,
    get_distance_callback,
)

__all__ = [
    "PLSCAN",
    "clusters_from_spanning_forest",
    "extract_mutual_spanning_forest",
    "compute_mutual_spanning_tree",
    "get_distance_callback",
]
