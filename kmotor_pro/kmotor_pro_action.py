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
    import kmotor_geometry as kgeo
    import kmotor_kicad as kkicad
    import kmotor_pro_gui
    import kmotor_pro_linalg as kla
    import kmotor_pro_persist as kpers
    import kmotor_pro_solver as ksolve
else:
    from . import kmotor_geometry as kgeo
    from . import kmotor_kicad as kkicad
    from . import kmotor_pro_gui
    from . import kmotor_pro_linalg as kla
    from . import kmotor_pro_solver as ksolve
    from . import kmotor_pro_persist as kpers

# KMotorProPlugin moved to kmotor_api.py

from .kmotor_models import (
    MotorInputConfig,
    TopologyConfig,
    StatorMechanicsConfig,
    CoilLayoutConfig,
    StackPcbConfig,
    RotorMagnetConfig,
    PeripheralsConfig,
)

class KMotorProDialog ( kmotor_pro_gui.KMotorProGUI ):
    
    def to_motor_config(self) -> MotorInputConfig:
        """Convert GUI parameters to MotorInputConfig."""
        self.get_parameters()
        if hasattr(self, 'm_cbMagShape'):
            self.get_magnet_parameters()
        scheme = self.m_cbScheme.GetStringSelection() if hasattr(self, 'm_cbScheme') else "3P"
        term_size = self.m_termSize.GetStringSelection() if hasattr(self, 'm_termSize') else "1.0"
        return ksolve.build_motor_config(
            scheme=scheme,
            outline=self.outline,
            n_slots=self.n_slots,
            magnet_pole_pairs=getattr(self, 'magnet_pole_pairs', 30),
            scale=self.SCALE,
            r_in=self.r_in,
            r_out=self.r_out,
            o_fill=getattr(self, 'o_fill', 0.0),
            w_mnt=self.w_mnt,
            mhs=getattr(self, 'mhs', 'M3'),
            n_mh_out=self.n_mh_out,
            r_mh_out=self.r_mh_out,
            n_mh_in=self.n_mh_in,
            r_mh_in=self.r_mh_in,
            corner_hole_count=getattr(self, 'corner_hole_count', 4),
            corner_hole_dia=getattr(self, 'corner_hole_dia', 0.0),
            corner_hole_offset=getattr(self, 'corner_hole_offset', 0.0),
            winding_mode=getattr(self, 'winding_mode', 'PCB'),
            strategy=getattr(self, 'strategy', 1),
            max_spec=getattr(self, 'max_spec', False),
            n_loops=self.n_loops,
            r_coil_in=self.r_coil_in,
            r_coil_out=self.r_coil_out,
            trk_w=self.trk_w,
            trk_space=self.trk_space,
            r_fill=getattr(self, 'r_fill', 0.0),
            wire_dia_mm=getattr(self, 'wire_dia_mm', 0.50),
            n_layers=self.n_layers,
            copper_weight=getattr(self, 'copper_weight', '1 oz / 35um'),
            d_via=self.d_via,
            d_drill=self.d_drill,
            support_via_mode=getattr(self, 'support_via_mode', 2),
            d_support_hole=self.d_support_hole,
            ring_w=self.ring_w,
            ring_space=self.ring_space,
            fill_inner_gnd=getattr(self, 'fill_inner_gnd', True),
            inner_fill_dia=getattr(self, 'inner_fill_dia', 0),
            fill_outer_gnd=getattr(self, 'fill_outer_gnd', True),
            magnet_shape=getattr(self, 'magnet_shape', 'round'),
            magnet_ring_dia=getattr(self, 'magnet_ring_dia', 0.0),
            magnet_rotation=getattr(self, 'magnet_rotation', 0.0),
            magnet_dia=getattr(self, 'magnet_dia', 0.0),
            magnet_width=getattr(self, 'magnet_width', 0.0),
            magnet_height=getattr(self, 'magnet_height', 0.0),
            magnet_length=getattr(self, 'magnet_length', 0.0),
            magnet_gap=getattr(self, 'magnet_gap', 0.0),
            magnet_keepout=getattr(self, 'magnet_keepout', 0.0),
            magnet_b_est=getattr(self, 'magnet_b_est', 0.60),
            trmtype=getattr(self, 'trmtype', 'THT'),
            term_size=term_size,
            term_offset=self.term_offset,
            silk_cross_guides=getattr(self, 'silk_cross_guides', False),
            silk_slot_frames=getattr(self, 'silk_slot_frames', False),
            silk_deg_scale=getattr(self, 'silk_deg_scale', False),
            silk_hole_scales=getattr(self, 'silk_hole_scales', False),
            corner_scale_step_deg=getattr(self, 'corner_scale_step_deg', 1.0),
            corner_scale_span_deg=getattr(self, 'corner_scale_span_deg', 5.0),
        )

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
    PCB_PRESETS = {
        "JLCPCB 2L economy": {
            "layers": 2,
            "track_width": 0.20,
            "track_spacing": 0.20,
            "ring_width": 0.70,
            "ring_spacing": 0.30,
            "via_dia": 0.50,
            "via_drill": 0.30,
            "copper_weight": "1 oz / 35um",
        },
        "JLCPCB 4L balanced": {
            "layers": 4,
            "track_width": 0.15,
            "track_spacing": 0.15,
            "ring_width": 0.70,
            "ring_spacing": 0.25,
            "via_dia": 0.45,
            "via_drill": 0.20,
            "copper_weight": "1 oz / 35um",
        },
        "JLCPCB 6L dense": {
            "layers": 6,
            "track_width": 0.127,
            "track_spacing": 0.127,
            "ring_width": 0.60,
            "ring_spacing": 0.20,
            "via_dia": 0.40,
            "via_drill": 0.20,
            "copper_weight": "0.5 oz / 18um",
        },
        "PCBWay 2L standard": {
            "layers": 2,
            "track_width": 0.18,
            "track_spacing": 0.18,
            "ring_width": 0.70,
            "ring_spacing": 0.30,
            "via_dia": 0.50,
            "via_drill": 0.25,
            "copper_weight": "1 oz / 35um",
        },
        "PCBWay 4L balanced": {
            "layers": 4,
            "track_width": 0.15,
            "track_spacing": 0.15,
            "ring_width": 0.65,
            "ring_spacing": 0.25,
            "via_dia": 0.45,
            "via_drill": 0.20,
            "copper_weight": "1 oz / 35um",
        },
        "PCBWay 6L heavy": {
            "layers": 6,
            "track_width": 0.20,
            "track_spacing": 0.20,
            "ring_width": 0.80,
            "ring_spacing": 0.30,
            "via_dia": 0.50,
            "via_drill": 0.25,
            "copper_weight": "2 oz / 70um",
        },
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
        return kpers.eda_angle(angle, self.KICAD_VERSION)

    def init_persist(self, configFile):
        self.pm = kpers.init_persist(self, configFile)

    def _point_xy(self, pt):
        return kgeo.point_xy(pt)

    def _as_point(self, x, y):
        return kkicad.as_point(x, y, self.fpoint)

    def _item_token(self, item):
        return kkicad.item_token(item)

    def _tag_generated_zone(self, zone, kind):
        kkicad.tag_generated_zone(
            zone,
            kind,
            self.generated_zone_tokens,
            self.GENERATED_ZONE_PRIORITIES,
            self.GENERATED_ZONE_NAME_PREFIX,
        )

    def _is_generated_zone(self, zone):
        return kkicad.is_generated_zone(
            zone,
            self.generated_zone_tokens,
            self.GENERATED_ZONE_PRIORITIES,
            self.GENERATED_ZONE_NAME_PREFIX,
        )

    def _cleanup_generated_zones(self):
        kkicad.cleanup_generated_zones(
            self.board,
            self.generated_zone_tokens,
            self.GENERATED_ZONE_PRIORITIES,
            self.GENERATED_ZONE_NAME_PREFIX,
        )

    def _radial_vector(self, angle, radius=1.0):
        return kgeo.radial_vector(angle, radius)

    def _tangent_vector(self, angle, scale=1.0):
        return kgeo.tangent_vector(angle, scale)

    def _point_radius(self, pt):
        return kgeo.point_radius(pt)

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
        return kgeo.outline_outer_radius(self.r_out, self.n_edges)

    def _get_outline_corners(self):
        if self.n_edges < 4:
            return None
        points = kgeo.outline_poly_points(self.r_out, self.n_edges)
        if not points:
            return None
        return [kgeo.point_xy(pt) for pt in points]

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
        return kgeo.clip_segment_to_outline_box(start_xy, end_xy, bounds, margin)

    def _rotate_xy(self, xy, angle):
        return kgeo.rotate_xy(xy, angle)

    def _rotate_about_xy(self, xy, center_xy, angle):
        return kgeo.rotate_about_xy(xy, center_xy, angle)

    def _offset_xy(self, xy, origin_xy):
        return kgeo.offset_xy(xy, origin_xy)

    def _get_board_span(self):
        return ksolve.get_board_span(self.r_out)

    def _get_magnet_board_origin(self):
        return ksolve.get_magnet_board_origin(self._get_board_span())

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
        bounds = self._get_outline_bounds() if clip_to_outline and self.n_edges == 4 else None
        return kkicad.add_silk_segment(
            self.board,
            start_xy,
            end_xy,
            self.fpoint,
            self.SCALE,
            width=width,
            clip_to_outline=clip_to_outline and bounds is not None,
            clip_margin=clip_margin,
            bounds=bounds,
        )

    def _add_silk_circle(self, radius, width=None):
        return self._add_silk_circle_at((0.0, 0.0), radius, width)

    def _add_silk_circle_at(self, center_xy, radius, width=None):
        return kkicad.add_silk_circle(self.board, center_xy, radius, self.fpoint, self.SCALE, width=width)

    def _add_edge_cuts_circle_at(self, center_xy, radius, width=None):
        return kkicad.add_edge_cuts_circle(self.board, center_xy, radius, self.fpoint, self.SCALE, width=width)

    def _clear_generated_corner_holes(self):
        for fp in list(self.board.GetFootprints()):
            ref = fp.GetReferenceAsString() if hasattr(fp, "GetReferenceAsString") else ""
            if ref.startswith("KMH_"):
                self.board.RemoveNative(fp)

    def _add_npth_hole_at(self, center_xy, radius, index):
        return kkicad.add_npth_hole(self.board, center_xy, radius, index, self.fpoint, self.fsize)

    def _add_silk_arc_ticks(self, radius, angle_start, angle_end, step_deg=1.0, tick_inner=0.8, tick_outer=0.0, major_step=5):
        return kkicad.add_silk_arc_ticks(
            self._add_silk_segment,
            self.SCALE,
            radius,
            angle_start,
            angle_end,
            step_deg=step_deg,
            tick_inner=tick_inner,
            tick_outer=tick_outer,
            major_step=major_step,
        )

    def _add_local_tick_fan(self, center_xy, base_angle, fan_deg=18.0, radius_mm=3.0):
        return kkicad.add_local_tick_fan(
            self._add_silk_segment,
            self.SCALE,
            center_xy,
            base_angle,
            fan_deg=fan_deg,
            radius_mm=radius_mm,
        )

    def _add_linear_hole_scale(self, center_xy, radial_angle, hole_radius):
        step_deg = max(0.1, float(getattr(self, "corner_scale_step_deg", 1.0)))
        base_hole_count = max(1, int(getattr(self, "corner_hole_count", 4)))
        angle_span = float(getattr(self, "corner_scale_span_deg", 5.0))
        return kkicad.add_linear_hole_scale(
            self._add_npth_hole_at,
            self._add_silk_segment,
            self._rotate_xy,
            self.SCALE,
            center_xy,
            radial_angle,
            hole_radius,
            step_deg,
            base_hole_count,
            angle_span,
        )

    def _iter_outer_mount_points(self):
        return kkicad.iter_outer_mount_points(
            self.n_edges,
            self.corner_hole_offset,
            self.corner_hole_dia,
            self.corner_hole_count,
            self._get_outline_corners(),
            self.n_mh_out,
            self.r_mh_out,
            self.SCALE,
        )

    def _add_silk_cross_guides(self, radius):
        return kkicad.add_silk_cross_guides(self._add_silk_segment, self._get_outline_corners(), radius)

    def _add_silk_slot_frames(self, ri, ro):
        return kkicad.add_silk_slot_frames(self._add_silk_segment, self.n_slots, ri, ro)

    def _add_silk_hole_scales(self):
        self._clear_generated_corner_holes()
        for x, y, angle, dia in self._iter_outer_mount_points():
            self._add_linear_hole_scale((x, y), angle, max(dia * 0.5, 0.5 * self.SCALE))

    def _add_silk_text(self, text, pos_xy, size_scale=1.0, align="right"):
        return kkicad.add_silk_text(
            self.board,
            text,
            pos_xy,
            self.fpoint,
            self.fsize,
            self.txt_size,
            self.SCALE,
            size_scale=size_scale,
            align=align,
        )

    def _add_grouped_silk_segment(self, group, start_xy, end_xy, width=None):
        return self._add_grouped_segment(group, start_xy, end_xy, pcbnew.F_SilkS, width if width is not None else max(1, 0.127 * self.SCALE))

    def _add_grouped_segment(self, group, start_xy, end_xy, layer, width):
        return kkicad.add_grouped_segment(self.board, group, start_xy, end_xy, layer, width, self.fpoint)

    def _add_grouped_silk_circle(self, group, center_xy, radius, width=None):
        return self._add_grouped_circle(group, center_xy, radius, pcbnew.F_SilkS, width if width is not None else max(1, 0.127 * self.SCALE))

    def _add_grouped_circle(self, group, center_xy, radius, layer, width):
        return kkicad.add_grouped_circle(self.board, group, center_xy, radius, layer, width, self.fpoint)

    def _add_grouped_edge_circle(self, group, center_xy, radius, width=None):
        return self._add_grouped_circle(group, center_xy, radius, pcbnew.Edge_Cuts, width if width is not None else max(1, 0.09 * self.SCALE))

    def _get_magnet_aux_layer(self):
        return kkicad.get_magnet_aux_layer()

    def _add_grouped_rect_outline(self, group, center_xy, half_w, half_h, angle, layer, width):
        return kkicad.add_grouped_rect_outline(
            self.board,
            group,
            center_xy,
            half_w,
            half_h,
            angle,
            layer,
            width,
            self.fpoint,
        )

    def get_parameters(self):
        self.outline = self.m_cbOutline.GetStringSelection()
        self.n_edges = ksolve.resolve_outline_edges(self.outline)

        self.trmtype = kpers.read_selection(self.m_cbTP)
        scheme = kpers.read_selection(self.m_cbScheme)
        self.phases, self.n_term = ksolve.resolve_phase_scheme(scheme)
        
        self.n_layers = kpers.read_int(self.m_ctrlLayers)
        self.lset = self.udpate_lset(self.n_layers)
        self.n_loops = kpers.read_int(self.m_ctrlLoops)
        self.n_slots = kpers.read_int(self.m_ctrlSlots)
        self.winding_mode = kpers.read_selection(getattr(self, "m_cbWindingMode", None), "PCB")
        self.copper_weight = kpers.read_selection(getattr(self, "m_cbCopperWeight", None), "1 oz / 35um")
        self.copper_thickness_m = self.COPPER_WEIGHT_TO_THICKNESS_M.get(self.copper_weight, self.tthick)
        self.wire_dia_mm = kpers.read_float(getattr(self, "m_ctrlWireDia", None), 0.50)
        
        self.strategy = kpers.read_index(self.m_cbStrategy)
        self.max_spec = kpers.read_toggle(primary=getattr(self, "m_chkMaxSpec", None))

        self.trk_w = kpers.read_scaled(self.m_ctrlTrackWidth, self.SCALE)
        self.trk_space = kpers.read_scaled(self.m_ctrlTrackSpacing, self.SCALE)
        self.dr = self.trk_w + self.trk_space
        
        self.ring_w = kpers.read_scaled(self.m_ctrlRingWidth, self.SCALE)
        self.ring_space = kpers.read_scaled(self.m_ctrlRingSpacing, self.SCALE)
        self.ring_dr = self.ring_w + self.ring_space

        self.d_via = kpers.read_scaled(self.m_ctrlViaDia, self.SCALE)
        self.d_drill = kpers.read_scaled(self.m_ctrlViaDrill, self.SCALE)
        self.d_support_hole = kpers.read_scaled(getattr(self, "m_ctrlSupportHoleDia", None), self.SCALE, self.d_drill / self.SCALE) if hasattr(self, "m_ctrlSupportHoleDia") else self.d_drill

        self.via_rows = 2
        support_via_value = kpers.read_selection_with_fallback(
            getattr(self, "m_cbSupportViaMode", None),
            getattr(self, "m_cbSupportVias", None),
            2,
        )
        self.support_via_mode = ksolve.normalize_support_via_mode(support_via_value)

        if hasattr(self, "m_cbFillInnerGND"):
            self.fill_inner_gnd = kpers.read_toggle(primary=self.m_cbFillInnerGND)
        elif hasattr(self, "m_chkFillInnerGnd"):
            self.fill_inner_gnd = kpers.read_toggle(primary=self.m_chkFillInnerGnd)
        else:
            self.fill_inner_gnd = True
        if hasattr(self, "m_cbFillOuterGND"):
            self.fill_outer_gnd = kpers.read_toggle(primary=self.m_cbFillOuterGND)
        elif hasattr(self, "m_chkFillOuterGnd"):
            self.fill_outer_gnd = kpers.read_toggle(primary=self.m_chkFillOuterGnd)
        else:
            self.fill_outer_gnd = True
        self.silk_cross_guides = kpers.read_toggle(primary=getattr(self, "m_cbSilkCross", None))
        self.silk_deg_scale = kpers.read_toggle(primary=getattr(self, "m_cbSilkDeg", None))
        self.silk_slot_frames = kpers.read_toggle(primary=getattr(self, "m_cbSilkSlots", None))
        self.silk_hole_scales = kpers.read_toggle(primary=getattr(self, "m_cbSilkHoleScale", None))
        self.corner_hole_offset = kpers.read_scaled(getattr(self, "m_ctrlCornerHoleOffset", None), self.SCALE)
        self.corner_hole_dia = kpers.read_scaled(getattr(self, "m_ctrlCornerHoleDia", None), self.SCALE)
        self.corner_hole_count = kpers.read_int(getattr(self, "m_ctrlCornerHoleCount", None), 4)
        self.corner_scale_step_deg = kpers.read_float(getattr(self, "m_ctrlCornerScaleStep", None), 1.0)
        self.corner_scale_span_deg = kpers.read_float(getattr(self, "m_ctrlCornerScaleSpan", None), 5.0)
        if hasattr(self, "m_ctrlInnerGndDia"):
            self.inner_fill_dia = kpers.read_nonnegative_scaled(self.m_ctrlInnerGndDia, self.SCALE)
        else:
            self.inner_fill_dia = 0

        self.r_fill = kpers.read_scaled(self.m_ctrlRfill, self.SCALE)
        self.o_fill = kpers.read_scaled(self.m_ctrlFilletRadius, self.SCALE)

        self.r_in = kpers.read_scaled_radius(self.m_ctrlDbore, self.SCALE)
        self.r_out = kpers.read_scaled_radius(self.m_ctrlDout, self.SCALE)
        self.r_coil_in = kpers.read_scaled_radius(self.m_ctrlDin, self.SCALE)
        self.r_coil_out = kpers.read_scaled_radius(self.m_ctrlDend, self.SCALE)
        
        self.w_mnt = kpers.read_scaled(self.m_ctrlWmnt, self.SCALE)
        self.term_offset = kpers.read_scaled(self.m_ctrlDterm, self.SCALE)
        
        self.mhs = kpers.read_selection(self.m_cbMountSize)
        self.n_mh_out = kpers.read_int(self.m_mhOut)
        self.r_mh_out = kpers.read_scaled_radius(self.m_mhOutR, self.SCALE)
        self.n_mh_in = kpers.read_int(self.m_mhIn)
        self.r_mh_in = kpers.read_scaled_radius(self.m_mhInR, self.SCALE)

        self.txt_size = int(0.5 * self.SCALE)
        self.txt_loc = int(self.r_out - 3*self.txt_size)

        if self.group:
            self.btn_clear.Enable(True)

    def _effective_winding_layers(self):
        return ksolve.effective_winding_layers(getattr(self, "n_layers", 1))

    def _winding_pitch_mm(self):
        return ksolve.winding_pitch_mm(
            getattr(self, "winding_mode", "PCB"),
            getattr(self, "wire_dia_mm", 0.50),
            self.trk_space,
            self.trk_w,
            self.SCALE,
        )

    def _estimate_turns_per_layer(self):
        return ksolve.estimate_turns_per_layer(
            self.r_coil_in,
            self.r_coil_out,
            self.SCALE,
            self._effective_winding_layers(),
            self._winding_pitch_mm(),
            self.n_loops,
        )

    def _apply_pcb_preset(self, preset_name):
        preset = kpers.resolve_pcb_preset(preset_name, self.PCB_PRESETS)
        if not preset:
            return False

        kpers.apply_pcb_preset_values(
            preset,
            self.m_ctrlLayers,
            self.m_ctrlTrackWidth,
            self.m_ctrlTrackSpacing,
            self.m_ctrlRingWidth,
            self.m_ctrlRingSpacing,
            self.m_ctrlViaDia,
            self.m_ctrlViaDrill,
            getattr(self, "m_cbCopperWeight", None),
        )
        kpers.run_event_callbacks(self.on_nr_layers, self.on_cb_winding_mode)
        return True

    def set_status(self, text):
        kpers.set_status(self, text)

    def _format_exception(self, exc):
        return kpers.format_exception(exc)

    def _log_exception(self, title, exc):
        return kpers.log_exception(title, exc, self._format_exception)

    def _safe_ui_yield(self):
        return kpers.safe_ui_yield(self)

    def _safe_refresh_board(self):
        return kpers.safe_refresh_board(self.board)

    def _run_action(self, start_status, success_status, title, callback, summary_target=None):
        return kpers.run_action(
            start_status,
            success_status,
            title,
            callback,
            self.set_status,
            self._safe_ui_yield,
            self._safe_refresh_board,
            self._format_exception,
            self._log_exception,
            update_magnet_summary=self._update_magnet_summary,
            summary_target=summary_target,
        )

    def validate_parameters(self):
        return ksolve.validate_parameters(self.n_slots, self.n_loops, self.phases)

    def get_magnet_parameters(self):
        params = ksolve.magnet_parameters_from_values(
            magnet_shape=kpers.read_selection(self.m_cbMagShape),
            magnet_dia=kpers.read_scaled(self.m_ctrlMagDia, self.SCALE),
            magnet_width=kpers.read_scaled(self.m_ctrlMagWidth, self.SCALE),
            magnet_height=kpers.read_scaled(self.m_ctrlMagHeight, self.SCALE),
            magnet_length=kpers.read_scaled(self.m_ctrlMagLength, self.SCALE),
            magnet_ring_dia=kpers.read_scaled(self.m_ctrlMagRingDia, self.SCALE),
            magnet_pole_pairs=kpers.read_int(self.m_ctrlMagPolePairs),
            magnet_gap=kpers.read_scaled(self.m_ctrlMagGap, self.SCALE),
            magnet_keepout=kpers.read_scaled(self.m_ctrlMagKeepout, self.SCALE),
            magnet_rotation=kpers.read_float(self.m_ctrlMagRotation),
            magnet_b_est=kpers.read_float(getattr(self, "m_ctrlMagBest", None), 0.60),
        )
        kpers.assign_attributes(self, params)

    def validate_magnet_parameters(self):
        self.get_magnet_parameters()
        return ksolve.validate_magnet_parameters(
            magnet_pole_pairs=self.magnet_pole_pairs,
            magnet_ring_dia=self.magnet_ring_dia,
            magnet_shape=self.magnet_shape,
            magnet_dia=self.magnet_dia,
            magnet_width=self.magnet_width,
            magnet_height=self.magnet_height,
            magnet_gap=self.magnet_gap,
            magnet_keepout=self.magnet_keepout,
            magnet_poles=self.magnet_poles,
            scale=self.SCALE,
            r_in=self.r_in,
            r_out=self.r_out,
            clearance_targets=self._iter_magnet_clearance_targets(),
            nearest_angle_delta_fn=self._nearest_magnet_angle_delta,
        )

    def _update_magnet_summary(self, text):
        return kpers.update_magnet_summary(self, text)

    def _get_mounting_hole_dia(self):
        fp_name = self.mhole_db.get(self.mhs or "", "")
        return ksolve.get_mounting_hole_dia(fp_name, self.SCALE)

    def _iter_magnet_clearance_targets(self):
        corner_targets = []
        if self.n_edges == 4 and self.corner_hole_offset > 0 and self.corner_hole_dia > 0:
            for x, y, angle, dia in self._iter_outer_mount_points():
                corner_targets.append((x, y, angle, dia))
        return ksolve.iter_magnet_clearance_targets(
            n_mh_out=self.n_mh_out,
            r_mh_out=self.r_mh_out,
            n_edges=self.n_edges,
            n_mh_in=self.n_mh_in,
            r_mh_in=self.r_mh_in,
            mh_dia=self._get_mounting_hole_dia(),
            corner_targets=corner_targets,
        )

    def _angle_delta(self, a, b):
        return ksolve.angle_delta(a, b)

    def _nearest_magnet_angle_delta(self, target_angle):
        return ksolve.nearest_magnet_angle_delta(target_angle, self.magnet_poles, self.magnet_rotation)

    def estimate_motor_constants(self, stats=None):
        if stats is None:
            stats = getattr(self, "last_stats", None)
        if not kpers.prepare_model_inputs(self.get_parameters, self.get_magnet_parameters):
            return {"ke_est": 0.0, "kt_est": 0.0, "kv_est": 0.0}

        return ksolve.estimate_motor_constants(
            self.phases,
            self.n_loops,
            self.r_coil_in,
            self.r_coil_out,
            self.SCALE,
            self.n_slots,
            kpers.get_attr(self, "magnet_b_est", 0.60),
        )

    def estimate_winding_factor(self):
        if not kpers.prepare_model_inputs(self.get_parameters, self.get_magnet_parameters):
            return 0.0

        return ksolve.estimate_winding_factor(
            self.phases,
            self.n_slots,
            self.magnet_poles,
            self.magnet_pole_pairs,
            self.n_loops,
        )

    def estimate_performance_stats(self, stats=None, motor_consts=None):
        stats = kpers.resolve_stats(stats, getattr(self, "last_stats", {}))
        if motor_consts is None:
            motor_consts = self.estimate_motor_constants(stats)

        return ksolve.estimate_performance_stats(
            stats,
            motor_consts,
            self.estimate_winding_factor(),
        )

    def estimate_model_warnings(self, stats=None, motor_consts=None, perf_stats=None):
        stats = kpers.resolve_stats(stats, getattr(self, "last_stats", {}))
        if motor_consts is None:
            motor_consts = self.estimate_motor_constants(stats)
        if perf_stats is None:
            perf_stats = self.estimate_performance_stats(stats, motor_consts)

        return ksolve.estimate_model_warnings(
            stats,
            perf_stats,
            kpers.get_attr(self, "magnet_b_est", 0.0),
            kpers.get_attr(self, "magnet_poles", 0),
        )

    def get_effective_coil_strategy(self, ri, ro, n_slots, n_loops):
        return ksolve.get_effective_coil_strategy(
            ri,
            ro,
            n_slots,
            n_loops,
            self.dr,
            self.trk_w,
            kpers.get_attr(self, "strategy", 1),
            kpers.get_attr(self, "max_spec", False),
        )

    def _clear_magnet_group(self):
        self.magnet_group = kkicad.clear_magnet_group(self.board, getattr(self, 'magnet_group', None))

    def _create_magnet_group(self):
        self.magnet_group = kkicad.reset_magnet_group(
            self.board,
            getattr(self, 'magnet_group', None),
            name='magnet_pcb',
        )
        return self.magnet_group

    def _add_mounting_hole_fp_at(self, group, center_xy, fp_lib, fp_name, ref, net=None):
        return kkicad.add_mounting_hole_fp_at(
            self.board,
            group,
            center_xy,
            fp_lib,
            fp_name,
            ref,
            self.fpoint,
            net=net,
        )

    def _iter_corner_points_for_origin(self, origin_xy):
        return kkicad.iter_corner_points_for_origin(
            self.n_edges,
            self.corner_hole_offset,
            self.corner_hole_dia,
            self.corner_hole_count,
            self.r_out,
            origin_xy,
        )

    def _add_linear_hole_scale_at(self, group, center_xy, radial_angle, hole_radius, origin_xy):
        step_deg = max(0.1, float(getattr(self, "corner_scale_step_deg", 1.0)))
        angle_span = float(getattr(self, "corner_scale_span_deg", 5.0))
        return kkicad.add_linear_hole_scale_at(
            group,
            center_xy,
            radial_angle,
            hole_radius,
            origin_xy,
            self.SCALE,
            step_deg,
            angle_span,
            self._add_npth_hole_at,
            self._add_grouped_silk_segment,
            self._rotate_about_xy,
        )

    def _build_offset_outline(self, group, origin_xy):
        outline_points = kgeo.outline_poly_points(self.r_out, self.n_edges) if self.n_edges != 0 else None
        return kkicad.build_offset_outline(
            self.board,
            group,
            origin_xy,
            self.r_in,
            self.r_out,
            self.n_edges,
            self.SCALE,
            outline_points,
            self._add_grouped_circle,
            self._add_grouped_segment,
            self.fpoint,
        )

    def _build_offset_mounting_holes(self, group, origin_xy):
        fp = self.mhole_db.get(self.mhs)
        fp_lib = self.fp_path + 'MountingHole.pretty' if self.fp_path else None
        ni_gnd = self.board.FindNet("gnd")
        return kkicad.build_offset_mounting_holes(
            group,
            origin_xy,
            self.mhs,
            fp_lib,
            fp,
            ni_gnd,
            self.n_mh_out,
            self.r_mh_out,
            self.n_edges,
            self.n_mh_in,
            self.r_mh_in,
            bool(getattr(self, "silk_hole_scales", False)),
            self.SCALE,
            self._iter_corner_points_for_origin,
            self._add_mounting_hole_fp_at,
            self._add_linear_hole_scale_at,
        )

    def _build_magnet_markers(self, group, origin_xy):
        return kkicad.build_magnet_markers(
            group,
            origin_xy,
            self.magnet_poles,
            self.magnet_ring_dia,
            self.magnet_rotation,
            self.magnet_shape,
            self.magnet_dia,
            self.magnet_width,
            self.magnet_height,
            self.magnet_keepout,
            self.SCALE,
            self._add_grouped_silk_circle,
            self._add_grouped_circle,
            self._add_grouped_rect_outline,
            self._get_magnet_aux_layer,
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
            kkicad.build_magnet_cross_guides(
                group,
                origin_xy,
                float(self.r_out),
                self._add_grouped_silk_segment,
            )

        summary = kpers.format_magnet_generation_summary(
            origin_xy[0],
            self.SCALE,
            self.magnet_poles,
            self.magnet_ring_dia,
            warnings,
        )
        self._update_magnet_summary(summary)

    def init_path(self):
        self.fp_path = None
        settings = pcbnew.SETTINGS_MANAGER.GetUserSettingsPath()
        try:
            env_vars = kpers.load_kicad_env_vars(settings)
            self.fp_path = kpers.first_present_value(
                env_vars,
                kpers.footprint_env_keys(self.KICAD_VERSION),
            )
        except IOError:
            kpers.log_missing_settings_file()
            return

        if self.fp_path is None:
            self.fp_path = kpers.first_present_env(
                kpers.footprint_env_keys(self.KICAD_VERSION)
            )

        if self.fp_path is not None:
            self.fp_path = kpers.normalize_dir_path(self.fp_path)
        else:
            kpers.log_missing_footprint_dir(self.KICAD_VERSION)

    def init_nets(self):
        kpers.ensure_named_nets(self.board, "gnd", "coil")

    def udpate_lset(self, n_layers):
        return kpers.layer_set_for_count(n_layers)

    def generate(self):
        self.set_status("Running")
        try:
            self.center_via_warning_count = 0
            self.get_parameters()
            validation_errors = self.validate_parameters()
            if validation_errors:
                raise ValueError("\n".join(validation_errors))

            error_msg = ksolve.validate_generate_geometry(
                self.r_coil_in,
                self.r_coil_out,
                self.n_loops,
                self.dr,
                self.trk_w,
                self.n_slots,
                self.SCALE,
            )

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
            
            kpers.refresh_board_view(self.board)

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
            kpers.refresh_board_view(self.board)

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
                    f"Coil style active: {getattr(self, 'active_coil_style_name', 'Radial')}\n"
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
        effective_mode, effective_name = self.get_effective_coil_strategy(ri, ro, n_slots, n_loops)
        self.active_coil_style_name = effective_name
        if effective_mode == 0:
            pcu0, pcu0m, pcu0mi = ksolve.parallel( ri, ro, self.dr, th0, n_loops, 0 )
            pcu1, pcu1m, pcu1mi = ksolve.parallel( ri, ro, self.dr, th0, n_loops, 1 )
        elif effective_mode == 2:
            # Keep Compact stable on the radial point-layout until the dedicated
            # compact solver path is fully validated against all tracker/routing cases.
            pcu0 = ksolve.radial( ri, ro, self.dr, th0, n_loops, 0 )
            pcu1 = ksolve.radial( ri, ro, self.dr, th0, n_loops, 1 )
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
        inner_edge = []
        center_eps = max(
            0.002,
            math.asin(min(0.95, max(float(self.trk_w), float(self.dr)) / max(float(self.r_coil_in), 1.0)))
        )
        for (x, y) in pts:
            r = math.hypot(x, y)
            # Primary target: real coil inner radius (corner region), not geometric r_min,
            # because r_min may hit the center bridge and cause mid-taps.
            if abs(r - self.r_coil_in) <= tol_inner:
                dth = self._angle_diff(math.atan2(y, x), th_center)
                row = (x, y, dth)
                inner.append(row)
                if abs(dth) > center_eps:
                    inner_edge.append(row)

        if len(inner_edge) >= 2:
            inner = inner_edge

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
        r_min = max(float(self.r_coil_in) - self.dr, 0.0)
        r_max = float(self.r_coil_out) + self.dr
        d_max = max(th_slot * 0.06, 0.008)
        via_inset = max(float(self.m_ctrlViaDia.GetValue()) * 0.60, self.SCALE * 0.04)

        def as_inset_point(radius):
            rr = max(radius - via_inset, 0.0)
            return self._as_point(rr * math.cos(th_center), rr * math.sin(th_center))

        def collect(arr):
            rows = []
            for p in arr:
                x, y = self._point_xy(p)
                r = math.hypot(x, y)
                if r < r_min or r > r_max:
                    continue
                d = abs(self._angle_diff(math.atan2(y, x), th_center))
                rows.append((d, r))
            if not rows:
                return []
            close = [row for row in rows if row[0] <= d_max]
            if close:
                return sorted(close, key=lambda c: (c[0], c[1]))
            return sorted(rows, key=lambda c: (c[0], c[1]))

        def discrete_centerline_radii(arr):
            radii = []
            merge_tol = max(self.dr * 0.20, self.SCALE * 0.05)
            for d, r in collect(arr):
                if d > d_max:
                    continue
                if not radii or abs(r - radii[-1]) > merge_tol:
                    radii.append(r)
            return radii

        cand_a = collect(arr_a)
        cand_b = collect(arr_b)
        if not cand_a or not cand_b:
            return None

        rails_a = discrete_centerline_radii(arr_a)
        rails_b = discrete_centerline_radii(arr_b)
        if rails_a and rails_b:
            same_rail_tol = max(self.dr * 0.20, self.SCALE * 0.05)
            shared = []
            for ra in rails_a:
                for rb in rails_b:
                    if abs(ra - rb) <= same_rail_tol:
                        rail_r = 0.5 * (ra + rb)
                        if not shared or abs(rail_r - shared[-1]) > same_rail_tol:
                            shared.append(rail_r)
                        break
            if shared:
                mid_r = 0.5 * (float(self.r_coil_in) + float(self.r_coil_out))
                outer_rails = [r for r in shared if r >= mid_r]
                if outer_rails:
                    outer_rails = sorted(outer_rails, reverse=True)
                    target_index = min(max(self.n_loops - 1, 0), len(outer_rails) - 1)
                    best = outer_rails[target_index]
                    return as_inset_point(best)

        # Prefer the outer bridge candidate when both inner and outer crossings exist.
        # In low-height / near-square slots the paired geometry often produces two
        # valid centerline intersections; the production-stable choice is the outer one.
        r_target = float(self.r_coil_in) + 0.62 * (float(self.r_coil_out) - float(self.r_coil_in))
        pair_limit = min(8, len(cand_a), len(cand_b))
        pair_candidates = []
        for da, ra in cand_a[:pair_limit]:
            for db, rb in cand_b[:pair_limit]:
                avg_r = 0.5 * (ra + rb)
                pair_candidates.append((
                    (da + db, abs(ra - rb), abs(avg_r - r_target), -avg_r),
                    avg_r,
                ))
        if not pair_candidates:
            return None

        valid_radii = []
        threshold = max(self.trk_w * 0.85, self.dr * 0.65, self.SCALE * 0.15)
        for _, radius in sorted(pair_candidates, key=lambda item: item[0]):
            dist_a = self._nearest_point_distance(radius, th_center, arr_a)
            dist_b = self._nearest_point_distance(radius, th_center, arr_b)
            worst = max(dist_a if dist_a is not None else 1e9, dist_b if dist_b is not None else 1e9)
            if worst <= threshold:
                valid_radii.append(radius)

        if not valid_radii:
            return None
        best = max(valid_radii)
        return as_inset_point(best)

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
        return ksolve.get_support_hole_width(self.d_support_hole, self.SCALE)

    def get_selected_terminal_od_iu(self):
        term_size = self.m_termSize.GetStringSelection() if hasattr(self, "m_termSize") else ""
        return ksolve.get_selected_terminal_od_iu(self.trmtype, self.term_db, term_size, self.SCALE)

    def estimate_safe_inner_fill_radius(self, net_name="coil"):
        """Upper bound for center fill radius to avoid touching net copper/pads."""
        safe_margin = max(self.trk_space, int(0.2 * self.SCALE))
        clearance_values = []

        for item in self.board.GetTracks():
            try:
                net = item.GetNet()
            except Exception:
                net = None
            if net is None or net.GetNetname() != net_name:
                continue

            width = item.GetWidth() if hasattr(item, "GetWidth") else self.trk_w
            points = []
            for getter in ("GetStart", "GetEnd", "GetMid"):
                if hasattr(item, getter):
                    try:
                        p = getattr(item, getter)()
                        points.append((float(p.x), float(p.y)))
                    except Exception:
                        pass
            clearance_values.extend(ksolve.track_clearance_values(points, width, safe_margin))

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
                clearance_values.append(
                    ksolve.pad_clearance_value(
                        (float(pos.x), float(pos.y)),
                        (float(size.x), float(size.y)),
                        safe_margin,
                    )
                )

        return ksolve.estimate_safe_inner_fill_radius(clearance_values)

    def hole_collides(self, position, placed_points, min_distance):
        return ksolve.hole_collides(position, placed_points, min_distance)

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
        segments = []
        for item in board.GetTracks():
            net = item.GetNet()
            if net is None or net.GetNetname() != net_name:
                continue
            segments.append({
                "length_m": item.GetLength() / self.SCALE / 1000.0,
                "width_m": item.GetWidth() / self.SCALE / 1000.0,
                "layer": item.GetLayer(),
                "width_iu": item.GetWidth(),
            })

        winding_stats = self._estimate_turns_per_layer()
        return ksolve.calculate_stats_breakdown(
            segments=segments,
            temp=temp,
            phases=self.phases,
            n_slots=self.n_slots,
            winding_mode=getattr(self, "winding_mode", "PCB"),
            wire_dia_mm=float(getattr(self, "wire_dia_mm", 0.5)),
            copper_thickness_m=float(getattr(self, "copper_thickness_m", self.tthick)),
            ring_width_iu=self.ring_w,
            front_cu_layer=pcbnew.F_Cu,
            winding_stats=winding_stats,
        )

    def calculate_stats(self, board, net_name="coil", temp=20):
        stats = self.calculate_stats_breakdown(board, net_name=net_name, temp=temp)
        return ksolve.calculate_stats(stats)

    def on_close(self, event):
        kpers.handle_close(self.pm, event, self.set_status, self._log_exception)

    def on_btn_clear(self, event):
        self.group = kpers.clear_group(self.group, self.btn_clear)
        event.Skip()

    def on_btn_generate(self, event):
        kpers.handle_action_event(
            event,
            self._run_action,
            "Started: generation running (can take 5-60 s)",
            "Finished",
            "Generation",
            self.generate,
        )

    def on_btn_generate_magnet(self, event):
        kpers.handle_action_event(
            event,
            self._run_action,
            "Started: magnet PCB generation running",
            "Magnet PCB generated",
            "Magnet PCB generation",
            self.generate_magnet_pcb,
            summary_target="magnet",
        )

    def on_btn_generate_both(self, event):
        kpers.handle_action_event(
            event,
            self._run_action,
            "Started: combined stator + magnet generation running",
            "Stator and Magnet PCB generated",
            "Combined generation",
            lambda: kpers.run_callbacks(self.generate, self.generate_magnet_pcb),
            summary_target="magnet",
        )

    def on_btn_save(self, event):
        self.set_status("Saving preset")
        try:
            config = self.to_motor_config()
            json_str = config.to_json()
            saved = kpers.save_preset_dialog(self, json_str)
            if not saved:
                self.set_status("Save cancelled")
                return
            self.set_status("Preset saved")
        except Exception as exc:
            self.set_status("Save failed")
            self._log_exception("Preset save failed", exc)

    def _apply_config_to_gui(self, config: MotorInputConfig):
        """Apply MotorInputConfig values to GUI controls."""
        try:
            # Topology
            if hasattr(self, 'm_cbScheme'):
                idx = self.m_cbScheme.FindString(config.topology.scheme)
                if idx != wx.NOT_FOUND:
                    self.m_cbScheme.SetSelection(idx)
            if hasattr(self, 'm_ctrlSlots'):
                self.m_ctrlSlots.SetValue(config.topology.slots)
            if hasattr(self, 'm_ctrlMagPolePairs'):
                self.m_ctrlMagPolePairs.SetValue(config.topology.pole_pairs)
            
            # Mechanics
            if hasattr(self, 'm_cbOutline'):
                idx = self.m_cbOutline.FindString(config.mechanics.outline_type)
                if idx != wx.NOT_FOUND:
                    self.m_cbOutline.SetSelection(idx)
            if hasattr(self, 'm_ctrlDbore'):
                self.m_ctrlDbore.SetValue(config.mechanics.shaft_bore_dia_mm)
            if hasattr(self, 'm_ctrlDout'):
                self.m_ctrlDout.SetValue(config.mechanics.outer_dia_mm)
            if hasattr(self, 'm_ctrlFilletRadius'):
                self.m_ctrlFilletRadius.SetValue(config.mechanics.corner_fillet_mm)
            if hasattr(self, 'm_ctrlWmnt'):
                self.m_ctrlWmnt.SetValue(config.mechanics.annular_width_mm)
            if hasattr(self, 'm_cbMountSize'):
                idx = self.m_cbMountSize.FindString(config.mechanics.mount_size)
                if idx != wx.NOT_FOUND:
                    self.m_cbMountSize.SetSelection(idx)
            if hasattr(self, 'm_mhOut'):
                self.m_mhOut.SetValue(config.mechanics.mount_out_count)
            if hasattr(self, 'm_mhOutR'):
                self.m_mhOutR.SetValue(config.mechanics.mount_out_dia_mm)
            if hasattr(self, 'm_mhIn'):
                self.m_mhIn.SetValue(config.mechanics.mount_in_count)
            if hasattr(self, 'm_mhInR'):
                self.m_mhInR.SetValue(config.mechanics.mount_in_dia_mm)
            if hasattr(self, 'm_ctrlCornerHoleCount'):
                self.m_ctrlCornerHoleCount.SetValue(config.mechanics.corner_hole_count)
            if hasattr(self, 'm_ctrlCornerHoleDia'):
                self.m_ctrlCornerHoleDia.SetValue(config.mechanics.corner_hole_dia_mm)
            if hasattr(self, 'm_ctrlCornerHoleOffset'):
                self.m_ctrlCornerHoleOffset.SetValue(config.mechanics.corner_hole_offset_mm)
            
            # Coil
            if hasattr(self, 'm_cbWindingMode'):
                idx = self.m_cbWindingMode.FindString(config.coil.winding_mode)
                if idx != wx.NOT_FOUND:
                    self.m_cbWindingMode.SetSelection(idx)
            if hasattr(self, 'm_cbStrategy'):
                strategy_map = {"Parallel": 0, "Radial": 1, "Compact": 2}
                self.m_cbStrategy.SetSelection(strategy_map.get(config.coil.strategy, 1))
            if hasattr(self, 'm_chkMaxSpec'):
                self.m_chkMaxSpec.SetValue(config.coil.max_spec_layout)
            if hasattr(self, 'm_ctrlLoops'):
                self.m_ctrlLoops.SetValue(config.coil.turns_per_layer)
            if hasattr(self, 'm_ctrlDin'):
                self.m_ctrlDin.SetValue(config.coil.inner_dia_mm)
            if hasattr(self, 'm_ctrlDend'):
                self.m_ctrlDend.SetValue(config.coil.outer_dia_mm)
            if hasattr(self, 'm_ctrlTrackWidth'):
                self.m_ctrlTrackWidth.SetValue(config.coil.track_width_mm)
            if hasattr(self, 'm_ctrlTrackSpacing'):
                self.m_ctrlTrackSpacing.SetValue(config.coil.track_spacing_mm)
            if hasattr(self, 'm_ctrlRfill'):
                self.m_ctrlRfill.SetValue(config.coil.track_fillet_mm)
            if hasattr(self, 'm_ctrlWireDia') and config.coil.wire_dia_mm:
                self.m_ctrlWireDia.SetValue(config.coil.wire_dia_mm)
            
            # Stack
            if hasattr(self, 'm_ctrlLayers'):
                self.m_ctrlLayers.SetValue(config.stack.layers)
            if hasattr(self, 'm_cbCopperWeight'):
                idx = self.m_cbCopperWeight.FindString(config.stack.copper_weight)
                if idx != wx.NOT_FOUND:
                    self.m_cbCopperWeight.SetSelection(idx)
            if hasattr(self, 'm_ctrlViaDia'):
                self.m_ctrlViaDia.SetValue(config.stack.via_dia_mm)
            if hasattr(self, 'm_ctrlViaDrill'):
                self.m_ctrlViaDrill.SetValue(config.stack.via_drill_mm)
            if hasattr(self, 'm_cbSupportViaMode'):
                idx = self.m_cbSupportViaMode.FindString(str(config.stack.support_via_mode))
                if idx != wx.NOT_FOUND:
                    self.m_cbSupportViaMode.SetSelection(idx)
            if hasattr(self, 'm_ctrlSupportHoleDia'):
                self.m_ctrlSupportHoleDia.SetValue(config.stack.support_hole_dia_mm)
            if hasattr(self, 'm_ctrlRingWidth'):
                self.m_ctrlRingWidth.SetValue(config.stack.ring_width_mm)
            if hasattr(self, 'm_ctrlRingSpacing'):
                self.m_ctrlRingSpacing.SetValue(config.stack.ring_spacing_mm)
            if hasattr(self, 'm_cbFillInnerGND'):
                self.m_cbFillInnerGND.SetValue(config.stack.fill_inner_gnd)
            if hasattr(self, 'm_ctrlInnerGndDia'):
                self.m_ctrlInnerGndDia.SetValue(config.stack.inner_gnd_dia_mm)
            if hasattr(self, 'm_cbFillOuterGND'):
                self.m_cbFillOuterGND.SetValue(config.stack.fill_outer_gnd)
            
            # Rotor
            if hasattr(self, 'm_cbMagShape'):
                idx = self.m_cbMagShape.FindString(config.rotor.shape)
                if idx != wx.NOT_FOUND:
                    self.m_cbMagShape.SetSelection(idx)
            if hasattr(self, 'm_ctrlMagRingDia'):
                self.m_ctrlMagRingDia.SetValue(config.rotor.ring_dia_mm)
            if hasattr(self, 'm_ctrlMagRotation'):
                self.m_ctrlMagRotation.SetValue(config.rotor.rotation_offset_deg)
            if hasattr(self, 'm_ctrlMagDia') and config.rotor.dia_mm:
                self.m_ctrlMagDia.SetValue(config.rotor.dia_mm)
            if hasattr(self, 'm_ctrlMagWidth') and config.rotor.width_mm:
                self.m_ctrlMagWidth.SetValue(config.rotor.width_mm)
            if hasattr(self, 'm_ctrlMagHeight') and config.rotor.height_mm:
                self.m_ctrlMagHeight.SetValue(config.rotor.height_mm)
            if hasattr(self, 'm_ctrlMagLength'):
                self.m_ctrlMagLength.SetValue(config.rotor.length_mm or 0.0)
            if hasattr(self, 'm_ctrlMagGap'):
                self.m_ctrlMagGap.SetValue(config.rotor.gap_mm)
            if hasattr(self, 'm_ctrlMagKeepout'):
                self.m_ctrlMagKeepout.SetValue(config.rotor.keepout_mm)
            if hasattr(self, 'm_ctrlMagBest'):
                self.m_ctrlMagBest.SetValue(config.rotor.b_gap_est_tesla)
            
            # Peripherals
            if hasattr(self, 'm_cbTP'):
                idx = self.m_cbTP.FindString(config.peripherals.term_type)
                if idx != wx.NOT_FOUND:
                    self.m_cbTP.SetSelection(idx)
            if hasattr(self, 'm_ctrlDterm'):
                self.m_ctrlDterm.SetValue(config.peripherals.term_offset_mm)
            if hasattr(self, 'm_cbSilkCross'):
                self.m_cbSilkCross.SetValue(config.peripherals.silk_cross_guides)
            if hasattr(self, 'm_cbSilkSlots'):
                self.m_cbSilkSlots.SetValue(config.peripherals.silk_slot_frames)
            if hasattr(self, 'm_cbSilkDeg'):
                self.m_cbSilkDeg.SetValue(config.peripherals.silk_degree_scale)
            if hasattr(self, 'm_cbSilkHoleScale'):
                self.m_cbSilkHoleScale.SetValue(config.peripherals.silk_hole_scales)
            if hasattr(self, 'm_ctrlCornerScaleStep'):
                self.m_ctrlCornerScaleStep.SetValue(config.peripherals.corner_scale_step_deg)
            if hasattr(self, 'm_ctrlCornerScaleSpan'):
                self.m_ctrlCornerScaleSpan.SetValue(config.peripherals.corner_scale_span_deg)
            
            # Trigger dependent UI updates after value restore.
            callbacks = [
                self.on_cb_outline,
                self.on_cb_trmtype,
                self.on_cb_winding_mode,
                self.on_cb_magnet_shape,
            ]
            if hasattr(self, 'on_nr_layers'):
                callbacks.append(self.on_nr_layers)
            kpers.run_event_callbacks(*callbacks)
                
        except Exception as exc:
            self._log_exception("Apply config to GUI failed", exc)

    def on_btn_load(self, event):
        self.set_status("Loading preset")
        try:
            load_info = kpers.choose_preset_to_load(self)
            if not load_info:
                self.set_status("Load cancelled")
                return
            origin, directory = load_info

            if origin.lower().endswith('.json'):
                config = kpers.load_json_preset(origin, MotorInputConfig)
                self._apply_config_to_gui(config)
            else:
                kpers.load_legacy_preset(origin, directory, self.pf, self.pm, self)
                kpers.run_event_callbacks(
                    self.on_cb_outline,
                    self.on_cb_trmtype,
                    self.on_cb_winding_mode,
                    self.on_cb_magnet_shape,
                )

            self.set_status("Preset loaded")
        except Exception as exc:
            self.set_status("Load failed")
            self._log_exception("Preset load failed", exc)

    def on_cb_preset(self, event):
        return kpers.handle_preset_event(
            event,
            getattr(self, "m_cbPreset", None),
            self._apply_pcb_preset,
            self.set_status,
        )

    def on_cb_outline(self, event):
        return kpers.handle_outline_event(
            self.m_cbOutline.GetStringSelection(),
            self.m_ctrlDout,
            self.m_ctrlFilletRadius,
            event,
        )

    def on_cb_trmtype(self, event):
        return kpers.handle_terminal_type_event(
            self.m_cbTP.GetStringSelection(),
            self.term_db,
            self.m_termSize,
            event,
        )

    def on_cb_winding_mode(self, event):
        mode = self.m_cbWindingMode.GetStringSelection() if hasattr(self, "m_cbWindingMode") else "PCB"
        return kpers.handle_winding_mode_event(
            mode,
            (self.lbl_copperWeight, self.m_cbCopperWeight),
            (self.lbl_wireDia, self.m_ctrlWireDia, self.lbl_wireDiaUnit),
            event,
        )

    def on_cb_magnet_shape(self, event):
        shape = self.m_cbMagShape.GetStringSelection() if hasattr(self, "m_cbMagShape") else "Round"
        return kpers.handle_magnet_shape_event(
            shape,
            (self.lbl_magDia, self.m_ctrlMagDia, self.lbl_magDiaUnit),
            (
                self.lbl_magWidth, self.m_ctrlMagWidth, self.lbl_magWidthUnit,
                self.lbl_magHeight, self.m_ctrlMagHeight, self.lbl_magHeightUnit,
            ),
            self._update_magnet_summary,
            event,
        )

    def on_cb_mholes(self, event):
        return kpers.skip_event(event)

    def on_nr_layers(self, event):
        self.n_layers = kpers.read_layer_count(self.m_ctrlLayers)
        return kpers.skip_event(event)
