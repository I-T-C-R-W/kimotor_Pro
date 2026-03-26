# Forked from KiMotor by Stefano Cottafavi.
# Copyright 2022 Stefano Cottafavi <stefano.cottafavi@gmail.com>.
# Copyright 2026 I-T-C-R-W
# SPDX-License-Identifier: GPL-2.0-only

import math
import shutil
import traceback
from datetime import datetime

import wx 
import pcbnew
import wx.lib.agw.persist as PM
import wx.lib.agw.persist.persist_handlers as ph
import wx.lib.agw.persist.persistencemanager as pm


def eda_angle(angle, kicad_version):
    if kicad_version < 7:
        return angle * 180 / math.pi * 100
    return pcbnew.EDA_ANGLE(angle, pcbnew.RADIANS_T)


def init_persist(dialog, config_file):
    manager = PM.PersistenceManager.Get()
    manager.SetPersistenceFile(config_file)
    manager.RegisterAndRestoreAll(dialog)
    return manager


def set_status(dialog, text):
    ts = datetime.now().strftime("%H:%M:%S")
    if hasattr(dialog, "lbl_status") and dialog.lbl_status:
        dialog.lbl_status.SetLabel(str(text))
        dialog.lbl_status.GetParent().Layout()
    if hasattr(dialog, "m_txtStatus") and dialog.m_txtStatus:
        dialog.m_txtStatus.SetValue(f"[{ts}] {text}")


def format_exception(exc):
    msg = str(exc).strip()
    return msg if msg else exc.__class__.__name__


def log_exception(title, exc, format_exception_fn=format_exception):
    detail = format_exception_fn(exc)
    tb = traceback.format_exc().strip()
    if tb:
        wx.LogError(f"{title}:\n{detail}\n\n{tb}")
    else:
        wx.LogError(f"{title}:\n{detail}")


def safe_ui_yield(dialog):
    try:
        dialog.Update()
        wx.YieldIfNeeded()
    except Exception:
        pass


def safe_refresh_board(board):
    try:
        board.BuildConnectivity()
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


def run_action(start_status, success_status, title, callback, set_status_fn, safe_ui_yield_fn, safe_refresh_board_fn, format_exception_fn, log_exception_fn, update_magnet_summary=None, summary_target=None):
    set_status_fn(start_status)
    safe_ui_yield_fn()
    try:
        result = callback()
        safe_refresh_board_fn()
        set_status_fn(success_status)
        return result
    except Exception as exc:
        message = format_exception_fn(exc)
        set_status_fn(f"{title} failed")
        if summary_target == "magnet" and update_magnet_summary is not None:
            update_magnet_summary(message)
        log_exception_fn(f"{title} failed", exc)
        return None

class SpinCtrlDoublePersist(wx.SpinCtrlDouble, pm.PersistentObject):
    def __init__(self, parent, id=-1, value="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.SP_ARROW_KEYS, min=0, max=100, initial=0, inc=1, name="wxSpinCtrlDouble"):
        wx.SpinCtrlDouble.__init__(self, parent, id, value, pos, size, style, min, max, initial, inc, name)
        pm.PersistentObject.__init__(self, self, ph.SpinHandler) 


def update_magnet_summary(dialog, text):
    if hasattr(dialog, "lblMagnetSummary") and dialog.lblMagnetSummary:
        dialog.lblMagnetSummary.SetLabel(text)
        dialog.lblMagnetSummary.Wrap(520)
        dialog.lblMagnetSummary.GetParent().Layout()


def handle_close(pm_obj, event, set_status_fn, log_exception_fn):
    try:
        pm_obj.SaveAndUnregister()
    except Exception as exc:
        set_status_fn("Close warning")
        log_exception_fn("Close persistence failed", exc)
    event.Skip()


def resolve_pcb_preset(preset_name, presets):
    if preset_name == "Custom":
        return None
    presets = presets or {}
    return presets.get(preset_name)


def apply_pcb_preset_values(preset, layer_ctrl, track_width_ctrl, track_spacing_ctrl, ring_width_ctrl, ring_spacing_ctrl, via_dia_ctrl, via_drill_ctrl, copper_weight_ctrl=None):
    layer_ctrl.SetValue(preset["layers"])
    track_width_ctrl.SetValue(preset["track_width"])
    track_spacing_ctrl.SetValue(preset["track_spacing"])
    ring_width_ctrl.SetValue(preset["ring_width"])
    ring_spacing_ctrl.SetValue(preset["ring_spacing"])
    via_dia_ctrl.SetValue(preset["via_dia"])
    via_drill_ctrl.SetValue(preset["via_drill"])
    if copper_weight_ctrl is not None:
        idx = copper_weight_ctrl.FindString(preset["copper_weight"])
        if idx != wx.NOT_FOUND:
            copper_weight_ctrl.SetSelection(idx)


def clear_group(group, clear_button=None):
    if group:
        group.RemoveAll()
        group = None
        if clear_button is not None:
            clear_button.Enable(False)
    return group


def handle_action_event(event, run_action_fn, start_status, success_status, title, callback, summary_target=None):
    run_action_fn(start_status, success_status, title, callback, summary_target=summary_target)
    event.Skip()


def run_callbacks(*callbacks):
    result = None
    for callback in callbacks:
        result = callback()
    return result


def run_event_callbacks(*callbacks):
    result = None
    for callback in callbacks:
        result = callback(None)
    return result


def read_selection(ctrl, default=""):
    if ctrl is None:
        return default
    return ctrl.GetStringSelection()


def read_int(ctrl, default=0):
    if ctrl is None:
        return default
    return int(ctrl.GetValue())


def read_float(ctrl, default=0.0):
    if ctrl is None:
        return default
    return float(ctrl.GetValue())


def read_scaled(ctrl, scale, default=0.0):
    return int(read_float(ctrl, default) * scale)


def read_scaled_radius(ctrl, scale, default=0.0):
    return int(read_float(ctrl, default) / 2 * scale)


def read_toggle(primary=None, fallback=None, default=False):
    ctrl = primary if primary is not None else fallback
    if ctrl is None:
        return default
    if hasattr(ctrl, "IsChecked"):
        return bool(ctrl.IsChecked())
    return bool(ctrl.GetValue())


def read_index(ctrl, default=0):
    if ctrl is None:
        return default
    return ctrl.GetSelection()


def read_selection_with_fallback(primary=None, fallback=None, default=""):
    ctrl = primary if primary is not None else fallback
    return read_selection(ctrl, default)


def read_nonnegative_scaled(ctrl, scale, default=0.0):
    return int(max(0.0, read_float(ctrl, default)) * scale)


def assign_attributes(target, values):
    for key, value in values.items():
        setattr(target, key, value)
    return target


def prepare_model_inputs(*callbacks):
    try:
        for callback in callbacks:
            callback()
    except Exception:
        return False
    return True


def resolve_stats(stats, fallback):
    if stats is None:
        return fallback or {}
    return stats or {}


def save_preset_dialog(parent, json_str, default_filename="kmotor_pro.json"):
    with wx.FileDialog(
        parent,
        "Save KMotor_Pro preset",
        wildcard="JSON files (*.json)|*.json|KMT files (*.kmt)|*.kmt",
        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
    ) as file_dialog:
        file_dialog.SetFilename(default_filename)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return False
        target = file_dialog.GetPath()
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(json_str)
    return True


def choose_preset_to_load(parent):
    with wx.FileDialog(
        parent,
        "Load KMotor_Pro preset",
        wildcard="JSON files (*.json)|*.json|KMT files (*.kmt)|*.kmt",
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
    ) as file_dialog:
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return None
        return file_dialog.GetPath(), file_dialog.GetDirectory()


def load_json_preset(origin, config_cls):
    with open(origin, "r", encoding="utf-8") as handle:
        json_str = handle.read()
    return config_cls.from_json(json_str)


def load_legacy_preset(origin, directory, target, pm_obj, dialog):
    tmp = directory + "/kmotor_pro.tmp"
    pm_obj.SetPersistenceFile(tmp)
    pm_obj.SaveAndUnregister()
    shutil.copyfile(origin, target)
    pm_obj.SetPersistenceFile(target)
    pm_obj.RegisterAndRestoreAll(dialog)


def skip_event(event):
    if event is not None:
        event.Skip()


def handle_preset_event(event, preset_ctrl, apply_preset_fn, set_status_fn):
    if preset_ctrl is None:
        skip_event(event)
        return None
    preset_name = preset_ctrl.GetStringSelection()
    applied = apply_preset_fn(preset_name)
    if applied:
        set_status_fn(f"Preset applied: {preset_name}")
    skip_event(event)
    return applied


def handle_outline_event(selection, dout_ctrl, fillet_ctrl, event=None):
    enabled = selection != "None"
    dout_ctrl.Enable(enabled)
    fillet_ctrl.Enable(enabled)
    skip_event(event)


def read_layer_count(layer_ctrl):
    return int(layer_ctrl.GetValue())


def handle_terminal_type_event(pads, term_db, term_size_ctrl, event=None):
    if pads == "None":
        term_size_ctrl.Enable(False)
        skip_event(event)
        return
    if pads in ("THT", "SMD"):
        keys = list((term_db or {}).get(pads, {}).keys())
        for idx, key in enumerate(keys):
            term_size_ctrl.SetString(idx, key)
        while len(keys) < term_size_ctrl.GetCount():
            term_size_ctrl.Delete(term_size_ctrl.GetCount() - 1)
        term_size_ctrl.SetValue(term_size_ctrl.GetString(term_size_ctrl.GetCurrentSelection()))
        term_size_ctrl.Enable(True)
    skip_event(event)


def handle_winding_mode_event(mode, pcb_ctrls, wire_ctrls, event=None):
    is_pcb = (mode == "PCB")
    for ctrl in pcb_ctrls:
        ctrl.Enable(is_pcb)
    for ctrl in wire_ctrls:
        ctrl.Enable(not is_pcb)
    skip_event(event)


def handle_magnet_shape_event(shape, round_ctrls, rect_ctrls, update_magnet_summary_fn, event=None):
    is_round = (shape == "Round")
    for ctrl in round_ctrls:
        ctrl.Enable(is_round)
    for ctrl in rect_ctrls:
        ctrl.Enable(not is_round)
    update_magnet_summary_fn(
        "Round magnets use Magnet dia. Rect magnets use width (B) and height (H). "
        "Use Generate Magnet PCB for a first fit-check against ring diameter and pole count."
    )
    skip_event(event)
