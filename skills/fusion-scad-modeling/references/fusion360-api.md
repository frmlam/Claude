# Fusion 360 Python API Quick Reference

## Setup

The `adsk` module is only available inside Fusion 360's Python environment. No pip install.

```python
import adsk.core, adsk.fusion, adsk.cam, traceback
```

## Application & Design

```python
app = adsk.core.Application.get()
ui = app.userInterface
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
```

## Sketches

```python
# Create sketch on XY plane
sketches = root.sketches
xy_plane = root.xYConstructionPlane
sketch = sketches.add(xy_plane)

# Draw lines
lines = sketch.sketchCurves.sketchLines
line = lines.addByTwoPoints(
    adsk.core.Point3D.create(0, 0, 0),
    adsk.core.Point3D.create(100, 50, 0))

# Draw rectangle
rect = lines.addTwoPointRectangle(
    adsk.core.Point3D.create(0, 0, 0),
    adsk.core.Point3D.create(100, 50, 0))

# Draw circle
circles = sketch.sketchCurves.sketchCircles
circle = circles.addByCenterRadius(
    adsk.core.Point3D.create(50, 25, 0), 10)

# Draw arc
arcs = sketch.sketchCurves.sketchArcs
arc = arcs.addByThreePoints(
    adsk.core.Point3D.create(0, 0, 0),
    adsk.core.Point3D.create(50, 25, 0),
    adsk.core.Point3D.create(100, 0, 0))

# Add dimension
sketch.sketchDimensions.addDistanceDimension(
    line.startSketchPoint, line.endSketchPoint,
    adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
    adsk.core.Point3D.create(50, -10, 0))

# Add constraint (coincident, parallel, perpendicular, etc.)
sketch.geometricConstraints.addCoincident(line1.endSketchPoint, line2.startSketchPoint)
```

## Extrude

```python
# Get profile from sketch
prof = sketch.profiles.item(0)  # or iterate profiles

# Create extrude
extrudes = root.features.extrudeFeatures
ext_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyOperation)

# Set distance
ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(20))

# Or symmetric
ext_input.setSymmetricExtent(adsk.core.ValueInput.createByReal(10))

# Add to feature tree
ext = extrudes.add(ext_input)
```

## Revolve

```python
revolves = root.features.revolveFeatures
rev_input = revolves.createInput(prof, adsk.fusion.FeatureOperations.NewBodyOperation)
rev_input.setAngleExtent(False, adsk.core.ValueInput.createByReal(360))
rev = revolves.add(rev_input)
```

## Hole

```python
holes = root.features.holeFeatures
hole_input = holes.createSimpleInput(adsk.core.ValueInput.createByReal(5))  # diameter
hole_input.setPositionByPoint(
    adsk.core.Point3D.create(50, 25, 0))
hole_input.setDistanceExtent(adsk.core.ValueInput.createByReal(20))
hole = holes.add(hole_input)
```

## Fillet

```python
fillets = root.features.filletFeatures
edge_collection = adsk.core.ObjectCollection.create()
# Add edges to collection (from body.edges)
edge_collection.add(body.edges.item(0))
fillet_input = fillets.createInput()
fillet_input.addConstantRadiusEdgeSet(edge_collection, adsk.core.ValueInput.createByReal(3))
fillet = fillets.add(fillet_input)
```

## Chamfer

```python
chamfers = root.features.chamferFeatures
chamfer_input = chamfers.createInput()
chamfer_input.setToEqualDistance(adsk.core.ValueInput.createByReal(2))
# Add edges...
chamfer = chamfers.add(chamfer_input)
```

## Pattern

```python
# Rectangular pattern
rect_patterns = root.features.rectangularPatternFeatures
rect_input = rect_patterns.createInput(
    input_entities,  # ObjectCollection of features/bodies
    root.xDirection,  # direction
    adsk.core.ValueInput.createByReal(3),  # quantity
    adsk.core.ValueInput.createByReal(50))  # spacing
rect_pattern = rect_patterns.add(rect_input)

# Circular pattern
circ_patterns = root.features.circularPatternFeatures
circ_input = circ_patterns.createInput(input_entities, root.zConstructionAxis)
circ_input.quantity = adsk.core.ValueInput.createByReal(6)
circ_input.totalAngle = adsk.core.ValueInput.createByReal(360)
circ_pattern = circ_patterns.add(circ_input)
```

## Mirror

```python
mirrors = root.features.mirrorFeatures
mirror_input = mirrors.createInput(input_entities, root.xYConstructionPlane)
mirror = mirrors.add(mirror_input)
```

## Combine (Boolean)

```python
combines = root.features.combineFeatures
combine_input = combines.createInput(target_body, tool_bodies_collection)
combine_input.operation = adsk.fusion.FeatureOperations.CutOperation  # or Join, Intersect
combine = combines.add(combine_input)
```

## Construction Planes & Axes

```python
# Offset plane
planes = root.constructionPlanes
plane_input = planes.createInput()
plane_input.setByOffset(root.xYConstructionPlane, adsk.core.ValueInput.createByReal(100))
plane = planes.add(plane_input)

# Axis through cylinder
axes = root.constructionAxes
axis_input = axes.createInput()
axis_input.setByCylindricalFace(cylinder_face)
axis = axes.add(axis_input)
```

## Bodies & Components

```python
# Access bodies
bodies = root.bRepBodies
body = bodies.add(new_solid_body)

# Create new component
occurrences = root.occurrences
new_comp = occurrences.addNewComponent(adsk.core.Matrix3D.create()).component

# Move component
transform = occurrences.item(0).transform
transform.translation = adsk.core.Vector3D.create(100, 0, 0)
occurrences.item(0).transform = transform
```

## Materials & Appearance

```python
# Set body color (appearance)
appearance = app.materialLibrary.appearances.itemByName("Aluminum - Anodized (Blue)")
body.appearance = appearance
```

## Export

```python
export_mgr = design.exportManager

# STEP
step_opts = export_mgr.createSTEPExportOptions("~/output.step", root)
export_mgr.execute(step_opts)

# STL
stl_opts = export_mgr.createSTLExportOptions(root)
stl_opts.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
export_mgr.execute(stl_opts)

# IGES
iges_opts = export_mgr.createIGESExportOptions("~/output.iges", root)
export_mgr.execute(iges_opts)

# SAT
sat_opts = export_mgr.createSATExportOptions("~/output.sat", root)
export_mgr.execute(sat_opts)
```

## Drawings

```python
# Create drawing from design
drawing = design.drawings.add(adsk.fusion.DrawingSettings.DrawingStandard.ISO)
# Add base view, dimensions, annotations
# Export as PDF
```

## Parameters (User Parameters)

```python
# Access user parameters
params = design.userParameters
width_param = params.itemByName("width")

# Create new parameter
new_param = params.add("frame_height", adsk.core.ValueInput.createByString("500 mm"), "mm", "Frame height")

# Use parameter in sketch dimension
sketch_dim.parameter = new_param
```

## Error Handling

```python
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        # ... your code ...
        ui.messageBox("Success!")
    except Exception as e:
        if ui:
            ui.messageBox(f"Failed:\n{traceback.format_exc()}")
```

## Common Pitfalls

- **Profiles can be ambiguous** — `sketch.profiles.item(0)` may not be the one you want. Iterate and check area.
- **Features need valid references** — if a sketch is consumed by an extrude, you can't reuse it. Create a new sketch.
- **Units** — Fusion 360 uses cm internally. Use `ValueInput.createByString("500 mm")` or convert.
- **ObjectCollection** — many features require collections, not single objects.
- **Transaction management** — wrap multiple operations in `design.beginTransaction()` / `design.endTransaction()` for undo support.
