#!/usr/bin/env python3
# *****************************************************************************
"""                           MathEquation Class
 
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
from   SackosArt.core.CoordPolar import CoordPolar;
from   SackosArt.types.MathVar   import MathVar;


class MathEquation():
    # ======================================================================
    """Description: Parent class for a math equation.

        Attributes: version : Current version of class.

          Examples: None
           Related: None
    """
    # ======================================================================

    # ++++ Class Variables ++++
    version = 0.1;

    def __init__(self, equation) -> None:
        # ///////////////////////////////////////////////////////////////
        """Description: Class constructor
             Arguments: None
               Returns: None
        """
        # ///////////////////////////////////////////////////////////////
        self.pi       = math.pi;
        self.equation = equation;
        return;

    def __del__(self) -> None:
        # ///////////////////////////////////////////////////////////////
        """Description: Class destructor
             Arguments: None
               Returns: None
        """
        # ///////////////////////////////////////////////////////////////

        return;

    def decodeEquation(self) -> None:
        # ///////////////////////////////////////////////////////////////
        """Description: Function that 'draws' a shape, equation, etc.
                        into a matrix.
             Arguments: None
               Returns: None
        """
        # ///////////////////////////////////////////////////////////////
        print(self.equation);
        return;

# -----------------------------------------------------------------------------
#                           Application Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Equation variables
    r = MathVar(name='radius', range=(0,10)          , angular=False);
    b = MathVar(name='boom'  , range=(1, 1)          , angular=False);
    θ = MathVar(name='theta' , range=(0, 4.5*math.pi), angular=True );

    vars        = {
                   'r' : r,
                   'b' : b,
                   'θ' : θ
                  };
    
    # Equation of a spiral using polar coordinates
    equation_inst = MathEquation('s(r,θ) = r+bθ', vars);



    raise SystemExit(0);
