# -*- coding: utf-8 -*-
""" GERDPy - 'heatpipes.py'
    
    Class for the heatpipe configuration inside the boreholes

    Authors: Yannick Apfel, Meike Martin
"""
import numpy as np
from scipy.constants import pi


class Heatpipes(object):
    """
    Contains all relevant parameters regarding the heatpipe layout inside the boreholes
    which must be identical for all of the latter (circle).

    Attributes
    ----------
    N:          int
                number of heatpipes per borehole (arranged in a circle) [-]
    r_b:        float 
                borehole radius [m]
    r_w:        float
                radius of heatpipe centres [m]
    r_iso_a:    float
                outer radius of heatpipe insulation [m]
    r_pa:       float
                outer radius of heatpipes [m]
    r_pi:       float
                inner radius of heatpipes [m]
    lambda_b:   float
                thermal conductivity of borehole backfill [W/mK]
    lambda_iso: float
                thermal conductivity of insulation layer [W/mK]
    lambda_p:   float
                thermal conductivity of heatpipe material [W/mK]

    """

    def __init__(self, N, r_b, r_w, r_iso_a, r_pa, r_pi, lambda_b, lambda_iso, lambda_p):
        self.N = int(N)
        self.r_b = float(r_b)
        self.r_w = float(r_w)
        self.r_iso_a = float(r_iso_a)
        self.r_pa = float(r_pa)
        self.r_pi = float(r_pi)
        self.lambda_b = float(lambda_b)
        self.lambda_iso = float(lambda_iso)
        self.lambda_p = float(lambda_p)

    def __repr__(self):
        s = ('Heatpipes(N={self.N}, r_w={self.r_w}, r_iso_a={self.r_iso_a}, r_pa={self.r_pa},'
             ' r_pi={self.r_pi}, lambda_iso={self.lambda_iso},'
             ' lambda_p={self.lambda_p})').format(self=self)
        return s

    def xy_mat(self):
        """
        Returns a Nx2 matrix with the coordinates of the heatpipe centres
        in the borehole coordinate system (origin = borehole centre).
        The N heatpipes are uniformly spaced on a circle with
        radius r_w.

        """

        xy_mat = np.zeros([self.N, 2])  # 1. column: x, 2. column: y

        for i in range(self.N):
            xy_mat[i, 0] = self.r_w * np.cos(2 * pi * i / self.N)
            xy_mat[i, 1] = self.r_w * np.sin(2 * pi * i / self.N)

        return xy_mat

    def visualize_hp_config(self):
        """
        Plot of the cross-section of a borehole (visualizes heatpipe layout).

        Returns
        -------
        fig : figure
            Figure object (matplotlib).
        """
        import matplotlib.pyplot as plt
        from matplotlib.ticker import AutoMinorLocator

        # Initialization
        LW = .5    # Line width
        FS = 12.    # Font size

        plt.rc('figure')
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Outline of the borehole wall
        borewall = plt.Circle((0., 0.), radius=self.r_b,
                              fill=False, linestyle='--', linewidth=LW)
        ax.add_patch(borewall)

        # Heatpipes
        for i in range(self.N):
            # Coordinates
            xy = self.xy_mat()
            (x, y) = (xy[i, 0], xy[i, 1])

            # Plot heatpipes + insulation layer
            hp_iso = plt.Circle((x, y), radius=self.r_iso_a,
                                fill=False, linestyle='-', linewidth=LW)
            hp_itself_outer = plt.Circle((x, y), radius=self.r_pa,
                                fill=False, linestyle='-', linewidth=LW)
            hp_itself_inner = plt.Circle((x, y), radius=self.r_pi,
                                fill=False, linestyle='-', linewidth=LW)
            ax.text(x, y, i + 1,
                    ha="center", va="center", size=FS)

            ax.add_patch(hp_iso)
            ax.add_patch(hp_itself_outer)
            ax.add_patch(hp_itself_inner)

        # Achsen
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title('Heatpipe Layout')
        plt.axis('equal')
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        plt.tight_layout()

        return fig
