from setuptools import setup, find_packages

setup(
    name="bsm_calculator",
    version="0.1.0",  # Changed version to reflect Vectorized update
    description="High-performance Vectorized Black-Scholes-Merton Library",
    author="Alok Kumar Yadav",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",  # <--- Essential now
        "scipy"   # Essential for normal distribution functions
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)