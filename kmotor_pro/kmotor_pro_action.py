# Forked from KiMotor by Stefano Cottafavi.
# Copyright 2022 Stefano Cottafavi <stefano.cottafavi@gmail.com>
# Copyright 2026 I-T-C-R-W
# SPDX-License-Identifier: GPL-2.0-only

import os
import shutil
import numpy as np
import math
import json
import re
import traceback
import itertools
from datetime import datetime

import wx
import wx.lib.agw.persist.persistencemanager as PM
import pcbnew

if __name__ == '__main__':
    import kmotor_pro_gui
    import kmotor_pro_linalg as kla
else:
    from . import kmotor_pro_gui
    from . import kmotor_pro_linalg as kla
    from . import kmotor_pro_solver as ksolve
    from . import kmotor_pro_persist as kpers

class KMotorProPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "KMotor_Pro"
        self.category = "Modify Drawing PCB"
        self.description = "KMotor_Pro - Parametric PCB motor generator for KiCad"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'kmotor_pro_24x24.png')
    def Run( self ):
        self.frame = wx.FindWindowByName("PcbFrame")
        self.board = pcbnew.GetBoard()
        dlg = KMotorProDialog(self.frame, self.board)
        dlg.SetIcon( wx.Icon(self.icon_file_name) )
        dlg.Show()

class KMotorProDialog ( kmotor_pro_gui.KMotorProGUI ):

    group = None
    SCALE = 0
    KICAD_VERSION = 0
    GENERATED_ZONE_PRIORITIES = {
        "outer_cu": 111,
        "inner_cu": 112,
        "outer_mask": 113,
        "inner_mask": 114,
    }
    GENERATED_ZONE_NAME_PREFIX = "kmotor_pro:"

    tl = 0
    tr = 0

    outline = None
    trmtype = None
    fpoint = None
    angle = None

    tthick = 35e-6 # [m] copper thickness (1oz layer specs)
    COPPER_WEIGHT_TO_THICKNESS_M = {
        "0.5 oz / 18um": 18e-6,
        "1 oz / 35um": 35e-6,
        "2 oz / 70um": 70e-6,
        "3 oz / 105um": 105e-6,
    }

    term_tht_db = {
        "0.1"   : "SolderWire-0.1sqmm_1x01_D0.4mm_OD1mm",
        "0.15"  : "SolderWire-0.15sqmm_1x01_D0.5mm_OD1.5mm",
        "0.25"  : "SolderWire-0.25sqmm_1x01_D0.65mm_OD1.7mm",
        "0.5"   : "SolderWire-0.5sqmm_1x01_D0.9mm_OD2.1mm",
        "0.75"  : "SolderWire-0.75sqmm_1x01_D1.25mm_OD2.3mm",
        "1.0"   : "SolderWire-1sqmm_1x01_D1.4mm_OD2.7mm",
        "1.5"   : "SolderWire-1.5sqmm_1x01_D1.7mm_OD3.9mm",
        "2.0"   : "SolderWire-2sqmm_1x01_D2mm_OD3.9mm",
        "2.5"   : "SolderWire-2.5sqmm_1x01_D2.4mm_OD3.6mm"
    }
    term_smd_db = {
        "1"     : "TestPoint_Pad_1.0x1.0mm",
        "1.5"   : "TestPoint_Pad_1.5x1.5mm",
        "2"     : "TestPoint_Pad_2.0x2.0mm",
        "2.5"   : "TestPoint_Pad_2.5x2.5mm",
        "3"     : "TestPoint_Pad_3.0x3.0mm",
        "4"     : "TestPoint_Pad_4.0x4.0mm",
    }
    term_db = {
        "THT"   : term_tht_db,
        "SMD"   : term_smd_db
    }

    mhole_db = {
        "M2"    : "MountingHole_2.2mm_M2_Pad",
        "M2.5"  : "MountingHole_2.7mm_M2.5_Pad",
        "M3"    : "MountingHole_3.2mm_M3_Pad",
        "M3.5"  : "MountingHole_3.7mm_M3.5_Pad",
        "M4"    : "MountingHole_4.3mm_M4_Pad",
        "M5"    : "MountingHole_5.3mm_M5_Pad",
        "M6"    : "MountingHole_6.4mm_M6_Pad",
        "M8"    : "MountingHole_8.4mm_M8_Pad",
    }

    def __init__(self,  parent, board):
        kmotor_pro_gui.KMotorProGUI.__init__(self, parent)

        self.board = board
        self.generated_zone_tokens = set()
        self.center_via_warning_count = 0
        self.KICAD_VERSION = int(pcbnew.Version().split(".")[0])
        if self.KICAD_VERSION < 7:
            self.SCALE = pcbnew.IU_PER_MM
            self.fpoint = pcbnew.wxPoint
            self.fpoint_vector = pcbnew.wxPoint_Vector
            self.fsize = pcbnew.wxSize
        else:
            self.SCALE = pcbnew.FromMM(1)
            self.fpoint = pcbnew.VECTOR2I
            self.fpoint_vector = pcbnew.VECTOR_VECTOR2I
            self.fsize = pcbnew.VECTOR2I

        self.pf = os.path.join(
            pcbnew.SETTINGS_MANAGER.GetUserSettingsPath(),
            "kmotor_pro.cfg"
        )

        self.init_persist(self.pf)
        self.init_path()
        self.init_nets()
        self.on_cb_outline(None)
        self.on_cb_trmtype(None)
        self.on_cb_winding_mode(None)
        self.on_cb_magnet_shape(None)
        self.set_status("Ready")
    
    def eda_angle(self,angle):
        if self.KICAD_VERSION < 7:
            return angle *180/math.pi *100
        else:
            return pcbnew.EDA_ANGLE(angle, pcbnew.RADIANS_T)

    def init_persist(self, configFile):
        self.pm = PM.PersistenceManager.Get()
        self.pm.SetPersistenceFile(configFile)
        self.pm.RegisterAndRestoreAll(self)

    def _point_xy(self, pt):
        if hasattr(pt, "x") and hasattr(pt, "y"):
            return float(pt.x), float(pt.y)
        try:
            return float(pt[0,0]), float(pt[0,1])
        except Exception:
            flat = np.asarray(pt).reshape(-1)
            return float(flat[0]), float(flat[1])

    def _as_point(self, x, y):
        return self.fpoint(int(round(x)), int(round(y)))

    def _item_token(self, item):
        for getter in ("GetUuid", "GetKIID"):
            if hasattr(item, getter):
                try:
                    kiid = getattr(item, getter)()
                    if hasattr(kiid, "AsString"):
                        return kiid.AsString()
                    return str(kiid)
                except Exception:
                    pass
        if hasattr(item, "m_Uuid"):
            try:
                return item.m_Uuid.AsString()
            except Exception:
                pass
        return str(id(item))

    def _tag_generated_zone(self, zone, kind):
        priority = self.GENERATED_ZONE_PRIORITIES[kind]
        try:
            zone.SetAssignedPriority(priority)
        except Exception:
            pass
        zone_name = self.GENERATED_ZONE_NAME_PREFIX + kind
        for setter in ("SetZoneName", "SetName"):
            if hasattr(zone, setter):
                try:
                    getattr(zone, setter)(zone_name)
                    break
                except Exception:
                    pass
        self.generated_zone_tokens.add(self._item_token(zone))

    def _is_generated_zone(self, zone):
        token = self._item_token(zone)
        if token in self.generated_zone_tokens:
            return True
        for getter in ("GetZoneName", "GetName"):
            if hasattr(zone, getter):
                try:
                    name = getattr(zone, getter)()
                    if name and str(name).startswith(self.GENERATED_ZONE_NAME_PREFIX):
                        return True
                except Exception:
                    pass
        if hasattr(zone, "GetAssignedPriority"):
            try:
                return zone.GetAssignedPriority() in self.GENERATED_ZONE_PRIORITIES.values()
            except Exception:
                pass
        return False

    def _cleanup_generated_zones(self):
        zones_to_remove = []
        for zone in self.board.Zones():
            if self._is_generated_zone(zone):
                zones_to_remove.append(zone)
        for zone in zones_to_remove:
            self.board.Remove(zone)

    def _radial_vector(self, angle, radius=1.0):
        return np.array([radius * math.cos(angle), radius * math.sin(angle)])

    def _tangent_vector(self, angle, scale=1.0):
        return np.array([-scale * math.sin(angle), scale * math.cos(angle)])

    def _point_radius(self, pt):
        x, y = self._point_xy(pt)
        return math.hypot(x, y)

    def _nearest_point_distance(self, radius, angle, pts):
        target = np.array([radius * math.cos(angle), radius * math.sin(angle)])
        best = None
        for pt in pts:
            x, y = self._point_xy(pt)
            dist = math.hypot(x - target[0], y - target[1])
            if best is None or dist < best:
                best = dist
        return best

    def _get_outline_outer_radius(self):
        if self.n_edges == 0:
            return float(self.r_out)
        return float(self.r_out) / max(math.cos(math.pi / self.n_edges), 1e-6)

    def _get_outline_corners(self):
        if self.n_edges < 4:
            return None
        points = self._outline_poly_points(self.r_out, self.n_edges)
        if not points:
            return None
        return [self._point_xy(pt) for pt in points]

    def _get_outline_bounds(self):
        corners = self._get_outline_corners()
        if not corners or len(corners) < 4:
            return None
        xs = [p[0] for p in corners]
        ys = [p[1] for p in corners]
        return (min(xs), max(xs), min(ys), max(ys))

    def _clip_segment_to_outline_box(self, start_xy, end_xy, margin=0.0):
        bounds = self._get_outline_bounds()
        if not bounds or self.n_edges != 4:
            return start_xy, end_xy

        xmin, xmax, ymin, ymax = bounds
        xmin += margin
        xmax -= margin
        ymin += margin
        ymax -= margin

        x0, y0 = start_xy
        x1, y1 = end_xy
        dx = x1 - x0
        dy = y1 - y0
        p = (-dx, dx, -dy, dy)
        q = (x0 - xmin, xmax - x0, y0 - ymin, ymax - y0)
        u1 = 0.0
        u2 = 1.0

        for pi, qi in zip(p, q):
            if abs(pi) < 1e-12:
                if qi < 0:
                    return None
                continue
            t = qi / pi
            if pi < 0:
                if t > u2:
                    return None
                u1 = max(u1, t)
            else:
                if t < u1:
                    return None
                u2 = min(u2, t)

        return (
            (x0 + u1 * dx, y0 + u1 * dy),
            (x0 + u2 * dx, y0 + u2 * dy),
        )

    def _rotate_xy(self, xy, angle):
        x, y = xy
        ca = math.cos(angle)
        sa = math.sin(angle)
        return (x * ca - y * sa, x * sa + y * ca)

    def _rotate_about_xy(self, xy, center_xy, angle):
        x, y = xy
        cx, cy = center_xy
        xr, yr = self._rotate_xy((x - cx, y - cy), angle)
        return (xr + cx, yr + cy)

    def _offset_xy(self, xy, origin_xy):
        return (xy[0] + origin_xy[0], xy[1] + origin_xy[1])

    def _get_board_span(self):
        return 2.0 * float(self.r_out)

    def _get_magnet_board_origin(self):
        span = self._get_board_span()
        return (span * 1.1, 0.0)

    def _get_pcb_text_position(self, text_size):
        margin = max(2.0 * text_size, 1.2 * self.SCALE)
        outer = self._get_outline_outer_radius()
        inner_limit = max(float(self.r_coil_out) + self.trk_w + margin, 0.0)
        radius = max(inner_limit, outer - margin)
        radius = min(radius, outer - text_size)
        if radius <= inner_limit:
            radius = inner_limit

        angles = (-math.pi / 4.0, math.pi / 4.0)
        mounting_radii = [self.r_mh_out, self.r_mh_in]
        for angle in angles:
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            blocked = False
            for mount_r in mounting_radii:
                if mount_r <= 0:
                    continue
                if abs(math.hypot(x, y) - mount_r) <= max(self.w_mnt, margin):
                    blocked = True
                    break
            if not blocked:
                return self._as_point(x, y)
        return self._as_point(radius * math.cos(angles[0]), radius * math.sin(angles[0]))

    def _get_bottom_right_info_anchor(self):
        corners = self._get_outline_corners()
        if corners and len(corners) >= 4:
            xs = [p[0] for p in corners]
            ys = [p[1] for p in corners]
            outline_r = max(self._get_outline_outer_radius(), self.r_coil_out)
            text_x = max(xs) - max(18.0 * self.SCALE, 0.27 * outline_r)
            text_y = min(ys) + max(7.5 * self.SCALE, 0.10 * outline_r)
            return (text_x, text_y)
        outer = self._get_outline_outer_radius()
        return (0.32 * outer, -0.72 * outer)

    def _get_terminal_label_position(self, pad_pos, angle):
        pad_r = 0.5 * self.get_selected_terminal_od_iu()
        radial_offset = pad_r + max(self.trk_space, int(1.2 * self.SCALE))
        tangential_offset = max(int(0.8 * pad_r), int(0.8 * self.SCALE))
        radial = self._radial_vector(angle, radial_offset)
        tangent_sign = 1.0 if math.cos(angle) >= 0 else -1.0
        tangent = self._tangent_vector(angle, tangent_sign * tangential_offset)
        px, py = self._point_xy(pad_pos)
        return self._as_point(px + radial[0] + tangent[0], py + radial[1] + tangent[1])

    def _add_silk_segment(self, start_xy, end_xy, width=None, clip_to_outline=False, clip_margin=0.0):
        if clip_to_outline:
            clipped = self._clip_segment_to_outline_box(start_xy, end_xy, clip_margin)
            if clipped is None:
                return None
            start_xy, end_xy = clipped
        seg = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(self._as_point(start_xy[0], start_xy[1]))
        seg.SetEnd(self._as_point(end_xy[0], end_xy[1]))
        seg.SetLayer(pcbnew.F_SilkS)
        seg.SetWidth(int(width if width is not None else max(1, 0.127 * self.SCALE)))
        self.board.Add(seg)
        return seg

    def _add_silk_circle(self, radius, width=None):
        return self._add_silk_circle_at((0.0, 0.0), radius, width)

    def _add_silk_circle_at(self, center_xy, radius, width=None):
        circle = pcbnew.PCB_SHAPE(self.board)
        circle.SetShape(pcbnew.SHAPE_T_CIRCLE)
        circle.SetFilled(False)
        cx, cy = center_xy
        circle.SetStart(self._as_point(cx, cy))
        circle.SetEnd(self._as_point(cx + radius, cy))
        circle.SetCenter(self._as_point(cx, cy))
        circle.SetLayer(pcbnew.F_SilkS)
        circle.SetWidth(int(width if width is not None else max(1, 0.127 * self.SCALE)))
        self.board.Add(circle)
        return circle

    def _add_edge_cuts_circle_at(self, center_xy, radius, width=None):
        circle = pcbnew.PCB_SHAPE(self.board)
        circle.SetShape(pcbnew.SHAPE_T_CIRCLE)
        circle.SetFilled(False)
        cx, cy = center_xy
        circle.SetStart(self._as_point(cx, cy))
        circle.SetEnd(self._as_point(cx + radius, cy))
        circle.SetCenter(self._as_point(cx, cy))
        circle.SetLayer(pcbnew.Edge_Cuts)
        circle.SetWidth(int(width if width is not None else max(1, 0.09 * self.SCALE)))
        self.board.Add(circle)
        return circle

    def _clear_generated_corner_holes(self):
        for fp in list(self.board.GetFootprints()):
            ref = fp.GetReferenceAsString() if hasattr(fp, "GetReferenceAsString") else ""
            if ref.startswith("KMH_"):
                self.board.RemoveNative(fp)

    def _add_npth_hole_at(self, center_xy, radius, index):
        fp = pcbnew.FOOTPRINT(self.board)
        fp.SetReference(f"KMH_{index}")
        fp.SetValue("")
        fp.SetPosition(self._as_point(0, 0))
        if hasattr(fp, "Reference"):
            try:
                fp.Reference().SetVisible(False)
            except Exception:
                pass
        if hasattr(fp, "Value"):
            try:
                fp.Value().SetVisible(False)
            except Exception:
                pass

        pad = pcbnew.PAD(fp)
        dia = int(max(2.0 * radius, 1))
        pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetDrillSize(self.fsize(dia, dia))
        pad.SetSize(self.fsize(dia, dia))
        pad.SetPosition(self._as_point(center_xy[0], center_xy[1]))
        try:
            pad.SetLayerSet(pcbnew.LSET.AllCuMask())
        except Exception:
            pass
        fp.Add(pad)
        self.board.Add(fp)
        return fp

    def _add_silk_arc_ticks(self, radius, angle_start, angle_end, step_deg=1.0, tick_inner=0.8, tick_outer=0.0, major_step=5):
        angle = angle_start
        while angle <= angle_end + 1e-9:
            deg = int(round(math.degrees(angle)))
            tick_len = tick_inner * self.SCALE
            if deg % 10 == 0:
                tick_len *= 3.2
            elif major_step and deg % major_step == 0:
                tick_len *= 2.0
            r0 = radius - tick_len
            r1 = radius + (tick_outer * self.SCALE)
            a = angle
            p0 = (r0 * math.cos(a), r0 * math.sin(a))
            p1 = (r1 * math.cos(a), r1 * math.sin(a))
            self._add_silk_segment(p0, p1)
            angle += math.radians(step_deg)

    def _add_local_tick_fan(self, center_xy, base_angle, fan_deg=18.0, radius_mm=3.0):
        cx, cy = center_xy
        radius = radius_mm * self.SCALE
        start = math.radians(-fan_deg)
        end = math.radians(fan_deg)
        angle = start
        while angle <= end + 1e-9:
            deg = int(round(abs(math.degrees(angle))))
            if deg % 10 == 0:
                tick = 1.2 * self.SCALE
            elif deg % 5 == 0:
                tick = 0.8 * self.SCALE
            else:
                tick = 0.45 * self.SCALE
            local_angle = base_angle + angle
            p0 = (cx + (radius - tick) * math.cos(local_angle), cy + (radius - tick) * math.sin(local_angle))
            p1 = (cx + radius * math.cos(local_angle), cy + radius * math.sin(local_angle))
            self._add_silk_segment(p0, p1)
            angle += math.radians(1.0)

    def _add_linear_hole_scale(self, center_xy, radial_angle, hole_radius):
        cx, cy = center_xy
        radial = np.array([math.cos(radial_angle), math.sin(radial_angle)])
        axis_dir = np.array([math.cos(radial_angle), math.sin(radial_angle)])
        perp_dir = np.array([-math.sin(radial_angle), math.cos(radial_angle)])
        inward = -radial
        step_deg = max(0.1, float(getattr(self, "corner_scale_step_deg", 1.0)))
        base_hole_count = max(1, int(getattr(self, "corner_hole_count", 4)))
        angle_span = float(getattr(self, "corner_scale_span_deg", 5.0))
        auto_hole_count = max(3, int(round((2.0 * angle_span) / step_deg)) + 1)
        hole_count = max(base_hole_count, auto_hole_count)

        arc_radius = math.hypot(cx, cy)
        hole_arc_center = np.array([0.0, 0.0])
        hole_angles = np.linspace(
            radial_angle - math.radians(angle_span),
            radial_angle + math.radians(angle_span),
            hole_count,
        )
        hole_positions = []
        for hole_idx, angle in enumerate(hole_angles):
            hc = hole_arc_center + np.array([arc_radius * math.cos(angle), arc_radius * math.sin(angle)])
            hole_positions.append(hc)
            self._add_npth_hole_at((hc[0], hc[1]), hole_radius, hole_idx)

        # Base construction:
        # - 0deg hole center is the offset point
        # - helper line is parallel to the corner diagonal and shifted inward by r_hole
        # - holes stay on the outer side of the helper line
        # - coarse/fine marks stand perpendicular on the inner side of that helper line
        base_hole_center = np.array([cx, cy])
        helper_center = base_hole_center + inward * (hole_radius + 0.25 * self.SCALE)
        helper_half_len = max(1.2 * self.SCALE, 0.8 * hole_radius)
        p0 = helper_center - axis_dir * helper_half_len
        p1 = helper_center + axis_dir * helper_half_len
        self._add_silk_segment(
            tuple(p0),
            tuple(p1),
            width=max(1, 0.10 * self.SCALE),
            clip_to_outline=True,
            clip_margin=0.35 * self.SCALE,
        )

        def add_rotated_line_block(step_deg_local, span_deg_local, tick_len, width):
            count = max(1, int(round(span_deg_local / step_deg_local)))
            base_anchor = helper_center
            base_q0 = tuple(base_anchor)
            base_q1 = tuple(base_anchor + inward * tick_len)
            for idx in range(-count, count + 1):
                delta = math.radians(idx * step_deg_local)
                q0 = self._rotate_xy(base_q0, delta)
                q1 = self._rotate_xy(base_q1, delta)
                self._add_silk_segment(
                    q0,
                    q1,
                    width=width,
                    clip_to_outline=True,
                    clip_margin=0.35 * self.SCALE,
                )

        # Coarse degree marks: 1 degree, longer lines, opposite side of the helper line.
        add_rotated_line_block(
            1.0,
            angle_span,
            tick_len=max(7.0 * self.SCALE, 4.0 * hole_radius),
            width=max(1, 0.08 * self.SCALE),
        )

        # Fine degree marks: current step, short lines close to the helper line.
        add_rotated_line_block(
            step_deg,
            angle_span,
            tick_len=max(2.2 * self.SCALE, 1.2 * hole_radius),
            width=max(1, 0.10 * self.SCALE),
        )

    def _iter_outer_mount_points(self):
        if self.n_edges == 4 and self.corner_hole_offset > 0:
            corners = self._get_outline_corners()
            if corners and len(corners) >= 4:
                xs = [p[0] for p in corners]
                ys = [p[1] for p in corners]
                max_x = max(xs)
                max_y = max(ys)
                off = float(self.corner_hole_offset)
                dia = max(float(self.corner_hole_dia), 0.0)
                d = off / math.sqrt(2.0)
                points = [
                    ( max_x - d,  max_y - d, math.radians(45.0), dia),
                    (-max_x + d,  max_y - d, math.radians(135.0), dia),
                    (-max_x + d, -max_y + d, math.radians(225.0), dia),
                    ( max_x - d, -max_y + d, math.radians(315.0), dia),
                ]
                return points[:max(0, min(len(points), int(self.corner_hole_count)))]
        if self.n_mh_out <= 0 or self.r_mh_out <= 0:
            return []
        radius = float(self.r_mh_out)
        if self.n_edges > 0:
            radius /= max(math.cos(math.pi / self.n_edges), 1e-6)
        th0 = 2 * math.pi / self.n_mh_out
        points = []
        for idx in range(self.n_mh_out):
            angle = th0 * idx + th0 / 2.0
            points.append((radius * math.cos(angle), radius * math.sin(angle), angle, max(float(self.corner_hole_dia), 3.2 * self.SCALE)))
        return points

    def _add_silk_cross_guides(self, radius):
        corners = self._get_outline_corners()
        if corners and len(corners) >= 4:
            xs = [p[0] for p in corners]
            ys = [p[1] for p in corners]
            self._add_silk_segment((min(xs), 0.0), (max(xs), 0.0))
            self._add_silk_segment((0.0, min(ys)), (0.0, max(ys)))
            self._add_silk_segment(corners[0], corners[2])
            self._add_silk_segment(corners[1], corners[3])
            return
        guide_r = radius
        self._add_silk_segment((-guide_r, 0.0), (guide_r, 0.0))
        self._add_silk_segment((0.0, -guide_r), (0.0, guide_r))
        diag = guide_r / math.sqrt(2.0)
        self._add_silk_segment((-diag, -diag), (diag, diag))
        self._add_silk_segment((-diag, diag), (diag, -diag))

    def _add_silk_slot_frames(self, ri, ro):
        inner_r = ri
        outer_r = ro
        half_slot = math.pi / max(self.n_slots, 1)
        for idx in range(self.n_slots):
            a0 = idx * (2 * math.pi / self.n_slots) - half_slot
            a1 = idx * (2 * math.pi / self.n_slots) + half_slot
            p00 = (inner_r * math.cos(a0), inner_r * math.sin(a0))
            p01 = (outer_r * math.cos(a0), outer_r * math.sin(a0))
            p10 = (inner_r * math.cos(a1), inner_r * math.sin(a1))
            p11 = (outer_r * math.cos(a1), outer_r * math.sin(a1))
            self._add_silk_segment(p00, p01)
            self._add_silk_segment(p10, p11)

    def _add_silk_hole_scales(self):
        self._clear_generated_corner_holes()
        for x, y, angle, dia in self._iter_outer_mount_points():
            self._add_linear_hole_scale((x, y), angle, max(dia * 0.5, 0.5 * self.SCALE))

    def _add_silk_text(self, text, pos_xy, size_scale=1.0, align="right"):
        txt = pcbnew.PCB_TEXT(self.board)
        txt.SetText(text)
        size = int(max(self.txt_size * size_scale, 0.4 * self.SCALE))
        txt.SetTextSize(self.fsize(size, size))
        txt.SetPosition(self._as_point(pos_xy[0], pos_xy[1]))
        if hasattr(txt, "SetHorizJustify"):
            if align == "left":
                txt.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
            else:
                txt.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_RIGHT)
        txt.SetLayer(pcbnew.F_SilkS)
        self.board.Add(txt)
        return txt

    def _add_grouped_silk_segment(self, group, start_xy, end_xy, width=None):
        return self._add_grouped_segment(group, start_xy, end_xy, pcbnew.F_SilkS, width if width is not None else max(1, 0.127 * self.SCALE))

    def _add_grouped_segment(self, group, start_xy, end_xy, layer, width):
        seg = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(self._as_point(start_xy[0], start_xy[1]))
        seg.SetEnd(self._as_point(end_xy[0], end_xy[1]))
        seg.SetLayer(layer)
        seg.SetWidth(int(width))
        self.board.Add(seg)
        if group is not None:
            group.AddItem(seg)
        return seg

    def _add_grouped_silk_circle(self, group, center_xy, radius, width=None):
        return self._add_grouped_circle(group, center_xy, radius, pcbnew.F_SilkS, width if width is not None else max(1, 0.127 * self.SCALE))

    def _add_grouped_circle(self, group, center_xy, radius, layer, width):
        circle = pcbnew.PCB_SHAPE(self.board)
        circle.SetShape(pcbnew.SHAPE_T_CIRCLE)
        circle.SetFilled(False)
        circle.SetStart(self._as_point(center_xy[0], center_xy[1]))
        circle.SetEnd(self._as_point(center_xy[0] + radius, center_xy[1]))
        circle.SetCenter(self._as_point(center_xy[0], center_xy[1]))
        circle.SetLayer(layer)
        circle.SetWidth(int(width))
        self.board.Add(circle)
        if group is not None:
            group.AddItem(circle)
        return circle

    def _add_grouped_edge_circle(self, group, center_xy, radius, width=None):
        return self._add_grouped_circle(group, center_xy, radius, pcbnew.Edge_Cuts, width if width is not None else max(1, 0.09 * self.SCALE))

    def _get_magnet_aux_layer(self):
        return getattr(pcbnew, "Dwgs_User", pcbnew.F_SilkS)

    def _add_grouped_rect_outline(self, group, center_xy, half_w, half_h, angle, layer, width):
        tang = np.array([-math.sin(angle), math.cos(angle)])
        rad = np.array([math.cos(angle), math.sin(angle)])
        pts = []
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            p = np.array(center_xy) + tang * (sx * half_w) + rad * (sy * half_h)
            pts.append((p[0], p[1]))
        for i in range(4):
            self._add_grouped_segment(group, pts[i], pts[(i + 1) % 4], layer, width)
        return pts

    def get_parameters(self):
        self.outline = self.m_cbOutline.GetStringSelection()
        if self.outline=="Circle":
            self.n_edges = 0
        elif self.outline=="Square":
            self.n_edges = 4
        elif self.outline=="Hexagon":
            self.n_edges = 6
        elif self.outline=="Octagon":
            self.n_edges = 8
        else:
            self.n_edges = -1

        self.trmtype = self.m_cbTP.GetStringSelection()
        scheme = self.m_cbScheme.GetStringSelection()
        if scheme == "1P":
            self.phases = 1
            self.n_term = 2
        elif scheme == "3P+N":
            self.phases = 3
            self.n_term = 4
        else:
            self.phases = 3
            self.n_term = 3
        
        self.n_layers = int(self.m_ctrlLayers.GetValue())
        self.lset = self.udpate_lset(self.n_layers)
        self.n_loops  = int(self.m_ctrlLoops.GetValue())
        self.n_slots  = int(self.m_ctrlSlots.GetValue())
        self.winding_mode = self.m_cbWindingMode.GetStringSelection() if hasattr(self, "m_cbWindingMode") else "PCB"
        self.copper_weight = self.m_cbCopperWeight.GetStringSelection() if hasattr(self, "m_cbCopperWeight") else "1 oz / 35um"
        self.copper_thickness_m = self.COPPER_WEIGHT_TO_THICKNESS_M.get(self.copper_weight, self.tthick)
        self.wire_dia_mm = float(self.m_ctrlWireDia.GetValue()) if hasattr(self, "m_ctrlWireDia") else 0.50
        
        self.strategy = self.m_cbStrategy.GetSelection()

        self.trk_w = int(self.m_ctrlTrackWidth.GetValue() * self.SCALE) 
        self.trk_space = int(self.m_ctrlTrackSpacing.GetValue() * self.SCALE) 
        self.dr = self.trk_w + self.trk_space
        
        self.ring_w = int(self.m_ctrlRingWidth.GetValue() * self.SCALE)
        self.ring_space = int(self.m_ctrlRingSpacing.GetValue() * self.SCALE)
        self.ring_dr = self.ring_w + self.ring_space

        self.d_via = int(self.m_ctrlViaDia.GetValue() * self.SCALE)   
        self.d_drill = int(self.m_ctrlViaDrill.GetValue() * self.SCALE) 
        self.d_support_hole = int(self.m_ctrlSupportHoleDia.GetValue() * self.SCALE) if hasattr(self, "m_ctrlSupportHoleDia") else self.d_drill

        self.via_rows = 2
        try:
            if hasattr(self, "m_cbSupportViaMode"):
                self.support_via_mode = int(self.m_cbSupportViaMode.GetStringSelection())
            elif hasattr(self, "m_cbSupportVias"):
                self.support_via_mode = int(self.m_cbSupportVias.GetStringSelection())
            else:
                self.support_via_mode = 2
        except (ValueError, TypeError):
            self.support_via_mode = 2
        if self.support_via_mode not in (0, 2, 4):
            self.support_via_mode = 2

        if hasattr(self, "m_cbFillInnerGND"):
            self.fill_inner_gnd = bool(self.m_cbFillInnerGND.IsChecked() if hasattr(self.m_cbFillInnerGND, "IsChecked") else self.m_cbFillInnerGND.GetValue())
        elif hasattr(self, "m_chkFillInnerGnd"):
            self.fill_inner_gnd = bool(self.m_chkFillInnerGnd.IsChecked() if hasattr(self.m_chkFillInnerGnd, "IsChecked") else self.m_chkFillInnerGnd.GetValue())
        else:
            self.fill_inner_gnd = True
        if hasattr(self, "m_cbFillOuterGND"):
            self.fill_outer_gnd = bool(self.m_cbFillOuterGND.IsChecked() if hasattr(self.m_cbFillOuterGND, "IsChecked") else self.m_cbFillOuterGND.GetValue())
        elif hasattr(self, "m_chkFillOuterGnd"):
            self.fill_outer_gnd = bool(self.m_chkFillOuterGnd.IsChecked() if hasattr(self.m_chkFillOuterGnd, "IsChecked") else self.m_chkFillOuterGnd.GetValue())
        else:
            self.fill_outer_gnd = True
        self.silk_cross_guides = bool(self.m_cbSilkCross.GetValue()) if hasattr(self, "m_cbSilkCross") else False
        self.silk_deg_scale = bool(self.m_cbSilkDeg.GetValue()) if hasattr(self, "m_cbSilkDeg") else False
        self.silk_slot_frames = bool(self.m_cbSilkSlots.GetValue()) if hasattr(self, "m_cbSilkSlots") else False
        self.silk_hole_scales = bool(self.m_cbSilkHoleScale.GetValue()) if hasattr(self, "m_cbSilkHoleScale") else False
        self.corner_hole_offset = float(self.m_ctrlCornerHoleOffset.GetValue()) * self.SCALE if hasattr(self, "m_ctrlCornerHoleOffset") else 0.0
        self.corner_hole_dia = float(self.m_ctrlCornerHoleDia.GetValue()) * self.SCALE if hasattr(self, "m_ctrlCornerHoleDia") else 0.0
        self.corner_hole_count = int(self.m_ctrlCornerHoleCount.GetValue()) if hasattr(self, "m_ctrlCornerHoleCount") else 4
        self.corner_scale_step_deg = float(self.m_ctrlCornerScaleStep.GetValue()) if hasattr(self, "m_ctrlCornerScaleStep") else 1.0
        self.corner_scale_span_deg = float(self.m_ctrlCornerScaleSpan.GetValue()) if hasattr(self, "m_ctrlCornerScaleSpan") else 5.0
        if hasattr(self, "m_ctrlInnerGndDia"):
            self.inner_fill_dia = int(max(0.0, float(self.m_ctrlInnerGndDia.GetValue())) * self.SCALE)
        else:
            self.inner_fill_dia = 0

        self.r_fill = int(self.m_ctrlRfill.GetValue() * self.SCALE)         
        self.o_fill = int(self.m_ctrlFilletRadius.GetValue() * self.SCALE)  

        self.r_in = int(self.m_ctrlDbore.GetValue() /2 * self.SCALE)
        self.r_out = int(self.m_ctrlDout.GetValue() /2 * self.SCALE) 
        self.r_coil_in = int(self.m_ctrlDin.GetValue() /2 * self.SCALE )
        self.r_coil_out = int(self.m_ctrlDend.GetValue() /2 * self.SCALE )
        
        self.w_mnt = int(self.m_ctrlWmnt.GetValue() * self.SCALE) 
        self.term_offset = int(self.m_ctrlDterm.GetValue() * self.SCALE)
        
        self.mhs = self.m_cbMountSize.GetStringSelection()
        self.n_mh_out = int(self.m_mhOut.GetValue())
        self.r_mh_out = int(self.m_mhOutR.GetValue() /2 * self.SCALE)
        self.n_mh_in = int(self.m_mhIn.GetValue())
        self.r_mh_in = int(self.m_mhInR.GetValue() /2 * self.SCALE)

        self.txt_size = int(0.5 * self.SCALE)
        self.txt_loc = int(self.r_out - 3*self.txt_size)

        if self.group:
            self.btn_clear.Enable(True)

    def _effective_winding_layers(self):
        return max(int(getattr(self, "n_layers", 1)), 1)

    def _winding_pitch_mm(self):
        if getattr(self, "winding_mode", "PCB") == "Wire":
            return max(self.wire_dia_mm + (self.trk_space / self.SCALE), self.wire_dia_mm, 1e-6)
        return max((self.trk_w + self.trk_space) / self.SCALE, 1e-6)

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

    def set_status(self, text):
        ts = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, "lbl_status") and self.lbl_status:
            self.lbl_status.SetLabel(str(text))
            self.lbl_status.GetParent().Layout()
        if hasattr(self, "m_txtStatus") and self.m_txtStatus:
            self.m_txtStatus.SetValue(f"[{ts}] {text}")

    def _format_exception(self, exc):
        msg = str(exc).strip()
        return msg if msg else exc.__class__.__name__

    def _log_exception(self, title, exc):
        detail = self._format_exception(exc)
        tb = traceback.format_exc().strip()
        if tb:
            wx.LogError(f"{title}:\n{detail}\n\n{tb}")
        else:
            wx.LogError(f"{title}:\n{detail}")

    def _safe_ui_yield(self):
        try:
            self.Update()
            wx.YieldIfNeeded()
        except Exception:
            pass

    def _safe_refresh_board(self):
        try:
            self.board.BuildConnectivity()
        except Exception:
            pass
        try:
            pcbnew.Refresh()
        except Exception:
            pass
        try:
            pcbnew.UpdateUserInterface()
        except Exception:
            pass

    def _run_action(self, start_status, success_status, title, callback, summary_target=None):
        self.set_status(start_status)
        self._safe_ui_yield()
        try:
            result = callback()
            self._safe_refresh_board()
            self.set_status(success_status)
            return result
        except Exception as exc:
            message = self._format_exception(exc)
            self.set_status(f"{title} failed")
            if summary_target == "magnet":
                self._update_magnet_summary(message)
            self._log_exception(f"{title} failed", exc)
            return None

    def validate_parameters(self):
        errors = []
        if self.n_slots <= 0:
            errors.append("n_slots muss > 0 sein.")
        if self.n_loops <= 0:
            errors.append("n_loops muss > 0 sein.")
        if self.n_slots < self.phases:
            errors.append(f"n_slots ({self.n_slots}) muss mindestens phases ({self.phases}) sein.")
        if self.n_slots % self.phases != 0:
            errors.append(f"n_slots ({self.n_slots}) muss durch phases ({self.phases}) teilbar sein.")
        return errors

    def get_magnet_parameters(self):
        self.magnet_shape = self.m_cbMagShape.GetStringSelection().lower()
        self.magnet_dia = float(self.m_ctrlMagDia.GetValue()) * self.SCALE
        self.magnet_width = float(self.m_ctrlMagWidth.GetValue()) * self.SCALE
        self.magnet_height = float(self.m_ctrlMagHeight.GetValue()) * self.SCALE
        self.magnet_length = float(self.m_ctrlMagLength.GetValue()) * self.SCALE
        self.magnet_ring_dia = float(self.m_ctrlMagRingDia.GetValue()) * self.SCALE
        self.magnet_pole_pairs = int(self.m_ctrlMagPolePairs.GetValue())
        self.magnet_gap = float(self.m_ctrlMagGap.GetValue()) * self.SCALE
        self.magnet_keepout = float(self.m_ctrlMagKeepout.GetValue()) * self.SCALE
        self.magnet_rotation = float(self.m_ctrlMagRotation.GetValue())
        self.magnet_b_est = float(self.m_ctrlMagBest.GetValue()) if hasattr(self, "m_ctrlMagBest") else 0.60
        self.magnet_poles = max(self.magnet_pole_pairs * 2, 0)

    def validate_magnet_parameters(self):
        self.get_magnet_parameters()
        errors = []
        warnings = []

        if self.magnet_pole_pairs <= 0:
            errors.append("Pole pairs must be > 0.")
        if self.magnet_ring_dia <= 0:
            errors.append("Magnet ring dia must be > 0.")

        if self.magnet_shape == "round":
            if self.magnet_dia <= 0:
                errors.append("Magnet dia must be > 0 for round magnets.")
            magnet_span = self.magnet_dia
            radial_span = self.magnet_dia
        else:
            if self.magnet_width <= 0 or self.magnet_height <= 0:
                errors.append("Magnet width and height must be > 0 for rectangular magnets.")
            magnet_span = self.magnet_width
            radial_span = self.magnet_height

        if errors:
            return errors, warnings

        radius = self.magnet_ring_dia * 0.5
        circumference = 2.0 * math.pi * radius
        required_arc = self.magnet_poles * max(magnet_span + self.magnet_gap + self.magnet_keepout, 0.0)
        pole_pitch_arc = circumference / max(self.magnet_poles, 1)
        if required_arc > circumference:
            errors.append(
                "Magnets do not fit on the selected ring diameter. "
                f"Required arc {required_arc / self.SCALE:.2f} mm > circumference {circumference / self.SCALE:.2f} mm."
            )
        if (magnet_span + self.magnet_gap + self.magnet_keepout) > pole_pitch_arc:
            errors.append(
                "Single magnet pitch is too large for the selected pole count. "
                f"Needed { (magnet_span + self.magnet_gap + self.magnet_keepout) / self.SCALE:.2f} mm > "
                f"available { pole_pitch_arc / self.SCALE:.2f} mm."
            )

        inner_edge = radius - (0.5 * radial_span) - self.magnet_keepout
        outer_edge = radius + (0.5 * radial_span) + self.magnet_keepout
        if inner_edge <= float(self.r_in):
            errors.append(
                f"Magnet ring intersects shaft bore region ({inner_edge / self.SCALE:.2f} mm <= {float(self.r_in) / self.SCALE:.2f} mm)."
            )
        if outer_edge >= float(self.r_out):
            errors.append(
                f"Magnet ring exceeds safe board radius ({outer_edge / self.SCALE:.2f} mm >= {float(self.r_out) / self.SCALE:.2f} mm)."
            )

        radial_clearance = 0.5 * radial_span + self.magnet_keepout
        angular_half_span = (0.5 * magnet_span + self.magnet_keepout) / max(radius, 1.0)
        for target_r, target_angle, hr, label in self._iter_magnet_clearance_targets():
            radial_delta = abs(target_r - radius)
            if radial_delta > (radial_clearance + hr):
                continue
            target_half_span = math.asin(min(0.999999, (hr + self.magnet_keepout) / max(target_r, 1.0)))
            angle_delta = self._nearest_magnet_angle_delta(target_angle)
            if angle_delta <= (angular_half_span + target_half_span):
                warnings.append(
                    f"Magnet ring overlaps the clearance zone of {label} near angle {math.degrees(target_angle):.1f} deg."
                )
            else:
                warnings.append(
                    f"Magnet ring is close to {label} (radial delta {radial_delta / self.SCALE:.2f} mm)."
                )

        if self.magnet_ring_dia >= float(self.r_out) * 2.0:
            warnings.append("Magnet ring dia is at or outside board size.")
        if self.magnet_ring_dia <= float(self.r_in) * 2.0:
            warnings.append("Magnet ring dia is close to or inside the shaft bore region.")

        return errors, warnings

    def _update_magnet_summary(self, text):
        if hasattr(self, "lblMagnetSummary") and self.lblMagnetSummary:
            self.lblMagnetSummary.SetLabel(text)
            self.lblMagnetSummary.Wrap(520)
            self.lblMagnetSummary.GetParent().Layout()

    def _get_mounting_hole_dia(self):
        fp_name = self.mhole_db.get(self.mhs or "", "")
        if not fp_name:
            return 0.0
        m = re.search(r"MountingHole_([0-9.]+)mm", fp_name)
        if not m:
            return 0.0
        try:
            return float(m.group(1)) * self.SCALE
        except ValueError:
            return 0.0

    def _iter_magnet_clearance_targets(self):
        targets = []
        mh_dia = self._get_mounting_hole_dia()
        mh_radius = 0.5 * mh_dia if mh_dia > 0 else 0.0

        if self.n_mh_out > 0 and self.r_mh_out > 0:
            radius = float(self.r_mh_out)
            if self.n_edges > 0:
                radius /= max(math.cos(math.pi / self.n_edges), 1e-6)
            th0 = 2 * math.pi / self.n_mh_out
            for i in range(self.n_mh_out):
                angle = th0 * i + th0 / 2.0
                targets.append((radius, angle, mh_radius, "outer mounting holes"))

        if self.n_mh_in > 0 and self.r_mh_in > 0:
            th0 = 2 * math.pi / self.n_mh_in
            for i in range(self.n_mh_in):
                angle = th0 * i + th0 / 2.0
                radius = float(self.r_mh_in)
                targets.append((radius, angle, mh_radius, "inner mounting holes"))

        if self.n_edges == 4 and self.corner_hole_offset > 0 and self.corner_hole_dia > 0:
            for x, y, angle, dia in self._iter_outer_mount_points():
                targets.append((math.hypot(x, y), angle, 0.5 * dia, "corner alignment holes"))

        return targets

    def _angle_delta(self, a, b):
        d = (a - b + math.pi) % (2.0 * math.pi) - math.pi
        return abs(d)

    def _nearest_magnet_angle_delta(self, target_angle):
        if self.magnet_poles <= 0:
            return math.pi
        pitch = 2.0 * math.pi / self.magnet_poles
        rot0 = math.radians(self.magnet_rotation)
        rel = (target_angle - rot0) / pitch
        nearest_idx = round(rel)
        nearest_angle = rot0 + nearest_idx * pitch
        return self._angle_delta(target_angle, nearest_angle)

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

    def _clear_magnet_group(self):
        if getattr(self, "magnet_group", None):
            items = []
            try:
                items = list(self.magnet_group.GetItems())
            except Exception:
                items = []
            for item in items:
                try:
                    self.board.RemoveNative(item)
                except Exception:
                    try:
                        self.board.Remove(item)
                    except Exception:
                        pass
            try:
                self.magnet_group.RemoveAll()
            except Exception:
                pass
            try:
                self.board.Remove(self.magnet_group)
            except Exception:
                pass
            self.magnet_group = None

    def _create_magnet_group(self):
        self._clear_magnet_group()
        self.magnet_group = pcbnew.PCB_GROUP(self.board)
        self.magnet_group.SetName("magnet_pcb")
        self.board.Add(self.magnet_group)
        return self.magnet_group

    def _add_mounting_hole_fp_at(self, group, center_xy, fp_lib, fp_name, ref, net=None):
        m = pcbnew.FootprintLoad(fp_lib, fp_name)
        if m is None:
            return None
        m.Reference().SetVisible(False)
        m.Value().SetVisible(False)
        m.SetReference(ref)
        m.SetPosition(self._as_point(center_xy[0], center_xy[1]))
        if net is not None:
            for pad in m.Pads():
                pad.SetNet(net)
        self.board.Add(m)
        if group is not None:
            group.AddItem(m)
        return m

    def _iter_corner_points_for_origin(self, origin_xy):
        if self.n_edges == 4 and self.corner_hole_offset > 0:
            max_x = float(self.r_out)
            max_y = float(self.r_out)
            off = float(self.corner_hole_offset)
            dia = max(float(self.corner_hole_dia), 0.0)
            d = off / math.sqrt(2.0)
            pts = [
                ( origin_xy[0] + max_x - d, origin_xy[1] + max_y - d, math.radians(45.0), dia),
                ( origin_xy[0] - max_x + d, origin_xy[1] + max_y - d, math.radians(135.0), dia),
                ( origin_xy[0] - max_x + d, origin_xy[1] - max_y + d, math.radians(225.0), dia),
                ( origin_xy[0] + max_x - d, origin_xy[1] - max_y + d, math.radians(315.0), dia),
            ]
            return pts[:max(0, min(len(pts), int(self.corner_hole_count)))]
        return []

    def _add_linear_hole_scale_at(self, group, center_xy, radial_angle, hole_radius, origin_xy):
        cx, cy = center_xy
        axis_dir = np.array([math.cos(radial_angle), math.sin(radial_angle)])
        perp_dir = np.array([-math.sin(radial_angle), math.cos(radial_angle)])
        inward = -perp_dir
        step_deg = max(0.1, float(getattr(self, "corner_scale_step_deg", 1.0)))
        angle_span = float(getattr(self, "corner_scale_span_deg", 5.0))
        hole_count = max(3, int(round((2.0 * angle_span) / step_deg)) + 1)
        hole_angles = np.linspace(
            radial_angle - math.radians(angle_span),
            radial_angle + math.radians(angle_span),
            hole_count,
        )
        arc_radius = math.hypot(cx - origin_xy[0], cy - origin_xy[1])
        for idx, angle in enumerate(hole_angles):
            hc = (
                origin_xy[0] + arc_radius * math.cos(angle),
                origin_xy[1] + arc_radius * math.sin(angle),
            )
            fp = self._add_npth_hole_at(hc, hole_radius, f"{int(origin_xy[0])}_{int(origin_xy[1])}_{idx}")
            if group is not None and fp is not None:
                group.AddItem(fp)

        helper_center = np.array([cx, cy]) + inward * (hole_radius + 0.25 * self.SCALE)
        helper_half_len = max(1.2 * self.SCALE, 0.8 * hole_radius)
        p0 = tuple(helper_center - axis_dir * helper_half_len)
        p1 = tuple(helper_center + axis_dir * helper_half_len)
        self._add_grouped_silk_segment(group, p0, p1, width=max(1, 0.10 * self.SCALE))

        def add_rotated_line_block(step_deg_local, span_deg_local, tick_len, width):
            count = max(1, int(round(span_deg_local / step_deg_local)))
            base_anchor = tuple(helper_center)
            base_q0 = base_anchor
            base_q1 = tuple(helper_center + inward * tick_len)
            for idx in range(-count, count + 1):
                delta = math.radians(idx * step_deg_local)
                q0 = self._rotate_about_xy(base_q0, origin_xy, delta)
                q1 = self._rotate_about_xy(base_q1, origin_xy, delta)
                self._add_grouped_silk_segment(group, q0, q1, width=width)

        add_rotated_line_block(
            1.0,
            angle_span,
            tick_len=max(7.0 * self.SCALE, 4.0 * hole_radius),
            width=max(1, 0.08 * self.SCALE),
        )
        add_rotated_line_block(
            step_deg,
            angle_span,
            tick_len=max(2.2 * self.SCALE, 1.2 * hole_radius),
            width=max(1, 0.10 * self.SCALE),
        )

    def _build_offset_outline(self, group, origin_xy):
        cx, cy = origin_xy
        self._add_grouped_edge_circle(group, origin_xy, self.r_in)
        relief_dia = max(min(0.12 * (2.0 * self.r_in), 2.0 * self.SCALE), 0.8 * self.SCALE) if self.r_in > 0 else 0
        if relief_dia > 0 and self.r_in > (1.5 * relief_dia):
            relief_radius = self.r_in + (0.5 * relief_dia)
            for angle in (math.pi / 4.0, 3.0 * math.pi / 4.0, 5.0 * math.pi / 4.0, 7.0 * math.pi / 4.0):
                rp = (
                    cx + relief_radius * math.cos(angle),
                    cy + relief_radius * math.sin(angle),
                )
                self._add_grouped_edge_circle(group, rp, relief_dia / 2.0)

        if self.n_edges == 0:
            self._add_grouped_edge_circle(group, origin_xy, self.r_out)
            return

        points = self._outline_poly_points(self.r_out, self.n_edges)
        if not points:
            return
        pts = [self._offset_xy(self._point_xy(pt), origin_xy) for pt in points]
        for i in range(len(pts)):
            self._add_grouped_silk_segment(group, pts[i], pts[(i + 1) % len(pts)], width=max(1, 0.09 * self.SCALE))
            seg = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_SEGMENT)
            seg.SetStart(self._as_point(pts[i][0], pts[i][1]))
            seg.SetEnd(self._as_point(pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1]))
            seg.SetLayer(pcbnew.Edge_Cuts)
            self.board.Add(seg)
            if group is not None:
                group.AddItem(seg)

    def _build_offset_mounting_holes(self, group, origin_xy):
        if self.mhs == "None":
            return
        fp_lib = self.fp_path + 'MountingHole.pretty'
        fp = self.mhole_db.get(self.mhs)
        if not fp:
            return
        ni_gnd = self.board.FindNet("gnd")

        if self.n_mh_out > 0:
            r_mh_out = float(self.r_mh_out)
            if self.n_edges > 0:
                r_mh_out /= max(math.cos(math.pi / self.n_edges), 1e-6)
            th0 = 2 * math.pi / self.n_mh_out
            for i in range(self.n_mh_out):
                pos = (
                    origin_xy[0] + r_mh_out * math.cos(th0 * i + th0 / 2.0),
                    origin_xy[1] + r_mh_out * math.sin(th0 * i + th0 / 2.0),
                )
                self._add_mounting_hole_fp_at(group, pos, fp_lib, fp, f"MMO_{i}", net=ni_gnd)

        if self.n_mh_in > 0:
            th0 = 2 * math.pi / self.n_mh_in
            for i in range(self.n_mh_in):
                pos = (
                    origin_xy[0] + float(self.r_mh_in) * math.cos(th0 * i + th0 / 2.0),
                    origin_xy[1] + float(self.r_mh_in) * math.sin(th0 * i + th0 / 2.0),
                )
                self._add_mounting_hole_fp_at(group, pos, fp_lib, fp, f"MMI_{i}", net=ni_gnd)

        if getattr(self, "silk_hole_scales", False):
            for x, y, angle, dia in self._iter_corner_points_for_origin(origin_xy):
                self._add_linear_hole_scale_at(group, (x, y), angle, max(dia * 0.5, 0.5 * self.SCALE), origin_xy)

    def _build_magnet_markers(self, group, origin_xy):
        if self.magnet_poles <= 0:
            return
        radius = 0.5 * float(self.magnet_ring_dia)
        rot0 = math.radians(self.magnet_rotation)
        pitch = 2.0 * math.pi / self.magnet_poles
        aux_layer = self._get_magnet_aux_layer()
        body_width = max(1, 0.12 * self.SCALE)
        keepout_width = max(1, 0.08 * self.SCALE)
        for idx in range(self.magnet_poles):
            angle = rot0 + idx * pitch
            center = (
                origin_xy[0] + radius * math.cos(angle),
                origin_xy[1] + radius * math.sin(angle),
            )
            if self.magnet_shape == "round":
                body_r = 0.5 * float(self.magnet_dia)
                self._add_grouped_silk_circle(group, center, body_r, width=body_width)
                if self.magnet_keepout > 0:
                    self._add_grouped_circle(group, center, body_r + float(self.magnet_keepout), aux_layer, keepout_width)
            else:
                half_w = 0.5 * float(self.magnet_width)
                half_h = 0.5 * float(self.magnet_height)
                self._add_grouped_rect_outline(group, center, half_w, half_h, angle, pcbnew.F_SilkS, body_width)
                if self.magnet_keepout > 0:
                    self._add_grouped_rect_outline(
                        group,
                        center,
                        half_w + float(self.magnet_keepout),
                        half_h + float(self.magnet_keepout),
                        angle,
                        aux_layer,
                        keepout_width,
                    )

    def generate_magnet_pcb(self):
        self.get_parameters()
        errors, warnings = self.validate_magnet_parameters()
        if errors:
            raise ValueError("\n".join(errors))

        origin_xy = self._get_magnet_board_origin()
        group = self._create_magnet_group()
        self._build_offset_outline(group, origin_xy)
        self._build_offset_mounting_holes(group, origin_xy)
        self._build_magnet_markers(group, origin_xy)

        if getattr(self, "silk_cross_guides", False):
            outer = float(self.r_out)
            self._add_grouped_silk_segment(group, (origin_xy[0] - outer, origin_xy[1]), (origin_xy[0] + outer, origin_xy[1]))
            self._add_grouped_silk_segment(group, (origin_xy[0], origin_xy[1] - outer), (origin_xy[0], origin_xy[1] + outer))

        summary = (
            f"Magnet PCB generated at +{origin_xy[0] / self.SCALE:.2f} mm X offset.\n"
            f"Poles: {self.magnet_poles}\n"
            f"Ring dia: {self.magnet_ring_dia / self.SCALE:.2f} mm"
        )
        if warnings:
            summary += "\nWarnings:\n- " + "\n- ".join(warnings)
        self._update_magnet_summary(summary)

    def init_path(self):
        self.fp_path = None
        settings = pcbnew.SETTINGS_MANAGER.GetUserSettingsPath()
        try:
            with open(settings+'/kicad_common.json', 'r') as f:
                data = json.load(f)
                env_vars = data.get("environment", {}).get("vars") or {}
                fp_keys = [
                    f"KICAD{self.KICAD_VERSION}_FOOTPRINT_DIR",
                    "KICAD_FOOTPRINT_DIR",
                    "KICAD6_FOOTPRINT_DIR",
                ]
                for key in fp_keys:
                    if env_vars.get(key):
                        self.fp_path = env_vars[key]
                        break
        except IOError:
            wx.LogError("Settings file not found.")
            return

        if self.fp_path is None:
            for key in (
                f"KICAD{self.KICAD_VERSION}_FOOTPRINT_DIR",
                "KICAD_FOOTPRINT_DIR",
                "KICAD6_FOOTPRINT_DIR",
            ):
                self.fp_path = os.getenv(key, default=None)
                if self.fp_path:
                    break

        if self.fp_path is not None:
            self.fp_path = os.path.normpath(self.fp_path) + os.sep
        else:
            wx.LogError(
                f"Footprint library not found. Expected KICAD{self.KICAD_VERSION}_FOOTPRINT_DIR or KICAD_FOOTPRINT_DIR."
            )

    def init_nets(self):
        gnd = self.board.FindNet("gnd")
        if gnd is None:
            gnd = pcbnew.NETINFO_ITEM(self.board, "gnd")
            self.board.Add(gnd)
            
        coil = self.board.FindNet("coil")
        if coil is None:
            coil = pcbnew.NETINFO_ITEM(self.board, "coil")
            self.board.Add(coil)

    def udpate_lset(self, n_layers):
        lset =[pcbnew.F_Cu]
        if n_layers >= 4:
            lset.append(pcbnew.In1_Cu)
            lset.append(pcbnew.In2_Cu)
        if n_layers >= 6:
            lset.append(pcbnew.In3_Cu)
            lset.append(pcbnew.In4_Cu)
        if n_layers >= 8:
            lset.append(pcbnew.In5_Cu)
            lset.append(pcbnew.In6_Cu)
        if n_layers >= 10:
            lset.append(pcbnew.In7_Cu)
            lset.append(pcbnew.In8_Cu)
        if n_layers >= 12:
            lset.append(pcbnew.In9_Cu)
            lset.append(pcbnew.In10_Cu)
        if n_layers >= 14:
            lset.append(pcbnew.In11_Cu)
            lset.append(pcbnew.In12_Cu)
        if n_layers >= 16:
            lset.append(pcbnew.In13_Cu)
            lset.append(pcbnew.In14_Cu)
        if n_layers >= 18:
            lset.append(pcbnew.In15_Cu)
            lset.append(pcbnew.In16_Cu)
        if n_layers >= 20:
            lset.append(pcbnew.In17_Cu)
            lset.append(pcbnew.In18_Cu)   
        lset.append(pcbnew.B_Cu)
        return lset

    def generate(self):
        self.set_status("Running")
        try:
            self.center_via_warning_count = 0
            self.get_parameters()
            validation_errors = self.validate_parameters()
            if validation_errors:
                raise ValueError("\n".join(validation_errors))

            radial_available = self.r_coil_out - self.r_coil_in
            radial_required = self.n_loops * self.dr + self.trk_w
            inner_half_width = self.r_coil_in * math.sin(math.pi / self.n_slots)
            angular_required = self.n_loops * self.dr + (self.trk_w / 2)

            error_msg = ""
            if radial_required > radial_available:
                error_msg += (f"- Nicht genug radialer Platz!\n"
                            f"  Verfügbar: {radial_available/self.SCALE:.2f} mm\n"
                            f"  Benötigt: {radial_required/self.SCALE:.2f} mm\n\n")
            
            if angular_required >= inner_half_width:
                max_loops_estimated = int((inner_half_width - (self.trk_w / 2)) / self.dr)
                if max_loops_estimated < 0:
                    max_loops_estimated = 0
                error_msg += (f"- Nicht genug Platz im Zentrum (Kollision)!\n"
                            f"  Bei {self.n_slots} Slots und einem Innenradius von {self.r_coil_in/self.SCALE:.2f} mm "
                            f"sind maximal ca. {max_loops_estimated} Loops möglich.\n")

            if error_msg:
                wx.MessageBox(
                    f"Generierung abgebrochen (Geometriefehler):\n\n{error_msg}",
                    "Geometrie Konflikt (KMotor_Pro)",
                    wx.OK | wx.ICON_ERROR
                )
                self.set_status("Failed")
                return

            self.th0 = 2 * math.pi / self.n_slots

            coils = self.do_coils(
                self.r_coil_in,
                self.r_coil_out,
                self.n_slots,
                self.n_loops,
                self.lset,
                self.strategy)

            lowest_used_radius = self.do_professional_routing(coils, self.support_via_mode)

            if self.outline != "None":
                self.do_outline(
                    self.r_in,
                    self.r_out,
                    self.n_edges,
                    self.o_fill)
                
                self.do_mounting_holes(
                    self.r_mh_out,
                    self.n_mh_out,
                    self.r_mh_in,
                    self.n_mh_in,
                    self.n_edges,
                    hs=self.mhs)
                
                cri_thermal_auto = lowest_used_radius - self.trk_space - self.d_via/2.0
                cri_thermal = cri_thermal_auto
                cri_requested = cri_thermal
                if self.inner_fill_dia > 0:
                    cri_thermal = int(self.inner_fill_dia / 2.0)
                    cri_requested = cri_thermal
                safe_inner_r = self.estimate_safe_inner_fill_radius("coil")
                if safe_inner_r is not None:
                    cri_thermal = min(cri_thermal, safe_inner_r)
                if self.inner_fill_dia > 0 and cri_thermal < cri_requested:
                    self.set_status(
                        f"Running: Inner GND dia clipped to {2.0*cri_thermal/self.SCALE:.2f} mm (safety)"
                    )
                self.do_thermal_zones(
                    self.r_out,
                    cri_thermal,
                    fill_inner_area_gnd=self.fill_inner_gnd,
                    fill_outer_area_gnd=self.fill_outer_gnd)
            
            if hasattr(self.board, 'BuildConnectivity'):
                self.board.BuildConnectivity()
                
            pcbnew.Refresh()
            try:
                pcbnew.UpdateUserInterface()
            except AttributeError:
                pass

            temp = self.m_ambT.GetValue()
            stats = self.calculate_stats_breakdown(self.board, net_name="coil", temp=temp)
            self.last_stats = stats
            self.tl = stats["phase_len_mm"]
            self.tr = stats["phase_r_temp"]

            self.lbl_phaseLength.SetLabel('%.2f' % self.tl)
            if hasattr(self, "lbl_turnsPerLayer"):
                self.lbl_turnsPerLayer.SetLabel('%.2f' % stats["turns_per_layer_est"])
            if hasattr(self, "lbl_copperLength"):
                self.lbl_copperLength.SetLabel('%.3f' % stats["copper_length_total_m"])
            self.lbl_phaseR.SetLabel('%.3f' % self.tr)
            self.lbl_totalR.SetLabel('%.3f' % stats["total_resistance"])
            self.lbl_coilR.SetLabel('%.3f' % stats["coil_resistance_per_coil"])
            self.lbl_ringR.SetLabel('%.3f' % stats["ring_resistance_total"])
            motor_consts = self.estimate_motor_constants(stats)
            perf_stats = self.estimate_performance_stats(stats, motor_consts)
            if hasattr(self, "lbl_ke"):
                self.lbl_ke.SetLabel('%.4f' % motor_consts["ke_est"])
            if hasattr(self, "lbl_kt"):
                self.lbl_kt.SetLabel('%.4f' % motor_consts["kt_est"])
            if hasattr(self, "lbl_kv"):
                self.lbl_kv.SetLabel('%.1f' % motor_consts["kv_est"])
            if hasattr(self, "lbl_kw"):
                self.lbl_kw.SetLabel('%.3f' % perf_stats["winding_factor_est"])
            if hasattr(self, "lbl_rpm12"):
                self.lbl_rpm12.SetLabel('%.0f' % perf_stats["rpm_12v_est"])
            if hasattr(self, "lbl_stallCurrent"):
                self.lbl_stallCurrent.SetLabel('%.2f' % perf_stats["stall_current_est"])
            if hasattr(self, "lbl_stallTorque"):
                self.lbl_stallTorque.SetLabel('%.4f' % perf_stats["stall_torque_est"])

            self.do_silkscreen(self.r_coil_out + self.trk_w, self.r_coil_in, self.th0)
            if hasattr(self.board, 'BuildConnectivity'):
                self.board.BuildConnectivity()
            pcbnew.Refresh()
            try:
                pcbnew.UpdateUserInterface()
            except AttributeError:
                pass

            self.btn_clear.Enable(True)
            skipped = int(getattr(self, "support_hole_collision_count", 0))
            via_skipped = int(getattr(self, "center_via_warning_count", 0))
            warnings = []
            if skipped > 0:
                warnings.append(f"support holes skipped: {skipped}")
            if via_skipped > 0:
                warnings.append(f"center vias skipped: {via_skipped}")
            warnings.extend(self.estimate_model_warnings(stats, motor_consts, perf_stats))
            self.set_status("Finished" if not warnings else f"Finished ({', '.join(warnings)})")
            if hasattr(self, "m_txtStatus") and self.m_txtStatus:
                self.m_txtStatus.SetValue(
                    "Finished\n"
                    "Model: estimated, geometry + B gap assumption based\n"
                    f"Length total: {stats['total_length_mm']:.2f} mm\n"
                    f"Copper total: {stats['copper_length_total_m']:.3f} m\n"
                    f"Length / phase: {stats['phase_len_mm']:.2f} mm\n"
                    f"Length / coil: {stats['coil_length_per_coil_mm']:.2f} mm\n"
                    f"Turns / layer est: {stats['turns_per_layer_est']:.2f}\n"
                    f"Length rings total: {stats['ring_length_mm']:.2f} mm\n"
                    f"R total: {stats['total_resistance']:.4f} ohm\n"
                    f"R / phase: {stats['phase_r_temp']:.4f} ohm\n"
                    f"R / coil: {stats['coil_resistance_per_coil']:.4f} ohm\n"
                    f"R rings total: {stats['ring_resistance_total']:.4f} ohm\n"
                    f"kw est: {perf_stats['winding_factor_est']:.3f}\n"
                    f"No-load RPM @ 12V est: {perf_stats['rpm_12v_est']:.0f}\n"
                    f"Stall current est: {perf_stats['stall_current_est']:.2f} A\n"
                    f"Stall torque est: {perf_stats['stall_torque_est']:.4f} Nm"
                    + (f"\nWarnings: {', '.join(warnings)}" if warnings else "")
                )
        except Exception as e:
            self.set_status("Failed")
            wx.MessageBox(
                f"Generierung fehlgeschlagen:\n{e}",
                "KMotor_Pro Fehler",
                wx.OK | wx.ICON_ERROR
            )
            print(traceback.format_exc())

    def coil_tracker(self, mpt, layer, n_loops, group, is_first_layer=False, is_last_layer=False, is_ccw=False):
        """
        Zeichnet die Spule und liefert die zwei expliziten Ecke-Anker.
        Auf den Terminal-Layern wird der innere Stummel gezielt entfernt.
        """
        def mpt_point(idx):
            x, y = self._point_xy(mpt[idx])
            return self.fpoint(int(x), int(y))

        ip = 0
        t0 = None
        nseg = n_loops * 4 - 1

        actual_start = None
        actual_end = None
        skipped_inner_bridge = False

        for seg in range(nseg):
            ps = mpt_point(ip)

            is_arc = (not seg % 2)
            if is_arc:
                ip += 1
                mid_pt = mpt_point(ip)
                side = -1 if not seg % 4 else 1

            ip += 1
            pe = mpt_point(ip)

            d_s = math.hypot(ps.x, ps.y)
            d_e = math.hypot(pe.x, pe.y)
            # Remove only the inner bridge on terminal layers.
            # This is geometric, so it won't drop an outer coil segment by index mismatch.
            if (is_first_layer or is_last_layer):
                if (not skipped_inner_bridge) and abs(d_s - self.r_coil_in) < self.SCALE * 0.5 and abs(d_e - self.r_coil_in) < self.SCALE * 0.5:
                    # Break fillet chain when the inner bridge is intentionally removed.
                    # Otherwise the next segment is filleted against a non-adjacent segment
                    # and we lose one visible coil segment.
                    t0 = None
                    skipped_inner_bridge = True
                    continue

            if actual_start is None:
                actual_start = ps
            actual_end = pe

            if is_arc:
                t = pcbnew.PCB_ARC(self.board)
                t.SetMid(mid_pt)
            else:
                t = pcbnew.PCB_TRACK(self.board)

            t.SetWidth(self.trk_w)
            t.SetLayer(layer)
            t.SetStart(ps)
            t.SetEnd(pe)
            self.board.Add(t)

            net_coil = self.board.FindNet("coil")
            if net_coil:
                t.SetNet(net_coil)

            if t0 is not None and self.r_fill > 0:
                self.fillet(self.board, t0, t, self.r_fill, side)

            group.AddItem(t)
            t0 = t

        if actual_start is None:
            actual_start = mpt_point(0)
        if actual_end is None:
            actual_end = actual_start

        return [actual_start, actual_end]

    def do_coils(self, ri, ro, n_slots, n_loops=1, lset=None, mode=0):
        th0 = 2*math.pi/n_slots
        if mode == 0:
            pcu0, pcu0m, pcu0mi = ksolve.parallel( ri, ro, self.dr, th0, n_loops, 0 )
            pcu1, pcu1m, pcu1mi = ksolve.parallel( ri, ro, self.dr, th0, n_loops, 1 )
        else:
            pcu0 = ksolve.radial( ri, ro, self.dr, th0, n_loops, 0 )
            pcu1 = ksolve.radial( ri, ro, self.dr, th0, n_loops, 1 )
        pcu0 = np.asarray(pcu0, dtype=float)
        pcu1 = np.asarray(pcu1, dtype=float)
        
        coil_p =[]
        for i in range(self.phases):
            coil_p.append([])
        coil_slot = [None] * n_slots
        
        net_coil = self.board.FindNet("coil")

        for p in range(n_slots):
            pgroup = pcbnew.PCB_GROUP( self.board )
            pgroup.SetName("pole_"+str(p))
            self.board.Add(pgroup)

            th = th0 * p 
            R = np.array([[math.cos(th), -math.sin(th)],[math.sin(th), math.cos(th)]])
            Tcw = np.matmul(pcu0, R.transpose())
            Tccw = np.matmul(pcu1, R.transpose())
            slot_anchors = self.build_slot_anchors(Tcw, Tccw, th)
            slot_center_via = self.build_slot_center_via(Tcw, Tccw, th, th0)

            for idx, layer in enumerate(lset):
                is_first = (idx == 0)
                is_last = (idx == len(lset) - 1)
                is_ccw = (idx % 2 != 0)

                if is_ccw:
                    ct = self.coil_tracker(Tccw, layer, n_loops, pgroup, is_first, is_last, is_ccw)
                    via_pos = slot_center_via if len(lset) == 2 else ct[1]
                    if via_pos is not None:
                        via = pcbnew.PCB_VIA(self.board)
                        if len(lset)==2:
                            via.SetViaType(pcbnew.VIATYPE_THROUGH)
                        else:
                            via.SetViaType(pcbnew.VIATYPE_BLIND_BURIED)
                        via.SetLayerPair( lset[idx-1], lset[idx] )
                        via.SetPosition(via_pos)
                        via.SetDrill( self.d_drill )
                        via.SetWidth( self.d_via )
                        if net_coil: via.SetNet(net_coil)
                        self.board.Add(via)
                    else:
                        self.center_via_warning_count += 1
                else:
                    ct = self.coil_tracker(Tcw, layer, n_loops, pgroup, is_first, is_last, is_ccw)
                    if len(lset)>2 and idx:
                        via = pcbnew.PCB_VIA(self.board)
                        via.SetViaType(pcbnew.VIATYPE_BLIND_BURIED)
                        via.SetLayerPair( lset[idx-1], lset[idx] )
                        via.SetPosition( ct[0] )
                        via.SetDrill( self.d_drill )
                        via.SetWidth( self.d_via )
                        if net_coil: via.SetNet(net_coil)
                        self.board.Add(via)

            pins = [slot_anchors[0], slot_anchors[1]]
            coil_p[p % self.phases].append(pins)
            coil_slot[p] = pins

        self.coil_slot_pins = coil_slot

        return coil_p

    def _angle_diff(self, a, b):
        d = a - b
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        return d

    def build_slot_anchors(self, tcw, tccw, th_center):
        # Deterministically pick the two inner coil corners (left/right of slot centerline).
        raw_pts = {}
        def to_xy(pt):
            try:
                return int(pt[0,0]), int(pt[0,1])
            except Exception:
                flat = np.asarray(pt).reshape(-1)
                if flat.size < 2:
                    return None
                return int(flat[0]), int(flat[1])

        for arr in (tcw, tccw):
            for p in arr:
                xy = to_xy(p)
                if xy is None:
                    continue
                x, y = xy
                raw_pts[(x, y)] = True

        pts = list(raw_pts.keys())
        if not pts:
            z = self.fpoint(0, 0)
            return [z, z]

        radii = [math.hypot(x, y) for (x, y) in pts]
        r_min = min(radii)
        tol = max(self.dr * 0.75, self.trk_w * 1.5, self.SCALE * 0.3)
        tol_inner = max(self.dr * 1.25, self.trk_w * 2.0, self.SCALE * 0.5)

        inner = []
        for (x, y) in pts:
            r = math.hypot(x, y)
            # Primary target: real coil inner radius (corner region), not geometric r_min,
            # because r_min may hit the center bridge and cause mid-taps.
            if abs(r - self.r_coil_in) <= tol_inner:
                dth = self._angle_diff(math.atan2(y, x), th_center)
                inner.append((x, y, dth))

        # Fallback to r_min-based selection only if no/too few candidates were found.
        if len(inner) < 2:
            inner = []
            for (x, y) in pts:
                r = math.hypot(x, y)
                if abs(r - r_min) <= tol:
                    dth = self._angle_diff(math.atan2(y, x), th_center)
                    inner.append((x, y, dth))

        if len(inner) < 2:
            ranked = []
            for (x, y) in pts:
                r = math.hypot(x, y)
                dth = self._angle_diff(math.atan2(y, x), th_center)
                ranked.append((abs(r - r_min), x, y, dth))
            ranked.sort(key=lambda t: t[0])
            inner = [(t[1], t[2], t[3]) for t in ranked[:2]]

        neg = [p for p in inner if p[2] < 0]
        pos = [p for p in inner if p[2] >= 0]

        if neg and pos:
            left = min(neg, key=lambda p: p[2])   # most negative angle wrt slot centerline
            right = max(pos, key=lambda p: p[2])  # most positive angle wrt slot centerline
        else:
            ordered = sorted(inner, key=lambda p: p[2])
            left = ordered[0]
            right = ordered[-1]

        return [self.fpoint(left[0], left[1]), self.fpoint(right[0], right[1])]

    def build_slot_center_via(self, arr_a, arr_b, th_center, th_slot):
        # Pick a deterministic centerline point for the inter-layer via and verify
        # that it can actually bridge both coil halves.
        cand = []
        for arr in (arr_a, arr_b):
            for p in arr:
                x, y = self._point_xy(p)
                r = math.hypot(x, y)
                d = abs(self._angle_diff(math.atan2(y, x), th_center))
                cand.append((d, r))

        if not cand:
            return None

        d_max = max(th_slot * 0.06, 0.008)
        r_min = max(float(self.r_coil_in) - self.dr, 0.0)
        r_max = float(self.r_coil_out) + self.dr
        close = [c for c in cand if c[0] <= d_max and r_min <= c[1] <= r_max]
        if not close:
            close = [c for c in cand if r_min <= c[1] <= r_max]
        if not close:
            return None

        r_values = [c[1] for c in close]
        r_low = min(r_values)
        r_high = max(r_values)
        r_target = r_low + 0.62 * (r_high - r_low)
        best_radius = min(close, key=lambda c: (abs(c[1] - r_target), c[0]))[1]

        threshold = max(self.trk_w * 0.85, self.dr * 0.65, self.SCALE * 0.15)
        best = None
        for radius in sorted({best_radius} | {c[1] for c in close}, key=lambda r: abs(r - r_target)):
            dist_a = self._nearest_point_distance(radius, th_center, arr_a)
            dist_b = self._nearest_point_distance(radius, th_center, arr_b)
            worst = max(dist_a if dist_a is not None else 1e9, dist_b if dist_b is not None else 1e9)
            if worst <= threshold:
                best = radius
                break

        if best is None:
            return None
        return self._as_point(best * math.cos(th_center), best * math.sin(th_center))

    def add_through_via(self, position, net=None):
        return self.add_custom_through_via(position, net=net, drill=self.d_drill, width=self.d_via)

    def add_custom_through_via(self, position, net=None, drill=None, width=None):
        via = pcbnew.PCB_VIA(self.board)
        via.SetViaType(pcbnew.VIATYPE_THROUGH)
        via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        via.SetPosition(position)
        via.SetDrill(self.d_drill if drill is None else drill)
        via.SetWidth(self.d_via if width is None else width)
        if net is not None:
            via.SetNet(net)
        self.board.Add(via)
        return via

    def add_support_hole(self, position):
        pad_margin = int(0.25 * self.SCALE)
        hole_width = max(self.d_support_hole + pad_margin, self.d_support_hole + 1)
        return self.add_custom_through_via(position, net=None, drill=self.d_support_hole, width=hole_width)

    def get_support_hole_width(self):
        pad_margin = int(0.25 * self.SCALE)
        return max(self.d_support_hole + pad_margin, self.d_support_hole + 1)

    def get_selected_terminal_od_iu(self):
        # Estimate terminal outer diameter from selected THT footprint name "..._ODx.xmm".
        # Used to keep clustered terminals from overlapping.
        if self.trmtype != "THT":
            return int(4.0 * self.SCALE)
        try:
            fp = self.term_db.get("THT", {}).get(self.m_termSize.GetStringSelection(), "")
            if "_OD" in fp and "mm" in fp:
                token = fp.split("_OD", 1)[1].split("mm", 1)[0]
                return int(float(token) * self.SCALE)
        except Exception:
            pass
        return int(4.0 * self.SCALE)

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

    def hole_collides(self, position, placed_points, min_distance):
        for pt in placed_points:
            if math.hypot(pt.x - position.x, pt.y - position.y) < min_distance:
                return True
        return False

    # =========================================================================
    # PROFESSIONELLES ROUTING: 4 Anchor-Pins, Radial-Lines, Keine Kreuzungen
    # =========================================================================
    def do_professional_routing(self, coils, support_via_mode=2):
        net_coil = self.board.FindNet("coil")
        phases = self.phases
        th0 = 2 * math.pi / self.n_slots
        n_rc = int(self.n_slots / phases) - 1
        if support_via_mode not in (0, 2, 4):
            support_via_mode = 2
        support_collisions = 0
        support_pts = []
        support_hole_width = self.get_support_hole_width()
        support_min_dist = max(support_hole_width + self.trk_space, support_hole_width)

        def add_ring_path(layer, radius, th_start, th_end, p_start, p_end, width):
            """Draw robust ring connection as segmented path (avoids arc edge-case disconnects)."""
            d_th = th_end - th_start
            if d_th > math.pi:
                d_th -= 2 * math.pi
            elif d_th < -math.pi:
                d_th += 2 * math.pi

            # Very small angle: direct short track.
            if abs(d_th) < 1e-4:
                t = pcbnew.PCB_TRACK(self.board)
                t.SetLayer(layer)
                t.SetWidth(width)
                if net_coil:
                    t.SetNet(net_coil)
                t.SetStart(p_start)
                t.SetEnd(p_end)
                self.board.Add(t)
                return

            # 10 degree max step keeps geometry smooth and electrically contiguous.
            step = math.pi / 18.0
            nseg = max(2, int(abs(d_th) / step) + 1)
            prev = p_start
            for k in range(1, nseg + 1):
                if k == nseg:
                    nxt = p_end
                else:
                    th_k = th_start + d_th * (k / float(nseg))
                    nxt = self.fpoint(int(radius * math.cos(th_k)), int(radius * math.sin(th_k)))
                t = pcbnew.PCB_TRACK(self.board)
                t.SetLayer(layer)
                t.SetWidth(width)
                if net_coil:
                    t.SetNet(net_coil)
                t.SetStart(prev)
                t.SetEnd(nxt)
                self.board.Add(t)
                prev = nxt

        # 1. PLATZIERUNG DER ISOLIERTEN STÜTZ-THT-LÖCHER AUSSERHALB DER SPULEN
        # support_via_mode:
        # 0 = keine Stützlöcher
        # 2 = zwei äußere Stützlöcher je Slot
        # 4 = vier äußere Stützlöcher je Slot
        r_out_support = self.r_coil_out + self.trk_space + self.trk_w + (support_hole_width / 2.0)
        th_out_off_a = (th0 / 2.0) * 0.78
        th_out_off_b = (th0 / 2.0) * 0.48
        
        if support_via_mode >= 2:
            for slot in range(self.n_slots):
                th_c = slot * th0
                support_pts_slot = [
                    self.fpoint(int(r_out_support * math.cos(th_c - th_out_off_a)), int(r_out_support * math.sin(th_c - th_out_off_a))),
                    self.fpoint(int(r_out_support * math.cos(th_c + th_out_off_a)), int(r_out_support * math.sin(th_c + th_out_off_a))),
                ]

                for pt in support_pts_slot:
                    if self.hole_collides(pt, support_pts, support_min_dist):
                        support_collisions += 1
                        continue
                    self.add_support_hole(pt)
                    support_pts.append(pt)

        # 2. BERECHNUNG DES SICHEREN ABSTANDS FÜR DIE SAMMELSCHIENEN (inkl. Via)
        if support_via_mode == 0:
            first_ring_offset = 0
        elif support_via_mode == 2:
            first_ring_offset = int(0.5 * max(self.d_via, support_hole_width))
        else:
            first_ring_offset = max(self.d_via, support_hole_width)
        # Give extra clearance to support TH holes near the first ring.
        if support_via_mode in (2, 4):
            first_ring_offset += int(0.5 * support_hole_width)
        current_radius = self.r_coil_in - (self.d_via / 2.0) - self.ring_space - (self.ring_w / 2.0) - first_ring_offset
        lowest_used_radius = current_radius

        # Mode 4: zusätzlich 2 innere unverbundene Stützlöcher je Slot (nahe Ringanschlüssen).
        if support_via_mode == 4:
            # Anchor inner support holes to coil geometry (not current ring radius),
            # so increasing first-ring inset really increases ring-to-support clearance.
            r_in_support = self.r_coil_in - (self.d_via / 2.0) - self.trk_space - (support_hole_width / 2.0)
            th_in_off = (th0 / 2.0) * 0.45
            for slot in range(self.n_slots):
                th_c = slot * th0
                support_pts_slot = [
                    self.fpoint(int(r_in_support * math.cos(th_c - th_in_off)), int(r_in_support * math.sin(th_c - th_in_off))),
                    self.fpoint(int(r_in_support * math.cos(th_c + th_in_off)), int(r_in_support * math.sin(th_c + th_in_off))),
                ]
                for pt in support_pts_slot:
                    if self.hole_collides(pt, support_pts, support_min_dist):
                        support_collisions += 1
                        continue
                    self.add_support_hole(pt)
                    support_pts.append(pt)

        n_phase_coils = int(self.n_slots / phases)
        ring_levels_total = min(n_rc, 5 if phases >= 3 else 4)
        ring_levels_total = max(1, ring_levels_total)
        for p in range(phases):
            for i in range(n_rc):
                # Zyklische Ebenen je Verbindung:
                # - begrenzt die Anzahl Ringebenen (typisch 4/5 statt z.B. 9)
                # - sorgt dafür, dass in/out-Stubs einer Coil unterschiedlich lang sind
                level = ((i * phases) + p) % ring_levels_total
                cri = current_radius - (level * self.ring_dr)
                if cri < lowest_used_radius:
                    lowest_used_radius = cri

                slot_a = p + i * phases
                slot_b = p + (i + 1) * phases
                if hasattr(self, "coil_slot_pins") and self.coil_slot_pins[slot_a] and self.coil_slot_pins[slot_b]:
                    c1e = self.coil_slot_pins[slot_a][1]
                    c2s = self.coil_slot_pins[slot_b][0]
                else:
                    c1e = coils[p][i][1]
                    c2s = coils[p][i+1][0]

                # Löt-Via in die inneren Spulenecken setzen (Netz-Verbindung vorhanden)
                self.add_through_via(c1e, net_coil)
                self.add_through_via(c2s, net_coil)

                # 1P mode: direct via-to-via links, no inner ring buses.
                if phases == 1:
                    t = pcbnew.PCB_TRACK(self.board)
                    t.SetLayer(pcbnew.B_Cu)
                    t.SetWidth(self.trk_w)
                    if net_coil: t.SetNet(net_coil)
                    t.SetStart(c1e)
                    t.SetEnd(c2s)
                    self.board.Add(t)
                    continue

                # Schnurgerade radiale Zuleitung auf der UNTERSEITE (B_Cu) zum Sammelring ziehen
                th1 = math.atan2(c1e.y, c1e.x)
                via1_pt = self.fpoint(int(cri * math.cos(th1)), int(cri * math.sin(th1)))
                t1 = pcbnew.PCB_TRACK(self.board)
                t1.SetLayer(pcbnew.B_Cu)
                t1.SetWidth(self.trk_w)
                if net_coil: t1.SetNet(net_coil)
                t1.SetStart(c1e)
                t1.SetEnd(via1_pt)
                self.board.Add(t1)

                th2 = math.atan2(c2s.y, c2s.x)
                via2_pt = self.fpoint(int(cri * math.cos(th2)), int(cri * math.sin(th2)))
                t2 = pcbnew.PCB_TRACK(self.board)
                t2.SetLayer(pcbnew.B_Cu) # Unterquert alle Leitungen der anderen Phasen!
                t2.SetWidth(self.trk_w)
                if net_coil: t2.SetNet(net_coil)
                t2.SetStart(c2s)
                t2.SetEnd(via2_pt)
                self.board.Add(t2)

                arc_layer = pcbnew.B_Cu
                if support_via_mode in (2, 4):
                    self.add_through_via(via1_pt, net_coil)
                    self.add_through_via(via2_pt, net_coil)
                    arc_layer = pcbnew.F_Cu

                # 3. Ring connection robustly as segmented path (no arc discontinuity).
                add_ring_path(arc_layer, cri, th1, th2, via1_pt, via2_pt, self.ring_w)

        # 4. STERNSCHALTUNG (nur für 3-Phasen Motoren)
        neutral_tap = None
        if phases > 1:
            star_radius = lowest_used_radius - self.ring_dr
            lowest_used_radius = star_radius
            star_pts =[]
            
            for p in range(phases):
                last_slot = p + (n_phase_coils - 1) * phases
                if hasattr(self, "coil_slot_pins") and self.coil_slot_pins[last_slot]:
                    c_end = self.coil_slot_pins[last_slot][1]
                else:
                    c_end = coils[p][-1][1]
                
                # Eck-Via für die allerletzte Spule setzen
                self.add_through_via(c_end, net_coil)
                
                th = math.atan2(c_end.y, c_end.x)
                via_pt = self.fpoint(int(star_radius * math.cos(th)), int(star_radius * math.sin(th)))
                star_pts.append((th, via_pt))
                
                # B_Cu Leitung radial nach unten zum Sternpunkt
                t = pcbnew.PCB_TRACK(self.board)
                t.SetLayer(pcbnew.B_Cu)
                t.SetWidth(self.trk_w)
                if net_coil: t.SetNet(net_coil)
                t.SetStart(c_end)
                t.SetEnd(via_pt)
                self.board.Add(t)
                
                self.add_through_via(via_pt, net_coil)

            star_pts.sort(key=lambda x: x[0])
            if star_pts:
                neutral_tap = star_pts[0][1]
            for i in range(len(star_pts) - 1):
                th1, pt1 = star_pts[i]
                th2, pt2 = star_pts[i+1]
                
                add_ring_path(pcbnew.F_Cu, star_radius, th1, th2, pt1, pt2, self.ring_w)

            # 3P+N: create a dedicated neutral hub so N is not tied to a phase star point.
            if self.n_term > phases and len(star_pts) >= 3:
                ux = 0.0
                uy = 0.0
                for pidx in range(phases):
                    first_slot = pidx
                    if hasattr(self, "coil_slot_pins") and self.coil_slot_pins[first_slot]:
                        c0 = self.coil_slot_pins[first_slot][0]
                        ang = math.atan2(c0.y, c0.x)
                    else:
                        ang = star_pts[pidx][0]
                    ux += math.cos(ang)
                    uy += math.sin(ang)
                th_n = math.atan2(uy, ux) if (ux != 0 or uy != 0) else star_pts[0][0]
                neutral_radius = star_radius - self.ring_dr
                if neutral_radius <= 0:
                    neutral_radius = max(star_radius * 0.85, self.d_via * 2.0)
                neutral_tap = self.fpoint(
                    int(neutral_radius * math.cos(th_n)),
                    int(neutral_radius * math.sin(th_n))
                )
                self.add_through_via(neutral_tap, net_coil)
                for _, pt in star_pts:
                    tn = pcbnew.PCB_TRACK(self.board)
                    tn.SetLayer(pcbnew.B_Cu)
                    tn.SetWidth(self.trk_w)
                    if net_coil: tn.SetNet(net_coil)
                    tn.SetStart(pt)
                    tn.SetEnd(neutral_tap)
                    self.board.Add(tn)
                if neutral_radius < lowest_used_radius:
                    lowest_used_radius = neutral_radius

        # 5. FINALE TERMINAL-ANSCHLÜSSE (Zur Platine oder Kabel)
        term_radius = lowest_used_radius - self.term_offset
        n_phase_coils = int(self.n_slots / phases) if phases > 0 else 0

        def get_slot_start(slot, phase_idx):
            if hasattr(self, "coil_slot_pins") and self.coil_slot_pins and self.coil_slot_pins[slot]:
                return self.coil_slot_pins[slot][0]
            return coils[phase_idx][0][0]

        def segs_intersect(a, b, c, d):
            def orient(p, q, r):
                return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
            o1 = orient(a, b, c)
            o2 = orient(a, b, d)
            o3 = orient(c, d, a)
            o4 = orient(c, d, b)
            return (o1 * o2 < 0) and (o3 * o4 < 0)

        terminal_starts = []
        terminal_angles = []
        terminal_side_shift = []
        cluster_base = None
        if phases == 1:
            c0 = self.coil_slot_pins[0][0] if hasattr(self, "coil_slot_pins") and self.coil_slot_pins[0] else coils[0][0][0]
            last_slot_1p = self.n_slots - 1
            c1 = self.coil_slot_pins[last_slot_1p][1] if hasattr(self, "coil_slot_pins") and self.coil_slot_pins[last_slot_1p] else coils[0][-1][1]
            a0 = math.atan2(c0.y, c0.x)
            a1 = math.atan2(c1.y, c1.x)
            ux = math.cos(a0) + math.cos(a1)
            uy = math.sin(a0) + math.sin(a1)
            base = math.atan2(uy, ux) if (ux != 0 or uy != 0) else a0
            # Compact 1P terminals on one side with a small tangential spread.
            tangential_gap = max((self.d_via + self.trk_space) * 1.6, self.SCALE * 1.2)
            spread = tangential_gap / max(float(term_radius), 1.0)
            # Enforce minimum terminal separation so footprints don't overlap.
            min_sep_mm = 7.0 if self.trmtype == "THT" else 4.0
            min_sep_iu = min_sep_mm * self.SCALE
            ratio = min(0.95, min_sep_iu / max(2.0 * float(term_radius), 1.0))
            spread_req = math.asin(ratio)
            spread = max(spread, spread_req)
            spread = min(0.40, max(0.08, spread))

            cand_angles = [base - spread, base + spread]
            # Assign starts to angles to minimize crossings (choose better of 2 permutations).
            cost_01 = abs(self._angle_diff(a0, cand_angles[0])) + abs(self._angle_diff(a1, cand_angles[1]))
            cost_10 = abs(self._angle_diff(a0, cand_angles[1])) + abs(self._angle_diff(a1, cand_angles[0]))
            if cost_01 <= cost_10:
                terminal_starts = [c0, c1]
                terminal_angles = [cand_angles[0], cand_angles[1]]
            else:
                terminal_starts = [c0, c1]
                terminal_angles = [cand_angles[1], cand_angles[0]]
        elif phases == 3 and self.n_term == 3:
            # Keep 3P trunk connections radial from each phase start (no crossing with rings).
            # Only offset outer terminal footprints sideways by short side stubs.
            phase_starts = [get_slot_start(0, 0), get_slot_start(1, 1), get_slot_start(2, 2)]
            base_th = math.atan2(phase_starts[1].y, phase_starts[1].x)
            term_od = self.get_selected_terminal_od_iu()
            side_shift_iu = max(int(0.45 * term_od), int(0.8 * self.SCALE))
            for i, c in enumerate(phase_starts):
                th_i = math.atan2(c.y, c.x)
                terminal_starts.append(c)
                terminal_angles.append(th_i)
                if i == 1:
                    terminal_side_shift.append(0)
                else:
                    # Push outer pins away from the center pin along tangent.
                    dth = self._angle_diff(th_i, base_th)
                    sgn = 1 if dth >= 0 else -1
                    terminal_side_shift.append(sgn * side_shift_iu)
        else:
            # User preference: 3P terminals grouped in one local cluster (not 120deg separated).
            phase_starts = []
            for pidx in range(phases):
                phase_slot = pidx if n_phase_coils > 0 else pidx
                c = get_slot_start(phase_slot, pidx)
                phase_starts.append(c)

            base = math.atan2(phase_starts[0].y, phase_starts[0].x) if phase_starts else 0.0
            min_sep_mm = 7.0 if self.trmtype == "THT" else 4.0
            min_sep_iu = min_sep_mm * self.SCALE
            ratio = min(0.95, min_sep_iu / max(float(term_radius), 1.0))
            spread = math.asin(ratio)
            spread = min(0.35, max(0.05, spread))

            # symmetric cluster around base angle
            if phases == 3:
                phase_offsets = [-spread, 0.0, spread]
            elif phases == 2:
                phase_offsets = [-0.5 * spread, 0.5 * spread]
            else:
                phase_offsets = [((i - (phases - 1) / 2.0) * spread) for i in range(phases)]
            cand_angles = [base + off for off in phase_offsets]

            # Choose start->angle mapping that avoids crossings and minimizes route effort.
            best_perm = list(range(phases))
            best_cost = None
            for perm in itertools.permutations(range(phases)):
                # base cost: angular mismatch + radial segment length
                cost = 0.0
                segs = []
                for i in range(phases):
                    s = phase_starts[i]
                    th_i = cand_angles[perm[i]]
                    tpt = (term_radius * math.cos(th_i), term_radius * math.sin(th_i))
                    spt = (float(s.x), float(s.y))
                    cost += abs(self._angle_diff(math.atan2(s.y, s.x), th_i))
                    cost += math.hypot(tpt[0] - spt[0], tpt[1] - spt[1]) / max(float(self.SCALE), 1.0)
                    segs.append((spt, tpt))
                # heavy penalty for crossing segments
                crossing = 0
                for i in range(phases):
                    for j in range(i + 1, phases):
                        if segs_intersect(segs[i][0], segs[i][1], segs[j][0], segs[j][1]):
                            crossing += 1
                cost += 10000.0 * crossing
                if best_cost is None or cost < best_cost:
                    best_cost = cost
                    best_perm = perm

            for i, c in enumerate(phase_starts):
                terminal_starts.append(c)
                terminal_angles.append(cand_angles[best_perm[i]])
                terminal_side_shift.append(0)

            if self.n_term > phases:
                c_n = neutral_tap if neutral_tap is not None else coils[0][-1][1]
                terminal_starts.append(c_n)
                terminal_angles.append(base + (phase_offsets[-1] + spread))
                terminal_side_shift.append(0)

        if len(terminal_side_shift) < len(terminal_angles):
            terminal_side_shift.extend([0] * (len(terminal_angles) - len(terminal_side_shift)))

        for p in range(self.n_term):
            if p < len(terminal_starts):
                c_start = terminal_starts[p]
                th = terminal_angles[p]
            else:
                c_start = neutral_tap if neutral_tap is not None else coils[0][-1][1]
                th = math.atan2(c_start.y, c_start.x)

            # Via an die Anschlussecke
            self.add_through_via(c_start, net_coil)
            t_pt = self.fpoint(int(term_radius * math.cos(th)), int(term_radius * math.sin(th)))
            
            t = pcbnew.PCB_TRACK(self.board)
            t.SetLayer(pcbnew.B_Cu)
            t.SetWidth(self.trk_w)
            if net_coil: t.SetNet(net_coil)
            t.SetStart(c_start)
            t.SetEnd(t_pt)
            self.board.Add(t)

            if self.trmtype != "None":
                lib = self.fp_path + ('Connector_Wire.pretty' if self.trmtype == 'THT' else 'TestPoint.pretty')
                fp = self.term_db.get(self.trmtype).get(self.m_termSize.GetStringSelection())
                m = pcbnew.FootprintLoad(lib, fp)
                if m is not None:
                    m.Value().SetVisible(False)
                    lib_name = lib.split('.')[-2].split('/')[-1]
                    m.SetFPIDAsString(lib_name + ":" + fp)
                    fp_pos = t_pt
                    if p < len(terminal_side_shift):
                        shift = terminal_side_shift[p]
                        if shift != 0:
                            tx = -math.sin(th)
                            ty = math.cos(th)
                            fp_pos = self.fpoint(
                                int(t_pt.x + shift * tx),
                                int(t_pt.y + shift * ty)
                            )
                            # Keep main run radial and add a short side-stub to the shifted pad center.
                            ts = pcbnew.PCB_TRACK(self.board)
                            ts.SetLayer(pcbnew.B_Cu)
                            ts.SetWidth(self.trk_w)
                            if net_coil: ts.SetNet(net_coil)
                            ts.SetStart(t_pt)
                            ts.SetEnd(fp_pos)
                            self.board.Add(ts)
                    m.SetPosition(fp_pos)
                    m.Rotate(fp_pos, self.eda_angle(-th))
                    for pad in m.Pads():
                        pad.SetNet(net_coil)
                    ref_pos = self._get_terminal_label_position(fp_pos, th)
                    m.Reference().SetPosition(ref_pos)
                    m.SetReference("A" if p == 0 else ("B" if p == 1 else ("C" if p == 2 else "N")))
                    self.board.Add(m)

        self.support_hole_collision_count = support_collisions
        # Return the lowest ring radius (not terminal radius), so inner GND fill
        # starts inside the ring stack and does not swallow terminal area.
        return lowest_used_radius

    def do_outline(self, r_in, r_out, n_edge=0, r_fill=0):
        edge = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_CIRCLE)
        edge.SetCenter( self.fpoint(0,0) )
        edge.SetStart( self.fpoint(0,0) )
        edge.SetEnd( self.fpoint(r_in,0) )
        edge.SetLayer( pcbnew.Edge_Cuts )
        self.board.Add(edge)

        relief_dia = max(min(0.12 * (2.0 * r_in), 2.0 * self.SCALE), 0.8 * self.SCALE) if r_in > 0 else 0
        if relief_dia > 0 and r_in > (1.5 * relief_dia):
            relief_radius = r_in + (0.5 * relief_dia)
            for angle in (math.pi / 4.0, 3.0 * math.pi / 4.0, 5.0 * math.pi / 4.0, 7.0 * math.pi / 4.0):
                relief = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_CIRCLE)
                relief.SetCenter(self.fpoint(int(relief_radius * math.cos(angle)), int(relief_radius * math.sin(angle))))
                relief.SetStart(relief.GetCenter())
                relief.SetEnd(self.fpoint(int(relief.GetCenter().x + relief_dia / 2.0), int(relief.GetCenter().y)))
                relief.SetLayer(pcbnew.Edge_Cuts)
                self.board.Add(relief)

        if n_edge == 0:
            edge = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_CIRCLE)
            edge.SetCenter( self.fpoint(0,0) )
            edge.SetStart( self.fpoint(0,0) )
            edge.SetEnd( self.fpoint(r_out,0) )
            edge.SetLayer( pcbnew.Edge_Cuts )
            self.board.Add(edge)
        elif n_edge >= 4:
            r_out /= math.cos(math.pi/n_edge)
            thp = 2*math.pi/n_edge
            tho = thp/2
            points =[]
            for i in range(n_edge):
                points.append(
                    self.fpoint(
                        int(r_out * math.cos(i*thp+tho)), 
                        int(r_out * math.sin(i*thp+tho)) )
                )
            segs = {}
            for i in range(n_edge):
                seg = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_SEGMENT)
                seg.SetStart( points[i] )
                seg.SetEnd( points[(i+1)%n_edge] )
                seg.SetLayer( pcbnew.Edge_Cuts )
                self.board.Add(seg)
                segs[i] = seg

    def _outline_poly_points(self, r, n_edge):
        if n_edge < 4:
            return None
        rp = r / math.cos(math.pi / n_edge)
        thp = 2 * math.pi / n_edge
        tho = thp / 2
        pts = []
        for i in range(n_edge):
            pts.append(
                self.fpoint(
                    int(rp * math.cos(i * thp + tho)),
                    int(rp * math.sin(i * thp + tho))
                )
            )
        return pts

    def do_mounting_holes(self, r_mh_out=0, n_mh_out=0, r_mh_in=0, n_mh_in=0, n_edge=0, hs="None"):
        if hs != "None":
            fp_lib = self.fp_path + 'MountingHole.pretty'
            fp = self.mhole_db.get(hs)
        else:
            return

        ni_gnd = self.board.FindNet("gnd")

        if n_edge>0:
            r_mh_out /= math.cos(math.pi/n_edge) 

        if n_mh_out > 0:
            th0 = 2*math.pi/n_mh_out
            for i in range(n_mh_out):
                m = pcbnew.FootprintLoad( fp_lib, fp )
                if m is not None:
                    m.Reference().SetVisible(False)
                    m.Value().SetVisible(False)
                    m.SetReference('M'+str(i))
                    m.SetPosition(
                        self.fpoint( 
                            int(r_mh_out * math.cos(th0*i + th0/2)), 
                            int(r_mh_out * math.sin(th0*i + th0/2))))
                    for pad in m.Pads():
                        pad.SetNet(ni_gnd)
                    self.board.Add(m)

        if n_mh_in > 0:
            th0 = 2*math.pi/n_mh_in
            for i in range(n_mh_in):
                m = pcbnew.FootprintLoad( fp_lib, fp )
                if m is not None:
                    m.SetReference('')
                    m.SetPosition(
                    self.fpoint( 
                        int(r_mh_in * math.cos(th0*i + th0/2)), 
                        int(r_mh_in * math.sin(th0*i + th0/2))))
                    for pad in m.Pads():
                        pad.SetNet(ni_gnd)
                    self.board.Add(m)

    def do_thermal_zones(self, r_out, r_nosm_in, r_nosm_out=0, nvias=36, fill_inner_area_gnd=True, fill_outer_area_gnd=True):
        ni_gnd = self.board.FindNet("gnd")
        self._cleanup_generated_zones()

        ls = pcbnew.LSET()
        for ly in self.lset:
            ls.addLayer(ly)

        filler = pcbnew.ZONE_FILLER(self.board)

        if fill_outer_area_gnd:
            z = pcbnew.ZONE(self.board)
            if self.n_edges == 0:
                cpl = kla.circle_to_polygon( r_out, 100 )
                cp =[]
                for c in cpl:
                    cp.append(self.fpoint(c[0],c[1]))
                z.AddPolygon( self.fpoint_vector(cp) )
            elif self.n_edges >= 4:
                p = self._outline_poly_points(r_out, self.n_edges)
                z.AddPolygon(self.fpoint_vector(p))

            cpl = kla.circle_to_polygon( self.r_coil_out + 2*self.trk_w, 100 )
            cp =[]
            for c in cpl:
                cp.append(self.fpoint(c[0],c[1]))

            z.AddPolygon( self.fpoint_vector(cp) )
            z.SetLayerSet(ls)
            z.SetNet(ni_gnd)
            z.SetLocalClearance( self.trk_w )
            z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)
            z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
            self._tag_generated_zone(z, "outer_cu")
            self.board.Add(z)

        if fill_inner_area_gnd:
            z = pcbnew.ZONE(self.board)
            cpl = kla.circle_to_polygon( r_nosm_in, 100 )
            cp =[]
            for c in cpl:
                cp.append(self.fpoint(c[0],c[1]))

            z.AddPolygon( self.fpoint_vector(cp) )
            z.SetLayerSet(ls)
            z.SetNet(ni_gnd)
            z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)
            self._tag_generated_zone(z, "inner_cu")
            self.board.Add(z)

        nls = pcbnew.LSET()
        nls.addLayer(pcbnew.F_Mask)
        nls.addLayer(pcbnew.B_Mask)
        if fill_outer_area_gnd:
            z = pcbnew.ZONE(self.board)

            if self.n_edges == 0:
                cpl = kla.circle_to_polygon( r_out, 100 )
                cp =[]
                for c in cpl:
                    cp.append(self.fpoint(c[0],c[1]))
                z.AddPolygon( self.fpoint_vector(cp) )
                cpl = kla.circle_to_polygon( r_out - self.w_mnt,  100 )
                cp =[]
                for c in cpl:
                    cp.append(self.fpoint(c[0],c[1]))
                z.AddPolygon( self.fpoint_vector(cp) )

            elif self.n_edges >= 4:
                points_outer = self._outline_poly_points(r_out, self.n_edges)
                z.AddPolygon(self.fpoint_vector(points_outer))

                r_inner = r_out - self.w_mnt
                if r_inner > 0:
                    points_inner = self._outline_poly_points(r_inner, self.n_edges)
                    z.AddPolygon(self.fpoint_vector(points_inner))

            z.SetLayerSet(nls)
            z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)
            self._tag_generated_zone(z, "outer_mask")
            self.board.Add(z)

        if fill_inner_area_gnd:
            z = pcbnew.ZONE(self.board)
            cpl = kla.circle_to_polygon(r_nosm_in, 100)
            cp =[]
            for c in cpl:
                cp.append(self.fpoint(c[0],c[1]))

            z.AddPolygon( self.fpoint_vector(cp) )
            z.SetLayerSet(nls)
            z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)
            self._tag_generated_zone(z, "inner_mask")
            self.board.Add(z)

        filler.Fill(self.board.Zones())

    def do_silkscreen(self, ro, ri, th):
        slot_deg = 360.0 / max(self.n_slots, 1)
        stats = getattr(self, "last_stats", {}) or {}
        phase_r_est = float(stats.get("phase_r_temp", getattr(self, "tr", 0.0)))
        coil_r_est = float(stats.get("coil_resistance_per_coil", 0.0))
        build_label = (
            datetime.today().strftime('%Y%m%d') +
            "_ly" + str(self.n_layers) +
            "_s" + str(self.n_slots) +
            "_w" + str(self.n_loops)
        )

        for r in [ro,ri]:
            self._add_silk_circle(r)
  
        th_0 = 2*math.pi/self.n_slots
        la = 0.05
        for p in range(self.n_slots):
            xy_s = (
                (1 + la) * ri * math.cos(th_0 * p),
                (1 + la) * ri * math.sin(th_0 * p),
            )
            xy_e = (
                (1 - la) * ro * math.cos(th_0 * p),
                (1 - la) * ro * math.sin(th_0 * p),
            )
            self._add_silk_segment(xy_s, xy_e)

        outer_guide_r = max(ro, self._get_outline_outer_radius())
        degree_ring_r = ro + max(0.9 * self.SCALE, self.trk_space * 2.0)
        if getattr(self, "silk_cross_guides", False):
            self._add_silk_cross_guides(outer_guide_r)
        if getattr(self, "silk_slot_frames", False):
            self._add_silk_slot_frames(ri, ro)
        if getattr(self, "silk_deg_scale", False):
            self._add_silk_circle(degree_ring_r)
            self._add_silk_arc_ticks(
                degree_ring_r,
                0.0,
                2 * math.pi - math.radians(1.0),
                step_deg=1.0,
                tick_inner=0.35,
                tick_outer=0.0,
                major_step=10,
            )
        if getattr(self, "silk_hole_scales", False):
            self._add_silk_hole_scales()

        info_anchor = self._get_bottom_right_info_anchor()
        self._add_silk_text(
            build_label,
            (info_anchor[0] - 2.6 * self.SCALE, info_anchor[1]),
            0.95,
            "left",
        )
        self._add_silk_text(
            f"slots {self.n_slots} | {slot_deg:.2f} deg/slot",
            (info_anchor[0] - 2.6 * self.SCALE, info_anchor[1] - 1.8 * self.SCALE),
            0.95,
            "left",
        )
        self._add_silk_text(
            f"R / phase: {phase_r_est:.4f} ohm",
            (info_anchor[0], info_anchor[1] - 3.6 * self.SCALE),
            0.95,
            "left",
        )
        self._add_silk_text(
            f"R / coil: {coil_r_est:.4f} ohm",
            (info_anchor[0], info_anchor[1] - 5.4 * self.SCALE),
            0.95,
            "left",
        )

    def fillet(self, board, t1, t2, r, side=1):
        t1_arc = t1.GetClass() == 'PCB_ARC'
        t2_arc = t2.GetClass() == 'PCB_ARC'

        if t1_arc and t2_arc:
            return
        elif t1_arc or t2_arc:
            c = kla.line_arc_center(t1,t2,r,side)
        else:
            c = kla.line_line_center(t1,t2,r)
            l1 = kla.line_points(t1)
            p1 = kla.circle_line_tg( l1, c, r)
            l2 = kla.line_points(t2)
            p2 = kla.circle_line_tg( l2, c, r)

        if t1_arc:
            c1 = t1.GetCenter()
            c1 = np.array([c1.x, c1.y])
            r1 = t1.GetRadius()
            p1 = kla.circle_circle_tg(c,r,c1,r1)
            l2 = kla.line_points(t2)
            p2 = kla.circle_line_tg(l2,c,r)
            m = kla.circle_arc_mid(p1,p2,c,r)
        elif t2_arc:
            l1 = kla.line_points(t1)
            p1 = kla.circle_line_tg(l1,c,r)
            c2 = t2.GetCenter()
            c2 = np.array([c2.x, c2.y])
            r2 = t2.GetRadius()
            p2 = kla.circle_circle_tg(c,r, c2, r2)
            m = kla.circle_arc_mid(p1,p2, c,r)
        else:
            t1e = t1.GetEnd()
            l = np.array([c,[t1e.x, t1e.y, 0]])
            lv = kla.line_vec(l)
            m = c + np.dot(r, lv)

        t = pcbnew.PCB_ARC(board)
        t.SetLayer( t1.GetLayer() )
        t.SetWidth( t1.GetWidth() )
        t.SetStart( self.fpoint(int(p1[0]),int(p1[1])) )
        t.SetMid( self.fpoint(int(m[0]),int(m[1])) )
        t.SetEnd( self.fpoint(int(p2[0]),int(p2[1])) )
        board.Add(t)
        
        t1.SetEnd( self.fpoint(int(p1[0]),int(p1[1]))  )
        t2.SetStart( self.fpoint(int(p2[0]),int(p2[1]))  )

        return t

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

    def on_close(self, event):
        try:
            self.pm.SaveAndUnregister()
        except Exception as exc:
            self.set_status("Close warning")
            self._log_exception("Close persistence failed", exc)
        event.Skip()

    def on_btn_clear(self, event):
        if self.group:
            self.group.RemoveAll()
            self.group = None
            self.btn_clear.Enable(False)
        event.Skip()

    def on_btn_generate(self, event):
        self._run_action(
            "Started: generation running (can take 5-60 s)",
            "Finished",
            "Generation",
            self.generate,
        )
        event.Skip()

    def on_btn_generate_magnet(self, event):
        self._run_action(
            "Started: magnet PCB generation running",
            "Magnet PCB generated",
            "Magnet PCB generation",
            self.generate_magnet_pcb,
            summary_target="magnet",
        )
        event.Skip()

    def on_btn_generate_both(self, event):
        def _generate_both():
            self.generate()
            self.generate_magnet_pcb()

        self._run_action(
            "Started: combined stator + magnet generation running",
            "Stator and Magnet PCB generated",
            "Combined generation",
            _generate_both,
            summary_target="magnet",
        )
        event.Skip()

    def on_btn_save(self, event):
        self.set_status("Saving preset")
        try:
            self.pm.SaveAndUnregister()
            self.pm.RegisterAndRestoreAll(self)
            with wx.FileDialog(self, "Save KMotor_Pro preset", wildcard="KMT files (*.kmt)|*.kmt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                fileDialog.SetFilename("kmotor_pro.kmt")
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    self.set_status("Save cancelled")
                    return
                origin = self.pf
                target = fileDialog.GetPath()
                shutil.copyfile(origin, target)
            self.set_status("Preset saved")
        except Exception as exc:
            self.set_status("Save failed")
            self._log_exception("Preset save failed", exc)

    def on_btn_load(self, event):
        self.set_status("Loading preset")
        try:
            with wx.FileDialog(self, "Load KMotor_Pro preset", wildcard="KMT files (*.kmt)|*.kmt",
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    self.set_status("Load cancelled")
                    return
                origin = fileDialog.GetPath()
                target = self.pf
                tmp = fileDialog.GetDirectory() + "/kmotor_pro.tmp"

                self.pm.SetPersistenceFile(tmp)
                self.pm.SaveAndUnregister()
                shutil.copyfile(origin, target)
                self.pm.SetPersistenceFile(target)
                self.pm.RegisterAndRestoreAll(self)
                self.on_cb_outline(None)
                self.on_cb_trmtype(None)
                self.on_cb_winding_mode(None)
                self.on_cb_magnet_shape(None)
            self.set_status("Preset loaded")
        except Exception as exc:
            try:
                self.pm.SetPersistenceFile(self.pf)
                self.pm.RegisterAndRestoreAll(self)
                self.on_cb_outline(None)
                self.on_cb_trmtype(None)
                self.on_cb_winding_mode(None)
                self.on_cb_magnet_shape(None)
            except Exception:
                pass
            self.set_status("Load failed")
            self._log_exception("Preset load failed", exc)

    def on_cb_preset(self, event):
        if not hasattr(self, "m_cbPreset"):
            if event is not None:
                event.Skip()
            return
        preset = self.m_cbPreset.GetSelection()
        if preset == 0:
            self.m_ctrlTrackWidth.SetValue(0.3)
        elif preset == 1:
            self.m_ctrlTrackWidth.SetValue(0.127)
        elif preset == 2:
            self.m_ctrlTrackWidth.SetValue(0.15)
        if event is not None:
            event.Skip()

    def on_cb_outline(self, event):
        if self.m_cbOutline.GetStringSelection() == "None":
            self.m_ctrlDout.Enable(False)
            self.m_ctrlFilletRadius.Enable(False)
        elif self.m_cbOutline.GetStringSelection() == "Circle":
            self.m_ctrlDout.Enable(True)
            self.m_ctrlFilletRadius.Enable(True)
        else:
            self.m_ctrlDout.Enable(True)
            self.m_ctrlFilletRadius.Enable(True)

        if event is not None:
            event.Skip()

    def on_cb_trmtype(self, event):
        pads = self.m_cbTP.GetStringSelection()
        if pads == "None":
            self.m_termSize.Enable(False)
        elif pads == "THT" or pads == "SMD":
            keys = self.term_db.get(pads).keys()
            for i,k in enumerate(keys):
                self.m_termSize.SetString(i,k)
            while len(keys) < self.m_termSize.GetCount():
                self.m_termSize.Delete( self.m_termSize.GetCount()-1 )
            self.m_termSize.SetValue( 
                self.m_termSize.GetString(
                    self.m_termSize.GetCurrentSelection()))
            self.m_termSize.Enable(True)

        if event is not None:
            event.Skip()

    def on_cb_winding_mode(self, event):
        mode = self.m_cbWindingMode.GetStringSelection() if hasattr(self, "m_cbWindingMode") else "PCB"
        is_pcb = (mode == "PCB")
        for ctrl in (self.lbl_copperWeight, self.m_cbCopperWeight):
            ctrl.Enable(is_pcb)
        for ctrl in (self.lbl_wireDia, self.m_ctrlWireDia, self.lbl_wireDiaUnit):
            ctrl.Enable(not is_pcb)

        if event is not None:
            event.Skip()

    def on_cb_magnet_shape(self, event):
        shape = self.m_cbMagShape.GetStringSelection() if hasattr(self, "m_cbMagShape") else "Round"
        is_round = (shape == "Round")
        for ctrl in (self.lbl_magDia, self.m_ctrlMagDia, self.lbl_magDiaUnit):
            ctrl.Enable(is_round)
        for ctrl in (
            self.lbl_magWidth, self.m_ctrlMagWidth, self.lbl_magWidthUnit,
            self.lbl_magHeight, self.m_ctrlMagHeight, self.lbl_magHeightUnit,
        ):
            ctrl.Enable(not is_round)
        self._update_magnet_summary(
            "Round magnets use Magnet dia. Rect magnets use width (B) and height (H). "
            "Use Generate Magnet PCB for a first fit-check against ring diameter and pole count."
        )
        if event is not None:
            event.Skip()

    def on_cb_mholes(self, event):
        event.Skip()

    def on_nr_layers(self, event):
        self.n_layers = int(self.m_ctrlLayers.GetValue())
        event.Skip()
