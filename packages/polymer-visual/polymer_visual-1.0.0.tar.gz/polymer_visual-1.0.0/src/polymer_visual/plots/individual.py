"""
Individual composition profile plots for polymer visualization.

This module provides functions to create 3D isosurface plots for individual
polymer species using Plotly for interactive visualization.
"""

import os
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

from polymer_visual.utils.colormaps import get_colormaps, get_default_colors
from polymer_visual.utils.isovalues import get_isovalues, get_max_compositions


def create_colorscale(cmap):
    """Create a plotly colorscale from a colormap array."""
    colorscale = []
    n = len(cmap)
    for i, color in enumerate(cmap):
        colorscale.append([i / (n - 1), f'rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})'])
    return colorscale


def save_figure(fig, filename):
    """Save figure to file based on extension."""
    filepath = str(filename)
    ext = Path(filepath).suffix.lower()
    
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    
    if ext == '.html':
        fig.write_html(filepath)
    elif ext in ['.png', '.svg', '.jpeg', '.jpg']:
        fig.write_image(filepath)
    else:
        fig.write_html(filepath + '.html')


def plot_individual_profiles(R, x, y, z, dim=3, species=None, isovalues=None,
                             max_comps=None, mono_labels=None, colormaps=None,
                             title=None, save_file=None, show_fig=True,
                             opacity=1.0, view_3d=None):
    """
    Plot 3D isosurface for each individual species.
    
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
    title : str, optional
        Figure title
    save_file : str, optional
        Path to save HTML/PNG/SVG file
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
    
    if isovalues is None:
        isovalues = get_isovalues(R, dim)
    
    if max_comps is None:
        max_comps = get_max_compositions(R)
    
    if view_3d is None:
        view_3d = (-45, 45)
    
    if dim == 1:
        fig = go.Figure()
        
        for idx, s in enumerate(species):
            data = R[:-1, 0, 0, s]
            x_data = x[:-1, 0, 0]
            cmap = colormaps[s]
            
            mid_idx = min(len(cmap) // 2, len(cmap) - 1)
            color = [c * 255 for c in cmap[mid_idx]]
            color_str = f'rgb({int(color[0])}, {int(color[1])}, {int(color[2])})'
            
            fig.add_trace(go.Scatter(
                x=x_data,
                y=data,
                mode='lines+markers',
                name=f'{mono_labels[s]} block',
                line=dict(color=color_str, width=2),
                marker=dict(size=6, color=color_str)
            ))
        
        fig.update_layout(
            title=title or "1D Composition Profiles",
            xaxis_title='x',
            yaxis_title='phi(x)',
            height=500,
            width=700,
            showlegend=True,
            legend=dict(x=1.02, y=1)
        )
        
    elif dim == 2:
        fig = make_subplots(
            rows=1, cols=len(species),
            subplot_titles=[f"{mono_labels[s]} Block Density" for s in species],
            horizontal_spacing=0.08
        )
        
        for idx, s in enumerate(species):
            data_2d = R[:-1, :-1, 0, s]
            x_2d = x[:-1, :-1, 0]
            y_2d = y[:-1, :-1, 0]
            cmap = colormaps[s]
            isovalue = isovalues[s]
            max_comp = max_comps[s]
            
            color_scale = create_colorscale(cmap)
            
            fig.add_trace(
                go.Heatmap(
                    x=x_2d[0, :],
                    y=y_2d[:, 0],
                    z=data_2d,
                    colorscale=color_scale,
                    zmin=isovalue,
                    zmax=max_comp,
                    colorbar=dict(title=f'phi_{mono_labels[s]}'),
                    showscale=(idx == len(species) - 1)
                ),
                row=1, col=idx + 1
            )
            
            fig.update_xaxes(title_text='x', row=1, col=idx + 1)
            fig.update_yaxes(title_text='y', row=1, col=idx + 1)
        
        fig.update_layout(
            title=title or "2D Composition Profiles",
            height=400,
            width=350 * len(species),
            showlegend=False
        )
        
    else:
        fig = make_subplots(
            rows=1, cols=len(species),
            subplot_titles=[f"{mono_labels[s]} Block Density" for s in species],
            specs=[[{'type': 'mesh3d'}] * len(species)]
        )
        
        for idx, s in enumerate(species):
            data = R[:, :, :, s]
            isovalue = isovalues[s]
            max_comp = max_comps[s]
            cmap = colormaps[s]
            
            if max_comp <= isovalue:
                continue
            
            x_flat = x[:-1, :-1, :-1].flatten()
            y_flat = y[:-1, :-1, :-1].flatten()
            z_flat = z[:-1, :-1, :-1].flatten()
            data_flat = data[:-1, :-1, :-1].flatten()
            
            sliced_shape = (data.shape[0] - 1, data.shape[1] - 1, data.shape[2] - 1)
            
            if len(x_flat) == 0:
                continue
            
            mesh = create_isosurface_mesh(x_flat, y_flat, z_flat, data_flat, 
                                         sliced_shape, isovalue, cmap)
            
            for trace in mesh:
                fig.add_trace(trace, row=1, col=idx + 1)
            
            fig.update_scenes(
                dict(
                    xaxis_title='x',
                    yaxis_title='y', 
                    zaxis_title='z',
                    aspectmode='data'
                ),
                row=1, col=idx + 1
            )
        
        azimuth, elevation = view_3d
        camera_eye = dict(
            x=np.cos(np.radians(azimuth)) * np.cos(np.radians(elevation)),
            y=np.sin(np.radians(azimuth)) * np.cos(np.radians(elevation)),
            z=np.sin(np.radians(elevation))
        )
        
        for i in range(1, len(species) + 1):
            fig.update_scenes(camera=dict(eye=camera_eye), row=1, col=i)
        
        fig.update_layout(
            title=title or "3D Composition Profiles",
            height=500,
            width=400 * len(species),
            showlegend=False
        )
    
    if save_file:
        save_figure(fig, save_file)
    
    return fig


def create_isosurface_mesh(x_coords, y_coords, z_coords, values, grid_shape,
                           isovalue, colormap, n_contours=10):
    """Create isosurface mesh for 3D plotting."""
    nx, ny, nz = grid_shape
    
    x_grid = x_coords.reshape(grid_shape)
    y_grid = y_coords.reshape(grid_shape)
    z_grid = z_coords.reshape(grid_shape)
    data_grid = values.reshape(grid_shape)
    
    traces = []
    
    value_range = np.max(data_grid) - np.min(data_grid)
    contour_values = np.linspace(isovalue + value_range * 0.01, 
                                 np.max(data_grid), n_contours)
    
    from scipy import ndimage
    
    for contour_val in contour_values:
        try:
            data_smooth = ndimage.gaussian_filter(data_grid, sigma=1.0)
            
            mask = data_smooth >= contour_val
            
            labeled, n_features = ndimage.label(mask)
            
            for i in range(1, n_features + 1):
                component_mask = labeled == i
                
                if np.sum(component_mask) < 10:
                    continue
                
                indices = np.where(component_mask)
                
                if len(indices[0]) < 4:
                    continue
                
                x_vals = x_grid[indices]
                y_vals = y_grid[indices]
                z_vals = z_grid[indices]
                
                color_val = (contour_val - isovalue) / (np.max(data_grid) - isovalue)
                color_idx = int(color_val * (len(colormap) - 1))
                color_idx = np.clip(color_idx, 0, len(colormap) - 1)
                color = colormap[color_idx]
                
                color_str = f'rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})'
                
                trace = go.Mesh3d(
                    x=x_vals,
                    y=y_vals,
                    z=z_vals,
                    alphahull=5,
                    color=color_str,
                    opacity=0.8,
                    name=f'Isosurface'
                )
                traces.append(trace)
                
        except Exception:
            continue
    
    return traces


def plot_single_isosurface(R, x, y, z, species_idx=0, isovalue=None,
                           max_comp=None, mono_label='A', colormap=None,
                           title=None, show_fig=True):
    """Plot a single species isosurface."""
    n_species = R.shape[3]
    
    colormaps = get_colormaps(n_species)
    if colormap is None:
        colormap = colormaps[species_idx]
    
    isovalues = get_isovalues(R, 3)
    max_comps = get_max_compositions(R)
    
    if isovalue is None:
        isovalue = isovalues[species_idx]
    if max_comp is None:
        max_comp = max_comps[species_idx]
    
    fig = go.Figure()
    
    x_flat = x[:-1, :-1, :-1].flatten()
    y_flat = y[:-1, :-1, :-1].flatten()
    z_flat = z[:-1, :-1, :-1].flatten()
    data_flat = R[:-1, :-1, :-1, species_idx].flatten()
    
    sliced_shape = (R.shape[0] - 1, R.shape[1] - 1, R.shape[2] - 1)
    
    mesh_traces = create_isosurface_mesh(
        x_flat, y_flat, z_flat, data_flat,
        sliced_shape, isovalue, colormap
    )
    
    for trace in mesh_traces:
        fig.add_trace(trace)
    
    from polymer_visual.plots.base import get_basis_from_coords
    basis = get_basis_from_coords(x, y, z)
    
    edges = [
        ([0, basis[0,0]], [0, basis[0,1]], [0, basis[0,2]]),
        ([0, basis[1,0]], [0, basis[1,1]], [0, basis[1,2]]),
        ([0, basis[2,0]], [0, basis[2,1]], [0, basis[2,2]]),
    ]
    
    for edge in edges:
        fig.add_trace(go.Scatter3d(
            x=edge[0], y=edge[1], z=edge[2],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False
        ))
    
    fig.update_layout(
        title=title or f'{mono_label} Block Density Profile',
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z',
            aspectmode='data'
        ),
        height=600,
        width=800
    )
    
    return fig
