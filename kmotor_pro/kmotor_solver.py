# Forked from KiMotor by Stefano Cottafavi.
# Copyright 2022 Stefano Cottafavi <stefano.cottafavi@gmail.com>.
# Copyright 2026 I-T-C-R-W
# SPDX-License-Identifier: GPL-2.0-only

import math
import numpy as np
from . import kmotor_solvermath as kla
import wx

def parallel(r1,r2, dr,th,turns,dir):
        """ Compute layout points for coil with sides always aligned to radius

        Args:
            r1 (int): coil inner radius
            r2 (int): coil outer radius
            dr (int): spacing between coil loops (and also adj. coils)
            th (float): coil trapezoid angle 
            turns (int): number of coil loops (windings)
            dir (int): coil direction, from larger to smaller loop (0:CW normal, 1:CCW rverse)

        Returns:
            matrix, matrix, matrix: corners (excl. arc mids), outer arc mids, inner arc mids
        """

        pts = []
        mds = []
        mdsi = []

        # points 
        c = [0,0,0]
        l0 = np.array([ c, [r1*math.cos(th/2), r1*math.sin(th/2), 0] ])
        l0 = kla.line_offset(l0, -dr)
        
        for turn in range(turns):
            # offset line
            lr = kla.line_offset(l0, -turn*dr)
            # solve corners and order them
            pc1 = kla.circle_line_intersect(lr, c, r1+turn*dr)
            pc1 = pc1[0:2]
            pc2 = kla.circle_line_intersect(lr, c, r2-turn*dr)
            pc2 = pc2[0:2]
            pc3 = np.array([ pc2[0],-pc2[1] ])
            pc4 = np.array([ pc1[0],-pc1[1] ])
            if dir == 0:
                pts.extend([pc1, pc2, pc3, pc4])
            else:
                pts.extend([pc4, pc3, pc2, pc1])
            
            # solve outer and inner mid-points
            pm = np.array([ r2-turn*dr, 0 ])
            pmi = np.array([ r1+turn*dr, 0 ])
            mds.extend([pm])
            mdsi.extend([pmi])

        pm = np.matrix(pts)     # points, excl. arc mids
        mm = np.matrix(mds)     # arc (outer) mids only
        mmi = np.matrix(mdsi)    # arc (inner) mids only

        return pm, mm, mmi

def radial(ri,ro, dr,th,turns,dir):
        """ Compute layout points for coil with sides aligned to the local radial direction

        Args:
            ri (int): coil inner radius
            ro (int): coil outer radius
            dr (int): spacing between coil loops (and also adj. coils)
            th (float): coil trapezoid angle
            turns (int): number of coil loops (windings)
            dir (int): coil direction, from larger to smaller loop (0:CW normal, 1:CCW rverse)

        Returns:
            matrix, matrix, matrix: corners (excl. arc mids), outer-arc mid points, inner-arc mid points
        """
 
        pts = []

        # center
        c = [0,0,0]
        
        # rotation of first arc and last ard mid-mid-points
        Rcw = np.array([
            [math.cos(th/4), -math.sin(th/4)],
            [math.sin(th/4), math.cos(th/4)],
        ])

        # first line
        l0 = np.array([ c, [ri*math.cos(th/2), ri*math.sin(th/2), 0] ])


        for turn in range(turns):
            
            # solve corner points
            
            lr = kla.line_offset(l0, -dr)
            pc1 = kla.circle_line_intersect(lr, c, ri+turn*dr)
            pc1 = pc1[0:2]

            lr = [c, [pc1[0], pc1[1], 0]]
            pc2 = kla.circle_line_intersect(lr, c, ro-turn*dr)
            pc2 = pc2[0:2]
            pc3 = np.array([ pc2[0],-pc2[1] ])
            pc4 = np.array([ pc1[0],-pc1[1] ])
            
            # solve outer/inner mid-points
            pmo = np.array([ ro-turn*dr, 0 ])
            pmi = np.array([ ri+turn*dr, 0 ])

            # order points
            if dir == 0:
                if turn == 0:
                    tp = np.matmul(Rcw, pmi)
                    pts.extend([pmi, tp[0:2], pc1, pc2, pmo, pc3])
                elif turn == turns-1:
                    tp = np.matmul(Rcw, pmo)
                    pts.extend([pc4, pmi, pc1, pc2, tp[0:2], pmo])
                else:
                    pts.extend([pc4, pmi, pc1, pc2, pmo, pc3])
            else:
                if turn == 0:
                    tp = np.matmul(Rcw, pmi)
                    pts.extend([pmi, tp[0:2], pc4, pc3, pmo, pc2])
                elif turn == turns-1:
                    tp = np.matmul(Rcw, pmo)
                    pts.extend([pc1, pmi, pc4, pc3, tp[0:2], pmo])
                else:
                    pts.extend([pc1, pmi, pc4, pc3, pmo, pc2])
            
            # move to the next radial
            l0 = [ [pc1[0], pc1[1], 0], [pc2[0], pc2[1], 0] ] 

        mpt = np.matrix(pts)

        return mpt

def compact(ri, ro, dr, th, turns, dir):
        """Compute a denser radial-style coil with tighter bridge stubs.

        This keeps the same point layout contract as ``radial()`` so the existing
        tracker/routing code can use it unchanged, but reduces bridge rotation to
        waste less angular space in narrow slots.
        """

        pts = []
        c = [0, 0, 0]

        # Tighter than radial(): keep the first/last bridge closer to the slot
        # centerline so dense / near-square slots use less dead angular width.
        bridge_rot = th / 6.0
        Rcw = np.array([
            [math.cos(bridge_rot), -math.sin(bridge_rot)],
            [math.sin(bridge_rot), math.cos(bridge_rot)],
        ])

        l0 = np.array([c, [ri * math.cos(th / 2), ri * math.sin(th / 2), 0]])

        for turn in range(turns):
            lr = kla.line_offset(l0, -dr)
            pc1 = kla.circle_line_intersect(lr, c, ri + turn * dr)
            pc1 = pc1[0:2]

            lr = [c, [pc1[0], pc1[1], 0]]
            pc2 = kla.circle_line_intersect(lr, c, ro - turn * dr)
            pc2 = pc2[0:2]
            pc3 = np.array([pc2[0], -pc2[1]])
            pc4 = np.array([pc1[0], -pc1[1]])

            pmo = np.array([ro - turn * dr, 0])
            pmi = np.array([ri + turn * dr, 0])

            if dir == 0:
                if turn == 0:
                    tp = np.matmul(Rcw, pmi)
                    pts.extend([pmi, tp[0:2], pc1, pc2, pmo, pc3])
                elif turn == turns - 1:
                    tp = np.matmul(Rcw, pmo)
                    pts.extend([pc4, pmi, pc1, pc2, tp[0:2], pmo])
                else:
                    pts.extend([pc4, pmi, pc1, pc2, pmo, pc3])
            else:
                if turn == 0:
                    tp = np.matmul(Rcw, pmi)
                    pts.extend([pmi, tp[0:2], pc4, pc3, pmo, pc2])
                elif turn == turns - 1:
                    tp = np.matmul(Rcw, pmo)
                    pts.extend([pc1, pmi, pc4, pc3, tp[0:2], pmo])
                else:
                    pts.extend([pc1, pmi, pc4, pc3, pmo, pc2])

            l0 = [[pc1[0], pc1[1], 0], [pc2[0], pc2[1], 0]]

        return np.matrix(pts)
