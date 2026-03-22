# kmotor_geometry.py
# Pure geometry generation for KMotor_Pro
# Generated during Phase 1 refactoring

import math
import numpy as np


def point_xy(pt):
    """Extract x, y from various point formats."""
    if hasattr(pt, "x") and hasattr(pt, "y"):
        return float(pt.x), float(pt.y)
    try:
        return float(pt[0, 0]), float(pt[0, 1])
    except Exception:
        flat = np.asarray(pt).reshape(-1)
        return float(flat[0]), float(flat[1])


def radial_vector(angle, radius=1.0):
    """Calculate radial vector at given angle."""
    return np.array([radius * math.cos(angle), radius * math.sin(angle)])


def tangent_vector(angle, scale=1.0):
    """Calculate tangent vector at given angle."""
    return np.array([-scale * math.sin(angle), scale * math.cos(angle)])


def point_radius(pt):
    """Calculate radius of point from origin."""
    x, y = point_xy(pt)
    return math.hypot(x, y)


def rotate_xy(xy, angle):
    """Rotate point around origin."""
    x, y = xy
    ca = math.cos(angle)
    sa = math.sin(angle)
    return (x * ca - y * sa, x * sa + y * ca)


def rotate_about_xy(xy, center_xy, angle):
    """Rotate point around given center."""
    x, y = xy
    cx, cy = center_xy
    xr, yr = rotate_xy((x - cx, y - cy), angle)
    return (xr + cx, yr + cy)


def offset_xy(xy, origin_xy):
    """Offset point by origin."""
    return (xy[0] + origin_xy[0], xy[1] + origin_xy[1])


def clip_segment_to_outline_box(start_xy, end_xy, bounds, margin=0.0):
    """Clip line segment to rectangular outline bounds."""
    if not bounds:
        return start_xy, end_xy

    xmin, xmax, ymin, ymax = bounds
    xmin += margin
    xmax -= margin
    ymin += margin
    ymax -= margin

    x0, y0 = start_xy
    x1, y1 = end_xy
    dx = x1 - x0
    dy = y1 - y0
    p = (-dx, dx, -dy, dy)
    q = (x0 - xmin, xmax - x0, y0 - ymin, ymax - y0)
    u1 = 0.0
    u2 = 1.0

    for pi, qi in zip(p, q):
        if abs(pi) < 1e-12:
            if qi < 0:
                return None
            continue
        t = qi / pi
        if pi < 0:
            if t > u2:
                return None
            u1 = max(u1, t)
        else:
            if t < u1:
                return None
            u2 = min(u2, t)

    return (
        (x0 + u1 * dx, y0 + u1 * dy),
        (x0 + u2 * dx, y0 + u2 * dy),
    )


def outline_poly_points(r, n_edge):
    """Generate polygon points for outline."""
    if n_edge < 4:
        return None
    rp = r / math.cos(math.pi / n_edge)
    thp = 2 * math.pi / n_edge
    tho = thp / 2
    pts = []
    for i in range(n_edge):
        pts.append((
            int(rp * math.cos(i * thp + tho)),
            int(rp * math.sin(i * thp + tho))
        ))
    return pts


def outline_outer_radius(r_out, n_edges):
    """Calculate outer radius including outline edges."""
    if n_edges == 0:
        return float(r_out)
    return float(r_out) / max(math.cos(math.pi / n_edges), 1e-6)
