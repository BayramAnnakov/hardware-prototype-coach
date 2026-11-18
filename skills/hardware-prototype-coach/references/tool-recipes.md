# Tools for the selected prototype

Choose the tools after the concept. These recipes were exercised on macOS ARM on 18 November 2026. A working tool is not proof that a particular device works.

## Visual concepts before CAD

Start with appearance and the experience of using the object. Use available image generation for a board of two or three distinct directions. In Codex, use the built-in image tool; for an edit, include the chosen image and preserve the features the person liked. Use a short interaction storyboard when a still picture does not explain the behavior. Keep requests focused on the object's silhouette, character, surface, scale and interaction; engineering dimensions can follow.

If this environment has no image generator, create a simple viewable SVG/HTML sketch board without CAD dependencies. Show or open it using supported tools, or give a direct local file link if preview is unavailable. Say it is a concept sketch. Do not claim a visual was shown if only a text prompt was written. Ask the person what they like or would change, then iterate. Save the selected visual and the design decisions with the project. Do not infer real internal dimensions or working hardware from an attractive generated picture.

### An image API the person already uses

In an environment without a built-in image tool (Claude Code was one on 18 November 2026), an image API the person already has a key for is an image tool. Ask where the key lives instead of searching their disk; read it at run time, never print it, write it into project files or send it anywhere but that API. Keep scripts that call the API outside the project folder.

- Concepts: one request per direction, run in parallel; describe silhouette, size, materials, the interaction and the visible text, and ask for no logos.
- From the CAD: send a CAD render as the input image and ask to keep the exact geometry. This gives a better picture of the real shape than a concept prompt.
- Check every generated image against the CAD before showing it as the object: count keys, screens, ports and windows, and read the text. In one session a model drew eight keys in two rows from a render with four in one row, and labelled the wrong part in an exploded view. Regenerate once with the count stated outright, then say under the image where it still differs.

## Editable enclosure or mechanical object

CadQuery is a Python CAD library. Version 2.6.1 was used for the supplied example.

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python cadquery==2.6.1
```

Use the corresponding `.venv\Scripts\python.exe` path on Windows; that platform was not exercised in the host rehearsal. If `uv` is unavailable, create the project `.venv` with the person's existing Python (`python -m venv .venv`) and install only there. If the project `.venv` cannot import CadQuery, stop installing: do not install into any other environment, and continue with the no-CAD fallback in the skill.

A minimal modelling/export pattern:

```python
import cadquery as cq
from cadquery import exporters

shape = cq.Workplane("XY").box(40, 25, 8)
assert shape.val().isValid()
exporters.export(shape, "prototype.step")
exporters.export(shape, "prototype.stl")
```

Keep the Python source editable. For a fitted case, model each selected component separately, use its actual placement, and calculate the intersection volume with the case material and with other components. Also check containment: a component outside the case can have zero collision volume. Check connector access and assembly path separately; a valid final arrangement can still be impossible to assemble.

The example's nominal-envelope checks do not establish print tolerances, fastener retention, thermal behavior, connector accessibility with every cable, or fit of an unmeasured part. Pick the relevant next measurement instead of duplicating a generic checklist.

Documentation: [CadQuery quick start](https://cadquery.readthedocs.io/en/latest/quickstart.html).

The reference renderer uses matplotlib as well as CadQuery; install its `requirements.txt`. First import may build a font cache. `XDG_CACHE_HOME` and `MPLCONFIGDIR` can point to a task-specific temporary directory. CadQuery 2.6.1 may emit a deprecation warning for assembly `save`; inspect the exit code and exported files rather than treating that warning as a failed model.

## Quick physical estimates

Use these to find a problem early. Name each as an estimate in the report; none is a simulation or a measurement.

- **Sound path to a microphone:** a tube that is closed at the microphone and open to the outside resonates near `f = c / (4 * L)`, with `c` about 343,000 mm/s and `L` the effective length in mm: the tube length plus about 0.6 of the opening radius. A 25 mm path gives about 3.4 kHz, inside the voice band. A path of about 8 mm or less stays near or above 8 kHz. This is an approximate resonance, not a guarantee. Keep microphones close to the outer surface.
- **A hole that opens into a cavity:** choose the model from the geometry, not from the part list. A microphone behind a cavity with one or more holes to the outside is closer to a Helmholtz resonator: `f = c / (2 * pi) * sqrt(A / (V * L))`, with `c` in mm/s, `A` the total hole area in mm², `V` the cavity volume in mm³ and `L` in mm: the hole depth plus about 1.7 hole radii. It assumes equal holes and a cavity that is small against the wavelength. Example: 24 holes of 2 mm through a 2 mm plate above a 13.3 cm³ cavity give about 2.1 kHz, where the tube formula on the 9 mm depth alone gave about 9.5 kHz. A short sealed port for each microphone avoids the shared cavity.
- **Wall thickness:** a wall drawn as a horizontal or vertical shift of the profile becomes thinner where the surface slopes; an offset along the surface normal does not. Measure the shortest distance between the outer and inner surfaces.
- **Fit between two printed parts:** each part can be off by the accuracy that the service states. Convert that accuracy to millimetres first: the larger of the stated percentage of the dimension and the stated lower limit. The nominal clearance on diameter, minus the tolerance of the hole, minus the tolerance of the shaft, must leave the running clearance that the fit needs. This is a simple stack, not a promise of a smooth fit; a first sample decides.
- **Charge time:** battery capacity in mAh divided by charge current in mA gives hours for an ideal constant current. Real charging tapers near the end and takes longer. Also confirm that the charge current is within the limit in the cell's datasheet. Check the charge current of the selected board before choosing a battery size.

## Checks that found real faults

These patterns each caught a fault in a session on 18 November 2026 that a plain collision check missed.

- Group the report by kind: the model itself, print limits, process accuracy, fit of bought parts, joints and motion, assembly order, function. A reader sees at once which kind failed.
- Check containment as well as collision, and check what holds each part in place.
- For moving parts, check the end positions and the poses where parts come closest, in each state of the other moving parts. Record the range of motion that was not examined; sampled poses are not a full sweep.
- Import each exported file again and compare its size and volume with the report.
- When a margin improves and the design did not change, the check changed. Read the check before trusting the number.

More patterns from a second session on 18 November 2026, a sloped console taken through seven revisions:

- A part that must sit on a board can pass every collision check while hanging off its edge. Check it against the board outline: switches against the key board after the pitch changed.
- Sample the assembly path, not only the final pose: move the part back along its insertion direction in a few steps and check each pose. A key block cleared everything in place and hit microphone guide ribs 2 mm before it.
- A plug envelope placed on the wrong layer collides with glass that the real plug never reaches; when a collision is tiny, find where it is before changing the design.
- A check computed from the same numbers that built the geometry always passes. Measure the solid instead, for example by intersecting a small probe box with it.

## Interactive model page

A page where the person can rotate the assembly, explode it, cut a section and switch parts on and off explains the layout faster than renders.

- Export the assembly to glTF from CadQuery with one named, coloured node per part: `cadquery.occ_impl.exporters.assembly.exportGLTF(assy, "assembly.glb", binary=True)`. The file stays in millimetres; its root node carries the Z-up to Y-up rotation, so explode vectors written in CAD coordinates apply directly to the child nodes' positions.
- In the page, three.js with `GLTFLoader` and `OrbitControls`, pinned to an exact version; a clipping plane gives the section view.
- Some publishing hosts refuse `.glb` files: wrap the bytes as base64 in a JSON file and parse them with `GLTFLoader.parse`. For sharing without a host, inline the model and images into one HTML file; check that it opens from a `file://` URL.
- Draw plan views and sections from the same solids (intersect each with a thin slab and fill its triangles) so they cannot disagree with the model.
- The matplotlib renderer used for quick previews sorts triangles per object and can draw a board over a screen in front of it. Hide parts that do not need to be seen, or use the page.

## Circuit design with Diode

Public tooling: [Diode pcb](https://github.com/diodeinc/pcb), [quick start](https://docs.pcb.new/pages/quickstart). Follow the current installer and inspect what it changes. The host used launcher 0.2.8 with managed compiler **0.4.102**. The launcher and compiler have different versions.

```sh
pcb +0.4.102 build Device.zen --diagnostics diagnostics.json
pcb +0.4.102 bom Device.zen --format json --offline
pcb +0.4.102 layout --no-open Device.zen
```

`build` can run without KiCad. `layout` needs KiCad 10.x and its Python bindings. An imported layout can still have no useful placement and no copper routing. Inspect the actual board and DRC result before describing it as ready to fabricate. An offline BOM does not establish price, availability, or complete manufacturer part numbers.

The documented `KICAD_PCBNEW` override did not select Python in the host test. A portable macOS copy worked with `KICAD_PYTHON_INTERPRETER` and `KICAD_PYTHON_SITE_PACKAGES` set to its bundled interpreter/site-packages, plus `KICAD_CLI` for the CLI. Ordinary installed KiCad is the simpler participant route.

If layout setup consumes the build time, keep the source, compiled connectivity and CAD, and record the layout stage as unfinished. Do not replace a failed tool run with a screenshot that implies success.

## Behavior demonstration

For a device with a controller, make the smallest replay that exercises the chosen interaction. Identify what is simulated: GPIO, time, sensor input, network response. If firmware is only syntax-checked or run with mocked pins, say so. Keep the pin map consistent with the wiring plan. Flashing hardware is a separate step when hardware is available.

For a mechanical idea, a section view, motion envelope or interference check can be more useful than firmware. Avoid adding a microcontroller merely because the workshop is about AI-assisted hardware.
