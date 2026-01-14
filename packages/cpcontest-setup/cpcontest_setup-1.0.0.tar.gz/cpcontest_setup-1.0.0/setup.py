"""
cpcontest-setup - Generador Universal de Concursos de Programación Competitiva modo Colombiano año 2026
Autor: josuerom
Fecha: 12/01/2026 21:46:07
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="cpcontest-setup",
    version="1.0.0",
    author="josuerom",
    author_email="josueromram3@gmail.com",
    description="Generador automático de estructuras para concursos de programación competitiva modo Colombiano año 2026",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/josuerom/cpcontest-setup",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.10",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "cpcontest=cpcontest.cli:main",
        ],
    },
    keywords="competitive-programming codeforces contests setup automation",
    project_urls={
        "Bug Reports": "https://github.com/josuerom/cpcontest-setup/issues",
        "Source": "https://github.com/josuerom/cpcontest-setup",
    },
)
