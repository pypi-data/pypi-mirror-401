# SRAD - Speckle Reducing Anisotropic Diffusion

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python implementation of the **Speckle Reducing Anisotropic Diffusion (SRAD)** algorithm for denoising images affected by speckle noise, commonly found in ultrasound, SAR (Synthetic Aperture Radar), and other coherent imaging systems.

![Example: Noisy vs Denoised](noisyImage.png)

---

## 📖 About

This package is a **Python port** of the original MATLAB implementation by [Xingorno](https://github.com/Xingorno/Speckle-Reducing-Anisotropic-Diffusion-SRAD). The SRAD algorithm is based on anisotropic diffusion, which smooths homogeneous regions while preserving edges — making it ideal for speckle reduction without blurring important structures.

### How It Works

SRAD extends the classic Perona-Malik anisotropic diffusion by incorporating a speckle-sensitive diffusion coefficient. The algorithm iteratively applies a diffusion process where:

- **Homogeneous regions** (high speckle) → Strong smoothing
- **Edge regions** (low speckle, high gradient) → Preserved

The mathematical model follows:

$$\frac{\partial I}{\partial t} = \text{div}[c(q) \nabla I]$$

Where $c(q)$ is the diffusion coefficient computed from the instantaneous coefficient of variation $q$.

---

## 🚀 Installation

### From PyPI

```bash
pip install srad
```

### From Source

```bash
git clone https://github.com/Keno-00/Speckle-Reducing-Anisotropic-Diffusion-SRAD.git
cd Speckle-Reducing-Anisotropic-Diffusion-SRAD
pip install .
```

---

## 💻 Usage

### As a Library

```python
import cv2
import srad

# Load your grayscale image
img = cv2.imread('path/to/image.png', cv2.IMREAD_GRAYSCALE)

# SRAD Parameters
iteration_max = 200    # Number of diffusion iterations
time_step = 0.05       # Time step per iteration (stability: keep ≤ 0.25)
decay_factor = 1       # Controls how fast edges are "locked in"

# Apply SRAD denoising
denoised = srad.SRAD(img, iteration_max, time_step, decay_factor)

# Save result
cv2.imwrite('denoised.png', denoised)
```

### Command Line

Run the built-in example on `noisyImage.png`:

```bash
python -m srad
```

---

## ⚙️ Parameters

| Parameter | Type | Description | Recommended |
|-----------|------|-------------|-------------|
| `iterationMaxStep` | int | Maximum number of diffusion iterations | 100-300 |
| `timeSize` | float | Time step size (affects stability and speed) | 0.05-0.15 |
| `decayFactor` | float | Exponential decay for the diffusion coefficient | 1.0 |

**Tips:**
- Higher `iterationMaxStep` → More smoothing, longer runtime
- Larger `timeSize` → Faster convergence, but may become unstable if > 0.25
- Higher `decayFactor` → Edges lock in faster

---

## 📁 Repository Structure

```
.
├── srad/                    # Python package
│   ├── __init__.py          # SRAD algorithm implementation
│   └── __main__.py          # CLI entry point
├── SpeckleReducingAD.m      # Original MATLAB implementation (general)
├── SpeckleReducingAD_New.m  # Original MATLAB implementation (optimized)
├── testSRAD.m               # MATLAB test script
├── noisyImage.png           # Example input image
├── denoised.png             # Example output image
├── setup.py                 # Package configuration
├── pyproject.toml           # Build system configuration
├── LICENSE                  # MIT License
└── README.md                # This file
```

---

## 📚 References

This implementation is based on the following papers:

1. **Yu, Y., & Acton, S. T. (2002).** *Speckle reducing anisotropic diffusion.* IEEE Transactions on Image Processing, 11(11), 1260-1270.  
   📄 [IEEE Xplore](https://ieeexplore.ieee.org/document/1097762)

2. **Perona, P., & Malik, J. (1990).** *Scale-space and edge detection using anisotropic diffusion.* IEEE Transactions on Pattern Analysis and Machine Intelligence, 12(7), 629-639.  
   📄 [IEEE Xplore](https://ieeexplore.ieee.org/document/56205)

---

## 🙏 Acknowledgments

- **Original MATLAB Implementation:** [Xingorno](https://github.com/Xingorno/Speckle-Reducing-Anisotropic-Diffusion-SRAD)  
- **Python Port:** [Keno S. Jose](https://github.com/Keno-00) (this contribution)
- **Initial Python Contribution:** [namioj](https://github.com/Xingorno/Speckle-Reducing-Anisotropic-Diffusion-SRAD/issues/1#issuecomment-1023787900)

This project is a fork of the original repository, ported to Python for easier integration into image processing pipelines.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The original MATLAB implementation by Xingorno is also under the MIT License.
