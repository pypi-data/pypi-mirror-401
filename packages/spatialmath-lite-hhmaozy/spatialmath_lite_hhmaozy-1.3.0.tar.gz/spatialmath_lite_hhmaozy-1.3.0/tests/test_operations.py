"""
Test spatial matrix operations
"""
import numpy as np
import pytest
import spatialmath_lite as sm


def test_cube_addition():
    """Test spatial matrix addition"""
    # Test basic addition
    cube1 = sm.num_to_cube(3, dim=3, seed=1)
    cube2 = sm.num_to_cube(2, dim=3, seed=2)
    result = sm.cube_add(cube1, cube2, seed=3)

    assert sm.cube_to_num(result) == 5
    assert result.shape == (3, 3, 3)

    # Test addition with negative numbers
    cube3 = sm.num_to_cube(-3, dim=3, seed=4)
    cube4 = sm.num_to_cube(2, dim=3, seed=5)
    result2 = sm.cube_add(cube3, cube4, seed=6)
    assert sm.cube_to_num(result2) == -1

    # Test addition of two negatives
    cube5 = sm.num_to_cube(-2, dim=3, seed=7)
    cube6 = sm.num_to_cube(-3, dim=3, seed=8)
    result3 = sm.cube_add(cube5, cube6, seed=9)
    assert sm.cube_to_num(result3) == -5

    # Test addition with zero
    cube_zero = sm.num_to_cube(0)
    result4 = sm.cube_add(cube1, cube_zero, seed=10)
    assert np.array_equal(result4, cube1)


def test_cube_multiplication():
    """Test spatial matrix multiplication (intersection)"""
    # Create overlapping cubes
    cube1 = sm.num_to_cube(5, dim=3, seed=1)
    cube2 = sm.num_to_cube(3, dim=3, seed=2)
    result = sm.cube_multiply(cube1, cube2)

    # Intersection should have at most min(5, 3) = 3 ones
    result_ones = np.sum(result)
    assert result_ones <= 3
    assert result.shape == (3, 3, 3)

    # Test with different dimensions
    cube3 = sm.num_to_cube(5, dim=4, seed=3)
    cube4 = sm.num_to_cube(3, dim=3, seed=4)
    result2 = sm.cube_multiply(cube3, cube4)

    # Should use smaller dimension (3)
    assert result2.shape[0] == 3

    # Test multiplication with negative numbers
    cube5 = sm.num_to_cube(-4, dim=3, seed=5)
    cube6 = sm.num_to_cube(2, dim=3, seed=6)
    result3 = sm.cube_multiply(cube5, cube6)

    # Center should be 1 if both have center as 1
    center = (1, 1, 1)
    if cube5[center] == 1 and cube6[center] == 1:
        assert result3[center] == 1


def test_cube_merge():
    """Test merging multiple cubes"""
    cubes = [
        sm.num_to_cube(2, dim=3, seed=1),
        sm.num_to_cube(3, dim=3, seed=2),
        sm.num_to_cube(1, dim=3, seed=3)
    ]

    # Test union (add)
    union_result = sm.cube_merge(cubes, method='add', seed=4)
    union_ones = np.sum(union_result)
    assert union_ones <= 6  # At most 2+3+1=6
    assert union_result.shape == (3, 3, 3)

    # Test intersection (multiply)
    intersect_result = sm.cube_merge(cubes, method='multiply')
    intersect_ones = np.sum(intersect_result)
    assert intersect_ones <= 1  # At most min(2,3,1)=1

    # Test with single cube
    single_result = sm.cube_merge([cubes[0]], method='add')
    assert np.array_equal(single_result, cubes[0])

    # Test with empty list
    empty_result = sm.cube_merge([], method='add')
    assert empty_result.shape == (1, 1, 1)
    assert np.sum(empty_result) == 0


def test_cube_transform():
    """Test cube transformations"""
    # Create a test cube
    cube = sm.num_to_cube(5, dim=3, seed=42)
    original_ones = np.sum(cube)

    # Test rotation around X axis
    rotated_x = sm.cube_transform(cube, operation='rotate', axis='x', angle=np.pi / 2)
    assert rotated_x.shape == cube.shape
    assert np.sum(rotated_x) == original_ones

    # Test rotation around Y axis
    rotated_y = sm.cube_transform(cube, operation='rotate', axis='y', angle=np.pi)
    assert rotated_y.shape == cube.shape
    assert np.sum(rotated_y) == original_ones

    # Test rotation around Z axis
    rotated_z = sm.cube_transform(cube, operation='rotate', axis='z', angle=3 * np.pi / 2)
    assert rotated_z.shape == cube.shape
    assert np.sum(rotated_z) == original_ones

    # Test full rotation (360 degrees)
    full_rotate = sm.cube_transform(cube, operation='rotate', angle=2 * np.pi)
    assert np.array_equal(full_rotate, cube)

    # Test flipping
    flipped_x = sm.cube_transform(cube, operation='flip', axis='x')
    assert flipped_x.shape == cube.shape
    assert np.sum(flipped_x) == original_ones

    flipped_y = sm.cube_transform(cube, operation='flip', axis='y')
    assert flipped_y.shape == cube.shape
    assert np.sum(flipped_y) == original_ones

    flipped_z = sm.cube_transform(cube, operation='flip', axis='z')
    assert flipped_z.shape == cube.shape
    assert np.sum(flipped_z) == original_ones

    # Test identity transform
    identity = sm.cube_transform(cube, operation='rotate', angle=0)
    assert np.array_equal(identity, cube)


def test_fast_path_addition():
    """Test fast path for small dimension addition"""
    # Small dimension cubes (fast path)
    cube1 = sm.num_to_cube(2, dim=2, seed=1)
    cube2 = sm.num_to_cube(1, dim=2, seed=2)

    result = sm.cube_add(cube1, cube2, seed=3)

    total_ones = np.sum(result)
    assert total_ones <= 3  # 2+1=3
    assert result.shape[0] == 2

    # Test that fast path preserves shape
    assert result.shape == cube1.shape == cube2.shape

    # Test with maximum capacity
    cube3 = sm.num_to_cube(4, dim=2, seed=4)  # 2³=4, full cube
    cube4 = sm.num_to_cube(3, dim=2, seed=5)
    result2 = sm.cube_add(cube3, cube4, seed=6)
    assert result2.shape[0] == 2


def test_edge_cases_operations():
    """Test edge cases for operations"""
    # Test with zero cubes
    cube_zero = sm.num_to_cube(0)
    cube_five = sm.num_to_cube(5, dim=3, seed=42)

    result = sm.cube_add(cube_zero, cube_five, seed=123)
    assert sm.cube_to_num(result) == 5

    # Test with same cube
    result2 = sm.cube_add(cube_five, cube_five, seed=456)
    assert sm.cube_to_num(result2) == 10

    # Test multiplication with zero
    result3 = sm.cube_multiply(cube_zero, cube_five)
    assert np.sum(result3) == 0

    # Test merge with mixed dimensions
    cubes_mixed = [
        sm.num_to_cube(3, dim=2, seed=1),
        sm.num_to_cube(5, dim=3, seed=2),
        sm.num_to_cube(2, dim=4, seed=3)
    ]

    merged = sm.cube_merge(cubes_mixed, method='add', seed=4)
    assert merged.shape[0] >= 2  # Should handle different dimensions


def test_input_validation_operations():
    """Test input validation for operations"""
    cube = sm.num_to_cube(5, dim=3, seed=42)

    # Test invalid cube dimensions
    with pytest.raises(ValueError):
        sm.cube_add(np.array([1, 2, 3]), cube)  # 1D array

    with pytest.raises(ValueError):
        sm.cube_add(cube, np.array([[1, 2], [3, 4]]))  # 2D array

    # Test invalid merge method
    with pytest.raises(ValueError):
        sm.cube_merge([cube], method='invalid_method')

    # Test invalid cube list
    with pytest.raises(TypeError):
        sm.cube_merge("not a list", method='add')

    # Test invalid transform parameters
    with pytest.raises(ValueError):
        sm.cube_transform(cube, operation='invalid_op')

    with pytest.raises(ValueError):
        sm.cube_transform(cube, operation='rotate', axis='invalid_axis')

    with pytest.raises(TypeError):
        sm.cube_transform(cube, operation='rotate', angle='not_a_number')


def test_operation_properties():
    """Test mathematical properties of operations"""
    cube_a = sm.num_to_cube(3, dim=3, seed=1)
    cube_b = sm.num_to_cube(4, dim=3, seed=2)
    cube_c = sm.num_to_cube(2, dim=3, seed=3)

    # Test commutativity of addition (approximately, due to randomness)
    result1 = sm.cube_add(cube_a, cube_b, seed=4)
    result2 = sm.cube_add(cube_b, cube_a, seed=4)  # Same seed
    assert sm.cube_to_num(result1) == sm.cube_to_num(result2)

    # Test commutativity of multiplication
    result3 = sm.cube_multiply(cube_a, cube_b)
    result4 = sm.cube_multiply(cube_b, cube_a)
    assert np.array_equal(result3, result4)

    # Test associativity of merge (add)
    merge1 = sm.cube_merge([cube_a, cube_b, cube_c], method='add', seed=5)
    merge2 = sm.cube_merge([cube_a, sm.cube_merge([cube_b, cube_c], method='add', seed=6)], method='add', seed=5)
    assert sm.cube_to_num(merge1) == sm.cube_to_num(merge2)


def test_performance_optimizations():
    """Test performance optimizations"""
    # Test that small dimension addition uses fast path
    cube_small1 = sm.num_to_cube(2, dim=2, seed=1)
    cube_small2 = sm.num_to_cube(3, dim=2, seed=2)

    # This should use the fast path (dim <= 4 and same shape)
    result = sm.cube_add(cube_small1, cube_small2, seed=3)
    assert result.shape[0] == 2

    # Test that large dimension doesn't use fast path
    cube_large1 = sm.num_to_cube(10, dim=5, seed=4)
    cube_large2 = sm.num_to_cube(15, dim=5, seed=5)
    result2 = sm.cube_add(cube_large1, cube_large2, seed=6)
    assert result2.shape[0] == 5


def test_negative_center_preservation():
    """Test that negative numbers preserve center cell through operations"""
    # Create negative cubes
    cube_neg1 = sm.num_to_cube(-3, dim=3, seed=1)
    cube_neg2 = sm.num_to_cube(-2, dim=3, seed=2)

    # Addition of negatives should result in negative
    result_add = sm.cube_add(cube_neg1, cube_neg2, seed=3)
    assert sm.cube_to_num(result_add) == -5
    assert result_add[1, 1, 1] == 1  # Center should be 1

    # Multiplication of negatives
    result_mul = sm.cube_multiply(cube_neg1, cube_neg2)
    if cube_neg1[1, 1, 1] == 1 and cube_neg2[1, 1, 1] == 1:
        assert result_mul[1, 1, 1] == 1


def test_batch_operations_compatibility():
    """Test compatibility between batch and single operations"""
    numbers = [3, 5, 7]
    cubes_batch = sm.batch_num_to_cube(numbers, seed=42)

    # Compare with individual conversions
    for i, num in enumerate(numbers):
        cube_single = sm.num_to_cube(num, seed=42)
        assert sm.cube_to_num(cubes_batch[i]) == sm.cube_to_num(cube_single)


def test_transform_preserves_negativity():
    """Test that transformations preserve negative/positive nature"""
    cube_pos = sm.num_to_cube(4, dim=3, seed=1)
    cube_neg = sm.num_to_cube(-4, dim=3, seed=2)

    # Transform both
    rotated_pos = sm.cube_transform(cube_pos, operation='rotate', axis='x', angle=np.pi / 2)
    rotated_neg = sm.cube_transform(cube_neg, operation='rotate', axis='x', angle=np.pi / 2)

    # Should preserve positivity/negativity
    assert sm.cube_to_num(rotated_pos) > 0
    assert sm.cube_to_num(rotated_neg) < 0

    # Number of ones should be preserved
    assert np.sum(rotated_pos) == np.sum(cube_pos)
    assert np.sum(rotated_neg) == np.sum(cube_neg)


if __name__ == "__main__":
    # Run all tests
    test_cube_addition()
    test_cube_multiplication()
    test_cube_merge()
    test_cube_transform()
    test_fast_path_addition()
    test_edge_cases_operations()
    test_input_validation_operations()
    test_operation_properties()
    test_performance_optimizations()
    test_negative_center_preservation()
    test_batch_operations_compatibility()
    test_transform_preserves_negativity()

    print("All operations tests passed!")
