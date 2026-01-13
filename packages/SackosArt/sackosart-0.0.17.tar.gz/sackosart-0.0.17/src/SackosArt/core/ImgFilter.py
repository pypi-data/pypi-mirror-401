#!/usr/bin/env python3
# *****************************************************************************
"""                            ImgFilter Class
 
         Overview: 
 
        Author(s): Josh Sackos
          License: Licensed under the MIT License. See LICENSE file for details
         Revision: 0.0.1
    Revision Date: 12/25/2025
    Tool Versions: Python     3.13.3
                   Numpy      2.2.6
 
            Notes: None
"""
# *****************************************************************************

# ----* Native Imports *----
import sys;
import os;

# ----* Third Party Imports *----
import numpy as np;
import matplotlib.pyplot as plt;
import math;
from SackosArt.core.CoordPolar import CoordPolar;
from SackosArt.types.Equation   import Equation;
from SackosArt.types           import MathVar;

class ImgFilter():
    # ======================================================================
    """Description: Parent class for an image filter.

        Attributes: version : Current version of class.

          Examples: None
           Related: None
    """
    # ======================================================================

    # ++++ Class Variables ++++
    version = 0.1;

    def __init__(self, draw_mech) -> None:
        # ///////////////////////////////////////////////////////////////
        """Description: Class constructor
             Arguments: None
               Returns: None
        """
        # ///////////////////////////////////////////////////////////////
        self.pi = math.pi;

        return;

    def __del__(self) -> None:
        # ///////////////////////////////////////////////////////////////
        """Description: Class destructor
             Arguments: None
               Returns: None
        """
        # ///////////////////////////////////////////////////////////////

        return;

    def draw(self, pixel_src, pixel_t, vars=False) -> None:
        # ///////////////////////////////////////////////////////////////
        """Description: Function that 'draws' a shape, equation, etc.
                        into a matrix.
             Arguments: pixel_src : Pixel data, equation, etc., where all
                                    filter pixel data comes from.
                        pixel_t   : Pixel data types
                                      -> kernel
                                      -> ranges
                                      -> equation
                        vars      : Variables if an equation
               Returns: None
        """
        # ///////////////////////////////////////////////////////////////
        dtype = type(pixel_src);
        print(dtype);
        sys.exit();
        return;

# -----------------------------------------------------------------------------
#                           Application Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    filter_inst = ImgFilter();
    equation    = 's(r,θ) = r+bθ';

    r = MathVar(name='radius', range=(0,10)          , angular=False);
    b = MathVar(name='boom'  , range=(1, 1)          , angular=False);
    θ = MathVar(name='theta' , range=(0, 4.5*self.pi), angular=True );
    vars        = {
                   'r' : r,
                   'b' : b,
                   'θ' : θ
                  };
    
    filter_inst.draw(equation, pixel_t='equation', vars=vars);

    raise SystemExit(0);
