"""Isovalue calculation for polymer visualization."""

import numpy as np


def get_isovalues(R, dim=3, species_indices=None):
    """
    Calculate isovalues for each species based on the composition data.
    
    Parameters
    ----------
    R : ndarray
        4D array of composition data with shape (nx, ny, nz, n_species)
    dim : int
        Dimensionality of the system (1, 2, or 3)
    species_indices : array-like, optional
        Indices of species to calculate isovalues for
    
    Returns
    -------
    isovalues : ndarray
        1D array of isovalues for each species
    """
    n_species = R.shape[3]
    
    if species_indices is None:
        species_indices = range(n_species)
    
    isovalues = np.zeros(n_species)
    
    for i in species_indices:
        data = R[:, :, :, i]
        mean_val = np.mean(data)
        std_val = np.std(data)
        
        if std_val > 0:
            isovalues[i] = mean_val + 0.5 * std_val
        else:
            isovalues[i] = mean_val
        
        isovalues[i] = np.clip(isovalues[i], 0.01, 0.99)
    
    return isovalues


def get_max_compositions(R, species_indices=None):
    """
    Get maximum composition values for each species.
    
    Parameters
    ----------
    R : ndarray
        4D array of composition data with shape (nx, ny, nz, n_species)
    species_indices : array-like, optional
        Indices of species to get max values for
    
    Returns
    -------
    max_comps : ndarray
        1D array of maximum compositions for each species
    """
    n_species = R.shape[3]
    
    if species_indices is None:
        species_indices = range(n_species)
    
    max_comps = np.zeros(n_species)
    
    for i in species_indices:
        max_comps[i] = np.max(R[:, :, :, i])
    
    return max_comps
