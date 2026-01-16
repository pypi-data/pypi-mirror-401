from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="srad",
    version="0.1.0",
    author="Keno S. Jose",
    author_email="",
    description="Speckle Reducing Anisotropic Diffusion - Python implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Keno-00/Speckle-Reducing-Anisotropic-Diffusion-SRAD",
    project_urls={
        "Original MATLAB Implementation": "https://github.com/Xingorno/Speckle-Reducing-Anisotropic-Diffusion-SRAD",
        "Bug Tracker": "https://github.com/Keno-00/Speckle-Reducing-Anisotropic-Diffusion-SRAD/issues",
    },
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    keywords="srad speckle denoising anisotropic diffusion ultrasound image-processing",
    python_requires=">=3.6",
)
