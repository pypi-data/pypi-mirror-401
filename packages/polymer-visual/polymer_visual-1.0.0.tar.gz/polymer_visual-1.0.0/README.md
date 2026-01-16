# polymer-visual

<p align="center">
<img src="docs/figs/gyr_A.png" alt="gyroid A block" height="350"/>
<img src="docs/figs/gyr_comp.png" alt="gyroid all blocks" height="350"/> <br>
<font size="-1" align="center"><b>Fig. 1:</b> Density profiles generated with polymer-visual showing a double-gyroid morphology.</font>
</p>

A Python package for visualizing polymer self-assembly simulation data from [PSCF](https://pscf-home.cems.umn.edu/). This is a Python port of the original [MATLAB version](https://github.com/kdorfmanUMN/polymer_visual).

## Features

- **3D Isosurface Plots**: Visualize individual or composite density profiles
- **1D Line Profiles**: Plot composition along any direction through the unit cell
- **2D Contour Plots**: Generate contour maps on any plane
- **Scattering Profiles**: Predict scattering peak intensities
- **Interactive Visualization**: Using Plotly for interactive 3D graphics
- **Command-Line Interface**: Easy-to-use CLI for batch processing

## Installation

```bash
# Using pip
pip install polymer-visual

# Using poetry
poetry add polymer-visual
```

## Quick Start

### Command Line

```bash
# View file information
polymer-visual info examples/gyr.rf

# Generate all plots
polymer-visual plot examples/gyr.rf -o output/

# Generate specific plot types
polymer-visual plot examples/gyr.rf --composite --individual

# Generate a line profile
polymer-visual line examples/gyr.rf 1 1 1 --start 0 0 0
```

### Python API

```python
from polymer_visual import load_data, plot_all

# Load data from file
data = load_data('examples/gyr.rf')

# Generate all plots
figures = plot_all(data, output_dir='./output', show=True)

# Or use specific plot functions
from polymer_visual import plot_composite_profile, plot_individual_profiles

# Composite profile
plot_composite_profile(
    data['R'], data['x'], data['y'], data['z'],
    save_file='composite.html',
    show_fig=True
)

# Individual profiles for each species
plot_individual_profiles(
    data['R'], data['x'], data['y'], data['z'],
    save_file='individual.html',
    show_fig=True
)
```

## Supported File Formats

The package reads PSCF r-grid files (.rgrid, .rf) containing:
- Crystal system information
- Unit cell parameters
- Grid dimensions
- Volume fraction data for each monomer species

## Crystal Systems

Supported crystal systems include:
- Cubic, Tetragonal, Orthorhombic
- Hexagonal
- Triclinic, Monoclinic
- Trigonal/Rhombohedral
- 2D systems: Square, Rectangular, Oblique, Rhombic, Lamellar

## Documentation

For detailed documentation, see the [docs](docs/) directory.

## Development

```bash
# Clone the repository
git clone https://github.com/kdorfmanUMN/polymer_visual.git
cd polymer_visual

# Install development dependencies
poetry install

# Run tests
pytest

# Build package
poetry build
```

## License

This package is licensed under the MIT License. See LICENSE for details.

## Authors

- Original MATLAB code by Naveen Pillai, Akash Arora, Ben Magruder
- Python port by polymer-visual team

## References

For more information about the underlying science, see:
- [PSCF Software](https://pscf-home.cems.umn.edu/)
- [PSCF Publication](https://pubs.acs.org/doi/10.1021/acs.macromol.6b00107)
