"""Lattice basis vector calculations."""

import numpy as np


def get_basis(cell_d, angle):
    """
    Calculate lattice basis vectors from unit cell parameters.
    
    Parameters
    ----------
    cell_d : array-like
        Unit cell dimensions [a, b, c]
    angle : array-like
        Unit cell angles [alpha, beta, gamma] in radians
    
    Returns
    -------
    basis : ndarray
        3x3 array where each row is a lattice basis vector
        basis[0] = a vector
        basis[1] = b vector  
        basis[2] = c vector
    """
    a, b, c = cell_d
    alpha, beta, gamma = angle
    
    cos_alpha = np.cos(alpha)
    cos_beta = np.cos(beta)
    cos_gamma = np.cos(gamma)
    sin_gamma = np.sin(gamma)
    
    vx = a
    vy = 0
    vz = 0
    
    wx = b * cos_gamma
    wy = b * sin_gamma
    wz = 0
    
    tx = c * cos_beta
    ty = c * (cos_alpha - cos_beta * cos_gamma) / sin_gamma
    tz = np.sqrt(c**2 - tx**2 - ty**2)
    
    basis = np.array([
        [vx, vy, vz],
        [wx, wy, wz],
        [tx, ty, tz]
    ])
    
    return basis
