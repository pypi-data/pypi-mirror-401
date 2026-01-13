#!/usr/bin/env python3
# *****************************************************************************
"""                            MathVar Class
 
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
import math;

# ----* Third Party Imports *----

class MathVar():
    # ======================================================================
    """Description: Parent class for SackosArt math variables

        Attributes: version : Current version of class.

          Examples: None
           Related: None
    """
    # ======================================================================

    # ++++ Class Variables ++++
    version = 0.1;

    def __init__(self, name, range, precision=2**(-53)) -> None:
        # ///////////////////////////////////////////////////////////////
        """Description: Class constructor
             Arguments: None
               Returns: None
        """
        # ///////////////////////////////////////////////////////////////

        self.name      = name;
        self.range     = range;
        self.precision = precision;

        return;

    def __del__(self) -> None:
        # ///////////////////////////////////////////////////////////////
        """Description: Class destructor
             Arguments: None
               Returns: None
        """
        # ///////////////////////////////////////////////////////////////

        return;

# -----------------------------------------------------------------------------
#                           Application Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Example equation
    equation    = 's(r,θ) = r+bθ';

    # Variables for equation
    r = MathVar(name='Radius'       , range=(0,10)          );
    b = MathVar(name='Constriction' , range=(0, 3)          );
    θ = MathVar(name='Theta'        , range=(0, 4.5*math.pi));

    # Package the variables up neatly!
    vars = {
            'r' : r,
            'b' : b,
            'θ' : θ
           };

    raise SystemExit(0);
