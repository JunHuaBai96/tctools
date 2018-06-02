import numpy as np
import matplotlib.pyplot as plt


def load_exp_datafile(fname, blocks=False):
    """
    Load Thermo-Calc experimental datafile generated by 
    MAKE_EXPERIMENTAL_DATAFILE command

    Parameters
    ----------
    fname : str
        Filename to read
    blocks: boolean, optional
        If True, returns data separated by blocks as delimited in the
        exp datafile. Otherwise returns a single column x and y arrays;
        default: False

    Returns
    -------
    x, y, xlab, ylab, xlim, ylim: tuple
        - x, y: np.array
            x and y coordinates
        - xlab, ylab: str
            x and y axes labels
        - xlim, ylim: list length 2
            limits of x and y axes
    """
    blockin = False
    clip = True

    with open(fname) as f:
        x, y = [], []
        xlab, ylab = '', ''
        xlim, ylim = [], []

        for line in f:
            line = line.strip(' \t\n')
            arr = line.split()  # split line in the spaces into list

            if len(arr) > 0:
                if arr[0] == 'BLOCK':   # block begins
                    xblock = []
                    yblock = []
                    blockin = True

                if arr[0] == 'BLOCKEND':    # block ends
                    x.append(xblock)
                    y.append(yblock)
                    blockin = False

            if len(arr) > 1:
                if arr[0] == 'XTEXT':   # reads xlab
                    xlab = ' '.join(arr[1:])

                if arr[0] == 'YTEXT':   # reads ylab
                    ylab = ' '.join(arr[1:])

                if arr[0] == 'CLIP' and arr[1] == 'ON':     # clip begins
                    clip = True

                if arr[0] == 'CLIP' and arr[1] == 'OFF':    # clip ends
                    clip = False

                if blockin and clip:
                    # if line is '$ PLOTTED COLUMNS ARE ...' appends
                    # delimiter None to xblock, yblock
                    if arr[1] == 'PLOTTED':
                        xblock.append(None)
                        yblock.append(None)
                    else:
                        try:
                            xblock.append(float(arr[0]))
                            yblock.append(float(arr[1]))
                        except:
                            pass

            if len(arr) > 2:
                if arr[0] == 'XSCALE':  # reads xlim
                    xlim.append(float(arr[1]))
                    xlim.append(float(arr[2]))

                if arr[0] == 'YSCALE':  # reads ylim
                    ylim.append(float(arr[1]))
                    ylim.append(float(arr[2]))

    if not blocks:
        newx, newy = [], []
        # delimits each block by appending a None item
        for xblock, yblock in zip(x, y):
            newx += xblock + [None]
            newy += yblock + [None]
        x, y = newx, newy

    return (x, y, xlab, ylab, xlim, ylim)


def plot_exp_datafile(fname, ax=None, blocks=False, *args, **kwargs):
    """
    Plots Thermo-Calc experimental datafile generated by 
    MAKE_EXPERIMENTAL_DATAFILE command

    Parameters
    ----------
    fname: str
        Filename to read
    ax: matplotlib AxesSubplot object, optional
        Plots in the provided ax object. Otherwise, creates ax object;
        default: None
    blocks: boolean, optional
        If True, returns data separated by blocks as delimited in the
        exp datafile. Otherwise returns a single column x and y arrays;
        default: False
    *args and **kwargs: optional arguments passed to ax.plot function

    Returns
    -------
    ax: matplotlib AxesSubplot object
    """
    if ax is None:
        fig, ax = plt.subplots()

    x, y, xlab, ylab, xlim, ylim = load_exp_datafile(fname, blocks=blocks)

    if blocks:
        for xb, yb in zip(x, y):
            ax.plot(xb, yb, *args, **kwargs)
    else:
        ax.plot(x, y, *args, **kwargs)

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    return ax