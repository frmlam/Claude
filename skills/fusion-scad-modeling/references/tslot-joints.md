# T-Slot Extrusion Joint Design Guide

## Common T-Slot Profiles

| Profile | Size    | Slot Width | Common Use                      |
| ------- | ------- | ---------- | ------------------------------- |
| 2020    | 20×20mm | 5mm        | Light frames, 3D printer frames |
| 2040    | 20×40mm | 5mm        | Printer gantries, rails         |
| 2525    | 25×25mm | 6mm        | Medium robot frames             |
| 3030    | 30×30mm | 8mm        | Heavy frames, machine bases     |
| 4040    | 40×40mm | 10mm       | Industrial frames, workbenches  |

## Joint Types

### 1. Corner Bracket (Simplest)

Use purchased L-brackets or 3D printed corners.

```
    ┌───┐
    │   │ vertical tube
    │   │
    ├───┤─── horizontal tube
    │   │
    └───┘
```

- **Pros:** Fast, no machining, adjustable
- **Cons:** Less rigid, visible hardware
- **Fasteners:** M5 or M6 button head + T-nut
- **Printed alternative:** PETG or ABS corner brackets with M5 heat-set inserts

### 2. Internal Corner Bracket

Bracket sits inside the T-slot, hidden from view.

```
    ┌─────┐
    │ ┌─┐ │
    │ │ │ │  bracket inside slot
    │ └─┘ │
    └─────┘
```

- **Pros:** Clean look, good rigidity
- **Cons:** Requires machining or printed parts
- **Print in:** PETG (stronger than PLA for structural parts)

### 3. Gusset / Triangular Bracket

For high-stress joints.

```
    ┌───┐
    │  /│
    │ / │  gusset plate
    │/  │
    ├───┤
```

- **Pros:** Very rigid, distributes load
- **Cons:** More material, harder to assemble
- **Material:** 3-5mm aluminum laser-cut, or 3D printed

### 4. Butt Joint with End-Mill Slot

Machine a slot into one tube, bolt through it.

```
    ┌───┐
    │   │
    │ ┌─┼─── slot
    │ │ │
    └─┼─┘
      │
```

- **Pros:** Very strong, hidden fasteners
- **Cons:** Requires milling machine
- **Slot width:** Match tube slot width (6mm for 2525)

### 3D Printed Custom Brackets

Design custom brackets for non-standard angles or integrated features.

```openscad
// Corner bracket for 25x25 T-slot
module corner_bracket(size=25, thickness=5, height=40) {
    difference() {
        union() {
            // Vertical leg
            cube([height, thickness, size + thickness*2]);
            // Horizontal leg
            cube([thickness, height, size + thickness*2]);
            // Gusset
            translate([0, 0, size + thickness*2])
            rotate([0, 90, 0])
            linear_extrude(thickness)
            polygon([[0, 0], [height, 0], [0, height]]);
        }
        // Bolt holes
        translate([height/2, -1, size/2 + thickness])
        rotate([-90, 0, 0])
        cylinder(d=5.2, h=thickness + 2);
        translate([-1, height/2, size/2 + thickness])
        rotate([0, 90, 0])
        cylinder(d=5.2, h=thickness + 2);
    }
}
```

## T-Nut Types

| Type          | Description                     | Use                        |
| ------------- | ------------------------------- | -------------------------- |
| Drop-in       | Round, drops into slot          | Easy assembly, can rotate  |
| Slide-in      | Rectangular, slides in from end | Better alignment           |
| Hammer nut    | Hammered into slot              | Permanent, very secure     |
| Spring-loaded | Ball spring holds position      | Adjustable, stays in place |

## Fastener Torque (for aluminum T-slot)

| Bolt | Torque (Nm) | Notes                  |
| ---- | ----------- | ---------------------- |
| M4   | 1.2-1.5     | Light duty             |
| M5   | 2.5-3.0     | Most common for frames |
| M6   | 5.0-6.0     | Heavy duty             |
| M8   | 12-15       | Industrial             |

**Always use nyloc nuts** on vibrating assemblies (like robots).

## Design Rules

1. **Minimum 2 bolts per joint** — prevents rotation
2. **Bolt spacing ≥ 3× bolt diameter** — prevents pull-through
3. **Edge distance ≥ 1.5× bolt diameter** — prevents edge cracking
4. **Gusset height ≥ 0.6× tube length** — effective bracing
5. **Use corner brackets for prototyping** — faster iteration
6. **Add slots for adjustability** — 20mm slots allow ±10mm adjustment
7. **Consider cable routing** — leave space in T-slots for wires

## Printed Bracket Materials

| Material | Strength  | Temp Resistance | Use                      |
| -------- | --------- | --------------- | ------------------------ |
| PLA      | Medium    | 55°C            | Prototypes only          |
| PETG     | Good      | 75°C            | Most brackets            |
| ABS      | Good      | 100°C           | Enclosed frames          |
| Nylon    | Excellent | 120°C           | High-stress joints       |
| CF-Nylon | Best      | 150°C           | Motor mounts, arm joints |

## Heat-Set Inserts

For strong, reusable threads in printed parts:

- **M3 insert:** 5.0mm length, 4.0mm OD — heat to 220°C, press in
- **M4 insert:** 6.0mm length, 5.0mm OD
- **M5 insert:** 8.0mm length, 6.0mm OD

Use a soldering iron with insert tip for clean installation.
