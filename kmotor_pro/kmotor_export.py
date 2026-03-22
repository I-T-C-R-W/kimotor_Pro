# kmotor_export.py
# Export functionality for KMotor_Pro (SVG, DXF)
# Generated during Phase 5 refactoring

import math
import numpy as np
from typing import List, Tuple, Optional


def coils_to_svg_paths(coil_points: np.ndarray, scale: float = 1.0) -> str:
    """Convert coil points to SVG path data.
    
    Args:
        coil_points: Nx2 or Nx3 array of points
        scale: Scale factor for coordinates
        
    Returns:
        SVG path 'd' attribute string
    """
    if coil_points is None or len(coil_points) == 0:
        return ""
    
    # Extract x,y coordinates
    pts = coil_points[:, :2] if coil_points.shape[1] >= 2 else coil_points
    
    # Scale points
    pts = pts * scale
    
    # Build SVG path
    path_parts = []
    for i, pt in enumerate(pts):
        x, y = pt[0], pt[1]
        if i == 0:
            path_parts.append(f"M {x:.3f} {y:.3f}")
        else:
            path_parts.append(f"L {x:.3f} {y:.3f}")
    
    return " ".join(path_parts)


def generate_svg(
    coil_paths: List[str],
    width_mm: float,
    height_mm: float,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_color: str = "#FF0000",
    stroke_width: float = 0.1,
    background_color: str = "#FFFFFF"
) -> str:
    """Generate complete SVG document.
    
    Args:
        coil_paths: List of SVG path 'd' strings
        width_mm: Document width in mm
        height_mm: Document height in mm
        center_x: Center X offset
        center_y: Center Y offset
        stroke_color: Path stroke color
        stroke_width: Path stroke width in mm
        background_color: Background color
        
    Returns:
        Complete SVG document as string
    """
    # Calculate viewBox
    viewbox_x = -width_mm / 2 + center_x
    viewbox_y = -height_mm / 2 + center_y
    viewbox = f"{viewbox_x:.3f} {viewbox_y:.3f} {width_mm:.3f} {height_mm:.3f}"
    
    # Build paths
    paths_str = ""
    for path_d in coil_paths:
        if path_d:
            paths_str += f'    <path d="{path_d}" fill="none" stroke="{stroke_color}" stroke-width="{stroke_width}" />\n'
    
    # Build SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{width_mm}mm" height="{height_mm}mm" 
     viewBox="{viewbox}">
  <rect x="{viewbox_x}" y="{viewbox_y}" width="{width_mm}" height="{height_mm}" fill="{background_color}" />
  <g transform="scale(1, -1)">
{paths_str}  </g>
</svg>
'''
    return svg


def export_motor_svg(
    coil_points_list: List[np.ndarray],
    outer_radius: float,
    inner_radius: float,
    output_path: str,
    scale: float = 1.0
) -> bool:
    """Export motor coil geometry to SVG file.
    
    Args:
        coil_points_list: List of coil point arrays
        outer_radius: Outer motor radius
        inner_radius: Inner motor radius (shaft bore)
        output_path: Output file path
        scale: Scale factor (default 1.0 for mm)
        
    Returns:
        True if successful
    """
    try:
        # Convert coils to SVG paths
        paths = []
        for coil_pts in coil_points_list:
            if coil_pts is not None and len(coil_pts) > 0:
                path_d = coils_to_svg_paths(coil_pts, scale)
                if path_d:
                    paths.append(path_d)
        
        # Calculate document size
        size = 2.0 * outer_radius * scale * 1.1  # 10% margin
        
        # Generate SVG
        svg_content = generate_svg(
            coil_paths=paths,
            width_mm=size,
            height_mm=size,
            stroke_color="#CC0000",
            stroke_width=0.15
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        return True
        
    except Exception as e:
        print(f"SVG export failed: {e}")
        return False


def calculate_winding_length(
    coil_points: np.ndarray,
    copper_thickness_m: float = 35e-6,
    track_width_m: float = 0.00015
) -> dict:
    """Calculate winding length and resistance from coil points.
    
    Args:
        coil_points: Nx2 or Nx3 array of coil points
        copper_thickness_m: Copper thickness in meters (default 35um)
        track_width_m: Track width in meters (default 0.15mm)
        
    Returns:
        Dictionary with length_m, resistance_ohm, area_m2
    """
    if coil_points is None or len(coil_points) < 2:
        return {"length_m": 0.0, "resistance_ohm": 0.0, "area_m2": 0.0}
    
    # Calculate total length
    pts = coil_points[:, :2] if coil_points.shape[1] >= 2 else coil_points
    total_length = 0.0
    
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i-1][0]
        dy = pts[i][1] - pts[i-1][1]
        total_length += math.sqrt(dx*dx + dy*dy)
    
    # Convert to meters (assuming input in IU, need to know scale)
    # For now, assume input is already in mm
    length_m = total_length / 1000.0
    
    # Calculate cross-section area
    area_m2 = copper_thickness_m * track_width_m
    
    # Calculate resistance (copper resistivity at 20°C)
    rho_copper = 1.68e-8  # Ohm*meter
    resistance = rho_copper * length_m / max(area_m2, 1e-12)
    
    return {
        "length_m": length_m,
        "length_mm": length_m * 1000.0,
        "resistance_ohm": resistance,
        "area_m2": area_m2
    }
# Methods for export



    def __init__(self,  parent, board):
        kmotor_gui.KMotorProGUI.__init__(self, parent)

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



    def _radial_vector(self, angle, radius=1.0):
        return np.array([radius * math.cos(angle), radius * math.sin(angle)])



    def _tangent_vector(self, angle, scale=1.0):
        return np.array([-scale * math.sin(angle), scale * math.cos(angle)])



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



    def _get_board_span(self):
        return 2.0 * float(self.r_out)



    def _get_magnet_board_origin(self):
        span = self._get_board_span()
        return (span * 1.1, 0.0)



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



    def _get_magnet_aux_layer(self):
        return getattr(pcbnew, "Dwgs_User", pcbnew.F_SilkS)



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
        self.max_spec = bool(self.m_chkMaxSpec.GetValue()) if hasattr(self, "m_chkMaxSpec") else False

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



    def get_effective_coil_strategy(self, ri, ro, n_slots, n_loops):
        radial_available = max(ro - ri, 0.0)
        radial_required = max(n_loops * self.dr + self.trk_w, self.dr)
        slot_pitch = (2.0 * math.pi) / max(n_slots, 1)
        mean_radius = max(0.5 * (ri + ro), 1.0)
        tangential_span = max(mean_radius * slot_pitch, 1.0)
        aspect = float(radial_available) / float(tangential_span)

        selected = int(getattr(self, "strategy", 1))
        if selected == 2:
            return 2, "Compact"

        if getattr(self, "max_spec", False):
            dense_fill = radial_required >= radial_available * 0.82
            near_square = aspect <= 0.34
            if dense_fill or near_square:
                return 2, "Compact"

        if selected == 0:
            return 0, "Parallel"
        return 1, "Radial"



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



    def coil_tracker(self, mpt, layer, n_loops, group, is_first_layer=False, is_last_layer=False, is_ccw=False):
        """
        Zeichnet die Spule und liefert die zwei expliziten Ecke-Anker.
        Auf den Terminal-Layern wird der innere Stummel gezielt entfernt.
        """



    def _angle_diff(self, a, b):
        d = a - b
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        return d


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



    def hole_collides(self, position, placed_points, min_distance):
        for pt in placed_points:
            if math.hypot(pt.x - position.x, pt.y - position.y) < min_distance:
                return True
        return False

    # =========================================================================
    # PROFESSIONELLES ROUTING: 4 Anchor-Pins, Radial-Lines, Keine Kreuzungen
    # =========================================================================



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

