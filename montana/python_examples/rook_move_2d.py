#!/usr/bin/env python3
#

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

def _do_experiment(xy):
    print(f'Taking measurement @ {xy}')
    time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
    """
    Customer example demonstrating moving an axis through a list of setpoints.
    """, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--ip", help="The IP address of the system to control.", required=True)
    args = parser.parse_args()

    print("Connecting to remote system at %s" % (args.ip))
    rook = rook.Rook(args.ip)

    stack_num  = 1

    # This example was designed for a horizontal Cryo-Optic system where:
    #  Axis1 = Focus
    #  Axis2 = x
    #  Axis3 = y
    x_axis_num = 2
    y_axis_num = 3

    # Move through the list of target locations
    try:
        for xy in [(0,0), (0, 10), (-10, 10), (-10, 0), (0, 0)]: # um
            print(f'Move absolute to {xy}')

            # Move to x location
            rook.move_axis_absolute_position(stack_num, x_axis_num, xy[0]/1000/1000, True) # Convert to m

            # Move to y location
            rook.move_axis_absolute_position(stack_num, y_axis_num, xy[1]/1000/1000, True) # Convert to m
            
            # At x,y location, take measurement 
            _do_experiment(xy)
            
    except KeyboardInterrupt:
        # Exit loop on ctrl-c
        pass

