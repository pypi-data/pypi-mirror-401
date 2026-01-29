"""
SpatialMath-Lite - Lightweight Spatial Mathematics Library
"""

from .core import (
    num_to_cube, cube_to_num,
    batch_num_to_cube,
    instr_to_cube, cube_to_instr,
    clear_dim_cache, get_cache_stats,
    INSTRUCTION_LEVELS
)
from .operations import (
    cube_add, cube_multiply,
    cube_merge, cube_transform
)

__version__ = "1.3.0"
__author__ = "Hh"
__email__ = "ZM7x9@outlook.com"
__license__ = "MIT"

__all__ = [
    'num_to_cube',
    'cube_to_num',
    'batch_num_to_cube',
    'instr_to_cube',
    'cube_to_instr',
    'cube_add',
    'cube_multiply',
    'cube_merge',
    'cube_transform',
    'clear_dim_cache',
    'get_cache_stats',
    'INSTRUCTION_LEVELS',
    '__version__',
    '__author__',
    '__email__',
    '__license__'
]
