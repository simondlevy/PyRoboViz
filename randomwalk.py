#!/usr/bin/env python3
'''
randomwalk.py: PyRoboViz test with random walk

Copyright (C) 2018 Simon D. Levy

This file is part of PyRoboViz.

PyRoboViz is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

PyRoboViz is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http:#www.gnu.org/licenses/>.
'''


from roboviz import Visualizer
from time import time
import numpy as np
import argparse

MAP_SIZE_PIXELS = 800
MAP_SIZE_METERS = 32
SPEED_MPS       = 1

class _MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(1)

if __name__ == '__main__':

    # Parse optional command-line arguments
    parser = _MyArgumentParser(description='Visualize a random walk.')
    parser.add_argument('-s', '--seed', help='set seed for pseudo-random number generator')
    cmdargs = parser.parse_args()

    # Set seed for pseudo-random number generator if indicated
    if not cmdargs.seed is None:
        np.random.seed(int(cmdargs.seed))

    # Create a Visualizer object with a trajectory, centered at 0,0

    viz = Visualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'Random Walk', True)

    # Start in the center of the map with a random heading
    pose = np.array([0,0,360*np.random.random()])

    # Start timing
    prevtime = time()

    # Loop till user closes the display
    while True:

        # Set current pose in visualizer the display, exiting gracefully if user closes it
        if not viz.display(*pose):
            exit(0)

        # Rotate randomly and move forward
        currtime = time()
        s = SPEED_MPS * (currtime - prevtime)
        prevtime = currtime
        theta = np.radians(pose[2])
        pose[0] += s * np.cos(theta)
        pose[1] += s * np.sin(theta)
        pose[2] += 10 * np.random.randn()
