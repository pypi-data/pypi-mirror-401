#!/usr/bin/env python3
"""A simple implementation of a histogram."""

import json
import math
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

from vdaq_ana.utils.HstStats import Stats

class Histogram2D(object):
    """A Histogram.

    Attributes
    ----------
        name: The name of the histogram
        title: The title of the histogram
        nbinX: The number of bins in X
        xmin: The minimum value of the X axis
        xmax:  The maximun values if the X axis
        nbinY: The number of bins in X
        ymin: The minimum value of the X axis
        ymax:  The maximun values if the X axis

        data:
            The bin content

    """

    def __init__(self, name, title="title", nx=1, xmin=0.0, xmax=1.0, ny=1, ymin=0.0, ymax=1.0, file=None):
        """Initialization.

        Args:
        ----
            name (str): The name
            title (str): The title
            nx (int): Number of bins
            xmin (float): Minimum value of X axis
            xmax (float): Maximum value of X axis
            ny (int): Number of bins
            ymin (float): Minimum value of Y axis
            ymax (float): Maximum value of Y axis

        """
        self.name = name
        self.title = title
        self.nbinX = nx
        self.xmin = xmin
        self.xmax = xmax
        self.nbinY = ny
        self.ymin = ymin
        self.ymax = ymax
        self.data = np.zeros([ny, nx])
        self.ax = None
        self.adjust()
        self.stats = Stats()

        if file is not None:
            try:
                file.add(self)
            except ValueError:
                print("Histogram name {} already in file.".format(name))

    def adjust(self):
        """Sets other attributes of the Histogram.

        Sets the values of range, step and other attributes.
        """
        self.xrange = self.xmax - self.xmin
        self.stepx = self.xrange / float(self.nbinX)
        self.yrange = self.ymax - self.ymin
        self.stepy = self.yrange / float(self.nbinY)
        self.hsum = 0.0
        self.tsum = 0.0
        self.hsum = np.sum(self.data)
        self.tsum = self.hsum

    def bin_center(self, ix, iy):
        """Return center value of bin.

        Args:
            ix (int): The x bin
            iy (int): the y bin

        Returns
        -------
            [float, float]: The X and Y values at the center of the cell.

        """
        X = self.xmin + (0.5 + ix) * self.stepx
        Y = self.ymin + (0.5 + iy) * self.stepy
        return np.array([X, Y])

    def binX(self, x):
        """The X bin corresponding to the given X value.

        Args:
            x (float): Value

        Returns
        -------
            [int]: Bin number where the given value would fall.

        """
        return int(self.nbinX * (x - self.xmin) / self.xrange)

    def binY(self, y):
        """The Y bin corresponding to the given Y value.

        Args:
            y (float): Value

        Returns
        -------
            [int]: Bin number where the given value would fall.

        """
        return int(self.nbinY * (y - self.ymin) / self.xrange)

    def fill(self, x, y, w=1.0):
        """Fills the histogram.

        Args:
        ----
            x (float): The value X.
            Y (float): The value Y.
            w (float, optional): The weight used. Defaults to 1.0.

        """
        if not math.isfinite(x) or x==sys.float_info.max:
            return

        if not math.isfinite(y) or y==sys.float_info.max:
            return

        self.stats.add(x, y, w)
        ix = self.binX(x)
        iy = self.binY(y)
        self.tsum += w
        if ix >= 0 and ix < self.nbinX:
            if iy >= 0 and iy < self.nbinY:
                self.data[iy, ix] += w
                self.hsum += w

    def draw(self, ax=None, xlabel=None, ylabel=None, cmap=None, dpi=None, **kwargs):
        """Draw the histogram.
        """
        if ax is None:
            _, ax = plt.subplots(1, 1, tight_layout=True, dpi=dpi)

        self.ax = ax
        ax.set_title(self.title)
        ax.imshow(self.data, origin="lower", cmap=cmap,
                  extent=(self.xmin, self.xmax, self.ymin, self.ymax),
                  **kwargs)

        if xlabel:
            ax.set_xlabel(xlabel)

        if ylabel:
            ax.set_ylabel(ylabel)

        return ax

    def write(self):
        """Return a json structure that can be saved in a file.

        Returns
        -------
        A JSON representation of the Histogram.

        """
        out = json.dumps(
            {"hst": {
                "type": "2d",
                "name": self.name,
                "title": self.title,
                "nbinX": self.nbinX,
                "xmin": self.xmin,
                "xmax": self.xmax,
                "nbinY": self.nbinY,
                "ymin": self.ymin,
                "ymax": self.ymax,
                "data": [x for x in self.data.reshape(-1)],
                "stats": {
                    "nn": self.stats.nn,
                    "ss": self.stats.ss
                    }
                }
             })
        return out

    def read(self, val):
        """Read histogram values from memory.

        Args:
        ----
            val (str): JSON representation as produced in Histogram.write

        """
        try:
            obj = json.loads(val)['hst']
        except TypeError:
            obj = val["hst"]

        self.name = obj['name']
        self.title = obj['title']
        self.nbinX = int(obj['nbinX'])
        self.xmin = float(obj['xmin'])
        self.xmax = float(obj['xmax'])
        self.nbinY = int(obj['nbinY'])
        self.ymin = float(obj['ymin'])
        self.ymax = float(obj['ymax'])
        self.stats.nn = obj["stats"]["nn"]
        self.stats.ss = obj["stats"]["ss"]

        self.data = np.array(obj['data']).reshape(self.nbinX, self.nbinY)
        self.adjust()

    def dump(self):
        """Prints the contents."""
        values = " .+xoXO*"
        nval = len(values)
        print("Histogram:", self.name, '[', self.title, ']')
        print("X-axis: ", self.nbinX, self.xmin, self.xmax, 'step', self.stepx)
        print("Y-axis: ", self.nbinY, self.ymin, self.ymax, 'step', self.stepy)
        print("")
        maxV = np.max(self.data)
        if maxV > 0:
            def print_x_axis():
                line = '+'
                for _ in range(0, self.nbinX):
                    line+='-'
                line+='+'
                print(line)

            print_x_axis()
            for iy in range(self.nbinY-1, -1, -1):
                line = "|"
                for ix in range(0, self.nbinX):
                    ic = int( (nval-1) * self.data[iy, ix]/maxV )
                    line += values[ic]
                line += '|'

                print(line)

            print_x_axis()

        print('')

    def get_x_centers(self):
        """Return bin centers in X."""
        hstep = self.stepx/2.0
        bins = np.arange(self.xmin+hstep, self.xmax+hstep, self.stepx)
        return bins

    def get_y_centers(self):
        """Return bin centers in Y."""
        hstep = self.stepy/2.0
        bins = np.arange(self.ymin+hstep, self.ymax+hstep, self.stepx)
        return bins

    def meanX(self) -> float:
        """REturn mean value."""
        return self.stats.mean(0)

    def stdX(self) -> float:
        """Return std of distribution."""
        return self.stats.std(0)

    def get_x_bin_edges(self) -> np.ndarray:
        """Return bin edges."""
        hstep = self.stepx/2.0
        bins = np.arange(self.xmin-hstep, self.xmax+hstep, self.stepx)
        return bins

    def meanY(self) -> float:
        """REturn mean value."""
        return self.stats.mean(1)

    def stdY(self) -> float:
        """Return std of distribution."""
        return self.stats.std(1)

    def get_y_bins_edges(self) -> np.ndarray:
        """Return bin edges."""
        hstep = self.stepy/2.0
        bins = np.arange(self.ymin-hstep, self.ymax+hstep, self.stepy)
        return bins

    @staticmethod
    def load_histogram2d(jobj):
        """Create a new histogram from Json serialization."""
        hst = Histogram2D("")
        hst.read(jobj)
        return hst

def test_hst2d():
    """ Test Histogram2D objects."""
    hst = Histogram2D("Random", "The histogram title", 25, 0., 50., 25, 0.,50)
    muX = 10
    sigmaX = 2
    muY = 15
    sigmaY = 5
    for _ in range(0, 10000):
        x = random.gauss(muX, sigmaX)
        y = random.gauss(muY, sigmaY)
        hst.fill(x, y)

    hst.dump()
    hst.draw()
    print("X -> Mean: {:.4f} std: {:.4f}".format(hst.meanX(), hst.stdX()))
    print("Y -> Mean: {:.4f} std: {:.4f}".format(hst.meanY(), hst.stdY()))

    ss = hst.write()

    # Create new histogram.
    hnew = Histogram2D.load_histogram2d(ss)
    hnew.dump()

if __name__ == "__main__":
    test_hst2d()
