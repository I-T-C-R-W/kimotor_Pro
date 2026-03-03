# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE! (Angepasst: Relativer Terminal Offset)
###########################################################################

from .kimotor_persist import SpinCtrlDoublePersist
import wx
import wx.xrc

class KiMotorGUI ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"KiMotor", pos = wx.DefaultPosition, size = wx.Size( 1700,750 ), style = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL, name = u"kimotor" )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		bSizerMainRow = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Mechanical" ), wx.VERTICAL )

		bSizer21211 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time1211 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Board outline:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1211" )
		self.lbl_refresh_time1211.Wrap( -1 )
		bSizer21211.Add( self.lbl_refresh_time1211, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer21211.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbOutlineChoices =[ u"None", u"Circle", u"Square", u"Hexagon", u"Octagon" ]
		self.m_cbOutline = wx.ComboBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Circle", wx.DefaultPosition, wx.Size( 150,20 ), m_cbOutlineChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbOutline" )
		self.m_cbOutline.SetSelection( 0 )
		bSizer21211.Add( self.m_cbOutline, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer21211, 1, wx.EXPAND, 5 )

		bSizer221 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time21 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Board size:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time21" )
		self.lbl_refresh_time21.Wrap( -1 )
		bSizer221.Add( self.lbl_refresh_time21, 0, wx.ALL, 5 )

		bSizer221.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time114 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time114" )
		self.lbl_refresh_time114.Wrap( -1 )
		bSizer221.Add( self.lbl_refresh_time114, 0, wx.ALL, 5 )

		self.m_ctrlDout = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 9999, 100, 1, u"m_ctrlDout" )
		self.m_ctrlDout.SetDigits( 2 )
		bSizer221.Add( self.m_ctrlDout, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer221, 1, wx.EXPAND, 5 )

		bSizer22112 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time2112 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Board fillet:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2112" )
		self.lbl_refresh_time2112.Wrap( -1 )
		bSizer22112.Add( self.lbl_refresh_time2112, 0, wx.ALL, 5 )

		bSizer22112.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time11441 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time11441" )
		self.lbl_refresh_time11441.Wrap( -1 )
		bSizer22112.Add( self.lbl_refresh_time11441, 0, wx.ALL, 5 )

		self.m_ctrlFilletRadius = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 1000, 3.100000, 0.1, u"m_ctrlFilletRadius" )
		self.m_ctrlFilletRadius.SetDigits( 2 )
		bSizer22112.Add( self.m_ctrlFilletRadius, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer22112, 1, wx.EXPAND, 5 )

		bSizer2212 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time212 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Width, annular:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time212" )
		self.lbl_refresh_time212.Wrap( -1 )
		bSizer2212.Add( self.lbl_refresh_time212, 0, wx.ALL, 5 )

		bSizer2212.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time1141 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time212" )
		self.lbl_refresh_time1141.Wrap( -1 )
		bSizer2212.Add( self.lbl_refresh_time1141, 0, wx.ALL, 5 )

		self.m_ctrlWmnt = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 9999, 5, 0.1, u"m_ctrlWmnt" )
		self.m_ctrlWmnt.SetDigits( 2 )
		bSizer2212.Add( self.m_ctrlWmnt, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer2212, 1, wx.EXPAND, 5 )

		bSizer222 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time22 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Diameter, coil (outer):", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2" )
		self.lbl_refresh_time22.Wrap( -1 )
		bSizer222.Add( self.lbl_refresh_time22, 0, wx.ALL, 5 )

		bSizer222.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time11431 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1143" )
		self.lbl_refresh_time11431.Wrap( -1 )
		bSizer222.Add( self.lbl_refresh_time11431, 0, wx.ALL, 5 )

		self.m_ctrlDend = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 9999, 85, 1, u"m_ctrlDend" )
		self.m_ctrlDend.SetDigits( 2 )
		bSizer222.Add( self.m_ctrlDend, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer222, 1, wx.EXPAND, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time2 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Diameter, coil (inner):", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2" )
		self.lbl_refresh_time2.Wrap( -1 )
		bSizer22.Add( self.lbl_refresh_time2, 0, wx.ALL, 5 )

		bSizer22.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time1143 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1143" )
		self.lbl_refresh_time1143.Wrap( -1 )
		bSizer22.Add( self.lbl_refresh_time1143, 0, wx.ALL, 5 )

		self.m_ctrlDin = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 9999, 26.000000, 1, u"m_ctrlDin" )
		self.m_ctrlDin.SetDigits( 2 )
		bSizer22.Add( self.m_ctrlDin, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer22, 1, wx.EXPAND, 5 )

		bSizer2211 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time211 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Diameter, shaft bore:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time211" )
		self.lbl_refresh_time211.Wrap( -1 )
		bSizer2211.Add( self.lbl_refresh_time211, 0, wx.ALL, 5 )

		bSizer2211.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time1144 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1144" )
		self.lbl_refresh_time1144.Wrap( -1 )
		bSizer2211.Add( self.lbl_refresh_time1144, 0, wx.ALL, 5 )

		self.m_ctrlDbore = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 9999, 10, 1, u"m_ctrlDbore" )
		self.m_ctrlDbore.SetDigits( 2 )
		bSizer2211.Add( self.m_ctrlDbore, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer2211, 1, wx.EXPAND, 5 )

		bSizer22121 = wx.BoxSizer( wx.HORIZONTAL )

		# === NEU: OFFSET ANSTELLE VON ABSOLUTEM DURCHMESSER ===
		self.lbl_refresh_time2121 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Term. offset (to rings):", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2121" )
		self.lbl_refresh_time2121.Wrap( -1 )
		self.lbl_refresh_time2121.SetToolTip( u"Abstand der Anschlusspads zum innersten Verbindungsring" )
		bSizer22121.Add( self.lbl_refresh_time2121, 0, wx.ALL, 5 )

		bSizer22121.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time1142 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1142" )
		self.lbl_refresh_time1142.Wrap( -1 )
		bSizer22121.Add( self.lbl_refresh_time1142, 0, wx.ALL, 5 )

		self.m_ctrlDterm = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 999, 3.0, 0.1, u"m_ctrlWtrm" )
		self.m_ctrlDterm.SetDigits( 2 )
		bSizer22121.Add( self.m_ctrlDterm, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer22121, 1, wx.EXPAND, 5 )

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
		bSizer27.Add( self.m_cbMountSize, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer27, 1, wx.EXPAND, 5 )

		bSizer213 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time13 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"- outboard", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time13" )
		self.lbl_refresh_time13.Wrap( -1 )
		bSizer213.Add( self.lbl_refresh_time13, 0, wx.ALL, 5 )

		bSizer213.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_mhOut = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS, 0, 36, 6, 1, u"m_mhOut" )
		self.m_mhOut.SetDigits( 0 )
		bSizer213.Add( self.m_mhOut, 0, wx.ALL, 5 )

		self.lbl_refresh_time1312 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"@ [mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1312" )
		self.lbl_refresh_time1312.Wrap( -1 )
		bSizer213.Add( self.lbl_refresh_time1312, 0, wx.ALL, 5 )

		self.m_mhOutR = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 10, 1000, 90, 0.1, u"m_mhOutR" )
		self.m_mhOutR.SetDigits( 2 )
		bSizer213.Add( self.m_mhOutR, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer213, 1, wx.EXPAND, 5 )

		bSizer2111 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time111 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"- inboard", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time111" )
		self.lbl_refresh_time111.Wrap( -1 )
		bSizer2111.Add( self.lbl_refresh_time111, 0, wx.ALL, 5 )

		bSizer2111.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_mhIn = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS, 0, 36, 0.000000, 1, u"m_mhIn" )
		self.m_mhIn.SetDigits( 0 )
		bSizer2111.Add( self.m_mhIn, 0, wx.ALL, 5 )

		self.lbl_refresh_time13111 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"@ [mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time13111" )
		self.lbl_refresh_time13111.Wrap( -1 )
		bSizer2111.Add( self.lbl_refresh_time13111, 0, wx.ALL, 5 )

		self.m_mhInR = SpinCtrlDoublePersist( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 10, 1000, 20, 0.1, u"m_mhInR" )
		self.m_mhInR.SetDigits( 2 )
		bSizer2111.Add( self.m_mhInR, 0, wx.ALL, 5 )

		sbSizer2.Add( bSizer2111, 1, wx.EXPAND, 5 )

		bSizerMainRow.Add( sbSizer2, 15, wx.EXPAND|wx.ALL, 6 )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Electrical" ), wx.VERTICAL )

		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time3 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Motor Connections:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time" )
		self.lbl_refresh_time3.Wrap( -1 )
		bSizer23.Add( self.lbl_refresh_time3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer23.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbSchemeChoices =[ u"1P", u"3P", u"3P+N" ]
		self.m_cbScheme = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"3P", wx.DefaultPosition, wx.Size( 150,20 ), m_cbSchemeChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbConnections" )
		self.m_cbScheme.SetSelection( 1 )
		bSizer23.Add( self.m_cbScheme, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		sbSizer1.Add( bSizer23, 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Motor Slots:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time" )
		self.lbl_refresh_time.Wrap( -1 )
		bSizer2.Add( self.lbl_refresh_time, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlSlots = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS, 6, 60, 6.000000, 3, u"m_ctrlPoles" )
		self.m_ctrlSlots.SetDigits( 0 )
		bSizer2.Add( self.m_ctrlSlots, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Coil loops:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1" )
		self.lbl_refresh_time1.Wrap( -1 )
		bSizer21.Add( self.lbl_refresh_time1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer21.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlLoops = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS, 1, 999, 12.000000, 1, u"m_ctrlLoops" )
		self.m_ctrlLoops.SetDigits( 0 )
		bSizer21.Add( self.m_ctrlLoops, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizer21, 1, wx.EXPAND, 5 )

		bSizer214 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time14 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Coil style:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time14" )
		self.lbl_refresh_time14.Wrap( -1 )
		bSizer214.Add( self.lbl_refresh_time14, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		bSizer214.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbStrategyChoices = [ u"Parallel", u"Radial" ]
		self.m_cbStrategy = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), m_cbStrategyChoices, 0, wx.DefaultValidator, u"m_cbStrategy" )
		self.m_cbStrategy.SetSelection( 1 )
		bSizer214.Add( self.m_cbStrategy, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizer214, 1, wx.EXPAND, 5 )

		bSizer2121 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time121 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"PCB preset:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time121" )
		self.lbl_refresh_time121.Wrap( -1 )
		bSizer2121.Add( self.lbl_refresh_time121, 0, wx.ALL, 5 )

		bSizer2121.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbPresetChoices =[ u"Custom", u"JLCPCB, 1-2L", u"JLCPCB, 4-6L" ]
		self.m_cbPreset = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"JLCPCB, 6L", wx.DefaultPosition, wx.Size( 150,20 ), m_cbPresetChoices, 0, wx.DefaultValidator, u"m_cbPreset" )
		self.m_cbPreset.SetSelection( 2 )
		self.m_cbPreset.Enable( False )
		bSizer2121.Add( self.m_cbPreset, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizer2121, 1, wx.EXPAND, 5 )

		bSizer212 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time12 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"PCB layers:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time12" )
		self.lbl_refresh_time12.Wrap( -1 )
		bSizer212.Add( self.lbl_refresh_time12, 0, wx.ALL, 5 )

		bSizer212.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_ctrlLayers = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS, 2, 20, 2, 2, u"m_ctrlLayers" )
		self.m_ctrlLayers.SetDigits( 0 )
		bSizer212.Add( self.m_ctrlLayers, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizer212, 1, wx.EXPAND, 5 )

		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time11 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Track width:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time11" )
		self.lbl_refresh_time11.Wrap( -1 )
		bSizer211.Add( self.lbl_refresh_time11, 0, wx.ALL, 5 )

		bSizer211.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time112 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time112" )
		self.lbl_refresh_time112.Wrap( -1 )
		bSizer211.Add( self.lbl_refresh_time112, 0, wx.ALL, 5 )

		self.m_ctrlTrackWidth = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0.127, 10, 0.134000, 0.001, u"m_ctrlTrackWidth" )
		self.m_ctrlTrackWidth.SetDigits( 3 )
		bSizer211.Add( self.m_ctrlTrackWidth, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizer211, 1, wx.EXPAND, 5 )
        
		# TRACK SPACING
		bSizerSpacing = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_spacing = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Track spacing:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_spacing" )
		self.lbl_spacing.Wrap( -1 )
		bSizerSpacing.Add( self.lbl_spacing, 0, wx.ALL, 5 )

		bSizerSpacing.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_spacing_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_spacing_unit" )
		self.lbl_spacing_unit.Wrap( -1 )
		bSizerSpacing.Add( self.lbl_spacing_unit, 0, wx.ALL, 5 )

		self.m_ctrlTrackSpacing = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0.09, 10, 0.150, 0.001, u"m_ctrlTrackSpacing" )
		self.m_ctrlTrackSpacing.SetDigits( 3 )
		bSizerSpacing.Add( self.m_ctrlTrackSpacing, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizerSpacing, 1, wx.EXPAND, 5 )
        
		# RING WIDTH (Sammelschienen Breite)
		bSizerRingW = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_ringW = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Ring track width:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringW" )
		self.lbl_ringW.Wrap( -1 )
		bSizerRingW.Add( self.lbl_ringW, 0, wx.ALL, 5 )

		bSizerRingW.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_ringW_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringW_unit" )
		self.lbl_ringW_unit.Wrap( -1 )
		bSizerRingW.Add( self.lbl_ringW_unit, 0, wx.ALL, 5 )

		self.m_ctrlRingWidth = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0.1, 10, 0.800, 0.05, u"m_ctrlRingWidth" )
		self.m_ctrlRingWidth.SetDigits( 3 )
		bSizerRingW.Add( self.m_ctrlRingWidth, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizerRingW, 1, wx.EXPAND, 5 )

		# RING SPACING (Sammelschienen Abstand)
		bSizerRingSpace = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_ringSpace = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Ring spacing:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringSpace" )
		self.lbl_ringSpace.Wrap( -1 )
		bSizerRingSpace.Add( self.lbl_ringSpace, 0, wx.ALL, 5 )

		bSizerRingSpace.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_ringSpace_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_ringSpace_unit" )
		self.lbl_ringSpace_unit.Wrap( -1 )
		bSizerRingSpace.Add( self.lbl_ringSpace_unit, 0, wx.ALL, 5 )

		self.m_ctrlRingSpacing = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0.09, 10, 0.250, 0.05, u"m_ctrlRingSpacing" )
		self.m_ctrlRingSpacing.SetDigits( 3 )
		bSizerRingSpace.Add( self.m_ctrlRingSpacing, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizerRingSpace, 1, wx.EXPAND, 5 )

		# VIA DIAMETER
		bSizerViaDia = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_viadia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Via Diameter:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_viadia" )
		self.lbl_viadia.Wrap( -1 )
		bSizerViaDia.Add( self.lbl_viadia, 0, wx.ALL, 5 )

		bSizerViaDia.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_viadia_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_viadia_unit" )
		self.lbl_viadia_unit.Wrap( -1 )
		bSizerViaDia.Add( self.lbl_viadia_unit, 0, wx.ALL, 5 )

		self.m_ctrlViaDia = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0.1, 10, 0.45, 0.05, u"m_ctrlViaDia" )
		self.m_ctrlViaDia.SetDigits( 3 )
		bSizerViaDia.Add( self.m_ctrlViaDia, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizerViaDia, 1, wx.EXPAND, 5 )

		# VIA DRILL
		bSizerViaDrill = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_viadrill = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Via Drill:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_viadrill" )
		self.lbl_viadrill.Wrap( -1 )
		bSizerViaDrill.Add( self.lbl_viadrill, 0, wx.ALL, 5 )

		bSizerViaDrill.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_viadrill_unit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_viadrill_unit" )
		self.lbl_viadrill_unit.Wrap( -1 )
		bSizerViaDrill.Add( self.lbl_viadrill_unit, 0, wx.ALL, 5 )

		self.m_ctrlViaDrill = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0.1, 10, 0.30, 0.05, u"m_ctrlViaDrill" )
		self.m_ctrlViaDrill.SetDigits( 3 )
		bSizerViaDrill.Add( self.m_ctrlViaDrill, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizerViaDrill, 1, wx.EXPAND, 5 )

		bSizerSupportHoleDia = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_supportHoleDia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Support TH hole dia:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_supportHoleDia" )
		self.lbl_supportHoleDia.Wrap( -1 )
		bSizerSupportHoleDia.Add( self.lbl_supportHoleDia, 0, wx.ALL, 5 )

		bSizerSupportHoleDia.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_supportHoleDiaUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_supportHoleDiaUnit" )
		self.lbl_supportHoleDiaUnit.Wrap( -1 )
		bSizerSupportHoleDia.Add( self.lbl_supportHoleDiaUnit, 0, wx.ALL, 5 )

		self.m_ctrlSupportHoleDia = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0.1, 10, 0.800, 0.05, u"m_ctrlSupportHoleDia" )
		self.m_ctrlSupportHoleDia.SetDigits( 3 )
		bSizerSupportHoleDia.Add( self.m_ctrlSupportHoleDia, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizerSupportHoleDia, 1, wx.EXPAND, 5 )

		bSizerSupportVia = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_supportVia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Support via mode:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_supportVia" )
		self.lbl_supportVia.Wrap( -1 )
		bSizerSupportVia.Add( self.lbl_supportVia, 0, wx.ALL, 5 )

		bSizerSupportVia.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbSupportViaModeChoices = [ u"0", u"2", u"4" ]
		self.m_cbSupportViaMode = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 150,20 ), m_cbSupportViaModeChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbSupportViaMode" )
		self.m_cbSupportViaMode.SetSelection( 1 )
		bSizerSupportVia.Add( self.m_cbSupportViaMode, 0, wx.ALL, 5 )
		self.m_cbSupportVias = self.m_cbSupportViaMode

		sbSizer1.Add( bSizerSupportVia, 1, wx.EXPAND, 5 )

		bSizer22111 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time2111 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Track fillet radius:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time2111" )
		self.lbl_refresh_time2111.Wrap( -1 )
		bSizer22111.Add( self.lbl_refresh_time2111, 0, wx.ALL, 5 )

		bSizer22111.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time1122 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1122" )
		self.lbl_refresh_time1122.Wrap( -1 )
		bSizer22111.Add( self.lbl_refresh_time1122, 0, wx.ALL, 5 )

		self.m_ctrlRfill = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 100, 0.000000, 0.1, u"m_ctrlRfill" )
		self.m_ctrlRfill.SetDigits( 3 )
		bSizer22111.Add( self.m_ctrlRfill, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizer22111, 1, wx.EXPAND, 5 )

		bSizerInnerFill = wx.BoxSizer( wx.HORIZONTAL )

		self.m_cbFillInnerGND = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Fill inner area with GND", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"m_cbFillInnerGND" )
		self.m_cbFillInnerGND.SetValue( True ) 
		self.m_chkFillInnerGnd = self.m_cbFillInnerGND
		bSizerInnerFill.Add( self.m_cbFillInnerGND, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizerInnerFill.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_innerFillDia = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Dia:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_innerFillDia.Wrap( -1 )
		bSizerInnerFill.Add( self.lbl_innerFillDia, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_ctrlInnerGndDia = SpinCtrlDoublePersist( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 120,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 500, 0.000000, 0.1, u"m_ctrlInnerGndDia" )
		self.m_ctrlInnerGndDia.SetDigits( 3 )
		self.m_ctrlInnerGndDia.SetToolTip( u"Inner GND fill diameter [mm], 0 = auto" )
		bSizerInnerFill.Add( self.m_ctrlInnerGndDia, 0, wx.ALL, 5 )

		self.lbl_innerFillDiaUnit = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_innerFillDiaUnit.Wrap( -1 )
		bSizerInnerFill.Add( self.lbl_innerFillDiaUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		sbSizer1.Add( bSizerInnerFill, 1, wx.EXPAND, 5 )

		self.m_cbFillOuterGND = wx.CheckBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Fill outer area with GND", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"m_cbFillOuterGND" )
		self.m_cbFillOuterGND.SetValue( True ) 
		self.m_chkFillOuterGnd = self.m_cbFillOuterGND
		sbSizer1.Add( self.m_cbFillOuterGND, 0, wx.ALL, 5 )

		bSizer271 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time131122 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Terminal pads:", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1311" )
		self.lbl_refresh_time131122.Wrap( -1 )
		bSizer271.Add( self.lbl_refresh_time131122, 0, wx.ALL, 5 )

		bSizer271.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_cbTPChoices =[ u"None", u"THT", u"SMD" ]
		self.m_cbTP = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"THT", wx.DefaultPosition, wx.Size( 90,20 ), m_cbTPChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbTP" )
		self.m_cbTP.SetSelection( 0 )
		bSizer271.Add( self.m_cbTP, 0, wx.ALL, 5 )

		self.lbl_refresh_time1311221 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"[mm2]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1311" )
		self.lbl_refresh_time1311221.Wrap( -1 )
		bSizer271.Add( self.lbl_refresh_time1311221, 0, wx.ALL, 5 )

		m_termSizeChoices =[ u"0.1", u"0.15", u"0.25", u"0.5", u"0.75", u"1.0", u"1.5", u"2.0", u"2.5" ]
		self.m_termSize = wx.ComboBox( sbSizer1.GetStaticBox(), wx.ID_ANY, u"0.1", wx.DefaultPosition, wx.Size( 150,20 ), m_termSizeChoices, wx.CB_DROPDOWN|wx.CB_READONLY, wx.DefaultValidator, u"m_cbTPSize" )
		self.m_termSize.SetSelection( 1 )
		bSizer271.Add( self.m_termSize, 0, wx.ALL, 5 )

		sbSizer1.Add( bSizer271, 1, wx.EXPAND, 5 )

		bSizerMainRow.Add( sbSizer1, 15, wx.EXPAND|wx.ALL, 6 )

		sbSizer111 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Physics / Stats" ), wx.VERTICAL )

		bSizer2112 = wx.BoxSizer( wx.HORIZONTAL )

		self.lbl_refresh_time113 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"Temperature (ambient):", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time113" )
		self.lbl_refresh_time113.Wrap( -1 )
		bSizer2112.Add( self.lbl_refresh_time113, 0, wx.ALL, 5 )

		bSizer2112.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.lbl_refresh_time1121 = wx.StaticText( sbSizer111.GetStaticBox(), wx.ID_ANY, u"[°C]", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_refresh_time1121" )
		self.lbl_refresh_time1121.Wrap( -1 )
		bSizer2112.Add( self.lbl_refresh_time1121, 0, wx.ALL, 5 )

		self.m_ambT = SpinCtrlDoublePersist( sbSizer111.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,20 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, -50, 150, 20, 0.1, u"m_ambT" )
		self.m_ambT.SetDigits( 1 )
		bSizer2112.Add( self.m_ambT, 0, wx.ALL, 5 )

		sbSizer111.Add( bSizer2112, 1, wx.EXPAND, 5 )

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

		sbSizer111.Add( bSizer21321, 1, wx.EXPAND, 5 )

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

		sbSizer111.Add( bSizer21312, 1, wx.EXPAND, 5 )

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

		sbSizer111.Add( bSizerTotalR, 1, wx.EXPAND, 5 )

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

		sbSizer111.Add( bSizerCoilR, 1, wx.EXPAND, 5 )

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

		sbSizer111.Add( bSizerRingR, 1, wx.EXPAND, 5 )

		bSizerMainRow.Add( sbSizer111, 10, wx.EXPAND|wx.ALL, 6 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_load = wx.Button( self, wx.ID_OK, u"Load", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_ok" )
		bSizer3.Add( self.btn_load, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btn_save = wx.Button( self, wx.ID_OK, u"Save", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_ok" )
		bSizer3.Add( self.btn_save, 0, wx.ALL, 5 )

		bSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.btn_clear = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_clear" )
		self.btn_clear.Enable( False )
		self.btn_clear.Hide()
		bSizer3.Add( self.btn_clear, 0, wx.ALL, 5 )

		self.btn_ok = wx.Button( self, wx.ID_OK, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0, wx.DefaultValidator, u"btn_ok" )
		bSizer3.Add( self.btn_ok, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		bSizer5.Add( bSizer3, 0, wx.EXPAND|wx.TOP, 5 )

		sbSizerStatus = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Status" ), wx.VERTICAL )

		self.lbl_status = wx.StaticText( sbSizerStatus.GetStaticBox(), wx.ID_ANY, u"Ready", wx.DefaultPosition, wx.DefaultSize, 0, u"lbl_status" )
		self.lbl_status.Wrap( -1 )
		sbSizerStatus.Add( self.lbl_status, 0, wx.ALL, 5 )

		self.m_txtStatus = wx.TextCtrl( sbSizerStatus.GetStaticBox(), wx.ID_ANY, u"Ready.", wx.DefaultPosition, wx.Size( -1,60 ), wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_SIMPLE, wx.DefaultValidator, u"m_txtStatus" )
		sbSizerStatus.Add( self.m_txtStatus, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

		bSizerMainRow.Add( sbSizerStatus, 6, wx.EXPAND|wx.ALL, 6 )

		# Visual cleanup: emphasize section blocks with bold titles and clear borders.
		def _style_staticbox(box):
			if not box:
				return
			f = box.GetFont()
			f.SetWeight(wx.FONTWEIGHT_BOLD)
			# Use own font on the static box label only; avoid inheriting bold
			# style into all child controls.
			box.SetOwnFont(f)
			try:
				box.SetWindowStyleFlag(box.GetWindowStyleFlag() | wx.BORDER_SIMPLE)
			except Exception:
				pass

		for _sb in (sbSizer2, sbSizer1, sbSizer111, sbSizerStatus):
			_style_staticbox(_sb.GetStaticBox())

		# Restore normal font on all children to prevent label truncation caused
		# by inherited bold fonts on some GTK themes.
		_normal_font = self.GetFont()
		for _c in self.GetChildren():
			if not isinstance(_c, wx.StaticBox):
				_c.SetOwnFont(_normal_font)
				try:
					_c.InvalidateBestSize()
				except Exception:
					pass

		# Keep readable label area in the two input-heavy columns.
		sbSizer2.GetStaticBox().SetMinSize(wx.Size(500, -1))
		sbSizer1.GetStaticBox().SetMinSize(wx.Size(500, -1))
		sbSizer111.GetStaticBox().SetMinSize(wx.Size(380, -1))
		sbSizerStatus.GetStaticBox().SetMinSize(wx.Size(280, -1))

		# Free horizontal space for labels: shrink wide value widgets a bit.
		for _c in self.GetChildren():
			if isinstance(_c, (wx.ComboBox, wx.SpinCtrlDouble)):
				w, h = _c.GetSize()
				if w >= 150:
					_c.SetMinSize(wx.Size(110, h))
					_c.SetSize(wx.Size(110, h))

		bSizer5.Insert( 0, bSizerMainRow, 1, wx.EXPAND|wx.TOP, 8 )
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
		self.btn_load.Bind( wx.EVT_BUTTON, self.on_btn_load )
		self.btn_save.Bind( wx.EVT_BUTTON, self.on_btn_save )
		self.btn_clear.Bind( wx.EVT_BUTTON, self.on_btn_clear )
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
	def on_btn_load( self, event ):
		event.Skip()
	def on_btn_save( self, event ):
		event.Skip()
	def on_btn_clear( self, event ):
		event.Skip()
	def on_btn_generate( self, event ):
		event.Skip()
