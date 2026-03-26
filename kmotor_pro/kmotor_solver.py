bitte # Forked from KiMotor by Stefano Cottafavi.
# Copyright 2022 Stefano Cottafavi <stefano.cottafavi@gmail.com>.
# Copyright 2026 I-T-C-R-W
# SPDX-License-Identifier: GPL-2.0-only

import math
import re
import numpy as np
from . import kmotor_solvermath as kla
from .kmotor_models import (
    MotorInputConfig,
    TopologyConfig,
    StatorMechanicsConfig,
    CoilLayoutConfig,
    StackPcbConfig,
    RotorMagnetConfig,
    PeripheralsConfig,
)

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



def resolve_outline_edges(outline):
    mapping = {
        "Circle": 0,
        "Square": 4,
        "Hexagon": 6,
        "Octagon": 8,
    }
    return mapping.get(outline, -1)


def resolve_phase_scheme(scheme):
    if scheme == "1P":
        return 1, 2
    if scheme == "3P+N":
        return 3, 4
    return 3, 3


def normalize_support_via_mode(value, default=2):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return default
    return value if value in (0, 2, 4) else default


def angle_delta(a, b):
    d = (a - b + math.pi) % (2.0 * math.pi) - math.pi
    return abs(d)


def nearest_magnet_angle_delta(target_angle, magnet_poles, magnet_rotation):
    if magnet_poles <= 0:
        return math.pi
    pitch = 2.0 * math.pi / magnet_poles
    rot0 = math.radians(magnet_rotation)
    rel = (target_angle - rot0) / pitch
    nearest_idx = round(rel)
    nearest_angle = rot0 + nearest_idx * pitch
    return angle_delta(target_angle, nearest_angle)


def estimate_motor_constants(phases, n_loops, r_coil_in, r_coil_out, scale, n_slots, magnet_b_est):
    if phases <= 0 or n_loops <= 0:
        return {"ke_est": 0.0, "kt_est": 0.0, "kv_est": 0.0}

    radius_m = ((float(r_coil_in) + float(r_coil_out)) * 0.5) / scale / 1000.0
    radial_span_m = max(float(r_coil_out - r_coil_in), 0.0) / scale / 1000.0
    turns_series = max((n_slots / max(phases, 1)) * n_loops, 1.0)
    b_est = max(float(magnet_b_est), 0.0)

    if radius_m <= 0.0 or radial_span_m <= 0.0 or b_est <= 0.0:
        return {"ke_est": 0.0, "kt_est": 0.0, "kv_est": 0.0}

    ke_est = 2.0 * b_est * radial_span_m * turns_series * radius_m
    kt_est = ke_est
    kv_est = 0.0 if ke_est <= 0.0 else (60.0 / (2.0 * math.pi * ke_est))
    return {"ke_est": ke_est, "kt_est": kt_est, "kv_est": kv_est}


def estimate_winding_factor(phases, n_slots, magnet_poles, magnet_pole_pairs, n_loops):
    if phases <= 0 or n_slots <= 0 or magnet_poles <= 0:
        return 0.0

    q = n_slots / float(magnet_poles * phases)
    if q <= 0.0:
        return 0.0

    slot_pitch_e = 2.0 * math.pi * magnet_pole_pairs / max(n_slots, 1)
    coil_pitch_slots = max(n_loops, 1)
    coil_pitch_e = coil_pitch_slots * slot_pitch_e

    kd_num = math.sin(q * slot_pitch_e / 2.0)
    kd_den = max(q * math.sin(slot_pitch_e / 2.0), 1e-9)
    kd = abs(kd_num / kd_den)
    kp = abs(math.sin(coil_pitch_e / 2.0))

    if phases == 1:
        return min(max(kp, 0.0), 1.0)
    return min(max(kd * kp, 0.0), 1.0)


def estimate_performance_stats(stats, motor_consts, winding_factor_est):
    stats = stats or {}
    motor_consts = motor_consts or {}
    kv_est = float(motor_consts.get("kv_est", 0.0))
    kt_est = float(motor_consts.get("kt_est", 0.0))
    phase_r = max(float(stats.get("phase_r_temp", 0.0)), 0.0)

    rpm_12v = 12.0 * kv_est
    stall_current = 0.0 if phase_r <= 0.0 else 12.0 / phase_r
    stall_torque = kt_est * stall_current

    return {
        "winding_factor_est": winding_factor_est,
        "rpm_12v_est": rpm_12v,
        "stall_current_est": stall_current,
        "stall_torque_est": stall_torque,
    }


def estimate_model_warnings(stats, perf_stats, magnet_b_est, magnet_poles):
    stats = stats or {}
    perf_stats = perf_stats or {}
    warnings = []
    if float(magnet_b_est) <= 0.0:
        warnings.append("B gap est <= 0")
    if int(magnet_poles) <= 0:
        warnings.append("no magnet poles")
    if float(stats.get("phase_r_temp", 0.0)) <= 0.0:
        warnings.append("phase R <= 0")
    if float(perf_stats.get("winding_factor_est", 0.0)) < 0.2:
        warnings.append("low winding factor")
    if float(perf_stats.get("stall_current_est", 0.0)) > 50.0:
        warnings.append("high stall current")
    return warnings


def get_effective_coil_strategy(ri, ro, n_slots, n_loops, dr, trk_w, strategy, max_spec):
    radial_available = max(ro - ri, 0.0)
    radial_required = max(n_loops * dr + trk_w, dr)
    slot_pitch = (2.0 * math.pi) / max(n_slots, 1)
    mean_radius = max(0.5 * (ri + ro), 1.0)
    tangential_span = max(mean_radius * slot_pitch, 1.0)
    aspect = float(radial_available) / float(tangential_span)

    selected = int(strategy)
    if selected == 2:
        return 2, "Compact"

    if max_spec:
        dense_fill = radial_required >= radial_available * 0.82
        near_square = aspect <= 0.34
        if dense_fill or near_square:
            return 2, "Compact"

    if selected == 0:
        return 0, "Parallel"
    return 1, "Radial"


def get_mounting_hole_dia(fp_name, scale):
    if not fp_name:
        return 0.0
    m = re.search(r"MountingHole_([0-9.]+)mm", fp_name)
    if not m:
        return 0.0
    try:
        return float(m.group(1)) * scale
    except ValueError:
        return 0.0


def iter_magnet_clearance_targets(n_mh_out, r_mh_out, n_edges, n_mh_in, r_mh_in, mh_dia, corner_targets):
    targets = []
    mh_radius = 0.5 * mh_dia if mh_dia > 0 else 0.0

    if n_mh_out > 0 and r_mh_out > 0:
        radius = float(r_mh_out)
        if n_edges > 0:
            radius /= max(math.cos(math.pi / n_edges), 1e-6)
        th0 = 2 * math.pi / n_mh_out
        for idx in range(n_mh_out):
            angle = th0 * idx + th0 / 2.0
            targets.append((radius, angle, mh_radius, "outer mounting holes"))

    if n_mh_in > 0 and r_mh_in > 0:
        th0 = 2 * math.pi / n_mh_in
        radius = float(r_mh_in)
        for idx in range(n_mh_in):
            angle = th0 * idx + th0 / 2.0
            targets.append((radius, angle, mh_radius, "inner mounting holes"))

    for x, y, angle, dia in corner_targets or []:
        targets.append((math.hypot(x, y), angle, 0.5 * dia, "corner alignment holes"))

    return targets


def validate_magnet_parameters(magnet_pole_pairs, magnet_ring_dia, magnet_shape, magnet_dia, magnet_width, magnet_height, magnet_gap, magnet_keepout, magnet_poles, scale, r_in, r_out, clearance_targets, nearest_angle_delta_fn):
    errors = []
    warnings = []

    if magnet_pole_pairs <= 0:
        errors.append("Pole pairs must be > 0.")
    if magnet_ring_dia <= 0:
        errors.append("Magnet ring dia must be > 0.")

    if magnet_shape == "round":
        if magnet_dia <= 0:
            errors.append("Magnet dia must be > 0 for round magnets.")
        magnet_span = magnet_dia
        radial_span = magnet_dia
    else:
        if magnet_width <= 0 or magnet_height <= 0:
            errors.append("Magnet width and height must be > 0 for rectangular magnets.")
        magnet_span = magnet_width
        radial_span = magnet_height

    if errors:
        return errors, warnings

    radius = magnet_ring_dia * 0.5
    circumference = 2.0 * math.pi * radius
    required_arc = magnet_poles * max(magnet_span + magnet_gap + magnet_keepout, 0.0)
    pole_pitch_arc = circumference / max(magnet_poles, 1)
    if required_arc > circumference:
        errors.append(
            "Magnets do not fit on the selected ring diameter. "
            f"Required arc {required_arc / scale:.2f} mm > circumference {circumference / scale:.2f} mm."
        )
    if (magnet_span + magnet_gap + magnet_keepout) > pole_pitch_arc:
        errors.append(
            "Single magnet pitch is too large for the selected pole count. "
            f"Needed {(magnet_span + magnet_gap + magnet_keepout) / scale:.2f} mm > "
            f"available {pole_pitch_arc / scale:.2f} mm."
        )

    inner_edge = radius - (0.5 * radial_span) - magnet_keepout
    outer_edge = radius + (0.5 * radial_span) + magnet_keepout
    if inner_edge <= float(r_in):
        errors.append(
            f"Magnet ring intersects shaft bore region ({inner_edge / scale:.2f} mm <= {float(r_in) / scale:.2f} mm)."
        )
    if outer_edge >= float(r_out):
        errors.append(
            f"Magnet ring exceeds safe board radius ({outer_edge / scale:.2f} mm >= {float(r_out) / scale:.2f} mm)."
        )

    radial_clearance = 0.5 * radial_span + magnet_keepout
    angular_half_span = (0.5 * magnet_span + magnet_keepout) / max(radius, 1.0)
    for target_r, target_angle, hr, label in clearance_targets or []:
        radial_delta = abs(target_r - radius)
        if radial_delta > (radial_clearance + hr):
            continue
        target_half_span = math.asin(min(0.999999, (hr + magnet_keepout) / max(target_r, 1.0)))
        angle_delta = nearest_angle_delta_fn(target_angle)
        if angle_delta <= (angular_half_span + target_half_span):
            warnings.append(
                f"Magnet ring overlaps the clearance zone of {label} near angle {math.degrees(target_angle):.1f} deg."
            )
        else:
            warnings.append(
                f"Magnet ring is close to {label} (radial delta {radial_delta / scale:.2f} mm)."
            )

    if magnet_ring_dia >= float(r_out) * 2.0:
        warnings.append("Magnet ring dia is at or outside board size.")
    if magnet_ring_dia <= float(r_in) * 2.0:
        warnings.append("Magnet ring dia is close to or inside the shaft bore region.")

    return errors, warnings


def get_board_span(r_out):
    return 2.0 * float(r_out)


def get_magnet_board_origin(board_span):
    return (board_span * 1.1, 0.0)


def effective_winding_layers(n_layers):
    return max(int(n_layers), 1)


def winding_pitch_mm(winding_mode, wire_dia_mm, trk_space, trk_w, scale):
    if winding_mode == "Wire":
        return max(wire_dia_mm + (trk_space / scale), wire_dia_mm, 1e-6)
    return max((trk_w + trk_space) / scale, 1e-6)


def estimate_turns_per_layer(r_coil_in, r_coil_out, scale, layers, pitch_mm, n_loops):
    active_span_mm = max((r_coil_out - r_coil_in) / scale, 0.0)
    capacity = max(int(math.floor(active_span_mm / max(pitch_mm, 1e-6))), 0)
    turns_per_layer = n_loops / max(layers, 1)
    return {
        "turns_per_layer_est": turns_per_layer,
        "turn_capacity_per_layer_est": capacity,
        "effective_layers": layers,
        "active_span_mm": active_span_mm,
        "pitch_mm": pitch_mm,
    }


def validate_parameters(n_slots, n_loops, phases):
    errors = []
    if n_slots <= 0:
        errors.append("n_slots muss > 0 sein.")
    if n_loops <= 0:
        errors.append("n_loops muss > 0 sein.")
    if n_slots < phases:
        errors.append(f"n_slots ({n_slots}) muss mindestens phases ({phases}) sein.")
    if n_slots % phases != 0:
        errors.append(f"n_slots ({n_slots}) muss durch phases ({phases}) teilbar sein.")
    return errors


def get_support_hole_width(d_support_hole, scale):
    pad_margin = int(0.25 * scale)
    return max(d_support_hole + pad_margin, d_support_hole + 1)


def get_selected_terminal_od_iu(trmtype, term_db, term_size, scale):
    if trmtype != "THT":
        return int(4.0 * scale)
    try:
        fp = (term_db or {}).get("THT", {}).get(term_size, "")
        if "_OD" in fp and "mm" in fp:
            token = fp.split("_OD", 1)[1].split("mm", 1)[0]
            return int(float(token) * scale)
    except Exception:
        pass
    return int(4.0 * scale)


def hole_collides(position, placed_points, min_distance):
    for pt in placed_points:
        if math.hypot(pt.x - position.x, pt.y - position.y) < min_distance:
            return True
    return False


def build_motor_config(
    scheme,
    outline,
    n_slots,
    magnet_pole_pairs,
    scale,
    r_in,
    r_out,
    o_fill,
    w_mnt,
    mhs,
    n_mh_out,
    r_mh_out,
    n_mh_in,
    r_mh_in,
    corner_hole_count,
    corner_hole_dia,
    corner_hole_offset,
    winding_mode,
    strategy,
    max_spec,
    n_loops,
    r_coil_in,
    r_coil_out,
    trk_w,
    trk_space,
    r_fill,
    wire_dia_mm,
    n_layers,
    copper_weight,
    d_via,
    d_drill,
    support_via_mode,
    d_support_hole,
    ring_w,
    ring_space,
    fill_inner_gnd,
    inner_fill_dia,
    fill_outer_gnd,
    magnet_shape,
    magnet_ring_dia,
    magnet_rotation,
    magnet_dia,
    magnet_width,
    magnet_height,
    magnet_length,
    magnet_gap,
    magnet_keepout,
    magnet_b_est,
    trmtype,
    term_size,
    term_offset,
    silk_cross_guides,
    silk_slot_frames,
    silk_deg_scale,
    silk_hole_scales,
    corner_scale_step_deg,
    corner_scale_span_deg,
):
    outline_type = {
        "Circle": "Circle",
        "Square": "Square",
        "Hexagon": "Hexagon",
        "Octagon": "Octagon",
        "None": "None",
    }.get(outline, "Circle")

    if scheme == "1P":
        phases = 1
    elif scheme == "3P+N":
        phases = 3
    else:
        phases = 3

    strategy_name = {0: "Parallel", 1: "Radial", 2: "Compact"}.get(strategy, "Radial")
    magnet_shape_name = str(magnet_shape).capitalize()

    return MotorInputConfig(
        topology=TopologyConfig(
            scheme=scheme,
            phases=phases,
            slots=n_slots,
            pole_pairs=magnet_pole_pairs,
        ),
        mechanics=StatorMechanicsConfig(
            outline_type=outline_type,
            shaft_bore_dia_mm=r_in * 2 / scale,
            outer_dia_mm=r_out * 2 / scale,
            corner_fillet_mm=o_fill / scale if o_fill else 0.0,
            annular_width_mm=w_mnt / scale,
            mount_size=mhs,
            mount_out_count=n_mh_out,
            mount_out_dia_mm=r_mh_out * 2 / scale,
            mount_in_count=n_mh_in,
            mount_in_dia_mm=r_mh_in * 2 / scale,
            corner_hole_count=corner_hole_count,
            corner_hole_dia_mm=corner_hole_dia / scale,
            corner_hole_offset_mm=corner_hole_offset / scale,
        ),
        coil=CoilLayoutConfig(
            winding_mode=winding_mode,
            strategy=strategy_name,
            max_spec_layout=max_spec,
            turns_per_layer=n_loops,
            inner_dia_mm=r_coil_in * 2 / scale,
            outer_dia_mm=r_coil_out * 2 / scale,
            track_width_mm=trk_w / scale,
            track_spacing_mm=trk_space / scale,
            track_fillet_mm=r_fill / scale if r_fill else 0.0,
            wire_dia_mm=wire_dia_mm if winding_mode == "Wire" else None,
        ),
        stack=StackPcbConfig(
            layers=n_layers,
            copper_weight=copper_weight,
            via_dia_mm=d_via / scale,
            via_drill_mm=d_drill / scale,
            support_via_mode=support_via_mode,
            support_hole_dia_mm=d_support_hole / scale,
            ring_width_mm=ring_w / scale,
            ring_spacing_mm=ring_space / scale,
            fill_inner_gnd=fill_inner_gnd,
            inner_gnd_dia_mm=inner_fill_dia / scale,
            fill_outer_gnd=fill_outer_gnd,
        ),
        rotor=RotorMagnetConfig(
            shape=magnet_shape_name,
            ring_dia_mm=magnet_ring_dia / scale,
            rotation_offset_deg=magnet_rotation,
            dia_mm=magnet_dia / scale if magnet_shape_name == "Round" else None,
            width_mm=magnet_width / scale if magnet_shape_name == "Rect" else None,
            height_mm=magnet_height / scale if magnet_shape_name == "Rect" else None,
            length_mm=magnet_length / scale,
            gap_mm=magnet_gap / scale,
            keepout_mm=magnet_keepout / scale,
            b_gap_est_tesla=magnet_b_est,
        ),
        peripherals=PeripheralsConfig(
            term_type=trmtype,
            term_size=term_size,
            term_offset_mm=term_offset / scale,
            silk_cross_guides=silk_cross_guides,
            silk_slot_frames=silk_slot_frames,
            silk_degree_scale=silk_deg_scale,
            silk_hole_scales=silk_hole_scales,
            corner_scale_step_deg=corner_scale_step_deg,
            corner_scale_span_deg=corner_scale_span_deg,
        ),
    )


def calculate_stats_breakdown(segments, temp, phases, n_slots, winding_mode, wire_dia_mm, copper_thickness_m, ring_width_iu, front_cu_layer, winding_stats):
    rho = 1.77e-8
    alpha = 0.00393
    l_total = 0.0
    r_total_20 = 0.0
    l_ring = 0.0
    r_ring_20 = 0.0

    for segment in segments or []:
        length_m = float(segment.get("length_m", 0.0))
        width_m = float(segment.get("width_m", 0.0))
        l_total += length_m

        if winding_mode == "Wire":
            wire_dia_m = max(float(wire_dia_mm) / 1000.0, 1e-9)
            area = math.pi * (wire_dia_m * 0.5) ** 2
        else:
            area = width_m * float(copper_thickness_m)

        if area <= 0:
            continue

        r_part = rho * (length_m / area)
        r_total_20 += r_part
        if segment.get("layer") == front_cu_layer and segment.get("width_iu") == ring_width_iu:
            l_ring += length_m
            r_ring_20 += r_part

    l_coil = max(l_total - l_ring, 0.0)
    r_coil_20 = max(r_total_20 - r_ring_20, 0.0)

    phase_len_mm = (l_total / phases) * 1000.0
    phase_r_20 = r_total_20 / phases
    temp_factor = 1 + alpha * (temp - 20)
    phase_r_temp = phase_r_20 * temp_factor
    total_r_temp = r_total_20 * temp_factor
    ring_r_temp = r_ring_20 * temp_factor
    coil_r_temp = r_coil_20 * temp_factor
    coil_res_per_coil = coil_r_temp / max(n_slots, 1)

    coils_count = max(n_slots, 1)
    phases_count = max(phases, 1)
    winding_stats = winding_stats or {}
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
        "winding_mode": winding_mode,
        "turns_per_layer_est": winding_stats.get("turns_per_layer_est", 0.0),
        "turn_capacity_per_layer_est": winding_stats.get("turn_capacity_per_layer_est", 0),
        "effective_layers": winding_stats.get("effective_layers", 0),
        "copper_length_total_m": l_total,
    }


def calculate_stats(stats):
    stats = stats or {}
    return stats.get("phase_len_mm", 0.0), stats.get("phase_r_temp", 0.0)


def estimate_safe_inner_fill_radius(clearance_values):
    if not clearance_values:
        return None
    return max(0, int(min(clearance_values)))


def track_clearance_values(points, width, safe_margin):
    values = []
    for x, y in points or []:
        values.append(math.hypot(float(x), float(y)) - (float(width) / 2.0) - safe_margin)
    return values


def pad_clearance_value(position_xy, size_xy, safe_margin):
    pad_r = 0.5 * max(float(size_xy[0]), float(size_xy[1]))
    return math.hypot(float(position_xy[0]), float(position_xy[1])) - pad_r - safe_margin


def magnet_parameters_from_values(magnet_shape, magnet_dia, magnet_width, magnet_height, magnet_length, magnet_ring_dia, magnet_pole_pairs, magnet_gap, magnet_keepout, magnet_rotation, magnet_b_est):
    pole_pairs = int(magnet_pole_pairs)
    return {
        "magnet_shape": str(magnet_shape).lower(),
        "magnet_dia": float(magnet_dia),
        "magnet_width": float(magnet_width),
        "magnet_height": float(magnet_height),
        "magnet_length": float(magnet_length),
        "magnet_ring_dia": float(magnet_ring_dia),
        "magnet_pole_pairs": pole_pairs,
        "magnet_gap": float(magnet_gap),
        "magnet_keepout": float(magnet_keepout),
        "magnet_rotation": float(magnet_rotation),
        "magnet_b_est": float(magnet_b_est),
        "magnet_poles": max(pole_pairs * 2, 0),
    }
