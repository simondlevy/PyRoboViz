'''
roboviz.py - Python classes for displaying maps and robots

Requires: numpy, matplotlib

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

'''
# Essential imports
import matplotlib.pyplot as plt
import matplotlib.cm as colormap
import matplotlib.lines as mlines
import numpy as np

# This helps with Raspberry Pi
import matplotlib
matplotlib.use('TkAgg')

class Visualizer(object):

    # Robot display params
    ROBOT_HEIGHT_M = 0.5
    ROBOT_WIDTH_M  = 0.3

    def __init__(self, map_size_pixels, map_size_meters, title='RoboViz', trajectory=False):
    
        # Store constants for update
        map_size_meters = map_size_meters
        self.map_size_pixels = map_size_pixels
        self.map_scale_meters_per_pixel = map_size_meters / float(map_size_pixels)

        # Create a byte array to display the map with a color overlay
        self.bgrbytes = bytearray(map_size_pixels * map_size_pixels * 3)
        
        # Make a nice big (10"x10") figure
        fig = plt.figure(figsize=(10,10))

        # Store Python ID of figure to detect window close
        self.figid = id(fig)

        fig.canvas.set_window_title('SLAM')
        plt.title(title)

        self.ax = fig.gca()
        self.ax.set_aspect("auto")
        self.ax.set_autoscale_on(True)

        # Use an "artist" to speed up map drawing
        self.img_artist = None

        # We base the axis on pixels, to support displaying the map
        self.ax.set_xlim([0, map_size_pixels])
        self.ax.set_ylim([0, map_size_pixels])

        # Hence we must relabel the axis ticks to show millimeters
        half = self.map_size_pixels / 2
        ticks = np.arange(-half,half+100,100)
        labels = [str(self.map_scale_meters_per_pixel * tick) for tick in ticks]
        self.ax.set_xticklabels(labels)
        self.ax.set_yticklabels(labels)

        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')

        self.ax.grid(False)

        # Start vehicle at center
        map_center_m = self.map_scale_meters_per_pixel * map_size_pixels
        self._add_vehicle(map_center_m,map_center_m,0)

        # Store previous position for trjectory
        self.prevpos = None
        self.showtraj = trajectory

    def displayMap(self, mapbytes):

        mapimg = np.reshape(np.frombuffer(mapbytes, dtype=np.uint8), (self.map_size_pixels, self.map_size_pixels))

        # Pause to allow display to refresh
        plt.pause(.001)

        if self.img_artist is None:

            self.img_artist = self.ax.imshow(mapimg, cmap=colormap.gray)

        else:

            self.img_artist.set_data(mapimg)

    def setPose(self, x_m, y_m, theta_deg):
        '''
        Sets vehicle pose:
        X:      left/right   (m)
        Y:      forward/back (m)
        theta:  rotation (degrees)
        '''

        # Remove old arrow
        self.vehicle.remove()
        
        # Create a new arrow
        self._add_vehicle(x_m, y_m, theta_deg)

        # Show trajectory if indicated
        currpos = self._m2pix(x_m,y_m)
        if self.showtraj and not self.prevpos is None:
            self.ax.add_line(mlines.Line2D((self.prevpos[0],currpos[0]), (self.prevpos[1],currpos[1])))
        self.prevpos = currpos

    def refresh(self):                   

        # If we have a new figure, something went wrong (closing figure failed)
        if self.figid != id(plt.gcf()):
            return False

        # Redraw current objects without blocking
        plt.draw()

        # Refresh display, setting flag on window close or keyboard interrupt
        try:
            plt.pause(.01) # Arbitrary pause to force redraw
            return True
        except:
            return False

        return True

    def _m2pix(self, x_m, y_m):

        s = self.map_scale_meters_per_pixel

        return x_m/s, y_m/s
    
    def _add_vehicle(self, x_m, y_m, theta_deg):

        #Use a very short arrow shaft to orient the head of the arrow
        dx, dy = Visualizer._rotate(0, 0, 0.1, theta_deg)

        s = self.map_scale_meters_per_pixel

        self.vehicle=self.ax.arrow(x_m/s, y_m/s, 
                dx, dy, head_width=Visualizer.ROBOT_WIDTH_M/s, 
                head_length=Visualizer.ROBOT_HEIGHT_M/s, fc='r', ec='r')

    def _rotate(x, y, r, deg):
        rad = np.radians(deg)
        c = np.cos(rad)
        s = np.sin(rad)
        dx = r * c
        dy = r * s
        return x+dx, y+dy 
