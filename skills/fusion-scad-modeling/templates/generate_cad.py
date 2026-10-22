#!/usr/bin/env python3
"""
Parametric CAD Generator — Template
=====================================
Generates OpenSCAD model, dimensions, and manufacturing BOM from design parameters.

Usage:
    python3 generate_cad.py                    # generate all outputs
    python3 generate_cad.py --scad-only        # only OpenSCAD
    python3 generate_cad.py --bom-only         # only manufacturing data
    python3 generate_cad.py --wheel-dia 500    # override parameters
"""

import json
import argparse
import os
import sys

# ─────────────────────────────────────────────
# Design Parameters — EDIT THESE
# ─────────────────────────────────────────────
DESIGN = {
    # Wheel
    "wheel_diameter": 406,
    "wheel_width": 50,
    "axle_diameter": 12,
    "axle_length": 120,

    # Frame
    "frame_tube_size": 25,
    "frame_tube_wall": 2,
    "frame_height": 500,
    "frame_width": 200,
    "frame_depth": 150,

    # Motor
    "motor_diameter": 63,
    "motor_length": 80,
    "motor_mount_bolt_circle": 47,

    # Battery
    "battery_length": 140,
    "battery_width": 50,
    "battery_height": 35,

    # Electronics
    "pcb_length": 80,
    "pcb_width": 60,
    "pcb_height": 15,

    # Arm / actuator
    "arm_length": 300,
    "arm_tube_dia": 16,
    "arm_servo_size": 20,
    "arm_scoop_width": 60,
    "arm_scoop_depth": 30,

    # Fasteners
    "bolt_m5": 5,
    "bolt_m4": 4,
    "bolt_m3": 3,

    # Plates
    "mount_plate_thickness": 5,
    "bracket_thickness": 3,
}


def apply_overrides(design, overrides):
    """Apply command-line overrides to design parameters."""
    for key, val in overrides.items():
        if key in design and val is not None:
            design[key] = type(design[key])(val)
    return design


def generate_openscad(d):
    """Generate OpenSCAD source from design dict."""
    # Pre-compute all values
    wd = d['wheel_diameter']
    ww = d['wheel_width']
    ad = d['axle_diameter']
    al = d['axle_length']
    ts = d['frame_tube_size']
    tw = d['frame_tube_wall']
    fh = d['frame_height']
    fw = d['frame_width']
    fd = d['frame_depth']
    md = d['motor_diameter']
    ml = d['motor_length']
    bl = d['battery_length']
    bw = d['battery_width']
    bh = d['battery_height']
    pl = d['pcb_length']
    pw = d['pcb_width']
    ph = d['pcb_height']
    arl = d['arm_length']
    atd = d['arm_tube_dia']
    ass_ = d['arm_servo_size']
    asw = d['arm_scoop_width']
    asd = d['arm_scoop_depth']
    pt = d['mount_plate_thickness']

    wr = wd / 2
    axle_y = -(al/2 - ww/2)
    mx = ts/2 + md/2 + 5
    mmy = ww/2 + pt/2
    mby = ww/2 + 5
    bax = -(bl/2 + 30)
    bay = -(fd/2 - bw/2)
    baz = wr + 10
    pcbx = 30
    pcby = -(fd/2 - pw/2)
    pcbz = wr + fh - 40
    arx = -(wr + 20)
    arz = wr + fh + 30

    lines = []
    a = lines.append

    a("// Auto-generated parametric model")
    a(f"// Wheel: {wd}mm, Frame: {fw}x{fd}x{fh}mm")
    a("")
    a("$fn = 40;")
    a("")
    a(f"wheel_dia = {wd};")
    a(f"wheel_w = {ww};")
    a(f"axle_dia = {ad};")
    a(f"tube = {ts};")
    a(f"tube_wall = {tw};")
    a(f"frame_h = {fh};")
    a(f"frame_w = {fw};")
    a(f"frame_depth = {fd};")
    a(f"motor_dia = {md};")
    a(f"arm_len = {arl};")
    a(f"arm_dia = {atd};")
    a(f"plate_t = {pt};")
    a(f"battery_l = {bl};")
    a(f"battery_w = {bw};")
    a(f"battery_h = {bh};")
    a(f"pcb_l = {pl};")
    a(f"pcb_w = {pw};")
    a(f"pcb_h = {ph};")
    a(f"arm_servo = {ass_};")
    a(f"scoop_w = {asw};")
    a(f"scoop_d = {asd};")
    a("")
    a("module wheel() {")
    a('    color("darkgray")')
    a("    translate([0, 0, wheel_dia/2])")
    a("    rotate([0, 90, 0])")
    a("    cylinder(d=wheel_dia, h=wheel_w, center=true);")
    a("}")
    a("")
    a("module axle() {")
    a('    color("silver")')
    a(f"    translate([0, {axle_y}, wheel_dia/2])")
    a("    rotate([0, 90, 0])")
    a(f"    cylinder(d=axle_dia, h={al}, center=true);")
    a("}")
    a("")
    a("module frame_tube(x_pos, height) {")
    a("    translate([x_pos, 0, wheel_dia/2])")
    a("    color('lightgray')")
    a("    cube([tube, tube, height]);")
    a("}")
    a("")
    a("module cross_member(y_pos, width) {")
    a("    translate([-width/2, y_pos, wheel_dia/2 + frame_h - tube])")
    a("    color('lightgray')")
    a("    cube([width, tube, tube]);")
    a("}")
    a("")
    a("module motor_mount() {")
    a(f"    mx = {mx};")
    a('    color("orange")')
    a(f"    translate([mx, {mmy}, wheel_dia/2 + frame_h/2])")
    a("    cube([plate_t, motor_dia+20, motor_dia+10], center=true);")
    a('    color("darkblue")')
    a(f"    translate([mx+plate_t/2+motor_dia/2, {mby}, wheel_dia/2+frame_h/2])")
    a("    rotate([0, 90, 0])")
    a(f"    cylinder(d=motor_dia, h={ml}, center=true);")
    a("}")
    a("")
    a("module battery() {")
    a(f"    color('green')")
    a(f"    translate([{bax}, {bay}, {baz}])")
    a(f"    cube([battery_l, battery_w, battery_h]);")
    a("}")
    a("")
    a("module electronics() {")
    a(f"    color('darkgreen')")
    a(f"    translate([{pcbx}, {pcby}, {pcbz}])")
    a(f"    cube([pcb_l, pcb_w, pcb_h]);")
    a("}")
    a("")
    a("module juggling_arm() {")
    a(f"    arx = {arx}; arz = {arz};")
    a('    color("darkred")')
    a("    translate([arx, 0, arz])")
    a(f"    cube([{ass_+10}, {ass_+10}, {ass_+5}], center=true);")
    a('    color("lightblue")')
    a("    translate([arx, 0, arz])")
    a("    rotate([0, 20, 0])")
    a("    translate([0, 0, arm_len/2])")
    a("    cylinder(d=arm_dia, h=arm_len, center=true);")
    a('    color("yellow")')
    a("    translate([arx, 0, arz])")
    a("    rotate([0, 20, 0])")
    a("    translate([0, 0, arm_len+10])")
    a(f"    cube([scoop_w, scoop_d, 3], center=true);")
    a("}")
    a("")
    a("module assembly() {")
    a("    wheel(); axle();")
    a("    frame_tube(-frame_w/2, frame_h);")
    a("    frame_tube(frame_w/2, frame_h);")
    a("    cross_member(0, frame_w);")
    a("    cross_member(-frame_depth/2+tube, frame_w);")
    a("    motor_mount(); battery(); electronics(); juggling_arm();")
    a("}")
    a("assembly();")

    return "\n".join(lines)


def generate_dimensions(d):
    """Generate dimension dict."""
    return {
        "OVERALL": {
            "height_mm": d['wheel_diameter']/2 + d['frame_height'],
            "width_mm": d['frame_width'] + d['motor_diameter'] + 30,
            "depth_mm": d['axle_length'],
        },
        "FRAME": {
            "vertical_tubes": f"{d['frame_tube_size']}x{d['frame_tube_size']} T-slot x {d['frame_height']}mm, qty 2",
            "cross_members": f"{d['frame_tube_size']}x{d['frame_tube_size']} T-slot x {d['frame_width']}mm, qty 2",
        },
    }


def generate_manufacturing(d):
    """Generate cutting list and hardware BOM."""
    cutting = [
        {"item": "Vertical frame tube", "length": d['frame_height'], "qty": 2, "material": "AL 6060 T-slot"},
        {"item": "Cross member", "length": d['frame_width'], "qty": 2, "material": "AL 6060 T-slot"},
        {"item": "Motor mount plate", "size": f"{d['motor_diameter']+20}x{d['motor_diameter']+10}", "qty": 1, "material": f"AL {d['mount_plate_thickness']}mm"},
    ]
    hardware = [
        {"item": "M5x16 button head", "qty": 16, "note": "frame joints"},
        {"item": "M5 T-nut", "qty": 20, "note": "frame assembly"},
        {"item": "M5 nyloc nut", "qty": 16, "note": "frame joints"},
    ]
    return {"cutting_list": cutting, "hardware_list": hardware}


def main():
    parser = argparse.ArgumentParser(description="Parametric CAD Generator")
    parser.add_argument("--output-dir", default="./cad_output", help="Output directory")
    parser.add_argument("--scad-only", action="store_true")
    parser.add_argument("--bom-only", action="store_true")
    parser.add_argument("--wheel-dia", type=float, help="Override wheel diameter")
    parser.add_argument("--frame-height", type=float, help="Override frame height")
    parser.add_argument("--frame-width", type=float, help="Override frame width")
    args = parser.parse_args()

    design = DESIGN.copy()
    overrides = {
        "wheel_diameter": args.wheel_dia,
        "frame_height": args.frame_height,
        "frame_width": args.frame_width,
    }
    design = apply_overrides(design, overrides)

    os.makedirs(args.output_dir, exist_ok=True)

    if not args.bom_only:
        scad = generate_openscad(design)
        path = os.path.join(args.output_dir, "model.scad")
        with open(path, "w") as f:
            f.write(scad)
        print(f"Generated: {path}")

    if not args.scad_only:
        dims = generate_dimensions(design)
        path = os.path.join(args.output_dir, "dimensions.json")
        with open(path, "w") as f:
            json.dump(dims, f, indent=2)
        print(f"Generated: {path}")

        mfg = generate_manufacturing(design)
        path = os.path.join(args.output_dir, "manufacturing.json")
        with open(path, "w") as f:
            json.dump(mfg, f, indent=2)
        print(f"Generated: {path}")

    # Summary
    d = design
    total_h = d['wheel_diameter']/2 + d['frame_height']
    total_w = d['frame_width'] + d['motor_diameter'] + 30
    print(f"\nOverall: {total_w:.0f}x{d['axle_length']:.0f}x{total_h:.0f} mm (WxDXH)")
    print(f"Wheel: Ø{d['wheel_diameter']:.0f}mm, Frame: {d['frame_height']:.0f}mm tall")


if __name__ == "__main__":
    main()
