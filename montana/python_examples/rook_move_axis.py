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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
    """
    Customer example demonstrating moving an axis through a list of setpoints.
    """, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--ip", help="The IP address of the system to control.", required=True)
    args = parser.parse_args()

    print("Connecting to remote system at %s" % (args.ip))
    rook = rook.Rook(args.ip)

    stack_num = 1
    axis_num  = 1

    # Mark encoder zero at our starting point
    rook.zero_axis(stack_num, axis_num)

    # Move through the list of target locations
    try:
        for p in [0, 10, 20, 30, 40, 50, 0]: # um
            print(f'Move absolute to {p}')
            rook.move_axis_absolute_position(stack_num, axis_num, p/1000/1000) # Convert to m
            if rook.wait_for_axis_not_moving(stack_num, axis_num):
                print('Target acquired.')
            else:
                print('Failed to acquire target before timeout occurred.')
    except KeyboardInterrupt:
        # Exit loop on ctrl-c
        pass

