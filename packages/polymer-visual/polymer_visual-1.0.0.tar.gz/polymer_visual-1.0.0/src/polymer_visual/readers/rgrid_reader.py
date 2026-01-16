"""
Read PSCF r-grid files and return composition data.

This module provides functionality to read r-grid files produced by the PSCF
(Self-Consistent Field Theory) software for polymer simulations.
"""

import os
import re
import numpy as np
from polymer_visual.utils.basis import get_basis


def read_rgrid(filename, field_id=0):
    """
    Read data from a PSCF r-grid file.
    
    Parameters
    ----------
    filename : str
        Path to the r-grid file
    field_id : int, optional
        Field index for FTS trajectory files (default: 0)
    
    Returns
    -------
    result : tuple
        (R, x, y, z, dim, lattype)
        R : ndarray
            4D array of composition data with shape (nx, ny, nz, n_species)
        x, y, z : ndarray
            3D arrays of coordinates for each grid point
        dim : int
            Dimensionality of the system (1, 2, or 3)
        lattype : str
            Crystal system type (e.g., 'cubic', 'hexagonal')
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    if len(lines) < 10:
        raise ValueError("File is too short to be a valid rgrid file")
    
    header_info = parse_header(lines)
    
    dim = header_info['dim']
    lattype = header_info['lattype']
    n_mnr = header_info['n_monomer']
    grid = header_info['grid']
    data_start = header_info['data_start']
    
    n_pts = int(np.prod(grid[:dim]))
    
    multiplier = 1
    total_rows = n_pts
    
    data = np.zeros((total_rows, n_mnr))
    
    for i in range(total_rows):
        line_idx = data_start + i
        if line_idx >= len(lines):
            raise ValueError(f"Unexpected end of file at line {line_idx}")
        values = [float(x) for x in lines[line_idx].strip().split()]
        if len(values) != n_mnr:
            raise ValueError(f"Line {line_idx} has {len(values)} values, expected {n_mnr}")
        data[i, :] = values
    
    R = rearrange_pts(data, grid, dim, n_mnr)
    x, y, z = gen_xyz(lattype, header_info['cell_param'], grid)
    
    return R, x, y, z, dim, lattype


def parse_header(lines):
    """
    Parse the header of an rgrid file.
    
    Parameters
    ----------
    lines : list
        List of file lines
    
    Returns
    -------
    info : dict
        Dictionary containing header information
    """
    info = {}
    
    if 'format' in lines[0].lower():
        info['new_format'] = True
    else:
        info['new_format'] = False
    
    if info['new_format']:
        return parse_new_format(lines)
    else:
        return parse_old_format(lines)


def parse_new_format(lines):
    """
    Parse the new format rgrid file.
    
    Parameters
    ----------
    lines : list
        List of file lines
    
    Returns
    -------
    info : dict
        Dictionary containing header information
    """
    info = {}
    
    dim = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == 'dim':
            dim = int(lines[i + 1].strip())
            info['dim'] = dim
            break
    
    if dim is None:
        raise ValueError("Could not find 'dim' in file")
    
    lattype = None
    for i, line in enumerate(lines):
        if 'crystal_system' in line.lower():
            lattype = lines[i + 1].strip()
            info['lattype'] = lattype
            break
    
    if lattype is None:
        raise ValueError("Could not find 'crystal_system' in file")
    
    n_cell_param = None
    for i, line in enumerate(lines):
        if 'N_cell_param' in line:
            n_cell_param = int(lines[i + 1].strip())
            break
    
    cell_param = []
    for i, line in enumerate(lines):
        if 'cell_param' in line.lower():
            for j in range(n_cell_param):
                cell_param.append(float(lines[i + 1 + j].strip()))
            info['cell_param'] = np.array(cell_param)
            break
    
    n_monomer = None
    for i, line in enumerate(lines):
        if 'N_monomer' in line:
            n_monomer = int(lines[i + 1].strip())
            info['n_monomer'] = n_monomer
            break
    
    if n_monomer is None:
        raise ValueError("Could not find 'N_monomer' in file")
    
    grid = None
    data_start = None
    for i, line in enumerate(lines):
        if 'ngrid' in line.lower():
            grid_line = lines[i + 1].strip()
            grid_values = [int(x) for x in grid_line.split()]
            if len(grid_values) == 1:
                grid_array = np.array([grid_values[0], grid_values[0], grid_values[0]])
            elif len(grid_values) == 2:
                grid_array = np.array([grid_values[0], grid_values[1], grid_values[0]])
            else:
                grid_array = np.array(grid_values[:3])
            grid = grid_values[0]  # Set grid for the None check
            info['grid'] = grid_array
            data_start = i + 2
            info['data_start'] = data_start
            break
    
    if grid is None:
        raise ValueError("Could not find 'ngrid' in file")
    
    return info


def parse_old_format(lines):
    """
    Parse the old format rgrid file.
    
    Parameters
    ----------
    lines : list
        List of file lines
    
    Returns
    -------
    info : dict
        Dictionary containing header information
    """
    info = {}
    
    dim = int(lines[2].strip())
    info['dim'] = dim
    
    lattype = lines[4].strip().strip("'")
    info['lattype'] = lattype
    
    param_line = lines[8].strip()
    info['cell_param'] = np.fromstring(param_line, sep=' ')
    
    if lines[9].strip().startswith('N_monomer'):
        n_mnr = int(lines[10].strip())
        has_symmetry = False
        data_start = 13
    elif lines[11].strip().startswith('N_monomer'):
        n_mnr = int(lines[12].strip())
        has_symmetry = True
        data_start = 14
    else:
        raise ValueError("Could not find N_monomer in file")
    
    info['n_monomer'] = n_mnr
    
    grid = None
    for i, line in enumerate(lines[data_start:], start=data_start):
        if 'ngrid' in line.lower() or 'mesh' in line.lower():
            grid = np.fromstring(lines[i + 1].strip(), sep=' ')
            data_start = i + 2
            break
    
    if grid is None:
        raise ValueError("Could not find grid dimensions in file")
    
    if len(grid) == 1:
        grid = np.array([grid[0], grid[0], grid[0]])
    elif len(grid) == 2:
        grid = np.array([grid[0], grid[1], grid[0]])
    else:
        grid = grid[:3]
    
    info['grid'] = grid
    info['data_start'] = data_start
    
    return info


def rearrange_pts(A, grid, dim, n_mnr):
    """
    Rearrange linear data array into 4D composition array.
    
    Parameters
    ----------
    A : ndarray
        Linear array of shape (n_points, n_species)
    grid : array-like
        Grid dimensions [nx, ny, nz]
    dim : int
        System dimensionality
    n_mnr : int
        Number of monomer species
    
    Returns
    -------
    R : ndarray
        4D array of shape (nx+1, ny+1, nz+1, n_species)
    """
    grid = np.array(grid, dtype=int)
    
    nx, ny, nz = grid + 1
    
    R = np.zeros((nx, ny, nz, n_mnr))
    
    for iz in range(nz):
        for iy in range(ny):
            for ix in range(nx):
                orig_ix = ix % grid[0] if ix < grid[0] else 0
                orig_iy = iy % grid[1] if iy < grid[1] else 0
                orig_iz = iz % grid[2] if iz < grid[2] else 0
                
                if dim == 1:
                    linear_idx = orig_ix
                elif dim == 2:
                    linear_idx = orig_ix * grid[1] + orig_iy
                else:
                    linear_idx = (orig_ix * grid[1] + orig_iy) * grid[2] + orig_iz
                
                if ix == grid[0]:
                    R[ix, :, :, :] = R[0, :, :, :]
                elif iy == grid[1]:
                    R[:, iy, :, :] = R[:, 0, :, :]
                elif iz == grid[2]:
                    R[:, :, iz, :] = R[:, :, 0, :]
                else:
                    R[ix, iy, iz, :] = A[linear_idx, :]
    
    return R


def gen_xyz(lattype, param, grid):
    """
    Generate 3D coordinate arrays from lattice parameters.
    
    Parameters
    ----------
    lattype : str
        Crystal system type
    param : array-like
        Unit cell parameters
    grid : array-like
        Grid dimensions
    
    Returns
    -------
    x, y, z : ndarray
        3D coordinate arrays
    """
    grid = np.array(grid, dtype=int)
    
    if len(grid) == 1:
        grid = np.array([grid[0], grid[0], grid[0]])
    elif len(grid) == 2:
        grid = np.array([grid[0], grid[1], grid[0]])
    
    if lattype == 'hexagonal':
        angle = np.array([np.pi/2, np.pi/2, 2*np.pi/3])
        if len(param) >= 2:
            cell_d = np.array([param[0], param[0], param[1]])
        else:
            cell_d = np.array([param[0], param[0], param[0]])
    elif lattype == 'cubic':
        angle = np.array([np.pi/2, np.pi/2, np.pi/2])
        cell_d = np.array([param[0], param[0], param[0]])
    elif lattype == 'tetragonal':
        angle = np.array([np.pi/2, np.pi/2, np.pi/2])
        cell_d = np.array([param[0], param[0], param[1]])
    elif lattype == 'orthorhombic':
        angle = np.array([np.pi/2, np.pi/2, np.pi/2])
        cell_d = np.array([param[0], param[1], param[2]])
    elif lattype == 'lamellar':
        angle = np.array([np.pi/2, np.pi/2, np.pi/2])
        cell_d = np.array([param[0], param[0], param[0]])
    elif lattype == 'triclinic':
        phi = param[3]
        theta = param[4]
        gamma = param[5]
        beta = np.arccos(np.sin(theta) * np.cos(phi))
        alpha = np.arccos(np.sin(theta) * np.sin(phi) - 
                         (np.cos(beta) * np.cos(gamma) / np.sin(gamma)))
        angle = np.array([alpha, beta, gamma])
        cell_d = np.array([param[0], param[1], param[2]])
    elif lattype == 'monoclinic':
        angle = np.array([np.pi/2, param[3], np.pi/2])
        cell_d = np.array([param[0], param[1], param[2]])
    elif lattype in ['trigonal', 'rhombohedral']:
        angle = np.array([param[1], param[1], param[1]])
        cell_d = np.array([param[0], param[0], param[0]])
    elif lattype == 'square':
        angle = np.array([np.pi/2, np.pi/2, np.pi/2])
        cell_d = np.array([param[0], param[0], param[0]])
    elif lattype == 'rectangular':
        angle = np.array([np.pi/2, np.pi/2, np.pi/2])
        cell_d = np.array([param[0], param[1], param[0]])
    elif lattype == 'oblique':
        angle = np.array([np.pi/2, np.pi/2, param[2]])
        cell_d = np.array([param[0], param[1], param[0]])
    elif lattype == 'rhombic':
        angle = np.array([np.pi/2, np.pi/2, param[1]])
        cell_d = np.array([param[0], param[0], param[0]])
    else:
        angle = np.array([np.pi/2, np.pi/2, np.pi/2])
        cell_d = np.array([param[0], param[0], param[0]])
    
    basis = get_basis(cell_d, angle)
    
    nx, ny, nz = grid + 1
    x = np.zeros((nx, ny, nz))
    y = np.zeros((nx, ny, nz))
    z = np.zeros((nx, ny, nz))
    
    nround = 10
    
    for iz in range(nz):
        for iy in range(ny):
            for ix in range(nx):
                xtemp = (basis[0, 0] * ix / grid[0] +
                        basis[1, 0] * iy / grid[1] +
                        basis[2, 0] * iz / grid[2])
                ytemp = (basis[1, 1] * iy / grid[1] +
                        basis[2, 1] * iz / grid[2])
                ztemp = basis[2, 2] * iz / grid[2]
                
                x[ix, iy, iz] = np.round(xtemp, nround)
                y[ix, iy, iz] = np.round(ytemp, nround)
                z[ix, iy, iz] = np.round(ztemp, nround)
    
    return x, y, z
