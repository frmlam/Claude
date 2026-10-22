# OpenSCAD Gotchas & Workarounds

## Functions That Don't Exist

### `reverse()`

OpenSCAD has no `reverse()` function. Iterate backwards explicitly:

```openscad
// WRONG
for (p = reverse(pts)) { ... }

// RIGHT
for (i = [len(pts)-1 : -1 : 0]) { ... ; pts[i] ... }
```

## Geometry Gotchas

### `hull()` with few circles → flat shape

Use `polygon()` with many points for organic profiles:

```openscad
n = 40;
pts = [for (i = [0 : n]) let(t = i/n) [length*t, width(t)]];
polygon(pts);
```

### Coplanar face Z-fighting

Add epsilon (`_e = 0.01`) when subtracting coplanar faces.

## Hair Clip Design Notes

- Two separate arms, teeth interdigitate when closed
- Pin hinge: 2.0–2.2mm steel rod / piano wire
- Living hinge: 0.8mm thin section, PETG for 50–100 flex cycles
- Print arms flat (teeth up) — no supports needed
