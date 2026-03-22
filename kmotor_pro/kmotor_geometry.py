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
    safe_n = max(n_edge, 1e-9)
    cos_val = math.cos(math.pi / safe_n)
    rp = r / max(cos_val, 1e-6)
    thp = 2 * math.pi / safe_n
    tho = thp / 2
    pts = []
    for i in range(int(n_edge)):
        pts.append((
            int(rp * math.cos(i * thp + tho)),
            int(rp * math.sin(i * thp + tho))
        ))
    return pts


def outline_outer_radius(r_out, n_edges):
    """Calculate outer radius including outline edges."""
    if abs(n_edges) < 1e-9:
        return float(r_out)
    cos_val = math.cos(math.pi / max(n_edges, 1e-9))
    return float(r_out) / max(cos_val, 1e-6)
# Methods for geometry



    def _point_xy(self, pt):
        if hasattr(pt, "x") and hasattr(pt, "y"):
            return float(pt.x), float(pt.y)
        try:
            return float(pt[0,0]), float(pt[0,1])
        except Exception:
            flat = np.asarray(pt).reshape(-1)
            return float(flat[0]), float(flat[1])



    def _as_point(self, x, y):
        return self.fpoint(int(round(x)), int(round(y)))



    def _point_radius(self, pt):
        x, y = self._point_xy(pt)
        return math.hypot(x, y)



    def _nearest_point_distance(self, radius, angle, pts):
        target = np.array([radius * math.cos(angle), radius * math.sin(angle)])
        best = None
        for pt in pts:
            x, y = self._point_xy(pt)
            dist = math.hypot(x - target[0], y - target[1])
            if best is None or dist < best:
                best = dist
        return best



    def _rotate_xy(self, xy, angle):
        x, y = xy
        ca = math.cos(angle)
        sa = math.sin(angle)
        return (x * ca - y * sa, x * sa + y * ca)



    def _rotate_about_xy(self, xy, center_xy, angle):
        x, y = xy
        cx, cy = center_xy
        xr, yr = self._rotate_xy((x - cx, y - cy), angle)
        return (xr + cx, yr + cy)



    def _offset_xy(self, xy, origin_xy):
        return (xy[0] + origin_xy[0], xy[1] + origin_xy[1])



    def add_rotated_line_block(step_deg_local, span_deg_local, tick_len, width):
            count = max(1, int(round(span_deg_local / step_deg_local)))
            base_anchor = helper_center
            base_q0 = tuple(base_anchor)
            base_q1 = tuple(base_anchor + inward * tick_len)
            for idx in range(-count, count + 1):
                delta = math.radians(idx * step_deg_local)
                q0 = self._rotate_xy(base_q0, delta)
                q1 = self._rotate_xy(base_q1, delta)
                self._add_silk_segment(
                    q0,
                    q1,
                    width=width,
                    clip_to_outline=True,
                    clip_margin=0.35 * self.SCALE,
                )

        # Coarse degree marks: 1 degree, longer lines, opposite side of the helper line.
        add_rotated_line_block(
            1.0,
            angle_span,
            tick_len=max(7.0 * self.SCALE, 4.0 * hole_radius),
            width=max(1, 0.08 * self.SCALE),
        )

        # Fine degree marks: current step, short lines close to the helper line.
        add_rotated_line_block(
            step_deg,
            angle_span,
            tick_len=max(2.2 * self.SCALE, 1.2 * hole_radius),
            width=max(1, 0.10 * self.SCALE),
        )



    def _iter_outer_mount_points(self):
        if self.n_edges == 4 and self.corner_hole_offset > 0:
            corners = self._get_outline_corners()
            if corners and len(corners) >= 4:
                xs = [p[0] for p in corners]
                ys = [p[1] for p in corners]
                max_x = max(xs)
                max_y = max(ys)
                off = float(self.corner_hole_offset)
                dia = max(float(self.corner_hole_dia), 0.0)
                d = off / math.sqrt(2.0)
                points = [
                    ( max_x - d,  max_y - d, math.radians(45.0), dia),
                    (-max_x + d,  max_y - d, math.radians(135.0), dia),
                    (-max_x + d, -max_y + d, math.radians(225.0), dia),
                    ( max_x - d, -max_y + d, math.radians(315.0), dia),
                ]
                return points[:max(0, min(len(points), int(self.corner_hole_count)))]
        if self.n_mh_out <= 0 or self.r_mh_out <= 0:
            return []
        radius = float(self.r_mh_out)
        if self.n_edges > 0:
            radius /= max(math.cos(math.pi / self.n_edges), 1e-6)
        th0 = 2 * math.pi / self.n_mh_out
        points = []
        for idx in range(self.n_mh_out):
            angle = th0 * idx + th0 / 2.0
            points.append((radius * math.cos(angle), radius * math.sin(angle), angle, max(float(self.corner_hole_dia), 3.2 * self.SCALE)))
        return points



    def _iter_corner_points_for_origin(self, origin_xy):
        if self.n_edges == 4 and self.corner_hole_offset > 0:
            max_x = float(self.r_out)
            max_y = float(self.r_out)
            off = float(self.corner_hole_offset)
            dia = max(float(self.corner_hole_dia), 0.0)
            d = off / math.sqrt(2.0)
            pts = [
                ( origin_xy[0] + max_x - d, origin_xy[1] + max_y - d, math.radians(45.0), dia),
                ( origin_xy[0] - max_x + d, origin_xy[1] + max_y - d, math.radians(135.0), dia),
                ( origin_xy[0] - max_x + d, origin_xy[1] - max_y + d, math.radians(225.0), dia),
                ( origin_xy[0] + max_x - d, origin_xy[1] - max_y + d, math.radians(315.0), dia),
            ]
            return pts[:max(0, min(len(pts), int(self.corner_hole_count)))]
        return []



    def add_rotated_line_block(step_deg_local, span_deg_local, tick_len, width):
            count = max(1, int(round(span_deg_local / step_deg_local)))
            base_anchor = tuple(helper_center)
            base_q0 = base_anchor
            base_q1 = tuple(helper_center + inward * tick_len)
            for idx in range(-count, count + 1):
                delta = math.radians(idx * step_deg_local)
                q0 = self._rotate_about_xy(base_q0, origin_xy, delta)
                q1 = self._rotate_about_xy(base_q1, origin_xy, delta)
                self._add_grouped_silk_segment(group, q0, q1, width=width)

        add_rotated_line_block(
            1.0,
            angle_span,
            tick_len=max(7.0 * self.SCALE, 4.0 * hole_radius),
            width=max(1, 0.08 * self.SCALE),
        )
        add_rotated_line_block(
            step_deg,
            angle_span,
            tick_len=max(2.2 * self.SCALE, 1.2 * hole_radius),
            width=max(1, 0.10 * self.SCALE),
        )



    def _build_offset_outline(self, group, origin_xy):
        cx, cy = origin_xy
        self._add_grouped_edge_circle(group, origin_xy, self.r_in)
        relief_dia = max(min(0.12 * (2.0 * self.r_in), 2.0 * self.SCALE), 0.8 * self.SCALE) if self.r_in > 0 else 0
        if relief_dia > 0 and self.r_in > (1.5 * relief_dia):
            relief_radius = self.r_in + (0.5 * relief_dia)
            for angle in (math.pi / 4.0, 3.0 * math.pi / 4.0, 5.0 * math.pi / 4.0, 7.0 * math.pi / 4.0):
                rp = (
                    cx + relief_radius * math.cos(angle),
                    cy + relief_radius * math.sin(angle),
                )
                self._add_grouped_edge_circle(group, rp, relief_dia / 2.0)

        if self.n_edges == 0:
            self._add_grouped_edge_circle(group, origin_xy, self.r_out)
            return

        points = self._outline_poly_points(self.r_out, self.n_edges)
        if not points:
            return
        pts = [self._offset_xy(self._point_xy(pt), origin_xy) for pt in points]
        for i in range(len(pts)):
            self._add_grouped_silk_segment(group, pts[i], pts[(i + 1) % len(pts)], width=max(1, 0.09 * self.SCALE))
            seg = pcbnew.PCB_SHAPE(self.board, pcbnew.SHAPE_T_SEGMENT)
            seg.SetStart(self._as_point(pts[i][0], pts[i][1]))
            seg.SetEnd(self._as_point(pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1]))
            seg.SetLayer(pcbnew.Edge_Cuts)
            self.board.Add(seg)
            if group is not None:
                group.AddItem(seg)



    def _build_offset_mounting_holes(self, group, origin_xy):
        if self.mhs == "None":
            return
        fp_lib = self.fp_path + 'MountingHole.pretty'
        fp = self.mhole_db.get(self.mhs)
        if not fp:
            return
        ni_gnd = self.board.FindNet("gnd")

        if self.n_mh_out > 0:
            r_mh_out = float(self.r_mh_out)
            if self.n_edges > 0:
                r_mh_out /= max(math.cos(math.pi / self.n_edges), 1e-6)
            th0 = 2 * math.pi / self.n_mh_out
            for i in range(self.n_mh_out):
                pos = (
                    origin_xy[0] + r_mh_out * math.cos(th0 * i + th0 / 2.0),
                    origin_xy[1] + r_mh_out * math.sin(th0 * i + th0 / 2.0),
                )
                self._add_mounting_hole_fp_at(group, pos, fp_lib, fp, f"MMO_{i}", net=ni_gnd)

        if self.n_mh_in > 0:
            th0 = 2 * math.pi / self.n_mh_in
            for i in range(self.n_mh_in):
                pos = (
                    origin_xy[0] + float(self.r_mh_in) * math.cos(th0 * i + th0 / 2.0),
                    origin_xy[1] + float(self.r_mh_in) * math.sin(th0 * i + th0 / 2.0),
                )
                self._add_mounting_hole_fp_at(group, pos, fp_lib, fp, f"MMI_{i}", net=ni_gnd)

        if getattr(self, "silk_hole_scales", False):
            for x, y, angle, dia in self._iter_corner_points_for_origin(origin_xy):
                self._add_linear_hole_scale_at(group, (x, y), angle, max(dia * 0.5, 0.5 * self.SCALE), origin_xy)


    def mpt_point(idx):
            x, y = self._point_xy(mpt[idx])
            return self.fpoint(int(x), int(y))

        ip = 0
        t0 = None
        nseg = n_loops * 4 - 1

        actual_start = None
        actual_end = None
        skipped_inner_bridge = False

        for seg in range(nseg):
            ps = mpt_point(ip)

            is_arc = (not seg % 2)
            if is_arc:
                ip += 1
                mid_pt = mpt_point(ip)
                side = -1 if not seg % 4 else 1

            ip += 1
            pe = mpt_point(ip)

            d_s = math.hypot(ps.x, ps.y)
            d_e = math.hypot(pe.x, pe.y)
            # Remove only the inner bridge on terminal layers.
            # This is geometric, so it won't drop an outer coil segment by index mismatch.
            if (is_first_layer or is_last_layer):
                if (not skipped_inner_bridge) and abs(d_s - self.r_coil_in) < self.SCALE * 0.5 and abs(d_e - self.r_coil_in) < self.SCALE * 0.5:
                    # Break fillet chain when the inner bridge is intentionally removed.
                    # Otherwise the next segment is filleted against a non-adjacent segment
                    # and we lose one visible coil segment.
                    t0 = None
                    skipped_inner_bridge = True
                    continue

            if actual_start is None:
                actual_start = ps
            actual_end = pe

            if is_arc:
                t = pcbnew.PCB_ARC(self.board)
                t.SetMid(mid_pt)
            else:
                t = pcbnew.PCB_TRACK(self.board)

            t.SetWidth(self.trk_w)
            t.SetLayer(layer)
            t.SetStart(ps)
            t.SetEnd(pe)
            self.board.Add(t)

            net_coil = self.board.FindNet("coil")
            if net_coil:
                t.SetNet(net_coil)

            if t0 is not None and self.r_fill > 0:
                self.fillet(self.board, t0, t, self.r_fill, side)

            group.AddItem(t)
            t0 = t

        if actual_start is None:
            actual_start = mpt_point(0)
        if actual_end is None:
            actual_end = actual_start

        return [actual_start, actual_end]



    def as_inset_point(radius):
            rr = max(radius - via_inset, 0.0)
            return self._as_point(rr * math.cos(th_center), rr * math.sin(th_center))



    def _outline_poly_points(self, r, n_edge):
        if n_edge < 4:
            return None
        rp = r / math.cos(math.pi / n_edge)
        thp = 2 * math.pi / n_edge
        tho = thp / 2
        pts = []
        for i in range(n_edge):
            pts.append(
                self.fpoint(
                    int(rp * math.cos(i * thp + tho)),
                    int(rp * math.sin(i * thp + tho))
                )
            )
        return pts

