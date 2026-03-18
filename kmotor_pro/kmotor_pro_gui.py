# -*- coding: utf-8 -*-

# Forked from KiMotor by Stefano Cottafavi.
# Copyright 2022 Stefano Cottafavi <stefano.cottafavi@gmail.com>
# Copyright 2026 I-T-C-R-W
# SPDX-License-Identifier: GPL-2.0-only

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE! (Angepasst: Relativer Terminal Offset)
###########################################################################

from .kmotor_pro_persist import SpinCtrlDoublePersist
import wx
import wx.xrc

class KMotorProGUI ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"KMotor_Pro - by ITCRW", pos = wx.DefaultPosition, size = wx.Size( 1200,680 ), style = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL, name = u"kmotor_pro" )

		self.SetSizeHints( wx.Size(1000,650), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		self.m_notebookMain = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelStator = wx.Panel( self.m_notebookMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelMagnet = wx.Panel( self.m_notebookMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerMainRow = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panelStator, wx.ID_ANY, u"Mechanical" ), wx.VERTICAL )
		sbMechBoard = wx.StaticBoxSizer( wx.StaticBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Board / Coil" ), wx.VERTICAL )
		sbMechMount = wx.StaticBoxSizer( wx.StaticBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Mounting holes" ), wx.VERTICAL )
		sbMechSupport = wx.StaticBoxSizer( wx.StaticBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Support / Fill / Terminals" ), wx.VERTICAL )

		bSizer21211 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time1211 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Board outline:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1211" )
		self.lbl_refresh_time1211.Wrap( -1 )
		bSizer21211.Add( self.lbl_refresh_time1211, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer21211.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbOutlineChoices =[ u"None", u"Circle", u"Square", u"Hexagon", u"Octagon" ]
		self.m_cbOutline = wx.ComboBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Circle", wx.DefaultPosition, wx.Size( 150,20 ), m_cbOutlineChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbOutline" )
		self.m_cbOutline.SetSelection( 1 )
		bSizer21211.Add( self.m_cbOutline, 0, wx.ALL, 5 )

		sbMechBoard.Add( bSizer21211, 0, wx.EXPAND, 5 )

		bSizer221 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time21 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Board size:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time21" )
		self.lbl_refresh_time21.Wrap( -1 )
		bSizer221.Add( self.lbl_refresh_time21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer221.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_boardSizeDia = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_boardSizeDia" )
		self.lbl_boardSizeDia.Wrap( -1 )
		bSizer221.Add( self.lbl_boardSizeDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_ctrlDout = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 1, 9999, 100, 1, u"m_ctrlDout" )
		self.m_ctrlDout.SetDigits( 2 )
		bSizer221.Add( self.m_ctrlDout, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time114 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time114" )
		self.lbl_refresh_time114.Wrap( -1 )
		bSizer221.Add( self.lbl_refresh_time114, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechBoard.Add( bSizer221, 0, wx.EXPAND, 5 )

		bSizer22112 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time2112 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Board fillet:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2112" )
		self.lbl_refresh_time2112.Wrap( -1 )
		bSizer22112.Add( self.lbl_refresh_time2112, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer22112.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlFilletRadius = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 1000, 3.100000, 0.1, u"m_ctrlFilletRadius" )
		self.m_ctrlFilletRadius.SetDigits( 2 )
		bSizer22112.Add( self.m_ctrlFilletRadius, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time11441 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time11441" )
		self.lbl_refresh_time11441.Wrap( -1 )
		bSizer22112.Add( self.lbl_refresh_time11441, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechBoard.Add( bSizer22112, 0, wx.EXPAND, 5 )

		bSizer2212 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time212 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Width, annular:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time212" )
		self.lbl_refresh_time212.Wrap( -1 )
		bSizer2212.Add( self.lbl_refresh_time212, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer2212.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlWmnt = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 9999, 5, 0.1, u"m_ctrlWmnt" )
		self.m_ctrlWmnt.SetDigits( 2 )
		bSizer2212.Add( self.m_ctrlWmnt, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time1141 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time212" )
		self.lbl_refresh_time1141.Wrap( -1 )
		bSizer2212.Add( self.lbl_refresh_time1141, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechBoard.Add( bSizer2212, 0, wx.EXPAND, 5 )

		bSizer222 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time22 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Diameter, coil (outer):", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2" )
		self.lbl_refresh_time22.Wrap( -1 )
		bSizer222.Add( self.lbl_refresh_time22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer222.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_coilOuterDia = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_coilOuterDia" )
		self.lbl_coilOuterDia.Wrap( -1 )
		bSizer222.Add( self.lbl_coilOuterDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_ctrlDend = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 1, 9999, 85, 1, u"m_ctrlDend" )
		self.m_ctrlDend.SetDigits( 2 )
		bSizer222.Add( self.m_ctrlDend, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time11431 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1143" )
		self.lbl_refresh_time11431.Wrap( -1 )
		bSizer222.Add( self.lbl_refresh_time11431, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time2 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Diameter, coil (inner):", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2" )
		self.lbl_refresh_time2.Wrap( -1 )
		bSizer22.Add( self.lbl_refresh_time2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer22.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_coilInnerDia = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_coilInnerDia" )
		self.lbl_coilInnerDia.Wrap( -1 )
		bSizer22.Add( self.lbl_coilInnerDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_ctrlDin = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 1, 9999, 26.000000, 1, u"m_ctrlDin" )
		self.m_ctrlDin.SetDigits( 2 )
		bSizer22.Add( self.m_ctrlDin, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time1143 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1143" )
		self.lbl_refresh_time1143.Wrap( -1 )
		bSizer22.Add( self.lbl_refresh_time1143, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2211 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time211 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Diameter, shaft bore:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time211" )
		self.lbl_refresh_time211.Wrap( -1 )
		bSizer2211.Add( self.lbl_refresh_time211, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer2211.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_shaftDia = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_shaftDia" )
		self.lbl_shaftDia.Wrap( -1 )
		bSizer2211.Add( self.lbl_shaftDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_ctrlDbore = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 9999, 10, 1, u"m_ctrlDbore" )
		self.m_ctrlDbore.SetDigits( 2 )
		bSizer2211.Add( self.m_ctrlDbore, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time1144 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1144" )
		self.lbl_refresh_time1144.Wrap( -1 )
		bSizer2211.Add( self.lbl_refresh_time1144, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechBoard.Add( bSizer2211, 0, wx.EXPAND, 5 )

		bSizer22121 = wx.BoxSizer( wx.HORIZONTAL )

		# === NEU: OFFSET ANSTELLE VON ABSOLUTEM DURCHMESSER ===
		self.lbl_refresh_time2121 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Term. offset (to rings):", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2121" )
		self.lbl_refresh_time2121.Wrap( -1 )
		self.lbl_refresh_time2121.SetToolTip( u"Abstand der Anschlusspads zum innersten Verbindungsring" )
		bSizer22121.Add( self.lbl_refresh_time2121, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer22121.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlDterm = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 999, 3.0, 0.1, u"m_ctrlWtrm" )
		self.m_ctrlDterm.SetDigits( 2 )
		bSizer22121.Add( self.m_ctrlDterm, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time1142 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1142" )
		self.lbl_refresh_time1142.Wrap( -1 )
		bSizer22121.Add( self.lbl_refresh_time1142, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechBoard.Add( bSizer22121, 0, wx.EXPAND, 5 )

		bSizer27 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time13112 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Mounting holes:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1311" )
		self.lbl_refresh_time13112.Wrap( -1 )
		bSizer27.Add( self.lbl_refresh_time13112, 0, wx.ALL, 5 )

		bSizer27.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time131121 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"size", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1311" )
		self.lbl_refresh_time131121.Wrap( -1 )
		bSizer27.Add( self.lbl_refresh_time131121, 0, wx.ALL, 5 )

		m_cbMountSizeChoices =[ u"None", u"M2", u"M2.5", u"M3", u"M3.5", u"M4", u"M5", u"M6", u"M8" ]
		self.m_cbMountSize = wx.ComboBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"M3", wx.DefaultPosition, wx.Size( 150,20 ), m_cbMountSizeChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbMH" )
		self.m_cbMountSize.SetSelection( 0 )
		bSizer27.Add( self.m_cbMountSize, 1, wx.ALL|wx.EXPAND, 5 )

		sbMechMount.Add( bSizer27, 0, wx.EXPAND, 5 )

		bSizer213 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time13 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"- outboard:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time13" )
		self.lbl_refresh_time13.Wrap( -1 )
		bSizer213.Add( self.lbl_refresh_time13, 0, wx.ALL, 5 )

		bSizer213.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_mhOut = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS, 0, 36, 6, 1, u"m_mhOut" )
		self.m_mhOut.SetDigits( 0 )
		bSizer213.Add( self.m_mhOut, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_refresh_time1312 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1312" )
		self.lbl_refresh_time1312.Wrap( -1 )
		bSizer213.Add( self.lbl_refresh_time1312, 0, wx.ALL, 5 )

		self.m_mhOutR = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 10, 1000, 90, 0.1, u"m_mhOutR" )
		self.m_mhOutR.SetDigits( 2 )
		bSizer213.Add( self.m_mhOutR, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_refresh_time1312Unit = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1312Unit" )
		self.lbl_refresh_time1312Unit.Wrap( -1 )
		bSizer213.Add( self.lbl_refresh_time1312Unit, 0, wx.ALL, 5 )

		sbMechMount.Add( bSizer213, 0, wx.EXPAND, 5 )

		bSizer2111 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time111 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"- inboard:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time111" )
		self.lbl_refresh_time111.Wrap( -1 )
		bSizer2111.Add( self.lbl_refresh_time111, 0, wx.ALL, 5 )

		bSizer2111.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_mhIn = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS, 0, 36, 0.000000, 1, u"m_mhIn" )
		self.m_mhIn.SetDigits( 0 )
		bSizer2111.Add( self.m_mhIn, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_refresh_time13111 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time13111" )
		self.lbl_refresh_time13111.Wrap( -1 )
		bSizer2111.Add( self.lbl_refresh_time13111, 0, wx.ALL, 5 )

		self.m_mhInR = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 10, 1000, 20, 0.1, u"m_mhInR" )
		self.m_mhInR.SetDigits( 2 )
		bSizer2111.Add( self.m_mhInR, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_refresh_time13111Unit = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time13111Unit" )
		self.lbl_refresh_time13111Unit.Wrap( -1 )
		bSizer2111.Add( self.lbl_refresh_time13111Unit, 0, wx.ALL, 5 )

		sbMechMount.Add( bSizer2111, 0, wx.EXPAND, 5 )

		sbSizer2.Add( sbMechBoard, 0, wx.EXPAND|wx.ALL, 4 )
		sbSizer2.Add( sbMechMount, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 4 )
		sbSizer2.Add( sbMechSupport, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 4 )

		sbSizer2.GetStaticBox().SetMinSize( wx.Size( 340,-1 ) )
		bSizerMainRow.Add( sbSizer2, 1, wx.EXPAND|wx.ALL, 6 )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panelStator, wx.ID_ANY, u"Electrical" ), wx.VERTICAL )
		sbElecMotor = wx.StaticBoxSizer( wx.StaticBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Motor / Topology" ), wx.VERTICAL )
		sbElecRouting = wx.StaticBoxSizer( wx.StaticBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"PCB / Routing" ), wx.VERTICAL )

		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time3 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Motor Connections:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time" )
		self.lbl_refresh_time3.Wrap( -1 )
		bSizer23.Add( self.lbl_refresh_time3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer23.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbSchemeChoices =[ u"1P", u"3P", u"3P+N" ]
		self.m_cbScheme = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"3P", wx.DefaultPosition, wx.DefaultSize, m_cbSchemeChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbConnections" )
		self.m_cbScheme.SetSelection( 1 )
		bSizer23.Add( self.m_cbScheme, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )

		sbElecMotor.Add( bSizer23, 0, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Motor Slots:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time" )
		self.lbl_refresh_time.Wrap( -1 )
		bSizer2.Add( self.lbl_refresh_time, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlSlots = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 1, 600, 6.000000, 1, u"m_ctrlPoles" )
		self.m_ctrlSlots.SetDigits( 0 )
		bSizer2.Add( self.m_ctrlSlots, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		sbElecMotor.Add( bSizer2, 0, wx.EXPAND, 5 )

		# Move coil diameter controls from Mechanical column into Electrical column
		# between "Motor Slots" and "Coil loops".
		for _w in (self.lbl_refresh_time22, self.lbl_refresh_time11431, self.m_ctrlDend):
			_w.Reparent(sbSizer1.GetStaticBox())
		for _w in (self.lbl_refresh_time2, self.lbl_refresh_time1143, self.m_ctrlDin):
			_w.Reparent(sbSizer1.GetStaticBox())
		sbElecMotor.Add( bSizer222, 0, wx.EXPAND, 5 )
		sbElecMotor.Add( bSizer22, 0, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Coil loops:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1" )
		self.lbl_refresh_time1.Wrap( -1 )
		bSizer21.Add( self.lbl_refresh_time1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer21.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlLoops = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 1, 999, 12.000000, 1, u"m_ctrlLoops" )
		self.m_ctrlLoops.SetDigits( 0 )
		bSizer21.Add( self.m_ctrlLoops, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		sbElecMotor.Add( bSizer21, 0, wx.EXPAND, 5 )

		bSizer214 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time14 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Coil style:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time14" )
		self.lbl_refresh_time14.Wrap( -1 )
		bSizer214.Add( self.lbl_refresh_time14, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer214.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbStrategyChoices =[ u"Parallel", u"Radial" ]
		self.m_cbStrategy = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_cbStrategyChoices, 0, wx.DefaultValidator, u"m_cbStrategy" )
		self.m_cbStrategy.SetSelection( 1 )
		bSizer214.Add( self.m_cbStrategy, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		sbElecMotor.Add( bSizer214, 0, wx.EXPAND, 5 )


		bSizer2121 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time121 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"PCB preset:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time121" )
		self.lbl_refresh_time121.Wrap( -1 )
		self.lbl_refresh_time121.Hide()
		bSizer2121.Add( self.lbl_refresh_time121, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer2121.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbPresetChoices =[ u"Custom", u"JLCPCB, 1-2L", u"JLCPCB, 4-6L" ]
		self.m_cbPreset = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"JLCPCB, 6L", wx.DefaultPosition, wx.DefaultSize, m_cbPresetChoices, 0, wx.DefaultValidator, u"m_cbPreset" )
		self.m_cbPreset.SetSelection( 2 )
		self.m_cbPreset.Enable( False )
		self.m_cbPreset.Hide()
		bSizer2121.Add( self.m_cbPreset, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		

		bSizer212 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time12 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"PCB layers:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time12" )
		self.lbl_refresh_time12.Wrap( -1 )
		bSizer212.Add( self.lbl_refresh_time12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer212.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlLayers = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 2, 20, 2, 2, u"m_ctrlLayers" )
		self.m_ctrlLayers.SetDigits( 0 )
		bSizer212.Add( self.m_ctrlLayers, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		sbElecRouting.Add( bSizer212, 0, wx.EXPAND, 5 )

		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time11 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Track width:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time11" )
		self.lbl_refresh_time11.Wrap( -1 )
		bSizer211.Add( self.lbl_refresh_time11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer211.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlTrackWidth = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.127, 10, 0.134000, 0.001, u"m_ctrlTrackWidth" )
		self.m_ctrlTrackWidth.SetDigits( 3 )
		bSizer211.Add( self.m_ctrlTrackWidth, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time112 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time112" )
		self.lbl_refresh_time112.Wrap( -1 )
		bSizer211.Add( self.lbl_refresh_time112, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbElecRouting.Add( bSizer211, 0, wx.EXPAND, 5 )
        
		# TRACK SPACING
		bSizerSpacing = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_spacing = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Track spacing:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_spacing" )
		self.lbl_spacing.Wrap( -1 )
		bSizerSpacing.Add( self.lbl_spacing, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerSpacing.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlTrackSpacing = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.09, 10, 0.150, 0.001, u"m_ctrlTrackSpacing" )
		self.m_ctrlTrackSpacing.SetDigits( 3 )
		bSizerSpacing.Add( self.m_ctrlTrackSpacing, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_spacing_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_spacing_unit" )
		self.lbl_spacing_unit.Wrap( -1 )
		bSizerSpacing.Add( self.lbl_spacing_unit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbElecRouting.Add( bSizerSpacing, 0, wx.EXPAND, 5 )
        
		# RING WIDTH (Sammelschienen Breite)
		bSizerRingW = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_ringW = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Ring track width:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringW" )
		self.lbl_ringW.Wrap( -1 )
		bSizerRingW.Add( self.lbl_ringW, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerRingW.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlRingWidth = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.1, 10, 0.800, 0.05, u"m_ctrlRingWidth" )
		self.m_ctrlRingWidth.SetDigits( 3 )
		bSizerRingW.Add( self.m_ctrlRingWidth, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_ringW_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringW_unit" )
		self.lbl_ringW_unit.Wrap( -1 )
		bSizerRingW.Add( self.lbl_ringW_unit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbElecRouting.Add( bSizerRingW, 0, wx.EXPAND, 5 )

		# RING SPACING (Sammelschienen Abstand)
		bSizerRingSpace = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_ringSpace = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Ring spacing:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringSpace" )
		self.lbl_ringSpace.Wrap( -1 )
		bSizerRingSpace.Add( self.lbl_ringSpace, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerRingSpace.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlRingSpacing = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.09, 10, 0.250, 0.05, u"m_ctrlRingSpacing" )
		self.m_ctrlRingSpacing.SetDigits( 3 )
		bSizerRingSpace.Add( self.m_ctrlRingSpacing, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_ringSpace_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringSpace_unit" )
		self.lbl_ringSpace_unit.Wrap( -1 )
		bSizerRingSpace.Add( self.lbl_ringSpace_unit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbElecRouting.Add( bSizerRingSpace, 0, wx.EXPAND, 5 )

		# VIA DIAMETER
		bSizerViaDia = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_viadia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Via Diameter:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_viadia" )
		self.lbl_viadia.Wrap( -1 )
		bSizerViaDia.Add( self.lbl_viadia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerViaDia.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlViaDia = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.1, 10, 0.45, 0.05, u"m_ctrlViaDia" )
		self.m_ctrlViaDia.SetDigits( 3 )
		bSizerViaDia.Add( self.m_ctrlViaDia, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_viadia_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_viadia_unit" )
		self.lbl_viadia_unit.Wrap( -1 )
		bSizerViaDia.Add( self.lbl_viadia_unit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbElecRouting.Add( bSizerViaDia, 0, wx.EXPAND, 5 )

		# VIA DRILL
		bSizerViaDrill = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_viadrill = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Via Drill:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_viadrill" )
		self.lbl_viadrill.Wrap( -1 )
		bSizerViaDrill.Add( self.lbl_viadrill, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerViaDrill.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlViaDrill = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.1, 10, 0.30, 0.05, u"m_ctrlViaDrill" )
		self.m_ctrlViaDrill.SetDigits( 3 )
		bSizerViaDrill.Add( self.m_ctrlViaDrill, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_viadrill_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_viadrill_unit" )
		self.lbl_viadrill_unit.Wrap( -1 )
		bSizerViaDrill.Add( self.lbl_viadrill_unit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbElecRouting.Add( bSizerViaDrill, 0, wx.EXPAND, 5 )

		bSizerSupportHoleDia = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_supportHoleDia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Support TH hole dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_supportHoleDia" )
		self.lbl_supportHoleDia.Wrap( -1 )
		bSizerSupportHoleDia.Add( self.lbl_supportHoleDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerSupportHoleDia.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlSupportHoleDia = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.1, 10, 0.800, 0.05, u"m_ctrlSupportHoleDia" )
		self.m_ctrlSupportHoleDia.SetDigits( 3 )
		bSizerSupportHoleDia.Add( self.m_ctrlSupportHoleDia, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_supportHoleDiaUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_supportHoleDiaUnit" )
		self.lbl_supportHoleDiaUnit.Wrap( -1 )
		bSizerSupportHoleDia.Add( self.lbl_supportHoleDiaUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechSupport.Add( bSizerSupportHoleDia, 0, wx.EXPAND, 5 )

		bSizerSupportVia = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_supportVia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Support via mode:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_supportVia" )
		self.lbl_supportVia.Wrap( -1 )
		bSizerSupportVia.Add( self.lbl_supportVia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerSupportVia.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbSupportViaModeChoices =[ u"0", u"2", u"4" ]
		self.m_cbSupportViaMode = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, m_cbSupportViaModeChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbSupportViaMode" )
		self.m_cbSupportViaMode.SetSelection( 1 )
		bSizerSupportVia.Add( self.m_cbSupportViaMode, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		self.m_cbSupportVias = self.m_cbSupportViaMode

		sbMechSupport.Add( bSizerSupportVia, 0, wx.EXPAND, 5 )

		bSizer22111 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time2111 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Track fillet radius:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2111" )
		self.lbl_refresh_time2111.Wrap( -1 )
		bSizer22111.Add( self.lbl_refresh_time2111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer22111.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlRfill = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 100, 0.000000, 0.1, u"m_ctrlRfill" )
		self.m_ctrlRfill.SetDigits( 3 )
		bSizer22111.Add( self.m_ctrlRfill, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time1122 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1122" )
		self.lbl_refresh_time1122.Wrap( -1 )
		bSizer22111.Add( self.lbl_refresh_time1122, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechSupport.Add( bSizer22111, 0, wx.EXPAND, 5 )

		bSizerInnerFill = wx.BoxSizer( wx.HORIZONTAL )

		self.m_cbFillInnerGND = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Fill inner area with GND", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"m_cbFillInnerGND" )
		self.m_cbFillInnerGND.SetValue( True ) 
		self.m_chkFillInnerGnd = self.m_cbFillInnerGND
		bSizerInnerFill.Add( self.m_cbFillInnerGND, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		bSizerInnerFill.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_innerFillDia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Dia:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_innerFillDia.Wrap( -1 )
		bSizerInnerFill.Add( self.lbl_innerFillDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_ctrlInnerGndDia = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 500, 0.000000, 0.1, u"m_ctrlInnerGndDia" )
		self.m_ctrlInnerGndDia.SetDigits( 3 )
		self.m_ctrlInnerGndDia.SetToolTip( u"Inner GND fill diameter [mm], 0 = auto" )
		bSizerInnerFill.Add( self.m_ctrlInnerGndDia, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_innerFillDiaUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_innerFillDiaUnit.Wrap( -1 )
		bSizerInnerFill.Add( self.lbl_innerFillDiaUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechSupport.Add( bSizerInnerFill, 0, wx.EXPAND, 5 )

		self.m_cbFillOuterGND = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Fill outer area with GND", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"m_cbFillOuterGND" )
		self.m_cbFillOuterGND.SetValue( True ) 
		self.m_chkFillOuterGnd = self.m_cbFillOuterGND
		sbMechSupport.Add( self.m_cbFillOuterGND, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_cbSilkCross = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Silk cross + X guides", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"m_cbSilkCross" )
		self.m_cbSilkCross.SetValue( False ) 
		sbMechSupport.Add( self.m_cbSilkCross, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_cbSilkDeg = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Silk 1 deg ring scale", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"m_cbSilkDeg" )
		self.m_cbSilkDeg.SetValue( False ) 
		sbMechSupport.Add( self.m_cbSilkDeg, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_cbSilkSlots = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Silk slot frames", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"m_cbSilkSlots" )
		self.m_cbSilkSlots.SetValue( False ) 
		sbMechSupport.Add( self.m_cbSilkSlots, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_cbSilkHoleScale = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Silk hole angle scales", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"m_cbSilkHoleScale" )
		self.m_cbSilkHoleScale.SetValue( False ) 
		sbMechSupport.Add( self.m_cbSilkHoleScale, 1, wx.ALL|wx.EXPAND, 5 )

		bSizerCornerOffset = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_cornerHoleOffset = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Corner hole offset:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerHoleOffset" )
		self.lbl_cornerHoleOffset.Wrap( -1 )
		bSizerCornerOffset.Add( self.lbl_cornerHoleOffset, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerCornerOffset.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlCornerHoleOffset = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 100, 10.0, 0.1, u"m_ctrlCornerHoleOffset" )
		self.m_ctrlCornerHoleOffset.SetDigits( 2 )
		bSizerCornerOffset.Add( self.m_ctrlCornerHoleOffset, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_cornerHoleOffsetUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerHoleOffsetUnit" )
		self.lbl_cornerHoleOffsetUnit.Wrap( -1 )
		bSizerCornerOffset.Add( self.lbl_cornerHoleOffsetUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechSupport.Add( bSizerCornerOffset, 0, wx.EXPAND, 5 )

		bSizerCornerDia = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_cornerHoleDia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Corner hole dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerHoleDia" )
		self.lbl_cornerHoleDia.Wrap( -1 )
		bSizerCornerDia.Add( self.lbl_cornerHoleDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerCornerDia.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlCornerHoleDia = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 50, 3.2, 0.1, u"m_ctrlCornerHoleDia" )
		self.m_ctrlCornerHoleDia.SetDigits( 2 )
		bSizerCornerDia.Add( self.m_ctrlCornerHoleDia, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_cornerHoleDiaUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerHoleDiaUnit" )
		self.lbl_cornerHoleDiaUnit.Wrap( -1 )
		bSizerCornerDia.Add( self.lbl_cornerHoleDiaUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechSupport.Add( bSizerCornerDia, 0, wx.EXPAND, 5 )

		bSizerCornerCount = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_cornerHoleCount = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Corner hole count:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerHoleCount" )
		self.lbl_cornerHoleCount.Wrap( -1 )
		bSizerCornerCount.Add( self.lbl_cornerHoleCount, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerCornerCount.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlCornerHoleCount = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0, 4, 4, 1, u"m_ctrlCornerHoleCount" )
		self.m_ctrlCornerHoleCount.SetDigits( 0 )
		bSizerCornerCount.Add( self.m_ctrlCornerHoleCount, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		sbMechSupport.Add( bSizerCornerCount, 0, wx.EXPAND, 5 )

		bSizerCornerStep = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_cornerScaleStep = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Corner scale step:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerScaleStep" )
		self.lbl_cornerScaleStep.Wrap( -1 )
		bSizerCornerStep.Add( self.lbl_cornerScaleStep, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerCornerStep.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlCornerScaleStep = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.1, 5.0, 1.0, 0.1, u"m_ctrlCornerScaleStep" )
		self.m_ctrlCornerScaleStep.SetDigits( 2 )
		bSizerCornerStep.Add( self.m_ctrlCornerScaleStep, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_cornerScaleStepUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[deg]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerScaleStepUnit" )
		self.lbl_cornerScaleStepUnit.Wrap( -1 )
		bSizerCornerStep.Add( self.lbl_cornerScaleStepUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechSupport.Add( bSizerCornerStep, 0, wx.EXPAND, 5 )

		bSizerCornerSpan = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_cornerScaleSpan = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Corner scale span:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerScaleSpan" )
		self.lbl_cornerScaleSpan.Wrap( -1 )
		bSizerCornerSpan.Add( self.lbl_cornerScaleSpan, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerCornerSpan.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlCornerScaleSpan = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.5, 20.0, 5.0, 0.1, u"m_ctrlCornerScaleSpan" )
		self.m_ctrlCornerScaleSpan.SetDigits( 2 )
		bSizerCornerSpan.Add( self.m_ctrlCornerScaleSpan, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_cornerScaleSpanUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[deg]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_cornerScaleSpanUnit" )
		self.lbl_cornerScaleSpanUnit.Wrap( -1 )
		bSizerCornerSpan.Add( self.lbl_cornerScaleSpanUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbMechSupport.Add( bSizerCornerSpan, 0, wx.EXPAND, 5 )

		bSizer271 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time131122 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Terminal pads:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1311" )
		self.lbl_refresh_time131122.Wrap( -1 )
		bSizer271.Add( self.lbl_refresh_time131122, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer271.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbTPChoices =[ u"None", u"THT", u"SMD" ]
		self.m_cbTP = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"THT", wx.DefaultPosition, wx.DefaultSize, m_cbTPChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbTP" )
		self.m_cbTP.SetSelection( 0 )
		bSizer271.Add( self.m_cbTP, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_refresh_time1311221 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Area:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1311" )
		self.lbl_refresh_time1311221.Wrap( -1 )
		bSizer271.Add( self.lbl_refresh_time1311221, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_termSizeChoices =[ u"0.1", u"0.15", u"0.25", u"0.5", u"0.75", u"1.0", u"1.5", u"2.0", u"2.5" ]
		self.m_termSize = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"0.1", wx.DefaultPosition, wx.DefaultSize, m_termSizeChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbTPSize" )
		self.m_termSize.SetSelection( 1 )
		bSizer271.Add( self.m_termSize, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_termAreaUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm2]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_termAreaUnit" )
		self.lbl_termAreaUnit.Wrap( -1 )
		bSizer271.Add( self.lbl_termAreaUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		for _w in (
			self.lbl_supportHoleDia, self.lbl_supportHoleDiaUnit, self.m_ctrlSupportHoleDia,
			self.lbl_supportVia, self.m_cbSupportViaMode,
			self.lbl_refresh_time2111, self.lbl_refresh_time1122, self.m_ctrlRfill,
			self.m_cbFillInnerGND, self.lbl_innerFillDia, self.m_ctrlInnerGndDia, self.lbl_innerFillDiaUnit,
			self.m_cbFillOuterGND,
			self.m_cbSilkCross, self.m_cbSilkDeg, self.m_cbSilkSlots, self.m_cbSilkHoleScale,
			self.lbl_cornerHoleOffset, self.m_ctrlCornerHoleOffset, self.lbl_cornerHoleOffsetUnit,
			self.lbl_cornerHoleDia, self.m_ctrlCornerHoleDia, self.lbl_cornerHoleDiaUnit,
			self.lbl_cornerHoleCount, self.m_ctrlCornerHoleCount,
			self.lbl_cornerScaleStep, self.m_ctrlCornerScaleStep, self.lbl_cornerScaleStepUnit,
			self.lbl_refresh_time131122, self.m_cbTP, self.lbl_refresh_time1311221, self.m_termSize, self.lbl_termAreaUnit
		):
			_w.Reparent(sbSizer2.GetStaticBox())

		sbMechSupport.Add( bSizer271, 0, wx.EXPAND, 5 )

		sbSizer1.Add( sbElecMotor, 0, wx.EXPAND|wx.ALL, 4 )
		sbSizer1.Add( sbElecRouting, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 4 )

		sbSizer1.GetStaticBox().SetMinSize( wx.Size( 340,-1 ) )
		bSizerMainRow.Add( sbSizer1, 1, wx.EXPAND|wx.ALL, 6 )

		sbSizer111 = wx.StaticBoxSizer( wx.StaticBox( self.m_panelStator, wx.ID_ANY, u"Physics / Stats" ), wx.VERTICAL )

		bSizer2112 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time113 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Temperature (ambient):", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time113" )
		self.lbl_refresh_time113.Wrap( -1 )
		bSizer2112.Add( self.lbl_refresh_time113, 0, wx.ALL, 5 )

		bSizer2112.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ambT = SpinCtrlDoublePersist( sbSizer111.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, -50, 150, 20, 0.1, u"m_ambT" )
		self.m_ambT.SetDigits( 1 )
		bSizer2112.Add( self.m_ambT, 1, wx.ALL|wx.EXPAND, 5 )

		self.lbl_refresh_time1121 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[°C]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1121" )
		self.lbl_refresh_time1121.Wrap( -1 )
		bSizer2112.Add( self.lbl_refresh_time1121, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizer2112, 0, wx.EXPAND, 5 )

		bSizer21321 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time1321 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Phase wire length", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1321" )
		self.lbl_refresh_time1321.Wrap( -1 )
		bSizer21321.Add( self.lbl_refresh_time1321, 0, wx.ALL, 5 )

		bSizer21321.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_phaseLength = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 140,20 ), wx.ALIGN_RIGHT, u"lbl_phaseLength" )
		self.lbl_phaseLength.Wrap( -1 )
		bSizer21321.Add( self.lbl_phaseLength, 0, wx.ALL, 5 )

		self.lbl_refresh_time13121111 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time13121111" )
		self.lbl_refresh_time13121111.Wrap( -1 )
		bSizer21321.Add( self.lbl_refresh_time13121111, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizer21321, 0, wx.EXPAND, 5 )

		bSizer21312 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time1313 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Phase resistance (R)", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1313" )
		self.lbl_refresh_time1313.Wrap( -1 )
		bSizer21312.Add( self.lbl_refresh_time1313, 0, wx.ALL, 5 )

		bSizer21312.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_phaseR = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 140,20 ), wx.ALIGN_RIGHT, u"lbl_phaseR" )
		self.lbl_phaseR.Wrap( -1 )
		bSizer21312.Add( self.lbl_phaseR, 0, wx.ALL, 5 )

		self.lbl_refresh_time13121 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[ohm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time13121" )
		self.lbl_refresh_time13121.Wrap( -1 )
		bSizer21312.Add( self.lbl_refresh_time13121, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizer21312, 0, wx.EXPAND, 5 )

		bSizerTotalR = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_totalRText = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Total resistance", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_totalRText" )
		self.lbl_totalRText.Wrap( -1 )
		bSizerTotalR.Add( self.lbl_totalRText, 0, wx.ALL, 5 )

		bSizerTotalR.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_totalR = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 140,20 ), wx.ALIGN_RIGHT, u"lbl_totalR" )
		self.lbl_totalR.Wrap( -1 )
		bSizerTotalR.Add( self.lbl_totalR, 0, wx.ALL, 5 )

		self.lbl_totalRUnit = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[ohm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_totalRUnit" )
		self.lbl_totalRUnit.Wrap( -1 )
		bSizerTotalR.Add( self.lbl_totalRUnit, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizerTotalR, 0, wx.EXPAND, 5 )

		bSizerCoilR = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_coilRText = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Coil resistance / coil", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_coilRText" )
		self.lbl_coilRText.Wrap( -1 )
		bSizerCoilR.Add( self.lbl_coilRText, 0, wx.ALL, 5 )

		bSizerCoilR.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_coilR = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 140,20 ), wx.ALIGN_RIGHT, u"lbl_coilR" )
		self.lbl_coilR.Wrap( -1 )
		bSizerCoilR.Add( self.lbl_coilR, 0, wx.ALL, 5 )

		self.lbl_coilRUnit = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[ohm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_coilRUnit" )
		self.lbl_coilRUnit.Wrap( -1 )
		bSizerCoilR.Add( self.lbl_coilRUnit, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizerCoilR, 0, wx.EXPAND, 5 )

		bSizerRingR = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_ringRText = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Ring resistance total", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringRText" )
		self.lbl_ringRText.Wrap( -1 )
		bSizerRingR.Add( self.lbl_ringRText, 0, wx.ALL, 5 )

		bSizerRingR.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_ringR = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 140,20 ), wx.ALIGN_RIGHT, u"lbl_ringR" )
		self.lbl_ringR.Wrap( -1 )
		bSizerRingR.Add( self.lbl_ringR, 0, wx.ALL, 5 )

		self.lbl_ringRUnit = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[ohm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringRUnit" )
		self.lbl_ringRUnit.Wrap( -1 )
		bSizerRingR.Add( self.lbl_ringRUnit, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizerRingR, 0, wx.EXPAND, 5 )

		bSizerKe = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_keText = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Ke est", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_keText" )
		self.lbl_keText.Wrap( -1 )
		bSizerKe.Add( self.lbl_keText, 0, wx.ALL, 5 )

		bSizerKe.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_ke = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 140,20 ), wx.ALIGN_RIGHT, u"lbl_ke" )
		self.lbl_ke.Wrap( -1 )
		bSizerKe.Add( self.lbl_ke, 0, wx.ALL, 5 )

		self.lbl_keUnit = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[V*s/rad]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_keUnit" )
		self.lbl_keUnit.Wrap( -1 )
		bSizerKe.Add( self.lbl_keUnit, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizerKe, 0, wx.EXPAND, 5 )

		bSizerKt = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_ktText = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Kt est", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ktText" )
		self.lbl_ktText.Wrap( -1 )
		bSizerKt.Add( self.lbl_ktText, 0, wx.ALL, 5 )

		bSizerKt.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_kt = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 140,20 ), wx.ALIGN_RIGHT, u"lbl_kt" )
		self.lbl_kt.Wrap( -1 )
		bSizerKt.Add( self.lbl_kt, 0, wx.ALL, 5 )

		self.lbl_ktUnit = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[Nm/A]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ktUnit" )
		self.lbl_ktUnit.Wrap( -1 )
		bSizerKt.Add( self.lbl_ktUnit, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizerKt, 0, wx.EXPAND, 5 )

		bSizerKv = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_kvText = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Kv est", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_kvText" )
		self.lbl_kvText.Wrap( -1 )
		bSizerKv.Add( self.lbl_kvText, 0, wx.ALL, 5 )

		bSizerKv.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_kv = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size( 140,20 ), wx.ALIGN_RIGHT, u"lbl_kv" )
		self.lbl_kv.Wrap( -1 )
		bSizerKv.Add( self.lbl_kv, 0, wx.ALL, 5 )

		self.lbl_kvUnit = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[rpm/V]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_kvUnit" )
		self.lbl_kvUnit.Wrap( -1 )
		bSizerKv.Add( self.lbl_kvUnit, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizerKv, 0, wx.EXPAND, 5 )

		sbSizer111.GetStaticBox().SetMinSize( wx.Size( 340,-1 ) )
		bSizerMainRow.Add( sbSizer111, 1, wx.EXPAND|wx.ALL, 6 )

		sbSizerStatus = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Status" ), wx.VERTICAL )

		self.lbl_status = wx.StaticText( sbSizerStatus.GetStaticBox(), wx.ID_ANY, u"Ready", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_status" )
		self.lbl_status.Wrap( -1 )
		sbSizerStatus.Add( self.lbl_status, 0, wx.ALL, 5 )

		self.m_txtStatus = wx.TextCtrl( sbSizerStatus.GetStaticBox(), wx.ID_ANY, u"Ready.", wx.DefaultPosition, wx.Size( -1,60 ), wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_SIMPLE, wx.DefaultValidator, u"m_txtStatus" )
		sbSizerStatus.Add( self.m_txtStatus, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		bSizerBottomLeft = wx.BoxSizer( wx.VERTICAL )
		bSizerLeftRow = wx.BoxSizer( wx.HORIZONTAL )
		bSizerBottomRight = wx.BoxSizer( wx.VERTICAL )

		self.btn_load = wx.Button( self, wx.ID_OK, u"Load", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_ok" )
		bSizerLeftRow.Add( self.btn_load, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 8 )

		self.btn_save = wx.Button( self, wx.ID_OK, u"Save", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_ok" )
		bSizerLeftRow.Add( self.btn_save, 0, wx.ALIGN_CENTER_VERTICAL, 0 )

		bSizerBottomLeft.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		bSizerBottomLeft.Add( bSizerLeftRow, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		bSizerBottomLeft.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_clear = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_clear" )
		self.btn_clear.Enable( False )
		self.btn_clear.Hide()

		self.btn_generate_magnet = wx.Button( self, wx.ID_ANY, u"Generate Magnet PCB", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_generate_magnet" )
		self.btn_generate_magnet.SetForegroundColour( wx.Colour(255,255,255) )
		self.btn_generate_magnet.SetBackgroundColour( wx.Colour(25,118,210) )
		self.btn_generate_magnet.SetMinSize( wx.Size(170, 40) )

		self.btn_ok = wx.Button( self, wx.ID_OK, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_ok" )
		self.btn_ok.SetForegroundColour( wx.Colour(255,255,255) )
		self.btn_ok.SetBackgroundColour( wx.Colour(46,125,50) )
		self.btn_ok.SetMinSize( wx.Size(130, 40) )

		bSizerBottomRight.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		bSizerBottomRight.Add( self.btn_generate_magnet, 0, wx.ALIGN_CENTER|wx.BOTTOM, 8 )
		bSizerBottomRight.Add( self.btn_ok, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		bSizerBottomRight.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer3.Add( bSizerBottomLeft, 0, wx.EXPAND|wx.RIGHT, 8 )
		bSizer3.Add( sbSizerStatus, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 6 )
		bSizer3.Add( bSizerBottomRight, 0, wx.EXPAND|wx.LEFT, 8 )

		bSizer5.Add( bSizer3, 0, wx.EXPAND|wx.TOP, 5 )

		bSizerPanelStator = wx.BoxSizer( wx.VERTICAL )
		bSizerPanelStator.Add( bSizerMainRow, 1, wx.EXPAND|wx.ALL, 0 )
		self.m_panelStator.SetSizer( bSizerPanelStator )
		self.m_panelStator.Layout()

		bSizerPanelMagnet = wx.BoxSizer( wx.VERTICAL )

		sbSizerMagnet = wx.StaticBoxSizer( wx.StaticBox( self.m_panelMagnet, wx.ID_ANY, u"Magnet PCB" ), wx.VERTICAL )
		sbMagGeom = wx.StaticBoxSizer( wx.StaticBox( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet Geometry" ), wx.VERTICAL )
		sbMagPlacement = wx.StaticBoxSizer( wx.StaticBox( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Ring / Placement" ), wx.VERTICAL )
		sbMagOptional = wx.StaticBoxSizer( wx.StaticBox( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Optional" ), wx.VERTICAL )
		sbMagInfo = wx.StaticBoxSizer( wx.StaticBox( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Validation Preview" ), wx.VERTICAL )

		bSizerMagShape = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magShape = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet shape:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magShape.Wrap( -1 )
		bSizerMagShape.Add( self.lbl_magShape, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagShape.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		m_cbMagShapeChoices = [ u"Round", u"Rect" ]
		self.m_cbMagShape = wx.ComboBox( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Round", wx.DefaultPosition, wx.DefaultSize, m_cbMagShapeChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbMagShape" )
		self.m_cbMagShape.SetSelection( 0 )
		bSizerMagShape.Add( self.m_cbMagShape, 1, wx.ALL|wx.EXPAND, 5 )
		sbMagGeom.Add( bSizerMagShape, 0, wx.EXPAND, 5 )

		bSizerMagDia = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magDia = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet dia:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magDia.Wrap( -1 )
		bSizerMagDia.Add( self.lbl_magDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagDia.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagDia = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.1, 200, 8.0, 0.1, u"m_ctrlMagDia" )
		self.m_ctrlMagDia.SetDigits( 2 )
		bSizerMagDia.Add( self.m_ctrlMagDia, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magDiaUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magDiaUnit.Wrap( -1 )
		bSizerMagDia.Add( self.lbl_magDiaUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagGeom.Add( bSizerMagDia, 0, wx.EXPAND, 5 )

		bSizerMagWidth = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magWidth = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet width (B):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magWidth.Wrap( -1 )
		bSizerMagWidth.Add( self.lbl_magWidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagWidth.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagWidth = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.1, 200, 10.0, 0.1, u"m_ctrlMagWidth" )
		self.m_ctrlMagWidth.SetDigits( 2 )
		bSizerMagWidth.Add( self.m_ctrlMagWidth, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magWidthUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magWidthUnit.Wrap( -1 )
		bSizerMagWidth.Add( self.lbl_magWidthUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagGeom.Add( bSizerMagWidth, 0, wx.EXPAND, 5 )

		bSizerMagHeight = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magHeight = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet height (H):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magHeight.Wrap( -1 )
		bSizerMagHeight.Add( self.lbl_magHeight, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagHeight.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagHeight = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.1, 200, 5.0, 0.1, u"m_ctrlMagHeight" )
		self.m_ctrlMagHeight.SetDigits( 2 )
		bSizerMagHeight.Add( self.m_ctrlMagHeight, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magHeightUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magHeightUnit.Wrap( -1 )
		bSizerMagHeight.Add( self.lbl_magHeightUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagGeom.Add( bSizerMagHeight, 0, wx.EXPAND, 5 )

		bSizerMagLength = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magLength = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet length (L, optional):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magLength.Wrap( -1 )
		bSizerMagLength.Add( self.lbl_magLength, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagLength.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagLength = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.0, 500, 0.0, 0.1, u"m_ctrlMagLength" )
		self.m_ctrlMagLength.SetDigits( 2 )
		bSizerMagLength.Add( self.m_ctrlMagLength, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magLengthUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magLengthUnit.Wrap( -1 )
		bSizerMagLength.Add( self.lbl_magLengthUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagGeom.Add( bSizerMagLength, 0, wx.EXPAND, 5 )

		bSizerMagRingDia = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magRingDia = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet ring dia:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magRingDia.Wrap( -1 )
		bSizerMagRingDia.Add( self.lbl_magRingDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagRingDia.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagRingDia = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 1.0, 9999, 90.0, 0.1, u"m_ctrlMagRingDia" )
		self.m_ctrlMagRingDia.SetDigits( 2 )
		bSizerMagRingDia.Add( self.m_ctrlMagRingDia, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magRingDiaUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magRingDiaUnit.Wrap( -1 )
		bSizerMagRingDia.Add( self.lbl_magRingDiaUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagPlacement.Add( bSizerMagRingDia, 0, wx.EXPAND, 5 )

		bSizerMagPolePairs = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magPolePairs = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Pole pairs:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magPolePairs.Wrap( -1 )
		bSizerMagPolePairs.Add( self.lbl_magPolePairs, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagPolePairs.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagPolePairs = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 1, 500, 30, 1, u"m_ctrlMagPolePairs" )
		self.m_ctrlMagPolePairs.SetDigits( 0 )
		bSizerMagPolePairs.Add( self.m_ctrlMagPolePairs, 1, wx.ALL|wx.EXPAND, 5 )
		sbMagPlacement.Add( bSizerMagPolePairs, 0, wx.EXPAND, 5 )

		bSizerMagRot = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magRotation = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Rotation offset:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magRotation.Wrap( -1 )
		bSizerMagRot.Add( self.lbl_magRotation, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagRot.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagRotation = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, -180.0, 180.0, 0.0, 0.1, u"m_ctrlMagRotation" )
		self.m_ctrlMagRotation.SetDigits( 2 )
		bSizerMagRot.Add( self.m_ctrlMagRotation, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magRotationUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[deg]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magRotationUnit.Wrap( -1 )
		bSizerMagRot.Add( self.lbl_magRotationUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagPlacement.Add( bSizerMagRot, 0, wx.EXPAND, 5 )

		bSizerMagGap = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magGap = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet gap (optional):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magGap.Wrap( -1 )
		bSizerMagGap.Add( self.lbl_magGap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagGap.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagGap = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.0, 50.0, 0.5, 0.1, u"m_ctrlMagGap" )
		self.m_ctrlMagGap.SetDigits( 2 )
		bSizerMagGap.Add( self.m_ctrlMagGap, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magGapUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magGapUnit.Wrap( -1 )
		bSizerMagGap.Add( self.lbl_magGapUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagOptional.Add( bSizerMagGap, 0, wx.EXPAND, 5 )

		bSizerMagKeepout = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magKeepout = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Magnet keepout (optional):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magKeepout.Wrap( -1 )
		bSizerMagKeepout.Add( self.lbl_magKeepout, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagKeepout.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagKeepout = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.0, 50.0, 0.0, 0.1, u"m_ctrlMagKeepout" )
		self.m_ctrlMagKeepout.SetDigits( 2 )
		bSizerMagKeepout.Add( self.m_ctrlMagKeepout, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magKeepoutUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magKeepoutUnit.Wrap( -1 )
		bSizerMagKeepout.Add( self.lbl_magKeepoutUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagOptional.Add( bSizerMagKeepout, 0, wx.EXPAND, 5 )

		bSizerMagBest = wx.BoxSizer( wx.HORIZONTAL )
		self.lbl_magBest = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"B gap est:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magBest.Wrap( -1 )
		bSizerMagBest.Add( self.lbl_magBest, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizerMagBest.Add( ( 0, 0 ), 1, wx.EXPAND, 5 )
		self.m_ctrlMagBest = SpinCtrlDoublePersist( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_LEFT|wx.SP_ARROW_KEYS, 0.01, 3.0, 0.60, 0.01, u"m_ctrlMagBest" )
		self.m_ctrlMagBest.SetDigits( 2 )
		bSizerMagBest.Add( self.m_ctrlMagBest, 1, wx.ALL|wx.EXPAND, 5 )
		self.lbl_magBestUnit = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"[T]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_magBestUnit.Wrap( -1 )
		bSizerMagBest.Add( self.lbl_magBestUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		sbMagOptional.Add( bSizerMagBest, 0, wx.EXPAND, 5 )

		self.lblMagnetSummary = wx.StaticText( sbSizerMagnet.GetStaticBox(), wx.ID_ANY, u"Configure magnet geometry and use Generate Magnet PCB for validation.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblMagnetSummary.Wrap( 520 )
		sbMagInfo.Add( self.lblMagnetSummary, 0, wx.ALL|wx.EXPAND, 5 )

		sbSizerMagnet.Add( sbMagGeom, 0, wx.EXPAND|wx.ALL, 4 )
		sbSizerMagnet.Add( sbMagPlacement, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 4 )
		sbSizerMagnet.Add( sbMagOptional, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 4 )
		sbSizerMagnet.Add( sbMagInfo, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 4 )

		def _style_staticbox(box):
			if not box:
				return
			f = box.GetFont()
			f.SetWeight(wx.FONTWEIGHT_BOLD)
			box.SetOwnFont(f)
			try:
				box.SetWindowStyleFlag(box.GetWindowStyleFlag() | wx.BORDER_SIMPLE)
			except Exception:
				pass

		for _sb in (sbSizer2, sbSizer1, sbSizer111, sbSizerMagnet, sbSizerStatus):
			_style_staticbox(_sb.GetStaticBox())

		_normal_font = self.GetFont()
		def _reset_desc_font(win):
			for _child in win.GetChildren():
				if not isinstance(_child, wx.StaticBox):
					_child.SetOwnFont(_normal_font)
					try:
						_child.InvalidateBestSize()
					except Exception:
						pass
				_reset_desc_font(_child)

		for _sb in (sbSizer2, sbSizer1, sbSizer111, sbSizerMagnet, sbSizerStatus):
			_reset_desc_font(_sb.GetStaticBox())

		bSizerPanelMagnet.Add( sbSizerMagnet, 1, wx.EXPAND|wx.ALL, 6 )
		self.m_panelMagnet.SetSizer( bSizerPanelMagnet )
		self.m_panelMagnet.Layout()

		self.m_notebookMain.AddPage( self.m_panelStator, u"Stator PCB", True )
		self.m_notebookMain.AddPage( self.m_panelMagnet, u"Magnet PCB", False )
		bSizer5.Insert( 0, self.m_notebookMain, 1, wx.EXPAND|wx.TOP, 8 )
		bSizer1.Add( bSizer5, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )

		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.m_cbOutline.Bind( wx.EVT_TEXT, self.on_cb_outline )
		self.m_cbMountSize.Bind( wx.EVT_TEXT, self.on_cb_mholes )
		self.m_cbScheme.Bind( wx.EVT_TEXT, self.on_cb_connections )
		self.m_cbStrategy.Bind( wx.EVT_TEXT, self.on_cb_outline )
		self.m_cbPreset.Bind( wx.EVT_TEXT, self.on_cb_preset )
		self.m_ctrlLayers.Bind( wx.EVT_SPINCTRLDOUBLE, self.on_nr_layers )
		self.m_cbTP.Bind( wx.EVT_TEXT, self.on_cb_trmtype )
		self.m_termSize.Bind( wx.EVT_TEXT, self.on_cb_connections )
		self.m_cbMagShape.Bind( wx.EVT_TEXT, self.on_cb_magnet_shape )
		self.btn_load.Bind( wx.EVT_BUTTON, self.on_btn_load )
		self.btn_save.Bind( wx.EVT_BUTTON, self.on_btn_save )
		self.btn_clear.Bind( wx.EVT_BUTTON, self.on_btn_clear )
		self.btn_generate_magnet.Bind( wx.EVT_BUTTON, self.on_btn_generate_magnet )
		self.btn_ok.Bind( wx.EVT_BUTTON, self.on_btn_generate )

	def __del__( self ):
		pass

	def on_close( self, event ):
		event.Skip()
	def on_cb_outline( self, event ):
		event.Skip()
	def on_cb_mholes( self, event ):
		event.Skip()
	def on_cb_connections( self, event ):
		event.Skip()
	def on_cb_preset( self, event ):
		event.Skip()
	def on_nr_layers( self, event ):
		event.Skip()
	def on_cb_trmtype( self, event ):
		event.Skip()
	def on_cb_magnet_shape( self, event ):
		event.Skip()
	def on_btn_load( self, event ):
		event.Skip()
	def on_btn_save( self, event ):
		event.Skip()
	def on_btn_clear( self, event ):
		event.Skip()
	def on_btn_generate_magnet( self, event ):
		event.Skip()
	def on_btn_generate( self, event ):
		event.Skip()
