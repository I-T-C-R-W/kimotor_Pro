# Forked from KiMotor by Stefano Cottafavi.
# Copyright 2022 Stefano Cottafavi <stefano.cottafavi@gmail.com>.
# Copyright 2026 I-T-C-R-W
# SPDX-License-Identifier: GPL-2.0-only

import math
import numpy as np
from . import kmotor_solvermath as kla

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
        # Pre-compute constants
        th_half = th / 2
        cos_th_half = math.cos(th_half)
        sin_th_half = math.sin(th_half)
        
        pts = []
        mds = []
        mdsi = []

        # points 
        c = [0,0,0]
        l0 = np.array([ c, [r1*cos_th_half, r1*sin_th_half, 0] ])
        l0 = kla.line_offset(l0, -dr)
        
        for turn in range(turns):
            turn_dr = turn * dr
            # offset line
            lr = kla.line_offset(l0, -turn_dr)
            # solve corners and order them
            r1_inner = r1 + turn_dr
            r2_outer = r2 - turn_dr
            pc1 = kla.circle_line_intersect(lr, c, r1_inner)
            pc1 = pc1[0:2]
            pc2 = kla.circle_line_intersect(lr, c, r2_outer)
            pc2 = pc2[0:2]
            pc3 = np.array([ pc2[0], -pc2[1] ])
            pc4 = np.array([ pc1[0], -pc1[1] ])
            if dir == 0:
                pts.extend([pc1, pc2, pc3, pc4])
            else:
                pts.extend([pc4, pc3, pc2, pc1])
            
            # solve outer and inner mid-points
            pm = np.array([ r2_outer, 0 ])
            pmi = np.array([ r1_inner, 0 ])
            mds.append(pm)
            mdsi.append(pmi)

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
# Methods for solver



    def _estimate_turns_per_layer(self):
        active_span_mm = max((self.r_coil_out - self.r_coil_in) / self.SCALE, 0.0)
        layers = self._effective_winding_layers()
        pitch_mm = self._winding_pitch_mm()
        capacity = max(int(math.floor(active_span_mm / max(pitch_mm, 1e-6))), 0)
        turns_per_layer = self.n_loops / max(layers, 1)
        return {
            "turns_per_layer_est": turns_per_layer,
            "turn_capacity_per_layer_est": capacity,
            "effective_layers": layers,
            "active_span_mm": active_span_mm,
            "pitch_mm": pitch_mm,
        }



    def estimate_motor_constants(self, stats=None):
        if stats is None:
            stats = getattr(self, "last_stats", None)
        try:
            self.get_parameters()
            self.get_magnet_parameters()
        except Exception:
            return {"ke_est": 0.0, "kt_est": 0.0, "kv_est": 0.0}

        if self.phases <= 0 or self.n_loops <= 0:
            return {"ke_est": 0.0, "kt_est": 0.0, "kv_est": 0.0}

        radius_m = ((float(self.r_coil_in) + float(self.r_coil_out)) * 0.5) / self.SCALE / 1000.0
        radial_span_m = max(float(self.r_coil_out - self.r_coil_in), 0.0) / self.SCALE / 1000.0
        turns_series = max((self.n_slots / max(self.phases, 1)) * self.n_loops, 1.0)
        b_est = max(float(getattr(self, "magnet_b_est", 0.60)), 0.0)

        if radius_m <= 0.0 or radial_span_m <= 0.0 or b_est <= 0.0:
            return {"ke_est": 0.0, "kt_est": 0.0, "kv_est": 0.0}

        # First-order axial/radial PCB motor estimate:
        # E = B * l * v, v = omega * r, two active radial sides per turn.
        ke_est = 2.0 * b_est * radial_span_m * turns_series * radius_m
        kt_est = ke_est
        kv_est = 0.0 if ke_est <= 0.0 else (60.0 / (2.0 * math.pi * ke_est))
        return {"ke_est": ke_est, "kt_est": kt_est, "kv_est": kv_est}



    def estimate_winding_factor(self):
        try:
            self.get_parameters()
            self.get_magnet_parameters()
        except Exception:
            return 0.0

        if self.phases <= 0 or self.n_slots <= 0 or self.magnet_poles <= 0:
            return 0.0

        q = self.n_slots / float(self.magnet_poles * self.phases)
        if q <= 0.0:
            return 0.0

        slot_pitch_e = 2.0 * math.pi * self.magnet_pole_pairs / max(self.n_slots, 1)
        coil_pitch_slots = max(self.n_loops, 1)
        coil_pitch_e = coil_pitch_slots * slot_pitch_e

        kd_num = math.sin(q * slot_pitch_e / 2.0)
        kd_den = max(q * math.sin(slot_pitch_e / 2.0), 1e-9)
        kd = abs(kd_num / kd_den)
        kp = abs(math.sin(coil_pitch_e / 2.0))

        if self.phases == 1:
            kw = min(max(kp, 0.0), 1.0)
        else:
            kw = min(max(kd * kp, 0.0), 1.0)
        return kw



    def estimate_performance_stats(self, stats=None, motor_consts=None):
        if stats is None:
            stats = getattr(self, "last_stats", {}) or {}
        if motor_consts is None:
            motor_consts = self.estimate_motor_constants(stats)

        kv_est = float(motor_consts.get("kv_est", 0.0))
        kt_est = float(motor_consts.get("kt_est", 0.0))
        phase_r = max(float(stats.get("phase_r_temp", 0.0)), 0.0)

        rpm_12v = 12.0 * kv_est
        stall_current = 0.0 if phase_r <= 0.0 else 12.0 / phase_r
        stall_torque = kt_est * stall_current

        return {
            "winding_factor_est": self.estimate_winding_factor(),
            "rpm_12v_est": rpm_12v,
            "stall_current_est": stall_current,
            "stall_torque_est": stall_torque,
        }



    def estimate_model_warnings(self, stats=None, motor_consts=None, perf_stats=None):
        if stats is None:
            stats = getattr(self, "last_stats", {}) or {}
        if motor_consts is None:
            motor_consts = self.estimate_motor_constants(stats)
        if perf_stats is None:
            perf_stats = self.estimate_performance_stats(stats, motor_consts)

        warnings = []
        if float(getattr(self, "magnet_b_est", 0.0)) <= 0.0:
            warnings.append("B gap est <= 0")
        if int(getattr(self, "magnet_poles", 0)) <= 0:
            warnings.append("no magnet poles")
        if float(stats.get("phase_r_temp", 0.0)) <= 0.0:
            warnings.append("phase R <= 0")
        if float(perf_stats.get("winding_factor_est", 0.0)) < 0.2:
            warnings.append("low winding factor")
        if float(perf_stats.get("stall_current_est", 0.0)) > 50.0:
            warnings.append("high stall current")
        return warnings



    def estimate_safe_inner_fill_radius(self, net_name="coil"):
        """Upper bound for center fill radius to avoid touching net copper/pads."""
        safe_margin = max(self.trk_space, int(0.2 * self.SCALE))
        r_safe = None

        for item in self.board.GetTracks():
            try:
                net = item.GetNet()
            except Exception:
                net = None
            if net is None or net.GetNetname() != net_name:
                continue

            width = item.GetWidth() if hasattr(item, "GetWidth") else self.trk_w
            pts = []
            # Do not use arc/track center position here (e.g. ARC center at board origin),
            # otherwise safe radius can collapse incorrectly to 0.
            for getter in ("GetStart", "GetEnd", "GetMid"):
                if hasattr(item, getter):
                    try:
                        p = getattr(item, getter)()
                        pts.append((float(p.x), float(p.y)))
                    except Exception:
                        pass

            for x, y in pts:
                rr = math.hypot(x, y) - (width / 2.0) - safe_margin
                if r_safe is None or rr < r_safe:
                    r_safe = rr

        for fp in self.board.GetFootprints():
            for pad in fp.Pads():
                try:
                    net = pad.GetNet()
                except Exception:
                    net = None
                if net is None or net.GetNetname() != net_name:
                    continue
                pos = pad.GetPosition()
                size = pad.GetSize()
                pad_r = 0.5 * max(float(size.x), float(size.y))
                rr = math.hypot(float(pos.x), float(pos.y)) - pad_r - safe_margin
                if r_safe is None or rr < r_safe:
                    r_safe = rr

        if r_safe is None:
            return None
        return max(0, int(r_safe))



    def calculate_stats_breakdown(self, board, net_name="coil", temp=20):
        rho = 1.77e-8       
        alpha = 0.00393     
        l_total = 0.0
        r_total_20 = 0.0
        l_ring = 0.0
        r_ring_20 = 0.0
        
        for item in board.GetTracks():
            net = item.GetNet()
            if net is not None and net.GetNetname() == net_name:
                length_m = item.GetLength() / self.SCALE / 1000.0
                width_m = item.GetWidth() / self.SCALE / 1000.0
                
                l_total += length_m
                if getattr(self, "winding_mode", "PCB") == "Wire":
                    wire_dia_m = max(float(getattr(self, "wire_dia_mm", 0.5)) / 1000.0, 1e-9)
                    A = math.pi * (wire_dia_m * 0.5) ** 2
                else:
                    A = width_m * float(getattr(self, "copper_thickness_m", self.tthick))
                
                if A > 0:
                    r_part = rho * (length_m / A)
                    r_total_20 += r_part
                    if item.GetLayer() == pcbnew.F_Cu and item.GetWidth() == self.ring_w:
                        l_ring += length_m
                        r_ring_20 += r_part

        l_coil = max(l_total - l_ring, 0.0)
        r_coil_20 = max(r_total_20 - r_ring_20, 0.0)

        phase_len_mm = (l_total / self.phases) * 1000.0
        phase_r_20 = r_total_20 / self.phases
        phase_r_temp = phase_r_20 * (1 + alpha * (temp - 20))
        total_r_temp = r_total_20 * (1 + alpha * (temp - 20))
        ring_r_temp = r_ring_20 * (1 + alpha * (temp - 20))
        coil_r_temp = r_coil_20 * (1 + alpha * (temp - 20))
        coil_res_per_coil = coil_r_temp / max(self.n_slots, 1)
        winding_stats = self._estimate_turns_per_layer()

        coils_count = max(self.n_slots, 1)
        phases_count = max(self.phases, 1)
        return {
            "total_length_mm": l_total * 1000.0,
            "total_length_m": l_total,
            "phase_len_mm": phase_len_mm,
            "phase_r_temp": phase_r_temp,
            "total_resistance": total_r_temp,
            "coil_resistance_per_coil": coil_res_per_coil,
            "ring_resistance_total": ring_r_temp,
            "coil_length_mm": l_coil * 1000.0,
            "ring_length_mm": l_ring * 1000.0,
            "coil_length_per_coil_mm": (l_coil * 1000.0) / coils_count,
            "coil_resistance_total": coil_r_temp,
            "ring_resistance_per_phase": ring_r_temp / phases_count,
            "winding_mode": getattr(self, "winding_mode", "PCB"),
            "turns_per_layer_est": winding_stats["turns_per_layer_est"],
            "turn_capacity_per_layer_est": winding_stats["turn_capacity_per_layer_est"],
            "effective_layers": winding_stats["effective_layers"],
            "copper_length_total_m": l_total,
        }



    def calculate_stats(self, board, net_name="coil", temp=20):
        stats = self.calculate_stats_breakdown(board, net_name=net_name, temp=temp)
        return stats["phase_len_mm"], stats["phase_r_temp"]

