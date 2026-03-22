# kmotor_api.py
# Central orchestration layer for KMotor_Pro
# Generated during Phase 1 refactoring

import os
import pcbnew
import wx


class KMotorProPlugin(pcbnew.ActionPlugin):
    """KiCad Plugin Entry Point for KMotor_Pro."""

    def defaults(self):
        self.name = "KMotor_Pro"
        self.category = "Modify Drawing PCB"
        self.description = "KMotor_Pro - Parametric PCB motor generator for KiCad"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'kmotor_pro_24x24.png')

    def Run(self):
        from .kmotor_gui import KMotorProGUI
        self.frame = wx.FindWindowByName("PcbFrame")
        self.board = pcbnew.GetBoard()
        dlg = KMotorProGUI(self.frame)
        dlg.SetIcon(wx.Icon(self.icon_file_name))
        dlg.Show()
# Methods for api



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

