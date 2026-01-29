#!/usr/bin/env python3
""" Defines a Tracer.
    A Tracer is an object that 'follows' the value of a given
    variable. It does it either tracing individual values or the
    average over a given number of values.

    The idea is that for every new value, the user calls the fill
    method. This method will call user defined funtions that have been
    registered with the register method.

"""

import asyncio
import random
import matplotlib.pyplot as plt
import numpy as np


class Tracer(object):
    """Tracer Object.

    A tracer object tracks the value of a variable with time. 

    A Tracer accepts obserbers (callback functions) which are called
    whenever a new points is added. Use the register method to register new
    observers. The signature if the callback is fcn(data, *args) where args
    is user data  given at registration.
    
    """
    ntracers = 0

    def __init__(self, npoints, name=None, average=0):
        """Define a Tracer.

        Args:
            npoints (int): Number of points in the tracer. This is the size of
                           the buffer (FIFO)
            name (str, optional): The name of the tracer. Defaults to None.
            average (int, optional): Number of points to average before adding
                                     a point in the plot. Defaults to 0, which
                                     means no average.
        """

        self.data = []
        self.average = average
        self.size = npoints
        self.cntr = 1
        self.val = 0.0
        self.observers = {}
        if name is None:
            self.name = "tracer{}".format(Tracer.ntracers)
            Tracer.ntracers += 1
        else:
            self.name = name

    def set_npoints(self, npts):
        """Set the number of points.

        Args:
            npts (int): Number of points.
        """
        if npts == self.size:
            return

        if len(self.data) > npts:
            self.data = self.data[-npts:]
            self.size = npts

    def fill(self, val):
        """ Fills the tracer with a new value.

        This will automatically add a new point in the internal FIFO depending
        on the value of average.
        """
        if self.average > 1:
            self.val = ( val + self.cntr * self.val)/(self.cntr+1.)
            self.cntr += 1
            if self.cntr % self.average == 0:
                self.add_point(self.val)
                self.cntr = 1
                self.val  = 0.

        else:
            self.add_point(val)

    def add_point(self, val):
        """Add a new point in the FIFO.

        It will also call any registered observer with the FIFO buffer as
        argument.
        """
        self.data.append(val)
        if len(self.data) > self.size:
            self.data.pop(0)

        for cb in self.observers.values():
            cb()

    def register(self, fcn, args=None):
        """Register a new observer.

        Args:
            fcn (callable): the callback function
            args: Arguments for the callback. Defaults to None.

        """
        def __callback__():
            """Function"""
            return fcn(self.data, args)

        if callable(fcn):
            self.observers[fcn] = __callback__

class Monitor:
    """Shows various Tracer objects in same plot."""
    def __init__(self, axis=None, npoints=50):
        """ Initializes the instance of the object. The parameters
            are:
                 npoints: number of points to store
        """
        self.npoints = npoints
        if axis is not None:
            self.axis = axis
            self.fig = None
        else:
            self.fig, self.axis = plt.subplots(nrows=1, ncols=1)

        self.tracers = []
        self.X = np.arange(0, self.npoints, 1)

    def add_tracer(self, T):
        """Add a new tracer

        Args:
            T (Tracer): A new tracer.
        """
        T.set_npoints(self.npoints)
        T.register(self.show)
        self.tracers.append(T)


    def show(self, *args):
        """Draws all tracers."""
        self.axis.clear()
        self.axis.grid()
        self.axis.set_xlim(0, self.npoints)
        for T in self.tracers:
            npts = len(T.data)
            if npts > 0:
                self.axis.plot(self.X[:npts], T.data[:npts], '-', label=T.name)

        self.axis.legend(fontsize="x-small")
        plt.pause(1e-15)

def update_mon(M):
    """Updates the tracers."""
    it = random.randint(0, len(M.tracers)-1)
    val = random.gauss(it, 0.1)
    M.tracers[it].add_point(val)
    #asyncio.get_event_loop().call_soon(update_mon, M)
    asyncio.get_event_loop().call_later(0.01, update_mon, M)

def test_tracer():
    """Test the Tracer and Monitor objects."""
    loop = asyncio.new_event_loop()
    monitor = Monitor()

    for i in range(5):
        monitor.add_tracer(Tracer(50, name="kk{}".format(i)))

    loop.call_later(0.1, update_mon, monitor)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Arrggggg")

if __name__ == "__main__":
    test_tracer()
