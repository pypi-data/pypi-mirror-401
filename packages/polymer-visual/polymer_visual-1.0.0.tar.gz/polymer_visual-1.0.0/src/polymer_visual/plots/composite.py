"""
Composite composition profile plots for polymer visualization.

This module provides functions to create 3D isosurface plots showing all
polymer species on the same axes.
"""

import numpy as np
import plotly.graph_objects as go

from polymer_visual.utils.colormaps import get_colormaps, get_default_colors
from polymer_visual.utils.isovalues import get_isovalues, get_max_compositions
from polymer_visual.plots.base import get_basis_from_coords, rescale_data_for_colormap


def plot_composite_profile(R, x, y, z, dim=3, species=None, isovalues=None,
                           max_comps=None, mono_labels=None, colormaps=None,
                           colors=None, title=None, save_file=None, 
                           show_fig=True, opacity=1.0, view_3d=None):
    """
    Plot composite 3D density profile with all species on the same axes.
    
    Parameters
    ----------
    R : ndarray
        4D array of composition data with shape (nx, ny, nz, n_species)
    x, y, z : ndarray
        3D coordinate arrays
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
    colors : array-like, optional
        RGB colors for each species
    title : str, optional
        Figure title
    save_file : str, optional
        Path to save HTML/PNG file
    show_fig : bool
        Whether to display the figure
    opacity : float
        Surface opacity (0-1)
    view_3d : tuple, optional
        View angle (azimuth, elevation)
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
        Interactive figure object
    """
    nx, ny, nz, n_species = R.shape
    
    if species is None:
        species = list(range(n_species))
    
    if mono_labels is None:
        mono_labels = [chr(ord('A') + i) for i in range(n_species)]
    
    if colormaps is None:
        colormaps = get_colormaps(n_species)
    
    if colors is None:
        colors = get_default_colors(n_species)
    
    if isovalues is None:
        isovalues = get_isovalues(R, dim)
    
    if max_comps is None:
        max_comps = get_max_compositions(R)
    
    if view_3d is None:
        view_3d = (-45, 45)
    
    fig = go.Figure()
    
    basis = get_basis_from_coords(x, y, z)
    
    draw_unit_cell_box(fig, basis)
    
    for s in species:
        data = R[:, :, :, s]
        isovalue = isovalues[s]
        max_comp = max_comps[s]
        cmap = colormaps[s]
        color = colors[s]
        
        if max_comp <= isovalue:
            continue
        
        add_isosurface_trace(fig, x, y, z, data, isovalue, color, opacity)
    
    azimuth, elevation = view_3d
    fig.update_layout(
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z',
            aspectmode='data',
            camera=dict(
                eye=dict(
                    x=np.cos(np.radians(azimuth)) * np.cos(np.radians(elevation)),
                    y=np.sin(np.radians(azimuth)) * np.cos(np.radians(elevation)),
                    z=np.sin(np.radians(elevation))
                )
            )
        ),
        title=title or "Composite Density Profile",
        height=700,
        width=900,
        showlegend=True,
        legend=dict(
            x=1.0,
            y=0.98,
            bgcolor='rgba(255,255,255,0.8)'
        )
    )
    
    if save_file:
        if save_file.endswith('.html'):
            fig.write_html(save_file)
        else:
            fig.write_image(save_file)
    
    if show_fig:
        fig.show()
    
    return fig


def add_isosurface_trace(fig, x, y, z, data, isovalue, color, opacity=0.8):
    """
    Add an isosurface trace to a figure.
    
    Parameters
    ----------
    fig : go.Figure
        Figure to add trace to
    x, y, z : ndarray
        Coordinate arrays
    data : ndarray
        Scalar data array
    isovalue : float
        Isovalue for the surface
    color : array-like
        RGB color for the surface
    opacity : float
        Surface opacity
    """
    color_str = f'rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})'
    
    x_flat = x[:-1, :-1, :-1].flatten()
    y_flat = y[:-1, :-1, :-1].flatten()
    z_flat = z[:-1, :-1, :-1].flatten()
    data_flat = data[:-1, :-1, :-1].flatten()
    
    nx, ny, nz = data.shape
    
    try:
        from scipy import ndimage
        
        data_smooth = ndimage.gaussian_filter(data, sigma=1.0)
        
        mask = data_smooth >= isovalue
        
        if np.sum(mask) < 10:
            return
        
        labeled, n_features = ndimage.label(mask)
        
        for i in range(1, n_features + 1):
            component_mask = labeled == i
            
            if np.sum(component_mask) < 20:
                continue
            
            indices = np.where(component_mask)
            
            x_surf = x[indices]
            y_surf = y[indices]
            z_surf = z[indices]
            
            fig.add_trace(go.Mesh3d(
                x=x_surf,
                y=y_surf,
                z=z_surf,
                alphahull=5,
                color=color_str,
                opacity=opacity,
                name=f'Species'
            ))
            
    except ImportError:
        fig.add_trace(go.Mesh3d(
            x=x_flat,
            y=y_flat,
            z=z_flat,
            intensity=data_flat,
            isomin=isovalue,
            isomax=np.max(data),
            surfacecolor=data_flat,
            colorscale=[[0, color_str], [1, color_str]],
            opacity=opacity,
            name='Species'
        ))


def draw_unit_cell_box(fig, basis, color='gray', width=2):
    """
    Draw the unit cell box edges.
    
    Parameters
    ----------
    fig : go.Figure
        Figure to add lines to
    basis : ndarray
        3x3 basis vector array
    color : str
        Line color
    width : float
        Line width
    """
    origin = np.array([0, 0, 0])
    
    corners = np.array([
        origin,
        basis[0],
        basis[1],
        basis[2],
        basis[0] + basis[1],
        basis[0] + basis[2],
        basis[1] + basis[2],
        basis[0] + basis[1] + basis[2]
    ])
    
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 5), (2, 4), (2, 6),
        (3, 5), (3, 6), (4, 7), (5, 7), (6, 7)
    ]
    
    for start, end in edges:
        fig.add_trace(go.Scatter3d(
            x=[corners[start, 0], corners[end, 0]],
            y=[corners[start, 1], corners[end, 1]],
            z=[corners[start, 2], corners[end, 2]],
            mode='lines',
            line=dict(color=color, width=width),
            showlegend=False
        ))
