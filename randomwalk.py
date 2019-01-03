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
from time import sleep
import numpy as np

MAP_SIZE_PIXELS = 800
MAP_SIZE_METERS = 32
SPEED_MPS       = 10
DT_SEC          = .01

# Create a Visualizer object
viz = Visualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'Random Walk', True)

# Start in the center of the map
center_m = MAP_SIZE_METERS / 2
pose = np.array([center_m,center_m,360*np.random.random()])

# Loop till user closes the display
while True:

    # Set current pose in visualizer
    viz.setPose(*pose)

    # Refresh the display, exiting gracefully if user closes it
    if not viz.refresh():
        exit(0)

    # Rotate randomly and move forward
    s = SPEED_MPS * DT_SEC 
    theta = np.radians(pose[2])
    pose[0] += s * np.cos(theta)
    pose[1] += s * np.sin(theta)
    pose[2] += 10 * np.random.randn()

    # Hang a bit before next frame
    sleep(DT_SEC)
