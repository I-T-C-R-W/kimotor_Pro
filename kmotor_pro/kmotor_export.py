# kmotor_export.py
# Export functionality for KMotor_Pro (SVG, DXF)
# Generated during Phase 5 refactoring

import math
import numpy as np
from typing import List, Tuple, Optional


def coils_to_svg_paths(coil_points: np.ndarray, scale: float = 1.0) -> str:
    """Convert coil points to SVG path data.
    
    Args:
        coil_points: Nx2 or Nx3 array of points
        scale: Scale factor for coordinates
        
    Returns:
        SVG path 'd' attribute string
    """
    if coil_points is None or len(coil_points) == 0:
        return ""
    
    # Extract x,y coordinates
    pts = coil_points[:, :2] if coil_points.shape[1] >= 2 else coil_points
    
    # Scale points
    pts = pts * scale
    
    # Build SVG path
    path_parts = []
    for i, pt in enumerate(pts):
        x, y = pt[0], pt[1]
        if i == 0:
            path_parts.append(f"M {x:.3f} {y:.3f}")
        else:
            path_parts.append(f"L {x:.3f} {y:.3f}")
    
    return " ".join(path_parts)


def generate_svg(
    coil_paths: List[str],
    width_mm: float,
    height_mm: float,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_color: str = "#FF0000",
    stroke_width: float = 0.1,
    background_color: str = "#FFFFFF"
) -> str:
    """Generate complete SVG document.
    
    Args:
        coil_paths: List of SVG path 'd' strings
        width_mm: Document width in mm
        height_mm: Document height in mm
        center_x: Center X offset
        center_y: Center Y offset
        stroke_color: Path stroke color
        stroke_width: Path stroke width in mm
        background_color: Background color
        
    Returns:
        Complete SVG document as string
    """
    # Calculate viewBox
    viewbox_x = -width_mm / 2 + center_x
    viewbox_y = -height_mm / 2 + center_y
    viewbox = f"{viewbox_x:.3f} {viewbox_y:.3f} {width_mm:.3f} {height_mm:.3f}"
    
    # Build paths
    paths_str = ""
    for path_d in coil_paths:
        if path_d:
            paths_str += f'    <path d="{path_d}" fill="none" stroke="{stroke_color}" stroke-width="{stroke_width}" />\n'
    
    # Build SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{width_mm}mm" height="{height_mm}mm" 
     viewBox="{viewbox}">
  <rect x="{viewbox_x}" y="{viewbox_y}" width="{width_mm}" height="{height_mm}" fill="{background_color}" />
  <g transform="scale(1, -1)">
{paths_str}  </g>
</svg>
'''
    return svg


def export_motor_svg(
    coil_points_list: List[np.ndarray],
    outer_radius: float,
    inner_radius: float,
    output_path: str,
    scale: float = 1.0
) -> bool:
    """Export motor coil geometry to SVG file.
    
    Args:
        coil_points_list: List of coil point arrays
        outer_radius: Outer motor radius
        inner_radius: Inner motor radius (shaft bore)
        output_path: Output file path
        scale: Scale factor (default 1.0 for mm)
        
    Returns:
        True if successful
    """
    try:
        # Convert coils to SVG paths
        paths = []
        for coil_pts in coil_points_list:
            if coil_pts is not None and len(coil_pts) > 0:
                path_d = coils_to_svg_paths(coil_pts, scale)
                if path_d:
                    paths.append(path_d)
        
        # Calculate document size
        size = 2.0 * outer_radius * scale * 1.1  # 10% margin
        
        # Generate SVG
        svg_content = generate_svg(
            coil_paths=paths,
            width_mm=size,
            height_mm=size,
            stroke_color="#CC0000",
            stroke_width=0.15
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        return True
        
    except Exception as e:
        print(f"SVG export failed: {e}")
        return False


def calculate_winding_length(
    coil_points: np.ndarray,
    copper_thickness_m: float = 35e-6,
    track_width_m: float = 0.00015
) -> dict:
    """Calculate winding length and resistance from coil points.
    
    Args:
        coil_points: Nx2 or Nx3 array of coil points
        copper_thickness_m: Copper thickness in meters (default 35um)
        track_width_m: Track width in meters (default 0.15mm)
        
    Returns:
        Dictionary with length_m, resistance_ohm, area_m2
    """
    if coil_points is None or len(coil_points) < 2:
        return {"length_m": 0.0, "resistance_ohm": 0.0, "area_m2": 0.0}
    
    # Calculate total length
    pts = coil_points[:, :2] if coil_points.shape[1] >= 2 else coil_points
    total_length = 0.0
    
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i-1][0]
        dy = pts[i][1] - pts[i-1][1]
        total_length += math.sqrt(dx*dx + dy*dy)
    
    # Convert to meters (assuming input in IU, need to know scale)
    # For now, assume input is already in mm
    length_m = total_length / 1000.0
    
    # Calculate cross-section area
    area_m2 = copper_thickness_m * track_width_m
    
    # Calculate resistance (copper resistivity at 20°C)
    rho_copper = 1.68e-8  # Ohm*meter
    resistance = rho_copper * length_m / max(area_m2, 1e-12)
    
    return {
        "length_m": length_m,
        "length_mm": length_m * 1000.0,
        "resistance_ohm": resistance,
        "area_m2": area_m2
    }
