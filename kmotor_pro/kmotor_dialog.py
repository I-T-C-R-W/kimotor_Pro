# -*- coding: utf-8 -*-
# kmotor_dialog.py - Zentrale Dialog-Klasse für KMotor_Pro
# Diese Klasse erbt von KMotorProGUI und importiert alle benötigten Methoden

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

from . import kmotor_gui
from . import kmotor_solvermath as kla
from . import kmotor_solver as ksolve
from . import kmotor_persist as kpers
from .kmotor_models import (
    MotorInputConfig,
    TopologyConfig,
    StatorMechanicsConfig,
    CoilLayoutConfig,
    StackPcbConfig,
    RotorMagnetConfig,
    PeripheralsConfig,
)


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



    def _clear_generated_corner_holes(self):
        for fp in list(self.board.GetFootprints()):
            ref = fp.GetReferenceAsString() if hasattr(fp, "GetReferenceAsString") else ""
            if ref.startswith("KMH_"):
                self.board.RemoveNative(fp)



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



    def build_slot_anchors(self, tcw, tccw, th_center):
        # Deterministically pick the two inner coil corners (left/right of slot centerline).
        raw_pts = {}



    def build_slot_center_via(self, arr_a, arr_b, th_center, th_slot):
        # Pick a deterministic centerline point for the inter-layer via and verify
        # that it can actually bridge both coil halves.
        r_min = max(float(self.r_coil_in) - self.dr, 0.0)
        r_max = float(self.r_coil_out) + self.dr
        d_max = max(th_slot * 0.06, 0.008)
        via_inset = max(float(self.m_ctrlViaDia.GetValue()) * 0.60, self.SCALE * 0.04)


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



class KMotorProDialog(kmotor_gui.KMotorProGUI):
    """Zentrale Dialog-Klasse, die GUI und Logik verbindet."""
    
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

    tthick = 35e-6
    COPPER_WEIGHT_TO_THICKNESS_M = {
        "0.5 oz / 18um": 18e-6,
        "1 oz / 35um": 35e-6,
        "2 oz / 70um": 70e-6,
        "3 oz / 105um": 105e-6,
    }
    
    # Importiere alle Methoden aus kmotor_api
    from .kmotor_api import (
        _tag_generated_zone,
        _is_generated_zone,
        _cleanup_generated_zones,
        _clear_generated_corner_holes,
        _build_magnet_markers,
        generate,
        do_coils,
        build_slot_anchors,
        build_slot_center_via,
        do_professional_routing,
        do_outline,
        do_mounting_holes,
        do_thermal_zones,
        do_silkscreen,
        fillet,
        calculate_stats_breakdown,
        calculate_stats,
        coil_tracker,
        add_through_via,
        add_custom_through_via,
        add_support_hole,
        get_support_hole_width,
        get_selected_terminal_od_iu,
        estimate_safe_inner_fill_radius,
        hole_collides,
        generate_magnet_pcb,
        init_path,
        init_nets,
        udpate_lset,
        get_parameters,
        get_magnet_parameters,
        validate_parameters,
        validate_magnet_parameters,
        estimate_motor_constants,
        estimate_winding_factor,
        estimate_performance_stats,
        estimate_model_warnings,
        get_effective_coil_strategy,
        _effective_winding_layers,
        _winding_pitch_mm,
        _estimate_turns_per_layer,
        _update_magnet_summary,
        _get_mounting_hole_dia,
        _iter_magnet_clearance_targets,
        _angle_delta,
        _nearest_magnet_angle_delta,
        _clear_magnet_group,
        _create_magnet_group,
        _add_mounting_hole_fp_at,
        _iter_corner_points_for_origin,
        _add_linear_hole_scale_at,
        _build_offset_outline,
        _build_offset_mounting_holes,
    )

    def __init__(self, parent, board):
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

    def init_persist(self, configFile):
        self.pm = PM.PersistenceManager.Get()
        self.pm.SetPersistenceFile(configFile)
        self.pm.RegisterAndRestoreAll(self)

    def eda_angle(self, angle):
        if self.KICAD_VERSION < 7:
            return angle * 180 / math.pi * 100
        else:
            return pcbnew.EDA_ANGLE(angle, pcbnew.RADIANS_T)

    def _point_xy(self, pt):
        if hasattr(pt, "x") and hasattr(pt, "y"):
            return float(pt.x), float(pt.y)
        try:
            return float(pt[0, 0]), float(pt[0, 1])
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

    def _angle_diff(self, a, b):
        d = a - b
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        return d

    def _outline_poly_points(self, r, n_edge):
        if n_edge < 4:
            return None
        rp = r / math.cos(math.pi / n_edge)
        thp = 2 * math.pi / n_edge
        tho = thp / 2
        pts = []
        for i in range(n_edge):
            pts.append(self.fpoint(
                int(rp * math.cos(i * thp + tho)),
                int(rp * math.sin(i * thp + tho))
            ))
        return pts

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
            config = self.to_motor_config()
            json_str = config.to_json()
            
            with wx.FileDialog(self, "Save KMotor_Pro preset", 
                           wildcard="JSON files (*.json)|*.json|KMT files (*.kmt)|*.kmt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                fileDialog.SetFilename("kmotor_pro.json")
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    self.set_status("Save cancelled")
                    return
                target = fileDialog.GetPath()
                
                with open(target, 'w', encoding='utf-8') as f:
                    f.write(json_str)
            
            self.set_status("Preset saved")
        except Exception as exc:
            self.set_status("Save failed")
            self._log_exception("Preset save failed", exc)

    def on_btn_load(self, event):
        self.set_status("Loading preset")
        try:
            with wx.FileDialog(self, "Load KMotor_Pro preset", 
                           wildcard="JSON files (*.json)|*.json|KMT files (*.kmt)|*.kmt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    self.set_status("Load cancelled")
                    return
                origin = fileDialog.GetPath()
                
                if origin.lower().endswith('.json'):
                    with open(origin, 'r', encoding='utf-8') as f:
                        json_str = f.read()
                    config = MotorInputConfig.from_json(json_str)
                    self._apply_config_to_gui(config)
                else:
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
            self.set_status("Load failed")
            self._log_exception("Preset load failed", exc)

    def on_cb_preset(self, event):
        if not hasattr(self, "m_cbPreset"):
            if event is not None:
                event.Skip()
            return
        preset_name = self.m_cbPreset.GetStringSelection()
        applied = self._apply_pcb_preset(preset_name)
        if applied:
            self.set_status(f"Preset applied: {preset_name}")
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
            for i, k in enumerate(keys):
                self.m_termSize.SetString(i, k)
            while len(keys) < self.m_termSize.GetCount():
                self.m_termSize.Delete(self.m_termSize.GetCount() - 1)
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
        if event is not None:
            event.Skip()

    def to_motor_config(self) -> MotorInputConfig:
        """Convert GUI parameters to MotorInputConfig."""
        self.get_parameters()
        if hasattr(self, 'm_cbMagShape'):
            self.get_magnet_parameters()
        
        outline_map = {
            "Circle": "Circle",
            "Square": "Square", 
            "Hexagon": "Hexagon",
            "Octagon": "Octagon",
            "None": "None"
        }
        outline_type = outline_map.get(self.outline, "Circle")
        
        scheme = self.m_cbScheme.GetStringSelection() if hasattr(self, 'm_cbScheme') else "3P"
        if scheme == "1P":
            phases = 1
        elif scheme == "3P+N":
            phases = 3
        else:
            phases = 3
        
        winding_mode = getattr(self, 'winding_mode', 'PCB')
        strategy_map = {0: "Parallel", 1: "Radial", 2: "Compact"}
        strategy = strategy_map.get(getattr(self, 'strategy', 1), "Radial")
        magnet_shape = getattr(self, 'magnet_shape', 'round').capitalize()
        term_type = getattr(self, 'trmtype', 'THT')
        copper_weight = getattr(self, 'copper_weight', '1 oz / 35um')
        mount_size = getattr(self, 'mhs', 'M3')
        
        config = MotorInputConfig(
            topology=TopologyConfig(
                scheme=scheme,
                phases=phases,
                slots=self.n_slots,
                pole_pairs=getattr(self, 'magnet_pole_pairs', 30)
            ),
            mechanics=StatorMechanicsConfig(
                outline_type=outline_type,
                shaft_bore_dia_mm=self.r_in * 2 / self.SCALE,
                outer_dia_mm=self.r_out * 2 / self.SCALE,
                corner_fillet_mm=self.o_fill / self.SCALE if hasattr(self, 'o_fill') else 0.0,
                annular_width_mm=self.w_mnt / self.SCALE,
                mount_size=mount_size,
                mount_out_count=self.n_mh_out,
                mount_out_dia_mm=self.r_mh_out * 2 / self.SCALE,
                mount_in_count=self.n_mh_in,
                mount_in_dia_mm=self.r_mh_in * 2 / self.SCALE,
                corner_hole_count=getattr(self, 'corner_hole_count', 4),
                corner_hole_dia_mm=getattr(self, 'corner_hole_dia', 0.0) / self.SCALE,
                corner_hole_offset_mm=getattr(self, 'corner_hole_offset', 0.0) / self.SCALE
            ),
            coil=CoilLayoutConfig(
                winding_mode=winding_mode,
                strategy=strategy,
                max_spec_layout=getattr(self, 'max_spec', False),
                turns_per_layer=self.n_loops,
                inner_dia_mm=self.r_coil_in * 2 / self.SCALE,
                outer_dia_mm=self.r_coil_out * 2 / self.SCALE,
                track_width_mm=self.trk_w / self.SCALE,
                track_spacing_mm=self.trk_space / self.SCALE,
                track_fillet_mm=self.r_fill / self.SCALE if hasattr(self, 'r_fill') else 0.0,
                wire_dia_mm=getattr(self, 'wire_dia_mm', 0.50) if winding_mode == "Wire" else None
            ),
            stack=StackPcbConfig(
                layers=self.n_layers,
                copper_weight=copper_weight,
                via_dia_mm=self.d_via / self.SCALE,
                via_drill_mm=self.d_drill / self.SCALE,
                support_via_mode=getattr(self, 'support_via_mode', 2),
                support_hole_dia_mm=self.d_support_hole / self.SCALE,
                ring_width_mm=self.ring_w / self.SCALE,
                ring_spacing_mm=self.ring_space / self.SCALE,
                fill_inner_gnd=getattr(self, 'fill_inner_gnd', True),
                inner_gnd_dia_mm=getattr(self, 'inner_fill_dia', 0) / self.SCALE,
                fill_outer_gnd=getattr(self, 'fill_outer_gnd', True)
            ),
            rotor=RotorMagnetConfig(
                shape=magnet_shape,
                ring_dia_mm=getattr(self, 'magnet_ring_dia', 0.0) / self.SCALE,
                rotation_offset_deg=getattr(self, 'magnet_rotation', 0.0),
                dia_mm=getattr(self, 'magnet_dia', 0.0) / self.SCALE if magnet_shape == "Round" else None,
                width_mm=getattr(self, 'magnet_width', 0.0) / self.SCALE if magnet_shape == "Rect" else None,
                height_mm=getattr(self, 'magnet_height', 0.0) / self.SCALE if magnet_shape == "Rect" else None,
                length_mm=getattr(self, 'magnet_length', 0.0) / self.SCALE,
                gap_mm=getattr(self, 'magnet_gap', 0.0) / self.SCALE,
                keepout_mm=getattr(self, 'magnet_keepout', 0.0) / self.SCALE,
                b_gap_est_tesla=getattr(self, 'magnet_b_est', 0.60)
            ),
            peripherals=PeripheralsConfig(
                term_type=term_type,
                term_size=self.m_termSize.GetStringSelection() if hasattr(self, 'm_termSize') else "1.0",
                term_offset_mm=self.term_offset / self.SCALE,
                silk_cross_guides=getattr(self, 'silk_cross_guides', False),
                silk_slot_frames=getattr(self, 'silk_slot_frames', False),
                silk_degree_scale=getattr(self, 'silk_deg_scale', False),
                silk_hole_scales=getattr(self, 'silk_hole_scales', False),
                corner_scale_step_deg=getattr(self, 'corner_scale_step_deg', 1.0),
                corner_scale_span_deg=getattr(self, 'corner_scale_span_deg', 5.0)
            )
        )
        
        return config

    def _apply_config_to_gui(self, config: MotorInputConfig):
        """Apply MotorInputConfig values to GUI controls."""
        try:
            if hasattr(self, 'm_cbScheme'):
                idx = self.m_cbScheme.FindString(config.topology.scheme)
                if idx != wx.NOT_FOUND:
                    self.m_cbScheme.SetSelection(idx)
            if hasattr(self, 'm_ctrlSlots'):
                self.m_ctrlSlots.SetValue(config.topology.slots)
            if hasattr(self, 'm_ctrlMagPolePairs'):
                self.m_ctrlMagPolePairs.SetValue(config.topology.pole_pairs)
            
            if hasattr(self, 'm_cbOutline'):
                idx = self.m_cbOutline.FindString(config.mechanics.outline_type)
                if idx != wx.NOT_FOUND:
                    self.m_cbOutline.SetSelection(idx)
            if hasattr(self, 'm_ctrlDbore'):
                self.m_ctrlDbore.SetValue(config.mechanics.shaft_bore_dia_mm)
            if hasattr(self, 'm_ctrlDout'):
                self.m_ctrlDout.SetValue(config.mechanics.outer_dia_mm)
            
            if hasattr(self, 'm_cbWindingMode'):
                idx = self.m_cbWindingMode.FindString(config.coil.winding_mode)
                if idx != wx.NOT_FOUND:
                    self.m_cbWindingMode.SetSelection(idx)
            if hasattr(self, 'm_ctrlLoops'):
                self.m_ctrlLoops.SetValue(config.coil.turns_per_layer)
            if hasattr(self, 'm_ctrlTrackWidth'):
                self.m_ctrlTrackWidth.SetValue(config.coil.track_width_mm)
            
            if hasattr(self, 'm_ctrlLayers'):
                self.m_ctrlLayers.SetValue(config.stack.layers)
            if hasattr(self, 'm_ctrlViaDia'):
                self.m_ctrlViaDia.SetValue(config.stack.via_dia_mm)
            
            self.on_cb_outline(None)
            self.on_cb_trmtype(None)
            self.on_cb_winding_mode(None)
            self.on_cb_magnet_shape(None)
            if hasattr(self, 'on_nr_layers'):
                self.on_nr_layers(None)
                
        except Exception as exc:
            self._log_exception("Apply config to GUI failed", exc)