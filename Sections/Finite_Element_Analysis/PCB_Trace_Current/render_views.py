"""Draw the potential and the Joule heating from Elmer's VTU file.

This is the last step of the current-conduction pipeline. case_t0001.vtu
must already exist beside this script. The pictures are the two figures
on the page. Nothing here changes the solution.

The ParaView 5.10 build in openfoam/openfoam11-paraview510 is an X11
program. It has to run as the desktop user and see the host display.
Forcing offscreen rendering crashes it in XSync. From this directory:

    docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -e DISPLAY=:0 \
      -e XAUTHORITY=/tmp/.Xauthority \
      -v "$HOME/.Xauthority:/tmp/.Xauthority:ro" \
      -v /tmp/.X11-unix:/tmp/.X11-unix -v "$PWD":/work \
      --entrypoint bash openfoam/openfoam11-paraview510 \
      -lc '/opt/paraviewopenfoam510/bin/pvpython /work/render_views.py'

A later heat solution would be drawn by pointing this same script at the
heat case's VTU and naming the temperature field. This file draws the
current-case fields only.
"""
import os

from paraview.simple import (
    ColorBy,
    GetActiveCamera,
    GetActiveViewOrCreate,
    GetColorTransferFunction,
    GetScalarBar,
    HideScalarBarIfNotNeeded,
    LoadPalette,
    Render,
    ResetCamera,
    SaveScreenshot,
    Show,
    XMLUnstructuredGridReader,
)
from paraview import servermanager

def say(line):
    print(line, flush=True)


HERE = os.path.dirname(os.path.abspath(__file__))
# Elmer wrote this into the mesh directory. It was copied here next to the page.
VTU = os.path.join(HERE, "case_t0001.vtu")
OUT = os.path.join(HERE, "images")
os.makedirs(OUT, exist_ok=True)

say(f"Reading {os.path.basename(VTU)}.")
# Read the unstructured tetrahedra and the nodal fields.
reader = XMLUnstructuredGridReader(FileName=[VTU])
reader.UpdatePipeline()
# Fetch pulls the dataset out of the server so the ranges can be printed.
# The picture itself is drawn from reader, not from this fetched copy.
fetched = servermanager.Fetch(reader)
point_data = fetched.GetPointData()
names = [point_data.GetArrayName(i) for i in range(point_data.GetNumberOfArrays())]
say(
    f"VTU has {fetched.GetNumberOfPoints()} points and "
    f"{fetched.GetNumberOfCells()} cells."
)
say("Point fields: " + ", ".join(names) + ".")
say("Drawing potential and Joule heating. This script does not solve either field.")


def field_range(name):
    # GetRange on a scalar array is (min, max). On the three-component
    # "volume current" array it is the range of the first component only,
    # which is not the magnitude. The loop at the bottom computes that.
    array = fetched.GetPointData().GetArray(name)
    return array.GetRange()


view = GetActiveViewOrCreate("RenderView")
# The default palette is dark. The page figures need a white sheet.
LoadPalette("WhiteBackground")
# Wide frame so the color bar can sit in the empty region to the right.
view.ViewSize = [1700, 950]
# The corner triad overlaps the copper at this zoom.
view.OrientationAxesVisibility = 0

display = Show(reader, view)
# Surface paints the outside of the tetrahedra. The foil is thin, so the
# outside shows the pads, the traces, and the via barrel.
display.Representation = "Surface"

# Fit the copper, then look down at an angle so both pads and the via read
# as separate objects. The window center shifts the copper toward the left
# so the legend is not drawn on top of the output pad.
ResetCamera(view)
camera = GetActiveCamera()
camera.Azimuth(35)
camera.Elevation(25)
ResetCamera(view)
camera.Zoom(1.15)
camera.SetWindowCenter(0.28, 0.0)
say("Camera azimuth 35 degrees, elevation 25 degrees. The copper is shifted left to leave room for the legend.")


def save(field, filename, title):
    # Color the surface by this nodal field.
    ColorBy(display, ("POINTS", field))
    # Stretch the color scale across this field's own min and max.
    # The potential only falls 3.35 mV, so its bar runs from about
    # 11.997 V to 12 V, not from 0 V to 12 V.
    display.RescaleTransferFunctionToDataRange(False, True)
    # Drop both bars before showing the one for this field. Leaving the
    # potential bar up puts its tick labels on the heating figure.
    HideScalarBarIfNotNeeded(GetColorTransferFunction("potential"), view)
    HideScalarBarIfNotNeeded(GetColorTransferFunction("joule heating"), view)
    display.SetScalarBarVisibility(view, True)
    lut = GetColorTransferFunction(field)
    bar = GetScalarBar(lut, view)
    bar.Title = title
    # A scalar field has no component title. An empty string suppresses it.
    bar.ComponentTitle = ""
    bar.TitleColor = [0.0, 0.0, 0.0]
    bar.LabelColor = [0.0, 0.0, 0.0]
    # Place the bar by hand, in the open margin to the right of the copper.
    # "Any Location" lets Position take effect. Position is the lower-left
    # corner of the bar in fractions of the view.
    bar.WindowLocation = "Any Location"
    bar.Position = [0.90, 0.16]
    bar.ScalarBarLength = 0.68
    Render(view)
    path = os.path.join(OUT, filename)
    SaveScreenshot(path, view, ImageResolution=[1700, 950])
    low, high = field_range(field)
    say(f"Saved {filename}.")
    say(f"  {title}: minimum {low:.8g}, maximum {high:.8g}.")
    say("  The color bar is in the right margin, clear of the copper.")
    say(f"  File: images/{filename}")


save("potential", "potential.png", "Electric potential (V)")
save("joule heating", "joule_heating.png", "Joule heating (W/m^3)")
# Report the vector range too. GetRange here is one component, so the next
# loop is the magnitude a reader should compare with the 0.4 mm trace.
current = field_range("volume current")
say(
    "Volume current is a 3-component vector. VTK's range on that array is "
    f"the first component only: {current[0]:.8g} to {current[1]:.8g} A/m^2."
)
mag = fetched.GetPointData().GetArray("volume current")
lo = 1.0e300
hi = 0.0
for i in range(mag.GetNumberOfTuples()):
    x, y, z = mag.GetTuple(i)
    value = (x * x + y * y + z * z) ** 0.5
    if value < lo:
        lo = value
    if value > hi:
        hi = value
say(f"Volume-current magnitude over the nodes: {lo:.8g} to {hi:.8g} A/m^2.")
say("A 0.5 A current in a 0.4 mm by 0.035 mm section is about 3.57e7 A/m^2.")
