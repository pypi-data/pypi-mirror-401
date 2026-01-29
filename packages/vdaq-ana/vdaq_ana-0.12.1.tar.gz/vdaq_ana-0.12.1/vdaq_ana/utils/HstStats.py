"""A class for statatistics."""
import math
import random

class Stats(object):
    """ Compute statistics in 2D """

    def __init__(self):
        """ The array with values
            [ Sx, Sy, Sxx, Syy, Sxy ]
        """
        self.nn = 0.0
        self.ss = [0.0, 0.0, 0.0, 0.0, 0.0]

    def add(self, x, y=0.0, w=1.0):
        """ Add a new point
        """
        self.nn += w
        for i in range(0, 2):
            if i == 0:
                xv = x
            else:
                xv = y

            vv = w * xv
            self.ss[i] += vv
            self.ss[2 + i] += vv * xv

        self.ss[4] += w * x * y

    def mean(self, i=0):
        """Return mean value."""
        if self.nn == 0.:
            return 0.0

        return self.ss[i] / self.nn

    def rms(self, i=0):
        """Return RMS."""
        if self.nn < 2.0:
            return 0.0

        m = self.mean(i)
        val = self.ss[2 + i] / self.nn - m * m

        return val

    def std(self, i=0):
        """REturn std dev."""
        return math.sqrt(self.rms(i))

    def correlation(self):
        """Return correlation."""
        x = self.mean(0)
        y = self.mean(1)
        sxy = self.std(0) * self.std(1)
        if sxy == 0:
            val = 0.0
        else:
            val = (self.ss[4] / self.nn - x * y) / sxy

        return val


def test_stats():
    """ Test the Stats object."""
    S = Stats()
    for _ in range(10000):
        x = random.gauss(0., 5.)
        y = random.gauss(0.6*x, 5)
        S.add(x, y)

    print("X mean {:.4f} std: {:.4f}".format(S.mean(0), S.std(0)))
    print("Y mean {:.4f} std: {:.4f}".format(S.mean(1), S.std(1)))
    print("Correlation: {:.4f}".format(S.correlation()))

if __name__ == "__main__":
    test_stats()
