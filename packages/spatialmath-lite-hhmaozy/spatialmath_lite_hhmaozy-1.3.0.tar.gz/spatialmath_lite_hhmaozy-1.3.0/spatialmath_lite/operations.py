"""
Spatial matrix operations - Optimized negative support
"""

import numpy as np
from typing import Tuple, Optional, List, Any
import numpy.typing as npt
from .core import num_to_cube, cube_to_num, _validate_input


def _validate_cube(cube: npt.NDArray[np.uint8], name: str = "cube") -> None:
    """Validate cube input"""
    if not isinstance(cube, np.ndarray):
        raise TypeError(f"{name} must be a numpy array, got {type(cube).__name__}")

    if cube.ndim != 3:
        raise ValueError(f"{name} must be 3D, got {cube.ndim}D")

    if cube.shape[0] != cube.shape[1] or cube.shape[1] != cube.shape[2]:
        raise ValueError(f"{name} must be cubic (n×n×n), got {cube.shape}")


def cube_add(
        cube_a: npt.NDArray[np.uint8],
        cube_b: npt.NDArray[np.uint8],
        seed: Optional[int] = None,
        rng: Optional[np.random.Generator] = None
) -> npt.NDArray[np.uint8]:
    """
    Spatial matrix addition with optimization for small dimensions

    Args:
        cube_a, cube_b: Spatial matrices (can be negative)
        seed: Random seed for new positions
        rng: Reusable random generator

    Returns:
        Result of addition as spatial matrix

    Raises:
        ValueError: If inputs are not valid 3D matrices
    """
    # 输入验证
    _validate_cube(cube_a, "cube_a")
    _validate_cube(cube_b, "cube_b")

    # 快速路径：小维度且形状相同的情况
    if cube_a.shape == cube_b.shape and cube_a.shape[0] <= 4:
        combined = np.logical_or(cube_a, cube_b).astype(np.uint8)
        total_ones = np.sum(combined)

        max_capacity = cube_a.shape[0] ** 3
        if total_ones <= max_capacity:
            return combined

    # 通用路径：转换为数字再转换回来
    num_a = cube_to_num(cube_a)
    num_b = cube_to_num(cube_b)
    total = num_a + num_b

    return num_to_cube(total, seed=seed, rng=rng)


def cube_multiply(
        cube_a: npt.NDArray[np.uint8],
        cube_b: npt.NDArray[np.uint8]
) -> npt.NDArray[np.uint8]:
    """
    Spatial matrix multiplication (logical AND)

    Returns intersection of 1 positions

    Args:
        cube_a, cube_b: Spatial matrices to multiply

    Returns:
        Intersection matrix (1 where both have 1)

    Raises:
        ValueError: If inputs are not valid 3D matrices
    """
    # 输入验证
    _validate_cube(cube_a, "cube_a")
    _validate_cube(cube_b, "cube_b")

    dim_a, dim_b = cube_a.shape[0], cube_b.shape[0]

    # 相同维度的情况
    if dim_a == dim_b:
        return np.logical_and(cube_a, cube_b).astype(np.uint8)

    # 不同维度的情况：使用较小维度
    target_dim = min(dim_a, dim_b)

    def extract_center(cube: npt.NDArray[np.uint8], target_dim: int) -> npt.NDArray[np.uint8]:
        """Extract center region from cube"""
        dim = cube.shape[0]
        if dim == target_dim:
            return cube

        start = (dim - target_dim) // 2
        return cube[
               start:start + target_dim,
               start:start + target_dim,
               start:start + target_dim
               ]

    center_a = extract_center(cube_a, target_dim)
    center_b = extract_center(cube_b, target_dim)

    return np.logical_and(center_a, center_b).astype(np.uint8)


def cube_merge(
        cubes: List[npt.NDArray[np.uint8]],
        method: str = 'add',
        seed: Optional[int] = None,
        rng: Optional[np.random.Generator] = None
) -> npt.NDArray[np.uint8]:
    """
    Merge multiple spatial matrices

    Args:
        cubes: List of spatial matrices
        method: 'add' (union) or 'multiply' (intersection)
        seed: Random seed for addition
        rng: Reusable random generator

    Returns:
        Merged spatial matrix

    Raises:
        ValueError: If inputs are not valid or method is unknown
    """
    if not isinstance(cubes, list):
        raise TypeError(f"cubes must be a list, got {type(cubes).__name__}")

    if not cubes:
        return np.zeros((1, 1, 1), dtype=np.uint8)

    # 验证所有cube
    for i, cube in enumerate(cubes):
        _validate_cube(cube, f"cubes[{i}]")

    # 从第一个cube开始
    result = cubes[0].copy()

    # 合并其他cube
    for cube in cubes[1:]:
        if method == 'add':
            result = cube_add(result, cube, seed=seed, rng=rng)
        elif method == 'multiply':
            result = cube_multiply(result, cube)
        else:
            raise ValueError(f"Unknown merge method: {method}, use 'add' or 'multiply'")

    return result


def cube_transform(
        cube: npt.NDArray[np.uint8],
        operation: str = 'rotate',
        axis: str = 'x',
        angle: float = 0.0
) -> npt.NDArray[np.uint8]:
    """
    Transform spatial matrix (rotate or flip)

    Args:
        cube: Input spatial matrix
        operation: 'rotate' or 'flip'
        axis: 'x', 'y', or 'z'
        angle: Rotation angle in radians

    Returns:
        Transformed spatial matrix

    Raises:
        ValueError: If inputs are invalid
    """
    # 输入验证
    _validate_cube(cube, "cube")

    if operation not in ['rotate', 'flip']:
        raise ValueError(f"operation must be 'rotate' or 'flip', got {operation}")

    if axis not in ['x', 'y', 'z']:
        raise ValueError(f"axis must be 'x', 'y', or 'z', got {axis}")

    if not isinstance(angle, (int, float)):
        raise TypeError(f"angle must be a number, got {type(angle).__name__}")

    # 规范化角度
    angle = angle % (2 * np.pi)

    if operation == 'rotate':
        # 计算90度的倍数
        k = int(round(angle / (np.pi / 2))) % 4

        if axis == 'x':
            return np.rot90(cube, k=k, axes=(1, 2))
        elif axis == 'y':
            return np.rot90(cube, k=k, axes=(0, 2))
        elif axis == 'z':
            return np.rot90(cube, k=k, axes=(0, 1))

    elif operation == 'flip':
        if axis == 'x':
            return np.flip(cube, axis=0)
        elif axis == 'y':
            return np.flip(cube, axis=1)
        elif axis == 'z':
            return np.flip(cube, axis=2)

    # 理论上不会执行到这里
    return cube.copy()


# ============ Public API exports ============
__all__ = [
    'cube_add',
    'cube_multiply',
    'cube_merge',
    'cube_transform'
]
