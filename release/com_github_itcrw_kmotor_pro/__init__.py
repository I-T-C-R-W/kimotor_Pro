# KMotor_Pro is a GPL-2.0-only fork of KiMotor by Stefano Cottafavi.
# KiCad loads this package on startup to register the ActionPlugin.
# When imported outside KiCad's embedded Python (e.g. system python),
# wx/pcbnew are typically unavailable. Keep import side-effects safe.
try:
    from .kmotor_pro_action import KMotorProPlugin
except ModuleNotFoundError:
    KMotorProPlugin = None

if KMotorProPlugin is not None:
    KMotorProPlugin().register()
