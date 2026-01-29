"""
Test core functionality of spatialmath-lite
"""
import numpy as np
import pytest
import spatialmath_lite as sm


def test_basic_encoding_decoding():
    """Test basic number to cube conversion"""
    # Test zero
    cube = sm.num_to_cube(0)
    assert cube.shape == (1, 1, 1)
    assert sm.cube_to_num(cube) == 0

    # Test positive numbers
    for n in [1, 5, 10, 27, 64]:
        cube = sm.num_to_cube(n, seed=42)
        assert sm.cube_to_num(cube) == n
        assert cube.dtype == np.uint8
        assert np.all(cube <= 1)  # Binary matrix

    # Test negative numbers
    for n in [-1, -5, -10, -27, -64]:
        cube = sm.num_to_cube(n, seed=42)
        assert sm.cube_to_num(cube) == n

        # Negative numbers should have center cell as 1
        dim = cube.shape[0]
        center = (dim // 2, dim // 2, dim // 2)
        assert cube[center] == 1


def test_negative_encoding():
    """Test optimized negative number encoding"""
    test_cases = [-1, -8, -27, -64, -100, -500, -1000]

    for n in test_cases:
        cube = sm.num_to_cube(n, seed=123)
        decoded = sm.cube_to_num(cube)

        assert decoded == n, f"Failed for {n}: got {decoded}"

        dim = cube.shape[0]
        center = (dim // 2, dim // 2, dim // 2)
        assert cube[center] == 1, f"Center not set for {n}"


def test_dimension_calculation():
    """Test automatic dimension calculation"""
    test_cases = [
        (0, 1),
        (1, 1),
        (7, 2),
        (8, 2),
        (9, 3),
        (26, 3),
        (27, 3),
        (28, 4),
        (100, 5),
        (1000, 10),
        (1331, 11),
    ]

    for num, expected_dim in test_cases:
        cube = sm.num_to_cube(num, seed=42)
        assert cube.shape[0] == expected_dim, f"Failed for {num}: expected dim {expected_dim}, got {cube.shape[0]}"


def test_fixed_dimension():
    """Test fixed dimension parameter"""
    # Test with fixed dimension
    cube = sm.num_to_cube(5, dim=3, seed=42)
    assert cube.shape == (3, 3, 3)
    assert sm.cube_to_num(cube) == 5

    # Test with dimension too small
    cube = sm.num_to_cube(10, dim=2, seed=42)  # 2³=8 < 10
    assert cube.shape == (2, 2, 2)
    assert sm.cube_to_num(cube) == 8  # Limited by capacity


def test_batch_operations():
    """Test batch conversion"""
    numbers = [-5, 0, 3, -10, 7, 100, -27]
    cubes = sm.batch_num_to_cube(numbers, seed=42)

    assert len(cubes) == len(numbers)

    for i, (num, cube) in enumerate(zip(numbers, cubes)):
        decoded = sm.cube_to_num(cube)
        assert decoded == num, f"Failed at index {i}: {num} -> {decoded}"


def test_instruction_system():
    """Test instruction to cube mapping"""
    # Test basic instruction
    cube = sm.instr_to_cube("ADD", level="low", seed=42)
    assert cube.shape[0] == 2

    cube = sm.instr_to_cube("COMPLEX_OP", level="complex", seed=42)
    assert cube.shape[0] == 5

    # Test instruction set decoding
    instruction_set = {
        "ADD": (2, 3),
        "SUB": (2, 5),
        "MUL": (3, 7),
        "DIV": (3, 4),
    }

    # Test encoding and decoding
    for instr_name, (dim, ones) in instruction_set.items():
        cube = sm.num_to_cube(ones, dim=dim, seed=123)
        decoded = sm.cube_to_instr(cube, instruction_set)
        assert decoded == instr_name, f"Failed for {instr_name}: got {decoded}"

    # Test unknown instruction
    cube = sm.num_to_cube(99, dim=4, seed=42)
    decoded = sm.cube_to_instr(cube, instruction_set)
    assert decoded.startswith("UNKNOWN_")


def test_cache_management():
    """Test cache clearing functionality"""
    # Populate cache
    for i in range(1, 20):
        sm.num_to_cube(i * 10, seed=i)

    # Get initial stats
    stats_before = sm.get_cache_stats()
    assert stats_before['size'] > 0
    assert stats_before['misses'] > 0

    # Clear cache
    sm.clear_dim_cache()

    # Get stats after clearing
    stats_after = sm.get_cache_stats()
    assert stats_after['size'] == 0
    assert stats_after['hits'] == 0
    assert stats_after['misses'] == 0

    # Test that it still works
    cube = sm.num_to_cube(42, seed=123)
    assert sm.cube_to_num(cube) == 42


def test_cache_stats():
    """Test cache statistics"""
    sm.clear_dim_cache()
    stats = sm.get_cache_stats()

    assert stats['size'] == 0
    assert stats['hits'] == 0
    assert stats['misses'] == 0
    assert stats['hit_rate'] == 0.0
    assert stats['hit_rate_pct'] == 0.0

    # Process some numbers
    numbers = [10, 20, 30, 40, 50]
    for num in numbers:
        sm.num_to_cube(num, seed=num)

    # Process them again (should hit cache)
    for num in numbers:
        sm.num_to_cube(num, seed=num)

    stats = sm.get_cache_stats()
    assert stats['size'] > 0
    assert stats['hits'] > 0
    assert stats['misses'] > 0
    assert 0 <= stats['hit_rate'] <= 1
    assert 0 <= stats['hit_rate_pct'] <= 100


def test_input_validation():
    """Test input validation"""
    # Test invalid number type
    with pytest.raises(TypeError):
        sm.num_to_cube(3.14)  # Float

    with pytest.raises(TypeError):
        sm.num_to_cube("123")  # String

    # Test invalid dimension
    with pytest.raises(ValueError):
        sm.num_to_cube(5, dim=0)  # Zero dimension

    with pytest.raises(ValueError):
        sm.num_to_cube(5, dim=-1)  # Negative dimension

    with pytest.raises(ValueError):
        sm.num_to_cube(5, dim=101)  # Too large dimension

    # Test invalid cube input
    with pytest.raises(ValueError):
        sm.cube_to_num(np.array([1, 2, 3]))  # 1D array

    with pytest.raises(ValueError):
        sm.cube_to_num(np.array([[1, 2], [3, 4]]))  # 2D array

    # Test invalid batch input
    with pytest.raises(TypeError):
        sm.batch_num_to_cube("not a list")

    with pytest.raises(TypeError):
        sm.batch_num_to_cube([1, 2.5, 3])  # Float in list


def test_edge_cases():
    """Test edge cases"""
    # Test very large number
    cube = sm.num_to_cube(1000000, seed=42)
    assert cube.shape[0] >= 100  # Should be at least 100x100x100

    # Test negative zero (should be same as zero)
    cube = sm.num_to_cube(-0, seed=42)
    assert sm.cube_to_num(cube) == 0

    # Test minimum dimension
    cube = sm.num_to_cube(1, dim=1, seed=42)
    assert cube.shape == (1, 1, 1)
    assert sm.cube_to_num(cube) == 1

    # Test empty batch
    cubes = sm.batch_num_to_cube([], seed=42)
    assert cubes == []


def test_random_consistency():
    """Test that random seeds produce consistent results"""
    # Same seed should produce same cube
    cube1 = sm.num_to_cube(42, seed=123)
    cube2 = sm.num_to_cube(42, seed=123)
    assert np.array_equal(cube1, cube2)

    # Different seed should produce different cube
    cube3 = sm.num_to_cube(42, seed=456)
    assert not np.array_equal(cube1, cube3)

    # But all should decode to same number
    assert sm.cube_to_num(cube1) == 42
    assert sm.cube_to_num(cube2) == 42
    assert sm.cube_to_num(cube3) == 42


def test_instruction_levels():
    """Test instruction levels"""
    assert sm.INSTRUCTION_LEVELS['low'] == 2
    assert sm.INSTRUCTION_LEVELS['mid'] == 3
    assert sm.INSTRUCTION_LEVELS['high'] == 4
    assert sm.INSTRUCTION_LEVELS['complex'] == 5

    # Test invalid level
    with pytest.raises(ValueError):
        sm.instr_to_cube("TEST", level="invalid")


def test_reusable_rng():
    """Test reusable random number generator"""
    import numpy as np

    rng = np.random.default_rng(42)

    # Use same RNG for multiple conversions
    cube1 = sm.num_to_cube(10, rng=rng)
    cube2 = sm.num_to_cube(20, rng=rng)

    # Should both be valid
    assert sm.cube_to_num(cube1) == 10
    assert sm.cube_to_num(cube2) == 20


if __name__ == "__main__":
    # Run all tests
    test_basic_encoding_decoding()
    test_negative_encoding()
    test_dimension_calculation()
    test_fixed_dimension()
    test_batch_operations()
    test_instruction_system()
    test_cache_management()
    test_cache_stats()
    test_input_validation()
    test_edge_cases()
    test_random_consistency()
    test_instruction_levels()
    test_reusable_rng()

    print("All core tests passed!")
