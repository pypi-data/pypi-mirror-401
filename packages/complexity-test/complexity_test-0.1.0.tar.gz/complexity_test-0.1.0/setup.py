"""
Complexity Test - Test package for Multicouche architecture.
"""

from setuptools import setup, find_packages

setup(
    name="complexity-test",
    version="0.1.0",
    description="Test package for Complexity Multicouche architecture (KQV + INL + MLP)",
    author="Pacific Prime",
    author_email="contact@pacific-prime.ai",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
    ],
    extras_require={
        "triton": ["triton>=2.0.0"],
    },
    entry_points={
        "console_scripts": [
            "complexity-test=run_tests:main",
        ],
    },
)
