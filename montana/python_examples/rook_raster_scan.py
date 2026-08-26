#!/usr/bin/env python3
#
# Demonstrate a 2D raster scan with the Rook.

from datetime import datetime
from datetime import timedelta
import time
import argparse
import requests
import sys
import os
import random

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "pythonlibs"))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'libs')))
import rook

def _do_experiment(x_sp, y_sp):
    print(f'Taking measurement @ ({x_sp},{y_sp})')
    time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
    """
    Customer example demonstrating a 2D raster scan through a list of setpoints.
    """, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--ip", help="The IP address of the system to control.", required=True)
    args = parser.parse_args()

    print("Connecting to remote system at %s" % (args.ip))
    rook = rook.Rook(args.ip)

    stack_num = 1

    # This example was designed for a horizontal Cryo-Optic system where:
    #  Axis1 = Focus
    #  Axis2 = x
    #  Axis3 = y
    x_axis_num  = 2
    y_axis_num  = 3

    try:
        # Loop that repeats the raster scan 10 times
        for i in range(0, 10):
            # Move to starting location @ (0,0)
            rook.move_axis_absolute_position(stack_num, x_axis_num, 0, True)
            rook.move_axis_absolute_position(stack_num, y_axis_num, 0, True)
            
            # Move y axis from 0 to 100 microns in 10 micron steps
            for y_sp in range(0, -110, -10): # um
                rook.move_axis_absolute_position(stack_num, y_axis_num, y_sp/1000/1000, True) # Convert to m
                    
                # Move x axis from 0 to 100 microns in 10 micron steps
                for x_sp in range(0, 110, 10): # um
                    rook.move_axis_absolute_position(stack_num, x_axis_num, x_sp/1000/1000, True) # Convert to m

                    # At desired pixel, now perform experiment
                    _do_experiment(x_sp, y_sp)
                
    except KeyboardInterrupt:
        # Exit loop on ctrl-c
        pass
