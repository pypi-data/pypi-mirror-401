#!/usr/bin/env/python3
"""An Object to store histograms."""
import random
import json
import gzip
import numpy as np
from vdaq_ana.utils import Histogram, Histogram2D


class HstEncoder(json.JSONEncoder):
    """Encoder to dump in JSon."""

    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.floating):
            return float(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        elif isinstance(o, (Histogram.Histogram, Histogram2D.Histogram2D)):
            return o.write()
        else:
            return vars(o)


class HistFile(dict):
    """Store and eventually save and load Histogram and Histogram2 objects.

    Objects are stored in dictionary, where each histogram has an associated
    name. duplicated names are, therefore, not allowed.

    """
    def __init__(self, inp=None, file=None, out=None):
        """Initialization.

        Args:
            inp: can be another HistFile object or a JSon objects withthe proper
                 format.

            file: if given, it will open that file a load the existing
                  histograms.

            out: the output file file name if we want to save the HistFile
                 contents on deltetion.
        """
        if inp is not None:
            if isinstance(inp,dict):
                super(HistFile,self).__init__(inp)

            else:
                super(HistFile,self).__init__()
                try:
                    si = self.__setitem__
                    for k,v in inp:
                        si(k,v)

                except Exception:
                    pass

        self.out = out

        if file:
            self.read(file)

    def __del__(self):
        """Destruction.

        Save to file if out is not None
        """
        if self.out:
            self.write(self.out)

    def __setitem__(self, name, hst):
        """Adds a new item.

        It will comlpain if name exists already and thehistogram will not be
        added.

        Args:
            name: histogram name
            hst: Histogram
        """
        try:
            self.__getitem__(name)
            raise ValueError("duplicate key '{0}' found".format(name))

        except KeyError:
            super(HistFile,self).__setitem__(name, hst)

    def add(self, hst):
        """Add a hisogram."""
        self[hst.name] = hst

    def write(self, fname):
        """Write histograms into a file."""

        with gzip.open(fname, 'wt') as ofile:
            json.dump(self, ofile, cls=HstEncoder)
            print("Saving histograms in {}".format(fname))

        self.out = None

    def read(self, fname):
        """Load histograms from file."""
        with gzip.open(fname, 'rt') as ifile:
            jobj = json.load(ifile)

            for _, hst in jobj.items():
                j = json.loads(hst)
                H = j["hst"]
                htype = H["type"]
                if htype == "1d":
                    H = Histogram.Histogram.load_histogram(j)

                elif htype == "2d":
                    H = Histogram2D.Histogram2D.load_histogram2d(j)

                else:
                    H = None

                if H:
                    self.add(H)

    def ls(self):
        """return list of histograms."""
        mxlen = 0
        for key in self.keys():
            ln = len(key)
            if ln > mxlen:
                mxlen = ln

        fmt = "{:%d} - {}" % mxlen
        for key, hst in self.items():
            print(fmt.format(key, hst.title))


def test_hstfile():
    """Test."""
    hfile = HistFile(file="/tmp/nave-6mm-150MeV.hstz")
    hst = Histogram.Histogram("rand1d", "The histogram title", 50, 0., 50., file=hfile)
    hst2d = Histogram2D.Histogram2D("rand2d", "The histogram title", 25, 0., 50., 25, 0.,50, file=hfile)

    for _ in range(0, 10000):
        hst.fill(random.gauss(25.0, 5.0))

        x = random.gauss(25, 2)
        y = random.gauss(25, 5)
        hst2d.fill(x, y)

    hst.dump()
    hst2d.dump()
    print("\n\n")

    hfile.write("ofile.hst.gz")

    hfile = HistFile(file="ofile.hst.gz")

    hfile["rand1d"].dump()
    hfile["rand2d"].dump()
    hfile.ls()

if __name__ == "__main__":
    test_hstfile()
