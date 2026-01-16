#!/usr/bin/env python3
"""
Command-line interface for polymer-visual.

This module provides a CLI for generating polymer visualization plots
from PSCF r-grid files.
"""

import click
import sys
from pathlib import Path

from polymer_visual.api import load_data, plot_all
from polymer_visual.plots.individual import plot_individual_profiles
from polymer_visual.plots.composite import plot_composite_profile
from polymer_visual.plots.line import plot_line_profile
from polymer_visual.plots.contour import plot_contour
from polymer_visual.plots.scattering import plot_scattering


def get_save_path(output_dir, filename, ext='.html'):
    """Get full save path for a file."""
    if output_dir:
        return f"{output_dir}/{filename}{ext}"
    return None


def save_plot(fig, save_file):
    """Save plot to file, handling different formats."""
    if not save_file:
        return
    
    ext = Path(save_file).suffix.lower()
    
    try:
        if ext == '.html':
            fig.write_html(save_file)
        elif ext in ['.png', '.svg', '.jpeg', '.jpg']:
            import plotly.io as pio
            pio.write_image(fig, save_file)
        else:
            fig.write_html(save_file + '.html')
    except Exception as e:
        if 'Chrome' in str(e) or 'kaleido' in str(e).lower():
            click.echo(f"Note: PNG/SVG export requires Chrome or chromium to be installed.")
            click.echo(f"Falling back to HTML format: {Path(save_file).stem}.html")
            fig.write_html(str(Path(save_file).parent / f"{Path(save_file).stem}.html"))
        else:
            raise


@click.group()
def main():
    """polymer-visual: Visualization tools for polymer simulation data."""
    pass


@main.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory for plots')
@click.option('--format', '-f', type=click.Choice(['html', 'png', 'svg']), default='html',
              help='Output format for plots (png/svg require Chrome/chromium)')
@click.option('--show/--no-show', default=False, help='Show figures in browser')
@click.option('--individual', is_flag=True, help='Generate individual profiles')
@click.option('--composite', is_flag=True, help='Generate composite profile')
@click.option('--line', is_flag=True, help='Generate line profile')
@click.option('--contour', is_flag=True, help='Generate contour plot')
@click.option('--scattering', is_flag=True, help='Generate scattering plot')
@click.option('--all', 'all_plots', is_flag=True, help='Generate all plots')
def plot(filename, output_dir, format, show, individual, composite, line, contour,
         scattering, all_plots):
    """Generate visualization plots from an r-grid file."""
    filename = str(filename)
    
    if output_dir:
        output_dir = str(output_dir)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        data = load_data(filename)
        click.echo(f"Loaded data: {data['lattype']} system, {data['R'].shape[3]} species")
        
        ext = f'.{format}'
        
        if all_plots or not any([individual, composite, line, contour, scattering]):
            if output_dir:
                plot_all(data, output_dir, show)
            else:
                plot_all(data, None, show=False)
            click.echo("Generated all plots.")
        else:
            if individual:
                save_file = get_save_path(output_dir, 'individual', ext)
                fig = plot_individual_profiles(
                    data['R'], data['x'], data['y'], data['z'],
                    dim=data['dim'],
                    save_file=None,
                    show_fig=False
                )
                if save_file:
                    save_plot(fig, save_file)
                click.echo(f"Generated individual profiles: individual{ext}")
            
            if composite:
                save_file = get_save_path(output_dir, 'composite', ext)
                fig = plot_composite_profile(
                    data['R'], data['x'], data['y'], data['z'],
                    dim=data['dim'],
                    save_file=None,
                    show_fig=False
                )
                if save_file:
                    save_plot(fig, save_file)
                click.echo(f"Generated composite profile: composite{ext}")
            
            if line:
                save_file = get_save_path(output_dir, 'line', ext)
                fig = plot_line_profile(
                    data['R'], data['x'], data['y'], data['z'],
                    direction=[1, 1, 1],
                    dim=data['dim'],
                    save_file=None,
                    show_fig=False
                )
                if save_file:
                    save_plot(fig, save_file)
                click.echo(f"Generated line profile: line{ext}")
            
            if contour:
                save_file = get_save_path(output_dir, 'contour', ext)
                fig = plot_contour(
                    data['R'], data['x'], data['y'], data['z'],
                    dim=data['dim'],
                    save_file=None,
                    show_fig=False
                )
                if save_file:
                    save_plot(fig, save_file)
                click.echo(f"Generated contour plot: contour{ext}")
            
            if scattering:
                save_file = get_save_path(output_dir, 'scattering', ext)
                fig = plot_scattering(
                    data['R'], data['x'], data['y'], data['z'],
                    save_file=None,
                    show_fig=False
                )
                if save_file:
                    save_plot(fig, save_file)
                click.echo(f"Generated scattering plot: scattering{ext}")
    
    except Exception as e:
        import traceback
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--field', '-f', default=0, help='Field index for FTS files')
def info(filename, field):
    """Display information about an r-grid file."""
    try:
        data = load_data(filename, field)
        R = data['R']
        click.echo(f"File: {filename}")
        click.echo(f"Crystal system: {data['lattype']}")
        click.echo(f"Dimensionality: {data['dim']}D")
        click.echo(f"Grid size: {R.shape[0]} x {R.shape[1]} x {R.shape[2]}")
        click.echo(f"Number of species: {R.shape[3]}")
        
        for i in range(R.shape[3]):
            min_val = R[:, :, :, i].min()
            max_val = R[:, :, :, i].max()
            mean_val = R[:, :, :, i].mean()
            click.echo(f"  Species {chr(65+i)}: min={min_val:.4f}, max={max_val:.4f}, mean={mean_val:.4f}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('species', type=int)
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['html', 'png', 'svg']), default='html',
              help='Output format')
@click.option('--isovalue', '-i', type=float, help='Isovalue for isosurface')
def isosurface(filename, species, output, format, isovalue):
    """Generate a 3D isosurface for a specific species."""
    try:
        data = load_data(filename)
        
        from polymer_visual.plots.individual import plot_single_isosurface
        
        if output:
            save_file = output if output.endswith(f'.{format}') else f'{output}.{format}'
        else:
            save_file = f'isosurface_{chr(65+species)}.{format}'
        
        fig = plot_single_isosurface(
            data['R'], data['x'], data['y'], data['z'],
            species_idx=species,
            isovalue=isovalue,
            mono_label=chr(65 + species),
            show_fig=False
        )
        
        if save_file:
            save_plot(fig, save_file)
        
        click.echo(f"Generated isosurface for species {chr(65+species)}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('direction', nargs=3, type=float)
@click.option('--start', '-s', nargs=3, default=[0, 0, 0], help='Starting point')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['html', 'png', 'svg']), default='html',
              help='Output format')
def line(filename, direction, start, output, format):
    """Generate a 1D line profile."""
    try:
        data = load_data(filename)
        
        if output:
            save_file = output if output.endswith(f'.{format}') else f'{output}.{format}'
        else:
            save_file = f'line_profile.{format}'
        
        fig = plot_line_profile(
            data['R'], data['x'], data['y'], data['z'],
            direction=direction,
            startloc=start,
            dim=data['dim'],
            save_file=None,
            show_fig=False
        )
        
        if save_file:
            save_plot(fig, save_file)
        
        click.echo(f"Generated line profile along [{direction[0]} {direction[1]} {direction[2]}]")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
