# KiCad loads this package on startup to register the ActionPlugin.
# When imported outside KiCad's embedded Python (e.g. system python),
# wx/pcbnew are typically unavailable. Keep import side-effects safe.
try:
    from .kimotor_action import KiMotor
except ModuleNotFoundError:
    KiMotor = None

if KiMotor is not None:
    KiMotor().register()
