from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="k-reg",
    version="2.0.0",
    author="Romain",
    description="High-performance non-linear K-Regressor (v19, predict=stream).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/romain/regression-k",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=[
        "numpy>=1.19.0",
        "scikit-learn>=0.24.0",
        "numba>=0.53.0"
    ],
    python_requires='>=3.7',
)