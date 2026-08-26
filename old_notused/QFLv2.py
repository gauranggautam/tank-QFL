import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Scale plots for 4K resolution
mpl.rcParams['figure.dpi'] = 200        # Increase DPI
mpl.rcParams['savefig.dpi'] = 300       # Higher quality saved images
mpl.rcParams['figure.figsize'] = [10, 6]  # Default figure size in inches
mpl.rcParams['font.size'] = 14           # Increase font size for readability


# 20-category tab20 color palette using updated Matplotlib API
TAB20_COLORS = plt.colormaps['tab20'].colors

# --------------------------------------------------------------------------
def _set_tab20_cycle(ax):
    """
    Sets the color cycle of the given axes to the tab20 color palette.
    Ensures this is done only once per axes object.
    """
    if not hasattr(ax, '_color_cycle_set'):
        ax.set_prop_cycle(color=TAB20_COLORS)
        ax._color_cycle_set = True

# --------------------------------------------------------------------------

#def laser(mode='cw', cw_power=0, temp=None, softlock=None)


def plot_spectrum(input, compare=False, fig=11, id='Plot'):
    """
    Plots the photoluminescence (PL) spectrum from the input file.

    Parameters:
    - input: Path to the data file.
    - compare: Whether to overlay on an existing plot (True) or create a new one.
    - fig: Figure number to use if comparing multiple plots.
    - id: Identifier to label the plot.
    """
    v = readfile(input, encoding='latin1', multi_sweep='force')

    if compare:
        plt.figure(fig)
        ax = plt.gca()
    else:
        _, ax = plt.subplots()

    _set_tab20_cycle(ax)

    ax.plot(v[1], v[2], label=f'{id}_{os.path.basename(input)}')
    ax.set_xlim(np.min(v[1]), np.max(v[1]))
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Counts (Arb.)')
    ax.grid(True)

    ax.set_title('PL Spectrum compare' if compare else os.path.basename(input))
    ax.legend(loc='upper right')

# --------------------------------------------------------------------------
def plot_plmap(input, mode='custom', flog=False, xi=0, yi=2, zi=6, id='Plot',invxy=False):
    """
    Plots a PL map (2D spatial scan) from the input data.

    Parameters:
    - input: Path to the data file.
    - mode: Predefined mode for selecting x, y, z indices ('apd', 'spec', 'specw').
    - flog: If True, applies log10 scaling to Z axis.
    - xi, yi, zi: Custom indices if mode is 'custom'.
    - id: Identifier to label the plot.
    - invxy=True to invert xy on pl map
    """
    v = readfile(input, encoding='latin1', multi_sweep='force')
    fig, ax = plt.subplots()

    x_index, y_index, z_index = {
        'apd': (0, 2, 6),
        'spec': (0, 2, 5),
        'specw': (0, 2, 8)
    }.get(mode, (xi, yi, zi))

    Z = np.log10(v[z_index]) if flog else v[z_index]
    plmap = ax.pcolor(v[x_index], v[y_index], Z, cmap='plasma')
    cbar = fig.colorbar(plmap, ax=ax)
    cbar.set_label('Log10 Counts' if flog else 'Counts')

    if invxy:
        ax.invert_xaxis()
        ax.invert_yaxis()
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    ax.set_title(f'{id}_{os.path.basename(input)}')

# --------------------------------------------------------------------------
def plot_powerd(input, compare=False, fig=66, mode='custom', xi=2, yi=5, id='Plot'):
    """
    Plots power dependence of PL intensity from the input file.

    Parameters:
    - input: Path to the data file.
    - compare: Whether to overlay with previous plot.
    - fig: Figure number to use if comparing.
    - mode: Predefined index set ('apd', 'spec', 'specw').
    - xi, yi: Custom indices for x and y if mode is 'custom'.
    - id: Identifier to label the plot.
    """
    v = readfile(input, encoding='latin1', multi_sweep='force')

    x_index, y_index = {
        'apd': (2, 5),
        'spec': (2, 6),
        'specw': (5, 7)
    }.get(mode, (xi, yi))

    x = v[x_index] * 1000  # Convert power to mW
    y = v[y_index] - np.min(v[y_index])

    if compare:
        plt.figure(fig)
        ax = plt.gca()
    else:
        _, ax = plt.subplots()

    _set_tab20_cycle(ax)

    ax.plot(x, y, label=f'{id}_{os.path.basename(input)}')
    ax.set_title('Power dependence comparison' if compare else f'Power dependence for {os.path.basename(input)}')
    ax.set_xlabel('Power (mW)')
    ax.set_ylabel('Counts (a.u.)')
    ax.set_xlim(0, None)
    ax.set_ylim(0, None)
    ax.legend(loc='upper left')

# --------------------------------------------------------------------------
def plot_polarization(input, polar=True, mode='custom', flog=False, xi=0, yi=1):
    """
    Plots polarization dependence (as polar or Cartesian plot) of PL intensity.

    Parameters:
    - input: Path to the data file.
    - polar: Whether to plot in polar coordinates (True) or Cartesian (False).
    - mode: Predefined mode for indices ('apd', 'spec', 'specw').
    - flog: If True, applies log10 scaling to intensity values.
    - xi, yi: Custom indices for angle and intensity if mode is 'custom'.
    """
    v = readfile(input, encoding='latin1', multi_sweep='force')

    x_index, y_index = {
        'apd': (0, 4),
        'spec': (0, 5),
        'specw': (0, 6)
    }.get(mode, (xi, yi))

    x = v[x_index]
    y = v[y_index] - np.min(v[y_index])

    if polar:
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
    else:
        fig, ax = plt.subplots()
        x = np.radians(x)

    _set_tab20_cycle(ax)

    if polar:
        ax.scatter(x, y, label=os.path.basename(input), linewidth=0.5)
    else:
        ax.plot(x, y, label=os.path.basename(input))
        ax.set_xlabel('Theta (deg)')
        ax.set_ylabel('Counts (Arb.)')

    ax.set_title('Polarization dependence')
    ax.legend(loc='lower left' if polar else 'best')
    ax.grid(True)



def plot_parameters(xi,yi, xr,yr): #xi adn yi center; xr and yr total x-yrange 
    xs=xi-xr/2
    print(f'xstart= {xs}')
    xe=xi+xr/2
    print(f'xend= {xe}')
    ys=yi-yr/2
    print(f'ystart= {ys}')
    ye=yi+yr/2
    print(f'yend= {ye}')
