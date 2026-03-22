# -*- coding: utf-8 -*-
# KMotor_Pro - Parametric PCB motor generator for KiCad
# Copyright 2026 I-T-C-R-W
# SPDX-License-Identifier: GPL-2.0-only

try:
    from .kmotor_dialog import KMotorProDialog
except ModuleNotFoundError:
    KMotorProDialog = None

if KMotorProDialog is not None:
    # Register the plugin
    import pcbnew
    class KMotorProPlugin(pcbnew.ActionPlugin):
        def defaults(self):
            self.name = "KMotor_Pro"
            self.category = "Modify Drawing PCB"
            self.description = "KMotor_Pro - Parametric PCB motor generator for KiCad"
            self.show_toolbar_button = True
            import os
            self.icon_file_name = os.path.join(os.path.dirname(__file__), 'kmotor_pro_24x24.png')

        def Run(self):
            import wx
            self.frame = wx.FindWindowByName("PcbFrame")
            self.board = pcbnew.GetBoard()
            dlg = KMotorProDialog(self.frame, self.board)
            dlg.SetIcon(wx.Icon(self.icon_file_name))
            dlg.Show()

    KMotorProPlugin().register()
