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
