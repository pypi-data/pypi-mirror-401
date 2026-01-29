"""
Spatial mathematics core - Optimized negative number support
"""

import numpy as np
from typing import Tuple, Optional, Dict, Any, List, Union
import numpy.typing as npt

# ============ Core utility functions ============
_dim_cache = {}
_cache_keys = []
_cache_hits = 0
_cache_misses = 0
_MAX_CACHE_SIZE = 100


def get_cache_stats() -> dict:
    """Get cache statistics"""
    total = _cache_hits + _cache_misses
    return {
        'size': len(_dim_cache),
        'hits': _cache_hits,
        'misses': _cache_misses,
        'hit_rate': _cache_hits / total if total > 0 else 0.0,
        'hit_rate_pct': round(_cache_hits / total * 100, 1) if total > 0 else 0.0,
        'max_size': _MAX_CACHE_SIZE
    }


def clear_dim_cache() -> None:
    """Clear dimension calculation cache"""
    global _dim_cache, _cache_keys, _cache_hits, _cache_misses
    _dim_cache.clear()
    _cache_keys.clear()
    _cache_hits = 0
    _cache_misses = 0


def _get_cube_dimension(num: int) -> int:
    """Fast dimension calculation: (n-1)³ ≤ |num| < n³"""
    global _cache_hits, _cache_misses

    abs_num = abs(num)

    if abs_num in _dim_cache:
        _cache_hits += 1
        return _dim_cache[abs_num]

    _cache_misses += 1

    # 预计算常见值，提高性能
    if abs_num == 0:
        result = 1
    elif abs_num == 1:
        result = 1
    elif abs_num <= 8:
        result = 2
    elif abs_num <= 27:
        result = 3
    elif abs_num <= 64:
        result = 4
    elif abs_num <= 125:
        result = 5
    elif abs_num <= 216:
        result = 6
    elif abs_num <= 343:
        result = 7
    elif abs_num <= 512:
        result = 8
    elif abs_num <= 729:
        result = 9
    elif abs_num <= 1000:
        result = 10
    else:
        # 对于大数，使用近似计算
        result = int(abs_num ** (1 / 3)) + 1

        # 调整到正确范围
        if (result - 1) ** 3 >= abs_num:
            result -= 1
        while result ** 3 < abs_num:
            result += 1

    # 缓存管理
    if abs_num not in _dim_cache:
        if len(_cache_keys) >= _MAX_CACHE_SIZE:
            oldest = _cache_keys.pop(0)
            del _dim_cache[oldest]

        _dim_cache[abs_num] = result
        _cache_keys.append(abs_num)

    return result


def _create_random_generator(seed: Optional[int] = None) -> np.random.Generator:
    """Create or reuse random number generator"""
    return np.random.default_rng(seed)


def _get_center_index(dim: int) -> Tuple[int, int, int]:
    """Get center coordinate"""
    c = dim // 2
    return (c, c, c)


def _validate_input(num: int, dim: Optional[int] = None) -> None:
    """Validate input parameters"""
    if not isinstance(num, int):
        raise TypeError(f"num must be an integer, got {type(num).__name__}")

    if dim is not None:
        if not isinstance(dim, int):
            raise TypeError(f"dim must be an integer, got {type(dim).__name__}")
        if dim < 1:
            raise ValueError(f"dim must be a positive integer, got {dim}")
        if dim > 100:  # 防止内存溢出
            raise ValueError(f"dim too large (max 100), got {dim}")


# ============ Main API functions ============
def num_to_cube(
        num: int,
        seed: Optional[int] = None,
        dim: Optional[int] = None,
        rng: Optional[np.random.Generator] = None
) -> npt.NDArray[np.uint8]:
    """
    Convert integer to 3D spatial matrix

    Args:
        num: Integer to convert (positive, negative, or zero)
        seed: Random seed for spatial structure
        dim: Fixed cube dimension (None for auto)
        rng: Reusable random generator

    Returns:
        n×n×n binary matrix (1 = active signal)

    Raises:
        TypeError: If num is not an integer
        ValueError: If dim is invalid
    """
    # 输入验证
    _validate_input(num, dim)

    is_negative = num < 0
    abs_num = abs(num)

    # 处理0的特殊情况
    if abs_num == 0:
        return np.zeros((1, 1, 1), dtype=np.uint8)

    # 确定维度
    target_dim = dim if dim is not None else _get_cube_dimension(abs_num)
    total_cells = target_dim ** 3
    num_ones_needed = min(abs_num, total_cells)

    # 创建随机数生成器
    random_gen = rng if rng is not None else _create_random_generator(seed)

    # 负数的特殊处理（中心点必须为1）
    if is_negative:
        center_idx = _get_center_index(target_dim)

        # 如果只需要一个1，直接放在中心
        if num_ones_needed == 1:
            cube = np.zeros((target_dim, target_dim, target_dim), dtype=np.uint8)
            cube[center_idx] = 1
            return cube

        # 计算中心点的1D索引
        center_1d = center_idx[0] * target_dim * target_dim + \
                    center_idx[1] * target_dim + \
                    center_idx[2]

        # 选择其他位置
        all_indices = np.arange(total_cells)
        other_indices = all_indices[all_indices != center_1d]
        num_others = min(num_ones_needed - 1, len(other_indices))

        if num_others > 0:
            chosen_others = random_gen.choice(other_indices, size=num_others, replace=False)
            chosen_indices = np.concatenate([[center_1d], chosen_others])
        else:
            chosen_indices = np.array([center_1d])
    else:
        # 正数的处理
        all_indices = np.arange(total_cells)
        chosen_indices = random_gen.choice(
            all_indices,
            size=min(num_ones_needed, len(all_indices)),
            replace=False
        )

    # 将1D索引转换为3D坐标
    d = chosen_indices // (target_dim * target_dim)
    h = (chosen_indices % (target_dim * target_dim)) // target_dim
    w = chosen_indices % target_dim

    # 创建矩阵
    cube = np.zeros((target_dim, target_dim, target_dim), dtype=np.uint8)
    cube[d, h, w] = 1

    return cube


def cube_to_num(cube: npt.NDArray[np.uint8]) -> int:
    """
    Convert spatial matrix back to integer

    Args:
        cube: Spatial matrix to decode

    Returns:
        Original integer (positive, negative, or zero)

    Raises:
        ValueError: If cube is not a valid 3D matrix
    """
    # 验证输入
    if not isinstance(cube, np.ndarray):
        raise TypeError(f"cube must be a numpy array, got {type(cube).__name__}")

    if cube.ndim != 3:
        raise ValueError(f"cube must be 3D, got {cube.ndim}D")

    if cube.shape[0] != cube.shape[1] or cube.shape[1] != cube.shape[2]:
        raise ValueError(f"cube must be cubic (n×n×n), got {cube.shape}")

    if cube.dtype != np.uint8:
        cube = cube.astype(np.uint8)

    dim = cube.shape[0]
    center_idx = (dim // 2, dim // 2, dim // 2)
    is_negative = cube[center_idx] == 1
    total_ones = int(np.sum(cube))

    return -total_ones if is_negative else total_ones


def batch_num_to_cube(
        numbers: List[int],
        seed: Optional[int] = None,
        dim: Optional[int] = None
) -> List[npt.NDArray[np.uint8]]:
    """
    Batch conversion of numbers to spatial matrices

    Args:
        numbers: List of integers to convert
        seed: Base random seed
        dim: Fixed dimension for all numbers (None for auto)

    Returns:
        List of spatial matrices

    Raises:
        TypeError: If numbers is not a list of integers
    """
    if not isinstance(numbers, list):
        raise TypeError(f"numbers must be a list, got {type(numbers).__name__}")

    if not numbers:
        return []

    # 验证所有数字都是整数
    for i, num in enumerate(numbers):
        if not isinstance(num, int):
            raise TypeError(f"numbers[{i}] must be an integer, got {type(num).__name__}")

    rng = _create_random_generator(seed)
    return [num_to_cube(num, dim=dim, rng=rng) for num in numbers]


# ============ Instruction system ============
INSTRUCTION_LEVELS = {
    'low': 2,
    'mid': 3,
    'high': 4,
    'complex': 5
}


def instr_to_cube(
        instruction: str,
        level: str = 'low',
        seed: Optional[int] = None,
        rng: Optional[np.random.Generator] = None
) -> npt.NDArray[np.uint8]:
    """
    Map text instruction to spatial matrix

    Args:
        instruction: Text instruction (e.g., "ADD", "SUB")
        level: Instruction level (low/mid/high/complex)
        seed: Random seed for spatial structure
        rng: Reusable random generator

    Returns:
        Spatial matrix representing the instruction

    Raises:
        ValueError: If level is invalid
    """
    if not isinstance(instruction, str):
        raise TypeError(f"instruction must be a string, got {type(instruction).__name__}")

    if level not in INSTRUCTION_LEVELS:
        valid_levels = ", ".join(INSTRUCTION_LEVELS.keys())
        raise ValueError(f"Invalid instruction level: {level}, options: {valid_levels}")

    target_dim = INSTRUCTION_LEVELS[level]
    max_capacity = target_dim ** 3

    # 使用哈希函数生成确定性的值
    hash_val = hash(instruction + str(seed if seed is not None else 0))
    num_ones = max(1, abs(hash_val) % (max_capacity // 2 + 1))

    return num_to_cube(num_ones, dim=target_dim, seed=seed, rng=rng)


def cube_to_instr(
        cube: npt.NDArray[np.uint8],
        instruction_set: Optional[Dict[str, Tuple[int, int]]] = None
) -> str:
    """
    Decode spatial matrix back to instruction

    Args:
        cube: Spatial matrix to decode
        instruction_set: Instruction mapping {name: (dimension, num_ones)}

    Returns:
        Matched instruction name or "UNKNOWN_dim_num"
    """
    if instruction_set is None:
        instruction_set = {}

    cube_dim = cube.shape[0]
    cube_ones = cube_to_num(cube)

    for instr_name, (instr_dim, instr_ones) in instruction_set.items():
        if instr_dim == cube_dim and instr_ones == cube_ones:
            return instr_name

    return f"UNKNOWN_{cube_dim}_{cube_ones}"


# ============ Public API exports ============
__all__ = [
    'num_to_cube',
    'cube_to_num',
    'batch_num_to_cube',
    'instr_to_cube',
    'cube_to_instr',
    'clear_dim_cache',
    'get_cache_stats',
    'INSTRUCTION_LEVELS'
]
