"""Draw the last frame of the 0.1 W transient for the 2512 on FR4.

case_final.vtu is the field at 585 s. The pictures are the whole coupon
and a closer view of the chip. This does not solve again. The movie and
the stills on the page come from render_movie.py, which locks the color
scale at 25 C. This script scales the bar to the range in case_final.vtu.

ParaView 5.10 in openfoam/openfoam11-paraview510 is an X11 program. Run it
as the desktop user. Offscreen rendering crashes it. From this directory:

    docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -e DISPLAY=:0 \
      -e XAUTHORITY=/tmp/.Xauthority \
      -v "$HOME/.Xauthority:/tmp/.Xauthority:ro" \
      -v /tmp/.X11-unix:/tmp/.X11-unix -v "$PWD":/work \
      --entrypoint bash openfoam/openfoam11-paraview510 \
      -lc '/opt/paraviewopenfoam510/bin/pvpython /work/render_temperature.py'
"""
import os

from paraview.simple import (
    ColorBy,
    GetActiveCamera,
    GetActiveViewOrCreate,
    GetColorTransferFunction,
    GetScalarBar,
    Render,
    ResetCamera,
    SaveScreenshot,
    Show,
    XMLUnstructuredGridReader,
)
from paraview import servermanager

HERE = os.path.dirname(os.path.abspath(__file__))
VTU = os.path.join(HERE, "case_final.vtu")
OUT = os.path.join(HERE, "images")
os.makedirs(OUT, exist_ok=True)

print(f"Reading {os.path.basename(VTU)}.", flush=True)
reader = XMLUnstructuredGridReader(FileName=[VTU])
reader.UpdatePipeline()
fetched = servermanager.Fetch(reader)
temp = fetched.GetPointData().GetArray("temperature")
low, high = temp.GetRange()
print(
    f"Points {fetched.GetNumberOfPoints()}, cells {fetched.GetNumberOfCells()}.",
    flush=True,
)
print(f"Temperature {low:.4f} C to {high:.4f} C.", flush=True)

view = GetActiveViewOrCreate("RenderView")
view.ViewSize = [1700, 950]
view.OrientationAxesVisibility = 0
display = Show(reader, view)
display.Representation = "Surface"
ColorBy(display, ("POINTS", "temperature"))
display.RescaleTransferFunctionToDataRange(False, True)
display.SetScalarBarVisibility(view, True)
lut = GetColorTransferFunction("temperature")
bar = GetScalarBar(lut, view)
bar.Title = "Temperature (C)"
bar.ComponentTitle = ""
bar.TitleColor = [0.0, 0.0, 0.0]
bar.LabelColor = [0.0, 0.0, 0.0]
bar.WindowLocation = "Any Location"
bar.Position = [0.90, 0.16]
bar.ScalarBarLength = 0.68

# White sheet. LoadPalette is applied after the bar so the bar colors stay black.
from paraview.simple import LoadPalette
LoadPalette("WhiteBackground")
bar.TitleColor = [0.0, 0.0, 0.0]
bar.LabelColor = [0.0, 0.0, 0.0]

ResetCamera(view)
camera = GetActiveCamera()
camera.Azimuth(40)
camera.Elevation(30)
ResetCamera(view)
camera.Zoom(1.05)
# Shift the long coupon left so the color bar sits in the margin.
camera.SetWindowCenter(0.16, 0.0)
Render(view)
SaveScreenshot(os.path.join(OUT, "temperature.png"), view, ImageResolution=[1700, 950])
print("Saved images/temperature.png.", flush=True)

# Look down on the chip from the side of one trace so both end caps and the
# start of each 20 mil trace are in frame. Distances are metres.
camera.SetFocalPoint(0.0, 0.0, 0.0003)
camera.SetPosition(0.009, -0.011, 0.010)
camera.SetViewUp(0.0, 0.0, 1.0)
camera.SetParallelProjection(False)
view.CameraParallelScale = 0.006
camera.SetWindowCenter(0.10, 0.0)
Render(view)
SaveScreenshot(os.path.join(OUT, "temperature_chip.png"), view, ImageResolution=[1700, 950])
print("Saved images/temperature_chip.png.", flush=True)
print("Color bar is in the right margin.", flush=True)
