from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="calign",
    version="1.0.0",
    author="André Luiz Caliari Costa, Leonardo Pereira de Araújo, Evandro Neves Silva, Patrícia Paiva Corsetti, Leonardo Augusto de Almeida",
    author_email="andre.costa@sou.unifal-mg.edu.br",
    description="A Python package for aligning epitopes to protein sequences",
    long_description_content_type="text/markdown",
    url="https://github.com/labiomol/Calign-development",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: proprietary software",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Private :: Do Not Upload",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "biopython>=1.79",
        "matplotlib>=3.3.0",
    ],
    keywords="bioinformatics epitope alignment protein sequence",
    project_urls={
        "Bug Reports": "https://github.com/labiomol/Calign-development/issues",
        "Source": "https://github.com/labiomol/Calign-development",
    },
    
)