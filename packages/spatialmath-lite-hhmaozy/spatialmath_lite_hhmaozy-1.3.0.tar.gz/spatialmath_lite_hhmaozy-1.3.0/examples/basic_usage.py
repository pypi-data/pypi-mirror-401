"""
Basic usage examples for spatialmath-lite
"""
import numpy as np
import spatialmath_lite as sm


def example_basic_encoding():
    """Basic encoding and decoding examples"""
    print("=" * 60)
    print("BASIC ENCODING/DECODING EXAMPLES")
    print("=" * 60)

    # Example 1: Positive number
    num = 42
    cube = sm.num_to_cube(num, seed=123)
    decoded = sm.cube_to_num(cube)
    print(f"Example 1 - Positive number:")
    print(f"  Original: {num}")
    print(f"  Cube shape: {cube.shape}")
    print(f"  Number of ones: {np.sum(cube)}")
    print(f"  Decoded: {decoded}")
    print(f"  Success: {num == decoded}")

    # Example 2: Negative number
    num = -27
    cube = sm.num_to_cube(num, seed=456)
    decoded = sm.cube_to_num(cube)
    print(f"\\nExample 2 - Negative number:")
    print(f"  Original: {num}")
    print(f"  Cube shape: {cube.shape}")
    print(f"  Number of ones: {np.sum(cube)}")

    # Check center for negative numbers
    dim = cube.shape[0]
    center = (dim // 2, dim // 2, dim // 2)
    print(f"  Center cell ({center}): {cube[center]}")
    print(f"  Decoded: {decoded}")
    print(f"  Success: {num == decoded}")

    # Example 3: Zero
    num = 0
    cube = sm.num_to_cube(num)
    decoded = sm.cube_to_num(cube)
    print(f"\\nExample 3 - Zero:")
    print(f"  Original: {num}")
    print(f"  Cube shape: {cube.shape}")
    print(f"  Decoded: {decoded}")

    # Example 4: Fixed dimension
    num = 15
    cube = sm.num_to_cube(num, dim=4, seed=789)
    decoded = sm.cube_to_num(cube)
    print(f"\\nExample 4 - Fixed dimension (4x4x4):")
    print(f"  Original: {num}")
    print(f"  Cube shape: {cube.shape}")
    print(f"  Decoded: {decoded}")
    print(f"  Success: {num == decoded}")


def example_batch_operations():
    """Batch processing examples"""
    print("\\n" + "=" * 60)
    print("BATCH OPERATIONS")
    print("=" * 60)

    numbers = [-10, 0, 5, -3, 7, 12, -8, 100]
    cubes = sm.batch_num_to_cube(numbers, seed=789)

    print(f"Batch encoding {len(numbers)} numbers:")
    print(f"{'Index':<6} {'Original':<10} {'Shape':<12} {'Ones':<6} {'Decoded':<10} {'Status':<6}")
    print("-" * 60)

    for i, (num, cube) in enumerate(zip(numbers, cubes)):
        decoded = sm.cube_to_num(cube)
        ones = np.sum(cube)
        status = "✓" if num == decoded else "✗"
        print(f"{i:<6} {num:<10} {str(cube.shape):<12} {ones:<6} {decoded:<10} {status:<6}")

    # Show statistics
    total_ones = sum(np.sum(cube) for cube in cubes)
    avg_dim = np.mean([cube.shape[0] for cube in cubes])
    print(f"\\nStatistics:")
    print(f"  Total ones across all cubes: {total_ones}")
    print(f"  Average cube dimension: {avg_dim:.1f}")


def example_spatial_operations():
    """Spatial operations examples"""
    print("\\n" + "=" * 60)
    print("SPATIAL OPERATIONS")
    print("=" * 60)

    # Create test cubes
    cube1 = sm.num_to_cube(5, dim=3, seed=111)
    cube2 = sm.num_to_cube(3, dim=3, seed=222)
    cube3 = sm.num_to_cube(-4, dim=3, seed=333)

    print(f"Cube details:")
    print(f"  Cube1: {sm.cube_to_num(cube1)} ones, shape {cube1.shape}")
    print(f"  Cube2: {sm.cube_to_num(cube2)} ones, shape {cube2.shape}")
    print(f"  Cube3: {sm.cube_to_num(cube3)} ones, shape {cube3.shape}")

    # Addition
    result_add = sm.cube_add(cube1, cube2, seed=444)
    print(f"\\n1. Addition (5 + 3 = {sm.cube_to_num(result_add)}):")
    print(f"  Result shape: {result_add.shape}")
    print(f"  Result ones: {np.sum(result_add)}")

    # Addition with negative
    result_add_neg = sm.cube_add(cube1, cube3, seed=555)
    print(f"\\n2. Addition with negative (5 + (-4) = {sm.cube_to_num(result_add_neg)}):")
    print(f"  Result shape: {result_add_neg.shape}")
    print(f"  Result ones: {np.sum(result_add_neg)}")

    # Multiplication (intersection)
    result_mul = sm.cube_multiply(cube1, cube2)
    print(f"\\n3. Multiplication (intersection of 5 and 3):")
    print(f"  Intersection ones: {np.sum(result_mul)}")
    print(f"  Common cells: {np.sum(result_mul)} out of min(5,3)=3 possible")

    # Merge operations
    cubes = [cube1, cube2, cube3]
    result_union = sm.cube_merge(cubes, method='add', seed=666)
    result_intersect = sm.cube_merge(cubes, method='multiply')

    print(f"\\n4. Merge operations on 3 cubes:")
    print(f"  Union ones: {np.sum(result_union)}")
    print(f"  Intersection ones: {np.sum(result_intersect)}")

    # Show visual representation (2D slice)
    print(f"\\n5. Visual representation (middle slice of cube1):")
    middle_slice = cube1[1, :, :]  # Take middle slice in first dimension
    for row in middle_slice:
        row_str = ''.join('█' if cell else ' ' for cell in row)
        print(f"  |{row_str}|")


def example_instruction_system():
    """Instruction system examples"""
    print("\\n" + "=" * 60)
    print("INSTRUCTION SYSTEM")
    print("=" * 60)

    # Define an instruction set for a simple robot
    instruction_set = {
        "MOVE_FORWARD": (2, 3),
        "ROTATE_LEFT": (2, 5),
        "ROTATE_RIGHT": (2, 2),
        "STOP": (2, 1),
        "PICK_UP": (3, 7),
        "PUT_DOWN": (3, 4),
        "COMPLEX_TASK": (4, 10)
    }

    print("Instruction set for robot control:")
    for instr, (dim, ones) in instruction_set.items():
        print(f"  {instr:<15} -> dim={dim}, ones={ones}")

    # Encode an instruction
    instruction = "MOVE_FORWARD"
    cube = sm.instr_to_cube(instruction, level="low", seed=555)

    print(f"\\nEncoding instruction '{instruction}':")
    print(f"  Cube shape: {cube.shape}")
    print(f"  Cube ones: {np.sum(cube)}")

    # Decode it back
    decoded = sm.cube_to_instr(cube, instruction_set)
    print(f"  Decoded: {decoded}")
    print(f"  Success: {instruction == decoded}")

    # Test encoding multiple instructions
    print(f"\\nEncoding multiple instructions:")
    instructions = ["ROTATE_LEFT", "STOP", "PICK_UP"]
    for instr in instructions:
        cube = sm.instr_to_cube(instr, level="low" if instr in ["ROTATE_LEFT", "STOP"] else "mid", seed=777)
        decoded = sm.cube_to_instr(cube, instruction_set)
        status = "✓" if instr == decoded else "✗"
        print(f"  {instr:<15} -> {decoded:<15} {status}")

    # Show what happens with unknown instruction
    unknown_cube = sm.num_to_cube(99, dim=4, seed=888)
    decoded_unknown = sm.cube_to_instr(unknown_cube, instruction_set)
    print(f"\\nUnknown cube decoding:")
    print(f"  Cube ones: {np.sum(unknown_cube)}, dim: {unknown_cube.shape[0]}")
    print(f"  Decoded as: {decoded_unknown}")


def example_cache_management():
    """Cache management for edge devices"""
    print("\\n" + "=" * 60)
    print("CACHE MANAGEMENT (Edge Computing)")
    print("=" * 60)

    print("Simulating edge device processing sequence:")

    # Initial state
    stats = sm.get_cache_stats()
    print(f"\\n1. Initial state:")
    print(f"  Cache size: {stats['size']}")
    print(f"  Cache hits: {stats['hits']}")
    print(f"  Cache misses: {stats['misses']}")
    print(f"  Hit rate: {stats['hit_rate_pct']:.1f}%")

    # Process some numbers (populate cache)
    print(f"\\n2. Processing 10 numbers (populating cache):")
    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    for num in numbers:
        sm.num_to_cube(num, seed=num)

    # Check cache stats after population
    stats = sm.get_cache_stats()
    print(f"  After population:")
    print(f"    Cache size: {stats['size']}")
    print(f"    Cache misses: {stats['misses']}")
    print(f"    Hit rate: {stats['hit_rate_pct']:.1f}%")

    # Process same numbers again (cache hits)
    print(f"\\n3. Processing same numbers again (cache hits):")
    for num in numbers:
        sm.num_to_cube(num, seed=num)

    stats = sm.get_cache_stats()
    print(f"  After reprocessing:")
    print(f"    Cache hits: {stats['hits']}")
    print(f"    Hit rate: {stats['hit_rate_pct']:.1f}%")

    # Clear cache (critical for edge devices with limited memory)
    print(f"\\n4. Clearing cache (simulating memory cleanup):")
    sm.clear_dim_cache()

    stats = sm.get_cache_stats()
    print(f"  After clearing:")
    print(f"    Cache size: {stats['size']}")
    print(f"    Cache hits/misses: {stats['hits']}/{stats['misses']}")
    print(f"    Hit rate: {stats['hit_rate_pct']:.1f}%")

    # Verify functionality still works after cache clear
    cube = sm.num_to_cube(42, seed=123)
    decoded = sm.cube_to_num(cube)
    print(f"\\n5. Verification after cache clear:")
    print(f"  Encoded/decoded 42: {decoded == 42}")


# Run all examples
if __name__ == "__main__":
    print("SPATIALMATH-LITE - COMPLETE USAGE EXAMPLES")
    print("=" * 80)

    example_basic_encoding()
    example_batch_operations()
    example_spatial_operations()
    example_instruction_system()
    example_cache_management()

    print("\\n" + "=" * 80)
    print("All examples completed successfully!")