"""
Main API module for polymer-visual package.

This module provides a high-level API for all polymer visualization
functionality, allowing users to easily create various plots.
"""

from polymer_visual.readers.rgrid_reader import read_rgrid
from polymer_visual.plots.individual import (
    plot_individual_profiles,
    plot_single_isosurface
)
from polymer_visual.plots.composite import plot_composite_profile
from polymer_visual.plots.line import plot_line_profile, get_line_profile_data
from polymer_visual.plots.contour import plot_contour
from polymer_visual.plots.scattering import plot_scattering
from polymer_visual.utils.basis import get_basis
from polymer_visual.utils.colormaps import get_colormaps, get_default_colors
from polymer_visual.utils.isovalues import get_isovalues, get_max_compositions


__all__ = [
    'read_rgrid',
    'plot_individual_profiles',
    'plot_single_isosurface',
    'plot_composite_profile',
    'plot_line_profile',
    'get_line_profile_data',
    'plot_contour',
    'plot_scattering',
    'get_basis',
    'get_colormaps',
    'get_default_colors',
    'get_isovalues',
    'get_max_compositions',
]


def load_data(filename, field_id=0):
    """
    Load data from an r-grid file.
    
    Parameters
    ----------
    filename : str
        Path to the r-grid file
    field_id : int, optional
        Field index for FTS trajectory files
    
    Returns
    -------
    result : dict
        Dictionary containing:
        - 'R': composition data array
        - 'x', 'y', 'z': coordinate arrays
        - 'dim': system dimensionality
        - 'lattype': crystal system type
    """
    R, x, y, z, dim, lattype = read_rgrid(filename, field_id)
    return {
        'R': R,
        'x': x,
        'y': y,
        'z': z,
        'dim': dim,
        'lattype': lattype
    }


def plot_all(data, output_dir=None, show=True):
    """
    Generate all possible plots for a dataset.
    
    Parameters
    ----------
    data : dict
        Data dictionary from load_data()
    output_dir : str, optional
        Directory to save plots
    show : bool
        Whether to display figures
    
    Returns
    -------
    figures : dict
        Dictionary of figure objects
    """
    R = data['R']
    x = data['x']
    y = data['y']
    z = data['z']
    dim = data['dim']
    
    figures = {}
    
    if output_dir:
        individual_file = f"{output_dir}/individual_profile.html"
        composite_file = f"{output_dir}/composite_profile.html"
        line_file = f"{output_dir}/line_profile.html"
        contour_file = f"{output_dir}/contour.html"
        scattering_file = f"{output_dir}/scattering.html"
    else:
        individual_file = None
        composite_file = None
        line_file = None
        contour_file = None
        scattering_file = None
    
    try:
        figures['individual'] = plot_individual_profiles(
            R, x, y, z, dim=dim,
            save_file=individual_file,
            show_fig=show
        )
    except Exception as e:
        print(f"Error creating individual profiles: {e}")
    
    try:
        figures['composite'] = plot_composite_profile(
            R, x, y, z, dim=dim,
            save_file=composite_file,
            show_fig=show
        )
    except Exception as e:
        print(f"Error creating composite profile: {e}")
    
    try:
        figures['line'] = plot_line_profile(
            R, x, y, z,
            direction=[1, 1, 1],
            dim=dim,
            save_file=line_file,
            show_fig=show
        )
    except Exception as e:
        print(f"Error creating line profile: {e}")
    
    try:
        figures['contour'] = plot_contour(
            R, x, y, z,
            dim=dim,
            save_file=contour_file,
            show_fig=show
        )
    except Exception as e:
        print(f"Error creating contour plot: {e}")
    
    try:
        figures['scattering'] = plot_scattering(
            R, x, y, z,
            save_file=scattering_file,
            show_fig=show
        )
    except Exception as e:
        print(f"Error creating scattering plot: {e}")
    
    return figures
