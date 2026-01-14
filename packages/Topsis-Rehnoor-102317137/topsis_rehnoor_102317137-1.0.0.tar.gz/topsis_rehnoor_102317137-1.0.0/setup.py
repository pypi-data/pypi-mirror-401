from setuptools import setup, find_packages
import pathlib

#The directory containing this file
HERE= pathlib.Path(__file__).parent
#The text of the readme file
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="Topsis-Rehnoor-102317137",
    version="1.0.0",
    author="Rehnoor Aulakh",
    author_email="aulakhrehnoor@gmail.com",
    description="A Python package for TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) - Multi-Criteria Decision Making",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Rehnoor-Aulakh/Topsis-Rehnoor-102317137",
    packages=["Topsis"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    keywords="topsis, mcdm, multi-criteria decision making, decision analysis, ranking",
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    entry_points={
        "console_scripts": [
            "topsis=Topsis.__main__:main",
        ],
    },
)
