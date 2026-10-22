# OpenSCAD Patterns for Mechanical Design

## Basic Parametric Box

```openscad
module box(w, d, h, center=false) {
    if (center)
        translate([-w/2, -d/2, -h/2])
        cube([w, d, h]);
    else
        cube([w, d, h]);
}
```

## T-Slot Extrusion Profile (20x20, 25x25, 30x30)

```openscad
module tslot_profile(size, length, slot_width=6, slot_depth=6) {
    // Simplified T-slot cross-section
    difference() {
        cube([size, size, length]);
        // Center cross slot
        translate([size/2 - slot_width/2, -1, -1])
        cube([slot_width, size/2 - slot_depth/2 + 1, length + 2]);
        translate([-1, size/2 - slot_width/2, -1])
        cube([size/2 - slot_depth/2 + 1, slot_width, length + 2]);
    }
}
```

## Motor Mount Plate with Bolt Holes

```openscad
module motor_mount_plate(width, height, thickness, bolt_circle, bolt_dia, motor_dia) {
    difference() {
        // Base plate
        cube([width, height, thickness]);

        // Motor cutout (optional)
        translate([width/2, height/2, -1])
        cylinder(d=motor_dia + 2, h=thickness + 2);

        // Bolt holes
        for (angle = [0, 90, 180, 270]) {
            translate([
                width/2 + bolt_circle/2 * cos(angle),
                height/2 + bolt_circle/2 * sin(angle),
                -1
            ])
            cylinder(d=bolt_dia + 0.5, h=thickness + 2);
        }
    }
}
```

## Bearing Housing

```openscad
module bearing_housing(od, id, width, wall=3) {
    difference() {
        // Outer body
        cylinder(d=od + 2*wall, h=width);
        // Bearing bore
        translate([0, 0, -1])
        cylinder(d=od + 0.2, h=width + 2);
        // Shaft hole
        translate([0, 0, -1])
        cylinder(d=id - 0.2, h=width + 2);
    }
}
```

## Servo Mount

```openscad
module servo_mount(servo_w, servo_l, servo_h, wall=2, mount_h=3) {
    difference() {
        // Outer shell
        cube([servo_w + 2*wall, servo_l + 2*wall, servo_h + mount_h]);
        // Servo cavity
        translate([wall, wall, mount_h])
        cube([servo_w, servo_l + 1, servo_h + 1]);
        // Wire channel
        translate([servo_w/2 + wall - 2, -1, mount_h + servo_h/2])
        cube([4, wall + 2, 4]);
    }
    // Mounting tabs
    translate([-10, 0, 0])
    cube([10, servo_l + 2*wall, mount_h]);
    translate([servo_w + 2*wall, 0, 0])
    cube([10, servo_l + 2*wall, mount_h]);
}
```

## Wheel with Tire

```openscad
module wheel(diameter, width, tire_thickness=5, hub_dia=20) {
    // Rim
    color("gray")
    translate([0, 0, width/2])
    rotate([0, 90, 0])
    difference() {
        cylinder(d=diameter - tire_thickness*2, h=width, center=true);
        cylinder(d=hub_dia, h=width + 2, center=true);
    }

    // Tire
    color("black")
    translate([0, 0, width/2])
    rotate([0, 90, 0])
    difference() {
        cylinder(d=diameter, h=width - 4, center=true);
        cylinder(d=diameter - tire_thickness*2, h=width - 2, center=true);
    }
}
```

## Adjustable Slot Hole

```openscad
module slot_hole(length, width, depth) {
    // Rounded rectangle slot
    hull() {
        translate([length/2 - width/2, 0, 0])
        cylinder(d=width, h=depth);
        translate([-length/2 + width/2, 0, 0])
        cylinder(d=width, h=depth);
    }
}

// Usage: rotate([0, 90, 0]) slot_hole(20, 6, 100);
```

## Heat-Set Insert Boss

```openscad
module insert_boss(insert_od, insert_length, wall=3) {
    difference() {
        cylinder(d=insert_od + 2*wall, h=insert_length + 2);
        translate([0, 0, -1])
        cylinder(d=insert_od - 0.3, h=insert_length + 1);
    }
}
```

## Gusset Bracket

```openscad
module gusset(size, thickness, height) {
    difference() {
        union() {
            cube([size, thickness, height]);
            cube([thickness, size, height]);
        }
        // Triangular gusset
        translate([thickness, thickness, 0])
        linear_extrude(height=height)
        polygon([[0, 0], [size-thickness, 0], [0, size-thickness]]);
    }
}
```

## Common Patterns

### Pattern: Array of holes

```openscad
for (x = [0 : pitch : total_length - pitch]) {
    translate([x, 0, 0])
    cylinder(d=hole_dia, h=thickness + 2);
}
```

### Pattern: Mirrored features

```openscad
for (side = [-1, 1]) {
    translate([side * offset, 0, 0])
    children();
}
```

### Pattern: Rounded box (for 3D printing)

```openscad
module rounded_box(w, d, h, r=3) {
    hull() {
        translate([r, r, 0]) cylinder(r=r, h=h);
        translate([w-r, r, 0]) cylinder(r=r, h=h);
        translate([r, d-r, 0]) cylinder(r=r, h=h);
        translate([w-r, d-r, 0]) cylinder(r=r, h=h);
    }
}
```

## Tips

- Use `$fn` for circle smoothness: `$fn=64` for final, `$fn=20` for preview
- Use `center=true` on cylinders for symmetric positioning
- Use `hull()` for smooth transitions between shapes
- Use `minkowski()` for rounding edges (slow, use sparingly)
- Always add 0.2-0.5mm clearance for 3D printed parts that fit together
- Use `render()` for complex CSG to speed up preview
