"""Colormap definitions for polymer visualization."""

import numpy as np


def get_colormaps(n_species=8):
    """
    Get default colormaps for each species.
    
    Parameters
    ----------
    n_species : int
        Number of monomer species
    
    Returns
    -------
    maps : list
        List of colormap arrays, one per species
    """
    maps = []
    
    cmap_colors = [
        np.array([0.0, 0.7, 0.9]),    # Cyan/Blue
        np.array([0.9, 0.0, 0.0]),    # Red
        np.array([0.85, 0.85, 0.0]),  # Yellow
        np.array([0.0, 0.9, 0.2]),    # Green
        np.array([0.5, 0.0, 1.0]),    # Purple
        np.array([1.0, 0.0, 1.0]),    # Magenta
        np.array([1.0, 0.5, 0.0]),    # Orange
        np.array([0.75, 0.75, 0.75]), # Gray
    ]
    
    for i in range(n_species):
        base_color = cmap_colors[i % len(cmap_colors)]
        cmap = create_continuous_cmap(base_color)
        maps.append(cmap)
    
    return maps


def create_continuous_cmap(base_color, n_colors=64):
    """
    Create a continuous colormap from white through base_color to darker shade.
    
    Parameters
    ----------
    base_color : array-like
        RGB color to center the colormap on
    n_colors : int
        Number of colors in the colormap
    
    Returns
    -------
    cmap : ndarray
        n_colors x 3 array of RGB values
    """
    cmap = np.zeros((n_colors, 3))
    
    white = np.array([1.0, 1.0, 1.0])
    
    n_half = n_colors // 2
    for i in range(n_half):
        t = i / max(n_half - 1, 1)
        cmap[i] = white * (1 - t) + base_color * t
    
    for i in range(n_half, n_colors):
        t = (i - n_half) / max(n_colors - n_half - 1, 1)
        cmap[i] = base_color * (1 - t * 0.5)
    
    return cmap


def get_default_colors(n_species=8):
    """
    Get default line colors for each species.
    
    Parameters
    ----------
    n_species : int
        Number of monomer species
    
    Returns
    -------
    colors : ndarray
        n_species x 3 array of RGB values
    """
    colors = np.array([
        [0.0, 0.7, 0.9],    # Blue
        [0.9, 0.0, 0.0],    # Red
        [0.85, 0.85, 0.0],  # Yellow
        [0.0, 0.9, 0.2],    # Green
        [0.5, 0.0, 1.0],    # Purple
        [1.0, 0.0, 1.0],    # Magenta
        [1.0, 0.5, 0.0],    # Orange
        [0.75, 0.75, 0.75], # Gray
    ])
    
    if n_species <= len(colors):
        return colors[:n_species]
    else:
        full_colors = np.tile(colors, (n_species // len(colors) + 1, 1))
        return full_colors[:n_species]
