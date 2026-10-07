#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import threading
from threading import Thread
import numpy as np
from scipy.optimize import fsolve

# class teleop_coords(Node):
    # def __init__():
        # super.__init__().info("coords_control")

def main(args = None):
    l1 = 45
    l2 = 60
    l3 = 20

    uwu = True

    while uwu:
        try:           
            info = [float(x) for x in input("Enter x y z joint4: ").split()]
            if len(info)==4:
                uwu = False
            else: print("entrada no valida")
        except Exception as e:
            print(e)
    


