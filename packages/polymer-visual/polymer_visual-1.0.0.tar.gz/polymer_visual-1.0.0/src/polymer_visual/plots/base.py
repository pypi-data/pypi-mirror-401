"""
Base plotting utilities and common functions for polymer visualization.
"""

import numpy as np


def get_mono_labels(n_species):
    """
    Generate default monomer labels (A, B, C, ...).
    
    Parameters
    ----------
    n_species : int
        Number of monomer species
    
    Returns
    -------
    labels : list
        List of string labels
    """
    return [chr(ord('A') + i) for i in range(n_species)]


def get_basis_from_coords(x, y, z):
    """
    Extract lattice basis vectors from coordinate arrays.
    
    Parameters
    ----------
    x, y, z : ndarray
        3D coordinate arrays
    
    Returns
    -------
    basis : ndarray
        3x3 array of basis vectors
    """
    nx, ny, nz = x.shape
    
    basis = np.zeros((3, 3))
    basis[0, 0] = x[nx-1, 0, 0]
    basis[0, 1] = y[nx-1, 0, 0]
    basis[0, 2] = z[nx-1, 0, 0]
    
    basis[1, 0] = x[0, ny-1, 0]
    basis[1, 1] = y[0, ny-1, 0]
    basis[1, 2] = z[0, ny-1, 0]
    
    basis[2, 0] = x[0, 0, nz-1]
    basis[2, 1] = y[0, 0, nz-1]
    basis[2, 2] = z[0, 0, nz-1]
    
    return basis


def rescale_data_for_colormap(data, isovalue, max_comp, colormap_size=64):
    """
    Rescale data to fit into a colormap for combined plotting.
    
    Parameters
    ----------
    data : ndarray
        Input data array
    isovalue : float
        Minimum value to show
    max_comp : float
        Maximum value for colorbar
    colormap_size : int
        Size of the colormap
    
    Returns
    -------
    scaled_data : ndarray
        Data scaled to [0, colormap_size-1]
    """
    range_val = max_comp - isovalue
    if range_val <= 0:
        return np.zeros_like(data)
    
    scaled = (data - isovalue) * (colormap_size - 1) / range_val
    return np.clip(scaled, 0, colormap_size - 1)
