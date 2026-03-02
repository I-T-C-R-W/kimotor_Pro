# Copyright 2022 Stefano Cottafavi <stefano.cottafavi@gmail.com>
# SPDX-License-Identifier: GPL-2.0-only

import os
import shutil
import numpy as np
import math
import json
import traceback
from datetime import datetime

import wx
import wx.lib.agw.persist.persistencemanager as PM
import pcbnew

if __name__ == '__main__':
    import kimotor_gui
    import kimotor_linalg as kla
else:
    from . import kimotor_gui
    from . import kimotor_linalg as kla
    from . import kimotor_solver as ksolve
    from . import kimotor_persist as kpers

class KiMotor(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "KiMotor"
        self.category = "Modify Drawing PCB"
        self.description = "KiMotor - Parametric PCB motor design"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'kimotor_24x24.png')
    def Run( self ):
        self.frame = wx.FindWindowByName("PcbFrame")
        self.board = pcbnew.GetBoard()
        dlg = KiMotorDialog(self.frame, self.board)
        dlg.SetIcon( wx.Icon(self.icon_file_name) )
        dlg.Show()

class KiMotorDialog ( kimotor_gui.KiMotorGUI ):

    group = None
    SCALE = 0
    KICAD_VERSION = 0

    tl = 0
    tr = 0

    outline = None
    trmtype = None
    fpoint = None
    angle = None

    tthick = 35e-6 # [m] copper thickness (1oz layer specs)

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
        kimotor_gui.KiMotorGUI.__init__(self, parent)

        self.board = board
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
            "kimotor.cfg"
        )

        self.init_persist(self.pf)
        self.init_path()
        self.init_nets()
        self.on_cb_outline(None)
        self.on_cb_trmtype(None)
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
            self.fill_inner_gnd = bool(self.m_cbFillInnerGND.GetValue())
        elif hasattr(self, "m_chkFillInnerGnd"):
            self.fill_inner_gnd = bool(self.m_chkFillInnerGnd.GetValue())
        else:
            self.fill_inner_gnd = True

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

    def set_status(self, text):
        ts = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, "lbl_status") and self.lbl_status:
            self.lbl_status.SetLabel(str(text))
            self.lbl_status.GetParent().Layout()
        if hasattr(self, "m_txtStatus") and self.m_txtStatus:
            self.m_txtStatus.SetValue(f"[{ts}] {text}")

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

    def init_path(self):
        self.fp_path = None
        settings = pcbnew.SETTINGS_MANAGER.GetUserSettingsPath()
        try:
            with open(settings+'/kicad_common.json', 'r') as f:
                data = json.load(f)
                if not (data["environment"]["vars"] is None) and "KICAD6_FOOTPRINT_DIR" in data["environment"]["vars"]:
                    self.fp_path = data["environment"]["vars"]["KICAD6_FOOTPRINT_DIR"]
        except IOError:
            wx.LogError("Settings file not found.")
            return

        if self.fp_path is None:
            self.fp_path = os.getenv("KICAD"+str(self.KICAD_VERSION)+"_FOOTPRINT_DIR", default=None)

        if self.fp_path is not None:
            self.fp_path = os.path.normpath(self.fp_path) + os.sep
        else:
            wx.LogError("Footprint library not found.")

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
                    "Geometrie Konflikt (KiMotor)",
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
                
                cri_thermal = lowest_used_radius - self.trk_space - self.d_via/2.0
                self.do_thermal_zones(
                    self.r_out,
                    cri_thermal,
                    fill_inner_area_gnd=self.fill_inner_gnd)
            
            self.do_silkscreen(self.r_coil_out + self.trk_w, self.r_coil_in, self.th0)

            if hasattr(self.board, 'BuildConnectivity'):
                self.board.BuildConnectivity()
                
            pcbnew.Refresh()
            try:
                pcbnew.UpdateUserInterface()
            except AttributeError:
                pass

            temp = self.m_ambT.GetValue()
            stats = self.calculate_stats_breakdown(self.board, net_name="coil", temp=temp)
            self.tl = stats["phase_len_mm"]
            self.tr = stats["phase_r_temp"]

            self.lbl_phaseLength.SetLabel('%.2f' % self.tl)
            self.lbl_phaseR.SetLabel('%.3f' % self.tr)
            self.lbl_totalR.SetLabel('%.3f' % stats["total_resistance"])
            self.lbl_coilR.SetLabel('%.3f' % stats["coil_resistance_per_coil"])
            self.lbl_ringR.SetLabel('%.3f' % stats["ring_resistance_total"])

            self.btn_clear.Enable(True)
            skipped = int(getattr(self, "support_hole_collision_count", 0))
            if skipped > 0:
                self.set_status(f"Finished (support holes skipped: {skipped})")
            else:
                self.set_status("Finished")
            if hasattr(self, "m_txtStatus") and self.m_txtStatus:
                self.m_txtStatus.SetValue(
                    "Finished\n"
                    f"Length total: {stats['total_length_mm']:.2f} mm\n"
                    f"Length / phase: {stats['phase_len_mm']:.2f} mm\n"
                    f"Length / coil: {stats['coil_length_per_coil_mm']:.2f} mm\n"
                    f"Length rings total: {stats['ring_length_mm']:.2f} mm\n"
                    f"R total: {stats['total_resistance']:.4f} ohm\n"
                    f"R / phase: {stats['phase_r_temp']:.4f} ohm\n"
                    f"R / coil: {stats['coil_resistance_per_coil']:.4f} ohm\n"
                    f"R rings total: {stats['ring_resistance_total']:.4f} ohm"
                )
        except Exception as e:
            self.set_status("Failed")
            wx.MessageBox(
                f"Generierung fehlgeschlagen:\n{e}",
                "KiMotor Fehler",
                wx.OK | wx.ICON_ERROR
            )
            print(traceback.format_exc())

    def coil_tracker(self, mpt, layer, n_loops, group, is_first_layer=False, is_last_layer=False, is_ccw=False):
        """ 
        Zeichnet die Spule. 
        Trennt die lästigen "Stummel" ab, sodass die Spule an den äußeren Ecken endet.
        """
        ip = 0 
        t0 = None
        nseg = n_loops*4 - 1 

        # Bestimmen, welcher Abschnitt weggelassen wird, damit die Spule an der Ecke stoppt!
        skip_seg = -1
        if is_first_layer and not is_ccw: 
            skip_seg = 0
        if is_last_layer and is_ccw: 
            skip_seg = nseg - 1
        if is_last_layer and not is_ccw: 
            skip_seg = nseg - 1
            
        actual_start = None
        actual_end = None

        for seg in range(nseg):
            ps = self.fpoint( int(mpt[ip][0,0]), int(mpt[ip][0,1]) )
            
            is_arc = (not seg%2)
            if is_arc:
                ip += 1
                mid_pt = self.fpoint(int(mpt[ip][0,0]), int(mpt[ip][0,1]))
                side = -1 if not seg%4 else 1
            
            ip += 1
            pe = self.fpoint( int(mpt[ip][0,0]), int(mpt[ip][0,1]) )

            # Den Stummel überspringen (nicht zeichnen!)
            if seg == skip_seg:
                if skip_seg == 0:
                    actual_start = pe  # Start rückt auf die physikalische Ecke!
                if skip_seg == nseg - 1:
                    actual_end = ps    # Ende rückt auf die physikalische Ecke!
                continue

            if actual_start is None and seg == 0:
                actual_start = ps
            if actual_end is None and seg == nseg - 1:
                actual_end = pe

            if is_arc:
                t = pcbnew.PCB_ARC(self.board)
                t.SetMid(mid_pt)
            else:
                t = pcbnew.PCB_TRACK(self.board)

            t.SetWidth( self.trk_w )
            t.SetLayer( layer )
            t.SetStart( ps )
            t.SetEnd( pe )
            self.board.Add(t)
            
            net_coil = self.board.FindNet("coil")
            if net_coil:
                t.SetNet(net_coil)

            if t0 is not None and self.r_fill > 0:
                fa = self.fillet(self.board, t0, t, self.r_fill, side)
                
            group.AddItem(t)
            t0 = t
            
        return [actual_start, actual_end]

    def do_coils(self, ri, ro, n_slots, n_loops=1, lset=None, mode=0):
        th0 = 2*math.pi/n_slots
        if mode == 0:
            pcu0, pcu0m, pcu0mi = ksolve.parallel( ri, ro, self.dr, th0, n_loops, 0 )
            pcu1, pcu1m, pcu1mi = ksolve.parallel( ri, ro, self.dr, th0, n_loops, 1 )
        else:
            pcu0 = ksolve.radial( ri, ro, self.dr, th0, n_loops, 0 )
            pcu1 = ksolve.radial( ri, ro, self.dr, th0, n_loops, 1 )
        
        coil_p =[]
        for i in range(self.phases):
            coil_p.append([])
        
        net_coil = self.board.FindNet("coil")

        for p in range(n_slots):
            pgroup = pcbnew.PCB_GROUP( self.board )
            pgroup.SetName("pole_"+str(p))
            self.board.Add(pgroup)

            coil_se =[]
            th = th0 * p 
            R = np.array([[math.cos(th), -math.sin(th)],[math.sin(th), math.cos(th)]])
            Tcw = np.matmul(R, pcu0.transpose()).transpose()
            Tccw = np.matmul(R, pcu1.transpose()).transpose()

            for idx, layer in enumerate(lset):
                is_first = (idx == 0)
                is_last = (idx == len(lset)-1)
                is_ccw = (idx % 2 != 0)
                
                if is_ccw:
                    ct = self.coil_tracker(Tccw, layer, n_loops, pgroup, is_first, is_last, is_ccw)
                    via = pcbnew.PCB_VIA(self.board)
                    if len(lset)==2:
                        via.SetViaType(pcbnew.VIATYPE_THROUGH)
                    else:
                        via.SetViaType(pcbnew.VIATYPE_BLIND_BURIED)
                    via.SetLayerPair( lset[idx-1], lset[idx] )
                    via.SetPosition( ct[1] )
                    via.SetDrill( self.d_drill )
                    via.SetWidth( self.d_via )
                    if net_coil: via.SetNet(net_coil)
                    self.board.Add(via)
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

                if is_first:
                    coil_se_start = ct[0] # Exakte Ecke!
                if is_last:
                    coil_se_end = ct[1]   # Exakte Ecke!
   
            coil_se = [coil_se_start, coil_se_end]
            coil_p[ p%self.phases ].append(coil_se)

        return coil_p

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
        support_min_dist = max(self.d_support_hole + self.trk_space, self.d_support_hole)

        # 1. PLATZIERUNG DER ISOLIERTEN STÜTZ-VIAS (Dummy Anchor Pins) AN DEN AUSSENKANTEN
        # Leicht nach innen versetzt, damit sie perfekt im Kupfer der äußersten Spule sitzen
        r_out_via = self.r_coil_out - self.trk_w - self.d_via/2.0
        th_out_off = (th0 / 2.0) * 0.85
        
        if support_via_mode >= 2:
            for slot in range(self.n_slots):
                th_c = slot * th0
                pt_out_a = self.fpoint(int(r_out_via * math.cos(th_c - th_out_off)), int(r_out_via * math.sin(th_c - th_out_off)))
                pt_out_b = self.fpoint(int(r_out_via * math.cos(th_c + th_out_off)), int(r_out_via * math.sin(th_c + th_out_off)))
                for pt in [pt_out_a, pt_out_b]:
                    if self.hole_collides(pt, support_pts, support_min_dist):
                        support_collisions += 1
                        continue
                    self.add_support_hole(pt)
                    support_pts.append(pt)

        # 2. BERECHNUNG DES SICHEREN ABSTANDS FÜR DIE SAMMELSCHIENEN (inkl. Via)
        first_ring_offset = max(self.d_via, self.d_support_hole) if support_via_mode == 4 else 0
        current_radius = self.r_coil_in - (self.d_via / 2.0) - self.ring_space - (self.ring_w / 2.0) - first_ring_offset
        lowest_used_radius = current_radius

        # Mode 4: zusätzliche 2 unverbundene Stützlöcher je Coil nahe den Ringanschlüssen.
        if support_via_mode == 4:
            th_in_off = (th0 / 2.0) * 0.55
            r_inner_support = current_radius + (self.ring_w / 2.0) + self.trk_space + (self.d_support_hole / 2.0)
            if r_inner_support > 0:
                for slot in range(self.n_slots):
                    th_c = slot * th0
                    pt_in_a = self.fpoint(int(r_inner_support * math.cos(th_c - th_in_off)), int(r_inner_support * math.sin(th_c - th_in_off)))
                    pt_in_b = self.fpoint(int(r_inner_support * math.cos(th_c + th_in_off)), int(r_inner_support * math.sin(th_c + th_in_off)))
                    for pt in [pt_in_a, pt_in_b]:
                        if self.hole_collides(pt, support_pts, support_min_dist):
                            support_collisions += 1
                            continue
                        self.add_support_hole(pt)
                        support_pts.append(pt)

        for p in range(phases):
            # Radius für diesen speziellen Phasenring
            cri = current_radius - p * self.ring_dr
            lowest_used_radius = cri

            for i in range(n_rc):
                # Durch den Löschvorgang des Stummels liegen c1e und c2s jetzt EXAKT an den physikalischen Ecken!
                c1e = coils[p][i][1]    # Ende von Coil i (auf B_Cu)
                c2s = coils[p][i+1][0]  # Start von Coil i+1 (auf F_Cu)

                # Löt-Via in die inneren Spulenecken setzen (Netz-Verbindung vorhanden)
                self.add_through_via(c1e, net_coil)
                self.add_through_via(c2s, net_coil)

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

                # 3. Den dicken Sammel-Ring AUF DER OBERSEITE (F_Cu) zeichnen (kreuzt über die blauen Linien drüber)
                d_th = th2 - th1
                if d_th > math.pi: d_th -= 2*math.pi
                elif d_th < -math.pi: d_th += 2*math.pi
                
                th_mid = th1 + d_th / 2.0
                via_mid = self.fpoint(int(cri * math.cos(th_mid)), int(cri * math.sin(th_mid)))
                
                arc = pcbnew.PCB_ARC(self.board)
                arc.SetLayer(arc_layer)
                arc.SetWidth(self.ring_w)
                if net_coil: arc.SetNet(net_coil)
                arc.SetStart(via1_pt)
                arc.SetMid(via_mid)
                arc.SetEnd(via2_pt)
                self.board.Add(arc)

        # 4. STERNSCHALTUNG (nur für 3-Phasen Motoren)
        if phases > 1:
            star_radius = lowest_used_radius - self.ring_dr
            lowest_used_radius = star_radius
            star_pts =[]
            
            for p in range(phases):
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
            for i in range(len(star_pts) - 1):
                th1, pt1 = star_pts[i]
                th2, pt2 = star_pts[i+1]
                
                d_th = th2 - th1
                if d_th > math.pi: d_th -= 2*math.pi
                elif d_th < -math.pi: d_th += 2*math.pi
                
                th_mid = th1 + d_th / 2.0
                pt_mid = self.fpoint(int(star_radius * math.cos(th_mid)), int(star_radius * math.sin(th_mid)))

                arc = pcbnew.PCB_ARC(self.board)
                arc.SetLayer(pcbnew.F_Cu)
                arc.SetWidth(self.ring_w)
                if net_coil: arc.SetNet(net_coil)
                arc.SetStart(pt1)
                arc.SetMid(pt_mid)
                arc.SetEnd(pt2)
                self.board.Add(arc)

        # 5. FINALE TERMINAL-ANSCHLÜSSE (Zur Platine oder Kabel)
        term_radius = lowest_used_radius - self.term_offset
        for p in range(self.n_term):
            if phases == 1:
                if p == 0:
                    c_start = coils[0][0][0]
                else:
                    c_start = coils[0][-1][1]
            else:
                c_start = coils[p][0][0]

            # Via an die Anschlussecke
            self.add_through_via(c_start, net_coil)
            
            th = math.atan2(c_start.y, c_start.x)
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
                    m.SetPosition(t_pt)
                    m.Rotate(t_pt, self.eda_angle(-th))
                    for pad in m.Pads():
                        pad.SetNet(net_coil)
                    dth = 0.05
                    m.Reference().SetPosition(self.fpoint(int(term_radius * math.cos(th+dth)), int(term_radius * math.sin(th+dth))))
                    m.SetReference( "A" if p==0 else ("B" if p==1 else "C") )
                    self.board.Add(m)

        self.support_hole_collision_count = support_collisions
        return term_radius

    def do_outline(self, r_in, r_out, n_edge=0, r_fill=0):
        edge = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_CIRCLE)
        edge.SetCenter( self.fpoint(0,0) )
        edge.SetStart( self.fpoint(0,0) )
        edge.SetEnd( self.fpoint(r_in,0) )
        edge.SetLayer( pcbnew.Edge_Cuts )
        self.board.Add(edge)

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

    def do_thermal_zones(self, r_out, r_nosm_in, r_nosm_out=0, nvias=36, fill_inner_area_gnd=True):
        ni_gnd = self.board.FindNet("gnd")
        ls = pcbnew.LSET()
        for ly in self.lset:
            ls.addLayer(ly)

        filler = pcbnew.ZONE_FILLER(self.board)

        z = pcbnew.ZONE(self.board)
        if self.n_edges == 0:
            cpl = kla.circle_to_polygon( r_out, 100 )
            cp =[]
            for c in cpl:
                cp.append(self.fpoint(c[0],c[1]))
            z.AddPolygon( self.fpoint_vector(cp) )
        elif self.n_edges >= 4:
            ro = int(r_out / math.cos(math.pi/self.n_edges) )
            p =[]
            p.append( self.fpoint(ro,ro) )
            p.append( self.fpoint(ro,-ro) )
            p.append( self.fpoint(-ro,-ro) )
            p.append( self.fpoint(-ro,ro) )
            z.AddPolygon( self.fpoint_vector(p) )

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
            self.board.Add(z)

        nls = pcbnew.LSET()
        nls.addLayer(pcbnew.F_Mask)
        nls.addLayer(pcbnew.B_Mask)
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
            r2 = int(r_out / math.cos(math.pi/self.n_edges))
            th0 = 2*math.pi/self.n_edges
            points =[]
            for i in range(self.n_edges):
                points.append(
                    self.fpoint(
                        int(r2 * math.cos(th0*i+th0/2)), 
                        int(r2 * math.sin(th0*i+th0/2))))
            z.AddPolygon( self.fpoint_vector(points) )
            
            points =[]
            r2 = int((r_out - self.w_mnt) / math.cos(math.pi/self.n_edges))
            for i in range(self.n_edges):
                points.append(
                    self.fpoint(
                        int(r2 * math.cos(th0*i+th0/2)), 
                        int(r2 * math.sin(th0*i+th0/2))))
            z.AddPolygon( self.fpoint_vector(points) )

        z.SetLayerSet(nls)
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)
        self.board.Add(z)

        z = pcbnew.ZONE(self.board)
        cpl = kla.circle_to_polygon(r_nosm_in, 100)
        cp =[]
        for c in cpl:
            cp.append(self.fpoint(c[0],c[1]))

        z.AddPolygon( self.fpoint_vector(cp) )
        z.SetLayerSet(nls)
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)
        self.board.Add(z)

        filler.Fill(self.board.Zones())

    def do_silkscreen(self, ro, ri, th):
        pcb_txt = pcbnew.PCB_TEXT(self.board)
        pcb_txt.SetText(
            datetime.today().strftime('%Y%m%d') + 
            "_ly" + str(self.n_layers) +
            "_s" + str(self.n_slots) +
            "_w" + str(self.n_loops)
        )
        pcb_txt.SetPosition( self.fpoint(0,self.txt_loc) )
        pcb_txt.SetTextSize( self.fsize(self.txt_size,self.txt_size) )
        pcb_txt.SetLayer(pcbnew.F_SilkS)
        self.board.Add(pcb_txt)

        for r in [ro,ri]:
            c = pcbnew.PCB_SHAPE(self.board)
            c.SetShape(pcbnew.SHAPE_T_CIRCLE)
            c.SetFilled(False)
            c.SetStart( self.fpoint(0,0) )
            c.SetEnd( self.fpoint(r,0) )
            c.SetCenter( self.fpoint(0,0) )
            c.SetLayer(pcbnew.F_SilkS)
            self.board.Add(c)
  
        th_0 = 2*math.pi/self.n_slots
        la = 0.05
        for p in range(self.n_slots):
            xy_s = self.fpoint( 
                int( (1+la)*ri*math.cos(th_0*p)), 
                int((1+la)*ri*math.sin(th_0*p))
            )
            xy_e = self.fpoint( 
                int((1-la)*ro*math.cos(th_0*p)), 
                int((1-la)*ro*math.sin(th_0*p))
            )
            c = pcbnew.PCB_SHAPE(self.board)
            c.SetShape(pcbnew.SHAPE_T_SEGMENT)
            c.SetStart(xy_s)
            c.SetEnd(xy_e)
            c.SetLayer(pcbnew.F_SilkS)
            c.SetWidth( int(0.127*1e6) )
            self.board.Add(c)

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
                A = width_m * self.tthick 
                
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

        coils_count = max(self.n_slots, 1)
        phases_count = max(self.phases, 1)
        return {
            "total_length_mm": l_total * 1000.0,
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
        }

    def calculate_stats(self, board, net_name="coil", temp=20):
        stats = self.calculate_stats_breakdown(board, net_name=net_name, temp=temp)
        return stats["phase_len_mm"], stats["phase_r_temp"]

    def on_close(self, event):
        self.pm.SaveAndUnregister()
        event.Skip()

    def on_btn_clear(self, event):
        if self.group:
            self.group.RemoveAll()
            self.group = None
            self.btn_clear.Enable(False)
        event.Skip()

    def on_btn_generate(self, event):
        self.generate()
        event.Skip()

    def on_btn_save(self, event):
        self.pm.SaveAndUnregister()
        self.pm.RegisterAndRestoreAll(self)
        with wx.FileDialog(self, "Save KiMotor preset", wildcard="KMT files (*.kmt)|*.kmt",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            fileDialog.SetFilename("kimotor.kmt")
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return   
            try:
                origin = self.pf
                target = fileDialog.GetPath()
                shutil.copyfile(origin, target)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % target)

    def on_btn_load(self, event):
        with wx.FileDialog(self, "Load KiMotor preset", wildcard="KMT files (*.kmt)|*.kmt",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            try:
                origin = fileDialog.GetPath()
                target = self.pf
                tmp = fileDialog.GetDirectory() + "/kimotor.tmp"
                
                self.pm.SetPersistenceFile(tmp)
                self.pm.SaveAndUnregister()
                shutil.copyfile(origin, target)
                self.pm.SetPersistenceFile(target)
                self.pm.RegisterAndRestoreAll(self)
                
            except IOError:
                wx.LogError("Cannot open file '%s'." % origin)

    def on_cb_preset(self, event):
        preset = self.m_cbPreset.GetSelection()
        if preset == 0:
            self.m_ctrlTrackWidth.SetValue(0.3)
        elif preset == 1:
            self.m_ctrlTrackWidth.SetValue(0.127)
        elif preset == 1:
            self.m_ctrlTrackWidth.SetValue(0.127)
        event.Skip()

    def on_cb_outline(self, event):
        if self.m_cbOutline.GetStringSelection() == "None":
            self.m_ctrlDout.Enable(False)
            self.m_ctrlFilletRadius.Enable(False)
        elif self.m_cbOutline.GetStringSelection() == "Circle":
            self.m_ctrlDout.Enable(True)
            self.m_ctrlFilletRadius.Enable(False)
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

    def on_cb_mholes(self, event):
        event.Skip()

    def on_nr_layers(self, event):
        self.n_layers = int(self.m_ctrlLayers.GetValue())
        event.Skip()
