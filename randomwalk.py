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

viz = Visualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS*1000/MAP_SIZE_PIXELS, 'Random Walk')

pose = np.array([16000,16000,0])

while True:

    # Set current pose in visualizer
    viz.setPose(*pose)

    # Refresh the display, exiting gracefully if user closes it
    if not viz.refresh():
        exit(0)

    # Rotate randomly and move forward
    pose[0] += 1000 * SPEED_MPS * DT_SEC * np.cos(np.radians(pose[2]))
    pose[1] += 1000 * SPEED_MPS * DT_SEC * np.sin(np.radians(pose[2]))
    pose[2] += 10 * np.random.randn()

    # Hang a bit before next frame
    sleep(DT_SEC)
