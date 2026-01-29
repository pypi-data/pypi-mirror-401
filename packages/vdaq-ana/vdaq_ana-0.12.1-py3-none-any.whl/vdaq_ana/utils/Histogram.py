#!/usr/bin/env python3
"""A simple implementation of a histogram."""

import json
import random
import math
import sys
import numpy as np
import matplotlib.pyplot as plt

from vdaq_ana.utils.HstStats import Stats

class Histogram(object):
    """A 1D Histogram.

    Attributes
    ----------
        name:   The name of the histogram
        title:  The title of the histogram
        nbin:   The number of bins
        xmin:   The minimum value of the axis
        xmax:   The maximun values if the axis
        data:   The bin content
        stats (Stats):  The statistics "recorder" of the Histogram.

    """

    def __init__(self, name, title="", nbin=1, xmin=0.0, xmax=1.0, data=None, file=None):
        """Initialization.

        Args:
        ----
            name (str): The name
            title (str): The title
            nbin (int): Number of bins
            xmin (float): Minimum value of axis
            xmax (float): Maximum value of axis
            data (tuple): a tuple n,bins where n is the values of the bins and bins the bin edges.
            file (HistFile): if given, the HistFile object where the Histogram will be stored.

        """
        self.name = name
        self.title = title
        self.ax = None
        self.stats = Stats()

        self.nbin = nbin
        self.xmin = xmin
        self.xmax = xmax
        if data is None:
            self.data = np.zeros(self.nbin)
            self.adjust()

        else:
            if len(data[0])+1 != len(data[1]):
                print("Wrong data input. len(bins) shuld be len(n)+1")
                return

            self.nbin = len(data[0])
            self.xmin = data[1][0]
            self.xmax = data[1][-1]
            self.data = np.array(data[0])
            self.adjust()
            for x, val in zip(self.data, self.get_centers()):
                self.stats.add(x, w=val)
                self.hsum += val
                self.tsum += val


        if file is not None:
            try:
                file.add(self)
            except ValueError:
                print("Histogram name {} already in file.".format(name))

    def adjust(self):
        """Sets/Adjust other attributes of the Histogram.

        Sets the values of range, step and other attributes.
        """
        self.range = self.xmax - self.xmin
        self.step = self.range / float(self.nbin)
        self.hsum = 0.0
        self.tsum = 0.0
        self.hsum = np.sum(self.data)
        self.tsum = self.hsum

    def bin_center(self, ibin):
        """Return center value of bin.

        Args:
        ----
            ibin (int): The bin

        Returns
        -------
            [float]: The X value at the center of the bin.

        """
        return self.xmin + (0.5 + ibin) * self.step

    def bin(self, x):
        """The bin corresponding to the given X value.

        Args:
            x (float): Value

        Returns
        -------
            [int]: Bin number where the given value would fall.

        """
        return int(self.nbin * (x - self.xmin) / self.range)

    def fill(self, x, w=1.0):
        """Fills the histogram.

        Args:
        ----
            x (float): The value of the abscissa to fill.
            w (float, optional): The weight used. Defaults to 1.0.

        """
        if not math.isfinite(x) or x==sys.float_info.max:
            return

        self.stats.add(x, 0, w)
        ibin = self.bin(x)
        self.tsum += w
        if ibin >= 0 and ibin < self.nbin:
            self.data[ibin] += w
            self.hsum += w

    def write(self):
        """Return a string that can be saved in a file.

        Returns
        -------
        A JSON representation of the Histogram.

        """
        out = json.dumps(
            {"hst": {
                "type": "1d",
                "name": self.name,
                "title": self.title,
                "nbin": self.nbin,
                "xmin": self.xmin,
                "xmax": self.xmax,
                "data": [x for x in self.data],
                "stats": {
                    "nn": self.stats.nn,
                    "ss": self.stats.ss
                    }
                }
             })
        return out

    def draw(self, ax=None, xlabel=None, ylabel=None, dpi=None, **kwargs):
        """Draw the histogram."""
        if ax is None:
            _, ax = plt.subplots(1, 1, tight_layout=True, dpi=dpi)

        self.ax = ax
        ax.set_title(self.title)

        ax.stairs(self.data, self.get_bins(), **kwargs)
        if xlabel:
            ax.set_xlabel(xlabel)

        if ylabel:
            ax.set_ylabel(ylabel)

        return ax

    def read(self, value):
        """Read histogram values from memory.

        Args:
        ----
            value (str): JSON representation as produced in Histogram.write

        """
        try:
            obj = json.loads(value)['hst']
        except TypeError:
            obj = value["hst"]

        self.name = obj['name']
        self.title = obj['title']
        self.nbin = int(obj['nbin'])
        self.xmin = float(obj['xmin'])
        self.xmax = float(obj['xmax'])
        self.data = np.array(obj['data'])
        self.stats.nn = obj["stats"]["nn"]
        self.stats.ss = obj["stats"]["ss"]

        self.adjust()

    def dump(self):
        """Prints the contents."""
        print("Histogram:", self.name, '[', self.title, ']')
        print(self.nbin, self.xmin, self.xmax, 'step', self.step)
        maxV = max(self.data)
        for ibin in range(0, self.nbin):
            ncol = int(40*self.data[ibin]/maxV)
            if ncol:
                line = ncol*'X'
                print("{:3d} {}".format(ibin, line))
            #if i > 0 and not (i % 6):
            #    print('')
            #print("%12.1f" % self.data[i], end=' ')

        print('')

    def get_centers(self):
        """Return bin centers."""
        hstep = self.step/2.0
        bins = np.arange(self.xmin+hstep, self.xmax+hstep, self.step)
        return bins

    def mean(self) -> float:
        """REturn mean value."""
        return self.stats.mean(0)

    def std(self) -> float:
        """Return std of distribution."""
        return self.stats.std(0)

    def get_bins(self) -> np.ndarray:
        """Return bin edges."""
        hstep = self.step/2.0
        bins = np.arange(self.xmin-hstep, self.xmax+hstep, self.step)
        return bins

    @staticmethod
    def load_histogram(jobj):
        """Create a histogram object from the JSon serialization."""
        hst = Histogram("")
        hst.read(jobj)
        return hst

def test_hst():
    """Tests the Histogram Object."""
    hst = Histogram("Random", "The histogram title", 50, 0., 50.)
    for _ in range(0, 10000):
        if random.random() > 0.6:
            val = random.gauss(12.5, 2.0)
        else:
            val = random.gauss(30.0, 2)

        val = random.gauss(25, 5.0)
        hst.fill(val)

    print("Mean: {:.4f} std: {:.4f}".format(hst.mean(), hst.std()))
    ss = hst.write()
    hst.draw(xlabel="X axis", ylabel="Y axis")

    # Creat a new histogram from JSon.
    hnew = Histogram.load_histogram(ss)
    hnew.dump()

if __name__ == "__main__":
    test_hst()
