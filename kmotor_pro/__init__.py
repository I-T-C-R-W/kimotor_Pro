# -*- coding: utf-8 -*-
# KMotor_Pro - Parametric PCB motor generator for KiCad
# Copyright 2026 I-T-C-R-W
# SPDX-License-Identifier: GPL-2.0-only

try:
    from .kmotor_api import KMotorProPlugin
except ModuleNotFoundError:
    KMotorProPlugin = None

if KMotorProPlugin is not None:
    KMotorProPlugin().register()
