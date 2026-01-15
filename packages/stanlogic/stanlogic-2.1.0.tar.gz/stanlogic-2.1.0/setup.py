from setuptools import setup, find_packages
import os

# Get the directory containing setup.py
here = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(here, "requirements.txt")

# Read requirements if file exists, otherwise use defaults
if os.path.exists(requirements_path):
    with open(requirements_path) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    # Default requirements if file not found
    requirements = ["matplotlib>=3.5.0", "numpy>=1.21.0"]

setup(
    name="StanLogic",
    version="2.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="Stan's Technologies",
    description="An advanced KMap solver and logic simplification engine",
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "web": ["Flask>=2.0", "Flask-Cors>=3.0"],
        "dev": ["pytest>=7.0.0", "pytest-cov>=3.0.0"],
    },
)
