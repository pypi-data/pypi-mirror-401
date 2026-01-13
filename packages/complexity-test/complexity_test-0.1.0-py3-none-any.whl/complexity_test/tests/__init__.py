"""
Test suite for Complexity Multicouche architecture.
"""

from complexity_test.tests.test_forward import test_forward_pass
from complexity_test.tests.test_backward import test_backward_pass
from complexity_test.tests.test_benchmark import test_speed_benchmark
from complexity_test.tests.test_cuda import test_cuda_compatibility
from complexity_test.tests.test_triton import test_triton_kernels

__all__ = [
    "test_forward_pass",
    "test_backward_pass",
    "test_speed_benchmark",
    "test_cuda_compatibility",
    "test_triton_kernels",
]
