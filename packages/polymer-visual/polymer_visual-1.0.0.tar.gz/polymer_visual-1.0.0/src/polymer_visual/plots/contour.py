"""
Contour plot for polymer visualization.

This module provides functions to create 2D contour plots showing composition
profiles on a specified plane through the unit cell.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from polymer_visual.utils.colormaps import get_colormaps
from polymer_visual.utils.isovalues import get_isovalues, get_max_compositions
from polymer_visual.plots.base import get_basis_from_coords


def plot_contour(R, x, y, z, contourvecs=None, basis=None, dim=3,
                 species=None, isovalues=None, max_comps=None,
                 mono_labels=None, colormaps=None, title=None,
                 save_file=None, show_fig=True):
    """
    Plot 2D contour profile on a specified plane.
    
    Parameters
    ----------
    R : ndarray
        4D array of composition data with shape (nx, ny, nz, n_species)
    x, y, z : ndarray
        3D coordinate arrays
    contourvecs : array-like, optional
        3x3 matrix specifying the plane:
        - Row 1: starting corner in reduced coordinates
        - Row 2: x-axis direction in reduced coordinates
        - Row 3: y-axis direction in reduced coordinates
    basis : ndarray, optional
        Lattice basis vectors (computed from coordinates if not provided)
    dim : int
        System dimensionality
    species : array-like, optional
        Species indices to plot
    isovalues : array-like, optional
        Isovalues for each species
    max_comps : array-like, optional
        Maximum composition values for colorbar
    mono_labels : list, optional
        Labels for each monomer species
    colormaps : list, optional
        Custom colormaps for each species
    title : str, optional
        Figure title
    save_file : str, optional
        Path to save HTML/PNG file
    show_fig : bool
        Whether to display the figure
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
        Interactive figure object
    """
    nx, ny, nz, n_species = R.shape
    grid = np.array([nx - 1, ny - 1, nz - 1])
    
    if species is None:
        species = list(range(n_species))
    
    if mono_labels is None:
        mono_labels = [chr(ord('A') + i) for i in range(n_species)]
    
    if colormaps is None:
        colormaps = get_colormaps(n_species)
    
    if isovalues is None:
        isovalues = get_isovalues(R, dim)
    
    if max_comps is None:
        max_comps = get_max_compositions(R)
    
    if basis is None:
        basis = get_basis_from_coords(x, y, z)
    
    if contourvecs is None:
        contourvecs = np.array([
            [0, 0, 0],
            [1, 1, 0],
            [0, 0, 1]
        ])
    
    startloc = contourvecs[0]
    xvec = contourvecs[1]
    yvec = contourvecs[2]
    
    start_coord = (startloc * grid + 1).astype(int)
    xvec_coord = xvec * grid
    yvec_coord = yvec * grid
    
    x_step_length = max(abs(xvec_coord))
    y_step_length = max(abs(yvec_coord))
    
    if x_step_length == 0:
        x_step_length = 1
    if y_step_length == 0:
        y_step_length = 1
    
    xvec_cart = np.zeros(3)
    yvec_cart = np.zeros(3)
    for i in range(3):
        xvec_cart += xvec[i] * basis[i]
        yvec_cart += yvec[i] * basis[i]
    
    cos_theta = np.dot(xvec_cart, yvec_cart) / (np.linalg.norm(xvec_cart) * np.linalg.norm(yvec_cart))
    theta = np.arccos(np.clip(cos_theta, -1, 1))
    
    x_init = np.linspace(0, np.linalg.norm(xvec_cart), x_step_length + 1)
    y_init = np.linspace(0, np.linalg.norm(yvec_cart), y_step_length + 1)
    
    contour_data = np.zeros((y_step_length + 1, x_step_length + 1, n_species))
    xcontour = np.zeros((y_step_length + 1, x_step_length + 1))
    ycontour = np.zeros((y_step_length + 1, x_step_length + 1))
    
    for ix in range(x_step_length + 1):
        for iy in range(y_step_length + 1):
            x_coord = start_coord[0] + ix * xvec_coord[0] / max(x_step_length, 1) + iy * yvec_coord[0] / max(y_step_length, 1)
            y_coord = start_coord[1] + ix * xvec_coord[1] / max(x_step_length, 1) + iy * yvec_coord[1] / max(y_step_length, 1)
            z_coord = start_coord[2] + ix * xvec_coord[2] / max(x_step_length, 1) + iy * yvec_coord[2] / max(y_step_length, 1)
            
            x_coord = int(np.clip(x_coord % grid[0], 0, grid[0] - 1))
            y_coord = int(np.clip(y_coord % grid[1], 0, grid[1] - 1))
            z_coord = int(np.clip(z_coord % grid[2], 0, grid[2] - 1))
            
            contour_data[iy, ix, :] = R[x_coord, y_coord, z_coord, :]
            
            xcontour[iy, ix] = x_init[ix] + y_init[iy] * np.cos(theta)
            ycontour[iy, ix] = y_init[iy] * np.sin(theta)
    
    fig = make_subplots(
        rows=1, cols=len(species),
        subplot_titles=[f'φ_{mono_labels[s]}' for s in species],
        horizontal_spacing=0.05
    )
    
    for idx, s in enumerate(species):
        data_2d = contour_data[:, :, s]
        cmap = colormaps[s]
        isovalue = isovalues[s]
        max_comp = max_comps[s]
        
        color_scale = create_colorscale(cmap)
        
        fig.add_trace(
            go.Heatmap(
                x=xcontour[0, :],
                y=ycontour[:, 0],
                z=data_2d,
                colorscale=color_scale,
                zmin=isovalue,
                zmax=max_comp,
                colorbar=dict(
                    title=f'φ_{mono_labels[s]}',
                    titleside='right'
                ),
                showscale=(idx == len(species) - 1)
            ),
            row=1, col=idx + 1
        )
    
    fig.update_layout(
        title=title or "2D Contour Plot",
        height=400,
        width=300 * len(species),
        showlegend=False
    )
    
    fig.update_xaxes(title_text='x (relative)', row=1, col=1)
    fig.update_yaxes(title_text='y (relative)', row=1, col=1)
    
    for idx in range(1, len(species)):
        fig.update_xaxes(title_text='x (relative)', row=1, col=idx + 1)
    
    if save_file:
        if save_file.endswith('.html'):
            fig.write_html(save_file)
        else:
            fig.write_image(save_file)
    
    if show_fig:
        fig.show()
    
    return fig


def create_colorscale(cmap):
    """
    Create a plotly colorscale from a colormap array.
    
    Parameters
    ----------
    cmap : ndarray
        N x 3 array of RGB values
    
    Returns
    -------
    colorscale : list
        Plotly colorscale format
    """
    colorscale = []
    n = len(cmap)
    for i, color in enumerate(cmap):
        colorscale.append([i / (n - 1), f'rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})'])
    return colorscale
