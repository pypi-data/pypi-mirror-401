"""
TPU-INL: Cross-Platform Integrator Neuron Layer Acceleration

Install with:
    pip install -e .

For CUDA acceleration:
    pip install -e ".[cuda]"

For TPU:
    pip install -e ".[tpu]"
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tpu-inl",
    version="0.2.1",
    author="Pacific Prime",
    author_email="contact@pacific-prime.ai",
    description="Cross-platform Integrator Neuron Layer acceleration for TPU, CUDA, AMD, Intel, DirectML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Web3-League/tpu-inl",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "cuda": [
            "triton>=2.0.0",
        ],
        "tpu": [
            "jax[tpu]>=0.4.0",
        ],
        "amd": [
            "triton>=2.0.0",  # Triton supports ROCm
        ],
        "intel": [
            "intel-extension-for-pytorch>=2.0.0",
        ],
        "directml": [
            "torch-directml>=0.2.0",
        ],
        "all": [
            "triton>=2.0.0",
            "jax>=0.4.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
        ],
    },
)
