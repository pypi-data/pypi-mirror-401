"""
Line profile plots for polymer visualization.

This module provides functions to create 1D composition profiles along
a specified direction through the unit cell.
"""

import numpy as np
import plotly.graph_objects as go

from polymer_visual.utils.colormaps import get_default_colors


def plot_line_profile(R, x, y, z, direction, startloc=None, dim=3,
                      species=None, mono_labels=None, colors=None,
                      title=None, save_file=None, show_fig=True):
    """
    Plot 1D composition profile along a specified direction.
    
    Parameters
    ----------
    R : ndarray
        4D array of composition data with shape (nx, ny, nz, n_species)
    x, y, z : ndarray
        3D coordinate arrays
    direction : array-like
        Direction vector in reduced coordinates
    startloc : array-like, optional
        Starting point in reduced coordinates (default: origin)
    dim : int
        System dimensionality
    species : array-like, optional
        Species indices to plot
    mono_labels : list, optional
        Labels for each monomer species
    colors : array-like, optional
        RGB colors for each species
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
    
    if colors is None:
        colors = get_default_colors(n_species)
    
    if startloc is None:
        startloc = np.zeros(3)
    
    direction = np.array(direction, dtype=float)
    startloc = np.array(startloc, dtype=float)
    
    direction = np.pad(direction, (0, 3 - len(direction)))
    startloc = np.pad(startloc, (0, 3 - len(startloc)))
    
    endloc = startloc + direction
    
    start_coord = (startloc * grid + 1).astype(int)
    end_coord = (endloc * grid + 1).astype(int)
    
    dir_vec = end_coord - start_coord
    n_steps = max(abs(dir_vec))
    
    if n_steps == 0:
        n_steps = 1
    
    t_values = np.linspace(0, 1, n_steps + 1)
    
    x_vals = np.zeros(n_steps + 1)
    line_data = np.zeros((n_steps + 1, n_species))
    
    total_length = np.linalg.norm(dir_vec)
    
    for i, t in enumerate(t_values):
        point = start_coord + t * dir_vec
        
        ix = int(np.clip(point[0] % grid[0], 0, grid[0] - 1))
        iy = int(np.clip(point[1] % grid[1], 0, grid[1] - 1))
        iz = int(np.clip(point[2] % grid[2], 0, grid[2] - 1))
        
        x_vals[i] = t
        
        for s in species:
            line_data[i, s] = R[ix, iy, iz, s]
    
    fig = go.Figure()
    
    for idx, s in enumerate(species):
        color = colors[s] if s < len(colors) else [0.5, 0.5, 0.5]
        color_str = f'rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})'
        
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=line_data[:, s],
            mode='lines+markers',
            name=f'{mono_labels[s]} block',
            line=dict(color=color_str, width=2),
            marker=dict(size=8, color=color_str)
        ))
    
    if title is None:
        if np.allclose(startloc, 0):
            title = f'Density Profile Along [{direction[0]:.2g} {direction[1]:.2g} {direction[2]:.2g}]'
        else:
            title = f'Density Profile from [{startloc[0]:.2g} {startloc[1]:.2g} {startloc[2]:.2g}] to [{endloc[0]:.2g} {endloc[1]:.2g} {endloc[2]:.2g}]'
    
    fig.update_layout(
        title=title,
        xaxis_title='r/r_max',
        yaxis_title='φ(r)',
        height=500,
        width=700,
        showlegend=True,
        legend=dict(
            x=1.02,
            y=1,
            bgcolor='rgba(255,255,255,0.8)'
        ),
        hovermode='x unified'
    )
    
    if save_file:
        if save_file.endswith('.html'):
            fig.write_html(save_file)
        else:
            fig.write_image(save_file)
    
    if show_fig:
        fig.show()
    
    return fig


def get_line_profile_data(R, x, y, z, direction, startloc=None, dim=3):
    """
    Get line profile data without plotting.
    
    Parameters
    ----------
    R : ndarray
        4D composition data
    x, y, z : ndarray
        Coordinate arrays
    direction : array-like
        Direction vector
    startloc : array-like, optional
        Starting point
    dim : int
        System dimensionality
    
    Returns
    -------
    result : tuple
        (x_values, line_data) where line_data is shape (n_points, n_species)
    """
    nx, ny, nz, n_species = R.shape
    grid = np.array([nx - 1, ny - 1, nz - 1])
    
    if startloc is None:
        startloc = np.zeros(3)
    
    direction = np.array(direction, dtype=float)
    startloc = np.array(startloc, dtype=float)
    
    direction = np.pad(direction, (0, 3 - len(direction)))
    startloc = np.pad(startloc, (0, 3 - len(startloc)))
    
    endloc = startloc + direction
    
    start_coord = (startloc * grid + 1).astype(int)
    end_coord = (endloc * grid + 1).astype(int)
    
    dir_vec = end_coord - start_coord
    n_steps = max(abs(dir_vec))
    
    if n_steps == 0:
        n_steps = 1
    
    t_values = np.linspace(0, 1, n_steps + 1)
    x_vals = np.zeros(n_steps + 1)
    line_data = np.zeros((n_steps + 1, n_species))
    
    for i, t in enumerate(t_values):
        point = start_coord + t * dir_vec
        
        ix = int(np.clip(point[0] % grid[0], 0, grid[0] - 1))
        iy = int(np.clip(point[1] % grid[1], 0, grid[1] - 1))
        iz = int(np.clip(point[2] % grid[2], 0, grid[2] - 1))
        
        x_vals[i] = t
        line_data[i, :] = R[ix, iy, iz, :]
    
    return x_vals, line_data
