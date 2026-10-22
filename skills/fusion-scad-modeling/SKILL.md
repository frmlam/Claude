---
name: fusion-scad-modeling
description: Generate parametric mechanical CAD models using Fusion 360 (Python API) and OpenSCAD. Creates robot/frame designs with manufacturing drawings, BOM, cutting lists, and export scripts. Use when designing mechanical structures, robot frames, brackets, enclosures, or any parametric mechanical assembly.
metadata:
  version: "0.1.0"
  category: mechanical
---

# Fusion & SCAD Modeling

Generate parametric mechanical CAD models using two complementary tools:

1. **OpenSCAD** — Fast programmatic preview, STL export for 3D printing, parametric `.scad` files
2. **Fusion 360** — Full parametric CAD with assemblies, drawings, STEP export (via Python API)

Typical workflow: design in OpenSCAD first (quick iteration), then recreate in Fusion 360 for manufacturing drawings.

---

## When to Use

- Designing robot frames, chassis, or mechanical assemblies
- Creating parametric brackets, mounts, or enclosures
- Generating manufacturing drawings with dimensions
- Producing cutting lists and hardware BOMs
- Exporting STEP/STL for CNC or 3D printing
- Need a quick OpenSCAD preview before committing to Fusion 360

---

## Step 1: Define Design Parameters

Start by collecting all dimensions into a parameter dict. Units are **mm** unless noted.

```python
DESIGN = {
    # Wheel / base
    "wheel_diameter": 406,
    "wheel_width": 50,
    "axle_diameter": 12,
    "axle_length": 120,

    # Frame
    "frame_tube_size": 25,       # T-slot extrusion size
    "frame_tube_wall": 2,
    "frame_height": 500,
    "frame_width": 200,
    "frame_depth": 150,

    # Motor
    "motor_diameter": 63,
    "motor_length": 80,

    # Battery
    "battery_length": 140,
    "battery_width": 50,
    "battery_height": 35,

    # Electronics
    "pcb_length": 80,
    "pcb_width": 60,
    "pcb_height": 15,

    # Juggling arm / actuator
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
```

**Tip:** Derive all positions from these base parameters so the model is fully parametric.

---

## Step 2: Generate OpenSCAD Model

OpenSCAD is the fastest way to preview and iterate. The generator creates:

- Parametric `.scad` file with all dimensions as variables
- Color-coded modules (wheel, frame, motor, battery, electronics, arm)
- Assembly module that renders everything together
- Dimension comments for reference

### Generator Structure

```python
def generate_openscad(design_params) -> str:
    """Generate OpenSCAD source code from design parameters."""
    d = design_params
    # Pre-compute all derived values
    wheel_r = d['wheel_diameter'] / 2
    # ... compute all positions

    lines = []
    # Build OpenSCAD source line by line
    lines.append(f"wheel_dia = {d['wheel_diameter']};")
    # ... modules for each component

    return "\n".join(lines)
```

### Key OpenSCAD Patterns

```openscad
// Parametric module with color
module my_component() {
    color("blue")
    translate([x, y, z])
    cube([w, d, h], center=false);
}

// Difference for cutouts
difference() {
    cube([outer_w, outer_d, outer_h]);
    translate([wall, wall, -1])
    cube([inner_w, inner_d, inner_h + 2]);
}

// Assembly
module full_assembly() {
    component_a();
    component_b();
}
full_assembly();
```

### Rendering

```bash
# Preview (fast)
openscad model.scad

# Export STL (for 3D printing)
openscad model.scad -o frame.stl

# Export PNG preview
openscad model.scad --imgsize=1920,1080 -o preview.png
```

---

## Step 3: Generate Fusion 360 Model

Fusion 360 provides full parametric CAD with constraints, assemblies, and manufacturing drawings. Use the `adsk` Python API.

### Running the Script

```bash
# Inside Fusion 360:
# Utilities > Add-ins > Scripts > Run

# Or headless (requires Fusion 360 installed):
"C:\Program Files\Autodesk\Fusion 360\Fusion360.exe" --run-script fusion_model.py
```

### Fusion 360 API Pattern

```python
import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent

    # Create sketch on XY plane
    sketches = root.sketches
    xy_plane = root.xYConstructionPlane
    sketch = sketches.add(xy_plane)

    # Draw rectangle
    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width, height, 0))

    # Extrude
    prof = sketch.profiles.item(0)
    extrudes = root.features.extrudeFeatures
    ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyOperation)
    ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(depth))
    extrudes.add(ext_input)

    # Add fillets, chamfers, holes as needed
    # Create drawings, export STEP/STL
```

### Export from Fusion 360

```python
export_mgr = design.exportManager

# STEP (for CAM / other CAD)
step_opts = export_mgr.createSTEPExportOptions("output.step", root)
export_mgr.execute(step_opts)

# STL (for 3D printing)
stl_opts = export_mgr.createSTLExportOptions(root)
stl_opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
export_mgr.execute(stl_opts)

# Drawing (PDF)
# Create drawing view, then export as PDF
```

---

## Step 4: Generate Manufacturing Documentation

### Dimensions Document

```python
def generate_drawing_dimensions(design_params) -> dict:
    """Generate structured dimension list for manufacturing drawing."""
    d = design_params
    return {
        "OVERALL": {
            "total_height_mm": d['wheel_diameter']/2 + d['frame_height'],
            "total_width_mm": d['frame_width'] + d['motor_diameter'] + 30,
            "total_depth_mm": d['axle_length'],
        },
        "FRAME": {
            "vertical_tubes": f"25x25 T-slot, {d['frame_height']}mm long, qty 2",
        },
    }
```

### Cutting List

```python
def generate_cutting_list(design_params) -> list:
    """Generate cutting list for raw materials."""
    d = design_params
    return [
        {"item": "Vertical frame tube (T-slot 25x25)",
         "length": d['frame_height'], "qty": 2, "material": "AL 6060"},
        {"item": "Cross member (T-slot 25x25)",
         "length": d['frame_width'], "qty": 2, "material": "AL 6060"},
    ]
```

### Hardware BOM

```python
def generate_hardware_bom() -> list:
    """Generate fastener and hardware BOM."""
    return [
        {"item": "M5x16 button head socket", "qty": 16, "note": "frame joints"},
        {"item": "M5 T-nut for 25x25 T-slot", "qty": 20, "note": "frame assembly"},
    ]
```

---

## Step 5: Output Files

The generator produces:

| File                 | Purpose                               |
| -------------------- | ------------------------------------- |
| `model.scad`         | OpenSCAD parametric source            |
| `model.stl`          | 3D printable mesh (from OpenSCAD)     |
| `model.step`         | CAD exchange format (from Fusion 360) |
| `dimensions.json`    | Structured dimension data             |
| `manufacturing.json` | Cutting list + hardware BOM           |
| `export_fusion.py`   | Fusion 360 export script              |

---

## Tips & Pitfalls

- **OpenSCAD is CSG, not a solid modeler** — great for quick previews, but use Fusion 360 for proper manufacturing drawings.
- **OpenSCAD i WSL2:** Installer med `sudo apt-get install -y openscad`. Rendrer til PNG med `openscad file.scad --imgsize=1920,1080 -o preview.png`. STL export med `openscad file.scad -o model.stl`.
- **Vær klar for at brukeren korrigerer designretning** — hvis du designer en "clam" men de ville ha en "clip", spør tilbake med konkrete spørsmål om form, funksjon og referanse _før_ du generer STL. Ikke anta — bekreft visuelt først.
- **`reverse()` fungerer IKKE i OpenSCAD** — bruk `[for (i = [len-1 : -1 : 0])` i stedet.
- **`concat()` med list comprehensions** — fungerer i OpenSCAD 2021+, test med enkel `echo()` først om komplekse uttrykker brukes.
- **Skjermbilde/visuell bekreftelse** — Rendr alltid en PNG-preview OG send til brukeren før du eksporterer STL. Brukerne vil se designet, ikke bare få filer.
- **Fusion 360 API runs in-process** — you can't `pip install adsk`. The API is only available inside Fusion 360's Python environment.
- **Parametric everything** — every dimension should derive from the base parameters. Never hardcode positions.
- **Use `center=true` for cylinders** — makes positioning symmetric parts much easier.
- **Fusion 360 free tier** — supports personal use with most features. Student license via Autodesk Education.
- **Export STL from OpenSCAD for 3D printing** — use `$fn=64` or higher for smooth curves.
- **T-slot extrusion joints** — use corner brackets (printed or purchased) rather than welding for prototyping.
- **Check interference** — in Fusion 360, use Inspect > Interference to find overlapping bodies before manufacturing.
- **Snapmaker A350T build volume** — 320×350×340mm. Design parts to fit, or split and bolt together.
- **OrcaSlicer** — use for generating G-code from STL. Supports the A350T natively.
- **`polygon()` vs `hull()` for smooth profiles** — `hull()` of 2-3 circles produces very few CSG elements and flat-looking shapes. For smooth organic profiles (e.g. hair clips, curved bodies), use `polygon()` with manually computed point lists (20-40 points) instead.
- **OpenSCAD `reverse()` doesn't exist** — Use `[for (i = [len-1 : -1 : 0]) ...]` to iterate backwards.
- **f-string escaping in OpenSCAD generators** — pre-compute all numeric values into local variables before building the OpenSCAD string. Never put Python expressions inside `{}` in f-strings that also contain OpenSCAD `{}` blocks.
- **OpenSCAD `reverse()` does NOT exist** — use `[for (i = [len-1 : -1 : 0])` to iterate backwards. Example: `function body_mirror(pts) = concat(pts, [for (i = [len(pts)-1 : -1 : 0]) [pts[i][0], -pts[i][1]]]);`
- **OpenSCAD `hull()` with `circle()` creates simple geometry** — hull of few circles → few CSG elements → flat/boring shape. Use `polygon()` with many points for smooth, complex profiles. Generate points programmatically with list comprehensions: `pts = [for (i = [0 : n]) let(t = i/n) [f_x(t), f_y(t)]];`
- **Design for the object class, not generically** — when user says "hair clip" (hårklype), they mean a classic French/barrette clip: two arms, spring hinge, interlocking teeth. Not a clam/shell. Ask for reference image if unsure about the specific style.
- **WSL path for Windows Desktop** — `~/Desktop/` doesn't exist in WSL. Use `/mnt/c/Users/<username>/Desktop/` for Windows desktop files.
- **Python STL fallback** — When OpenSCAD is unavailable or too slow, generate STL directly from Python. See `scripts/stl_generator.py` for a reusable mesh builder that writes binary STL from triangle lists. Key pattern: compute face normals from cross product, write 80-byte header + `<I` count + `<fff` normal + 3×`<fff` vertices + `<H` attribute per triangle.
- **claw3d CLI for AI→3D** — `claw3d convert --image <file> --output model.glb` generates 3D models from images using FAL.ai. Requires `FAL_API_KEY` env var. Install: `pip install --break-system-packages claw3d`. Convert GLB→STL with `claw3d` or Blender.
- **FAL API key format** — Keys are `key-id:secret` (e.g. `0dad9af5-...:b9e3adfe...`). Must be set as `FAL_API_KEY` environment variable, not just in `.env` — `claw3d` reads from env at runtime. Verify with `echo $FAL_API_KEY`.

## Reference Files

- `references/openscad-patterns.md` — Common OpenSCAD patterns for mechanical design
- `references/openscad-gotchas.md` — OpenSCAD gotchas & workarounds (`reverse()`, hull(), Z-fighting, and more)
- `references/fusion360-api.md` — Fusion 360 Python API quick reference
- `references/tslot-joints.md` — T-slot extrusion joint design guide
- `templates/generate_cad.py` — Parametric CAD generator template (OpenSCAD + dimensions + BOM from design params)
