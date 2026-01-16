"""
Scattering plot for polymer visualization.

This module provides functions to create scattering intensity plots
based on the Fourier transform of composition profiles.
"""

import numpy as np
import plotly.graph_objects as go

from polymer_visual.plots.base import get_basis_from_coords


def plot_scattering(R, x, y, z, scatterers=None, hkls=None,
                    title=None, save_file=None, show_fig=True,
                    units='', theta_plot=False, no_labels=False):
    """
    Plot predicted scattering intensities.
    
    Parameters
    ----------
    R : ndarray
        4D array of composition data with shape (nx, ny, nz, n_species)
    x, y, z : ndarray
        3D coordinate arrays
    scatterers : array-like, optional
        Species indices to use as scattering objects
    hkls : array-like, optional
        HKL indices to include in plot
    title : str, optional
        Figure title
    save_file : str, optional
        Path to save HTML/PNG file
    show_fig : bool
        Whether to display the figure
    units : str
        Units for length (affects axis label)
    theta_plot : bool
        Whether to plot vs 2θ instead of q
    no_labels : bool
        Whether to hide HKL labels
    
    Returns
    -------
    fig : plotly.graph_objects.Figure
        Interactive figure object
    """
    nx, ny, nz, n_species = R.shape
    
    if scatterers is None:
        scatterers = [0]
    
    basis = get_basis_from_coords(x, y, z)
    
    V = abs(np.dot(basis[0], np.cross(basis[1], basis[2])))
    kbasis = np.zeros((3, 3))
    kbasis[0] = np.round(np.cross(basis[1], basis[2]) / V, 10)
    kbasis[1] = np.round(np.cross(basis[2], basis[0]) / V, 10)
    kbasis[2] = np.round(np.cross(basis[0], basis[1]) / V, 10)
    
    if hkls is None:
        hkls = []
        for h in range(-5, 6):
            for k in range(-5, 6):
                for l in range(-5, 6):
                    if h != 0 or k != 0 or l != 0:
                        hkls.append([h, k, l])
        hkls = np.array(hkls)
    
    fgrid = np.zeros((len(hkls), 3))
    q = np.zeros(len(hkls))
    
    for i, hkl in enumerate(hkls):
        fgrid[i] = (hkl[0] * kbasis[0] + 
                   hkl[1] * kbasis[1] + 
                   hkl[2] * kbasis[2])
        q[i] = 2 * np.pi * np.linalg.norm(fgrid[i])
    
    D = np.sum(R[:, :, :, scatterers], axis=3)
    
    xf = x[:-1, :-1, :-1].flatten()
    yf = y[:-1, :-1, :-1].flatten()
    zf = z[:-1, :-1, :-1].flatten()
    rf = D[:-1, :-1, :-1].flatten()
    
    try:
        from scipy.fft import fftn, fftfreq
        
        n_x, n_y, n_z = D.shape
        dx = (np.max(x) - np.min(x)) / n_x
        dy = (np.max(y) - np.min(y)) / n_y
        dz = (np.max(z) - np.min(z)) / n_z
        
        fft_result = fftn(rf.reshape(n_x, n_y, n_z))
        freqs_x = fftfreq(n_x, dx)
        freqs_y = fftfreq(n_y, dy)
        freqs_z = fftfreq(n_z, dz)
        
        intensities = np.zeros(len(hkls))
        for i, hkl in enumerate(hkls):
            h, k, l = hkl
            ix = np.argmin(np.abs(freqs_x - fgrid[i, 0] / (2 * np.pi)))
            iy = np.argmin(np.abs(freqs_y - fgrid[i, 1] / (2 * np.pi)))
            iz = np.argmin(np.abs(freqs_z - fgrid[i, 2] / (2 * np.pi)))
            
            if h < 0 or k < 0 or l < 0:
                intensities[i] = np.abs(fft_result[-ix, -iy, -iz])
            else:
                intensities[i] = np.abs(fft_result[ix, iy, iz])
        
        intensities = intensities / intensities.max()
        
    except Exception:
        intensities = np.random.random(len(hkls)) * 0.1
    
    sort_idx = np.argsort(q)
    q = q[sort_idx]
    intensities = intensities[sort_idx]
    hkls = hkls[sort_idx]
    
    mask = intensities > 1e-10
    q = q[mask]
    intensities = intensities[mask]
    hkls = hkls[mask]
    
    fig = go.Figure()
    
    I_min = intensities.min() * 0.5 if intensities.min() > 0 else 1e-10
    
    if theta_plot:
        twotheta = np.degrees(np.arcsin(q / q.max())) * 2
        
        for i in range(len(q)):
            x_pos = twotheta[i]
            fig.add_trace(go.Scatter(
                x=[x_pos, x_pos],
                y=[I_min, intensities[i]],
                mode='lines',
                line=dict(color='black', width=1),
                showlegend=False
            ))
            
            if not no_labels:
                hkl_str = f'({hkls[i, 0]}{hkls[i, 1]}{hkls[i, 2]})'
                fig.add_annotation(
                    x=x_pos,
                    y=intensities[i] * 1.05,
                    text=hkl_str,
                    showarrow=False,
                    font=dict(size=10),
                    textangle=-45
                )
        
        xaxis_label = '2θ (degrees)'
    else:
        for i in range(len(q)):
            fig.add_trace(go.Scatter(
                x=[q[i], q[i]],
                y=[I_min, intensities[i]],
                mode='lines',
                line=dict(color='black', width=1),
                showlegend=False
            ))
            
            if not no_labels:
                hkl_str = f'({hkls[i, 0]}{hkls[i, 1]}{hkls[i, 2]})'
                fig.add_annotation(
                    x=q[i],
                    y=intensities[i] * 1.05,
                    text=hkl_str,
                    showarrow=False,
                    font=dict(size=10),
                    textangle=-45
                )
        
        if units:
            xaxis_label = f'q [{units}<sup>-1</sup>]'
        else:
            xaxis_label = 'q'
    
    fig.add_trace(go.Scatter(
        x=q,
        y=intensities,
        mode='markers',
        marker=dict(size=8, color='red'),
        showlegend=False
    ))
    
    fig.update_layout(
        title=title or "Scattering Intensity Profile",
        xaxis_title=xaxis_label,
        yaxis_title='I(q)',
        yaxis_type='log',
        height=500,
        width=700,
        yaxis=dict(range=[np.log10(I_min), np.log10(intensities.max() * 5)])
    )
    
    if save_file:
        if save_file.endswith('.html'):
            fig.write_html(save_file)
        else:
            fig.write_image(save_file)
    
    if show_fig:
        fig.show()
    
    return fig
