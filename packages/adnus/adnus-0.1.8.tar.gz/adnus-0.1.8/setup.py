# setup.py
from setuptools import setup, find_packages
import os

def get_version():
    """_version.py'den versiyon al"""
    version_file = os.path.join(os.path.dirname(__file__), 'src', 'adnus', '_version.py')
    try:
        with open(version_file, 'r') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    except FileNotFoundError:
        return "0.1.7"
    return "0.1.7"

setup(
    name="adnus",
    version=get_version(),
    description="A Python library for Advanced Number Systems (AdNuS), including Bicomplex, Neutrosophic, Hyperreal numbers, reals, Complex, Quaternion, Octonion, Sedenion, Pathion, Chingon, Routon, Voudon.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mehmet Keçeci",
    author_email="mkececi@yaani.com",
    maintainer="Mehmet Keçeci",
    maintainer_email="mkececi@yaani.com",
    url="https://github.com/WhiteSymmetry/adnus",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy>=2.3.3,<3.0.0",
        "hypercomplex>=0.3.4"
    ],
    extras_require={
        'dev': ["pytest>=8.4.2,<10.0.0"],
        'build': ["setuptools>=80.9.0,<85.0.0", "cython>=3.1.4,<4.0.0"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.11',
    license="MIT",
)
