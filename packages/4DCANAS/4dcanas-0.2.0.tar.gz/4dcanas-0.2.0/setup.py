from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="4DCANAS",
    version="0.2.0",
    author="MERO",
    author_email="mero@ps.com",
    description="Advanced 4D Visualization and Simulation Suite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/6x-u/4DCANAS",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Multimedia :: Graphics :: 3D Graphics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0,<2.0.0",
        "scipy>=1.7.0,<2.0.0",
        "matplotlib>=3.4.0",
        "PyOpenGL>=3.1.5",
        "PyQt5>=5.15.0",
        "pillow>=8.3.0",
        "scikit-learn>=0.24.0",
        "psutil>=5.8.0",
        "sympy>=1.9",
        "numba>=0.55.0",
        "pandas>=1.3.0",
        "plotly>=5.0.0",
        "opencv-python>=4.5.0",
        "networkx>=2.6",
        "pyyaml>=5.4",
        "tqdm>=4.62.0",
        "g4f>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "viz": [
            "pythreejs>=2.3.0",
            "jupyter>=1.0.0",
            "ipywidgets>=7.6.0",
        ],
        "torch": [
            "torch>=1.9.0",
            "torchvision>=0.10.0",
        ],
        "tensorflow": [
            "tensorflow>=2.6.0",
        ],
        "all": [
            "4DCANAS[torch,tensorflow,viz,dev]"
        ],
    },
    entry_points={
        "console_scripts": [
            "4dcanas=4DCANAS.cli:main",
        ],
    },
)
