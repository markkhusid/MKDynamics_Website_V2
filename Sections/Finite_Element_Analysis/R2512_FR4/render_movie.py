"""Draw the 0.1 W transient temperature of the 2512 on FR4.

Elmer writes one VTU per timestep, case_t0001.vtu onward. Pass that
directory as the first argument. The color scale is fixed from 25 C to the
hottest node in the series, so a late frame is not stretched to look like
an early one. The clock in the corner is the simulation time.

The step schedule has to match case.sif: 10 steps of 0.5 s, 20 of 5 s,
and 24 of 20 s. The last frame is at 585 s.

Stills of the last frame are images/temperature.png and
images/temperature_chip.png. The movie frames go to the directory given
by the second argument. ffmpeg on the host turns those frames into
images/temperature_evolution.mp4.

ParaView 5.10 is an X11 program. From this directory, with the VTU
directory and a frame directory mounted:

    docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -e DISPLAY=:0 \
      -e XAUTHORITY=/tmp/.Xauthority \
      -v "$HOME/.Xauthority:/tmp/.Xauthority:ro" \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      -v "$PWD":/work -v /tmp/r2512_vtus:/vtus -v /tmp/r2512_frames:/frames \
      --entrypoint bash openfoam/openfoam11-paraview510 \
      -lc '/opt/paraviewopenfoam510/bin/pvpython /work/render_movie.py /vtus /frames'
"""
import glob
import os
import sys

from paraview.simple import (
    ColorBy,
    GetActiveCamera,
    GetActiveViewOrCreate,
    GetColorTransferFunction,
    GetScalarBar,
    Hide,
    Render,
    ResetCamera,
    SaveScreenshot,
    Show,
    Text,
    XMLUnstructuredGridReader,
)
from paraview.simple import LoadPalette
from paraview import servermanager

# Must match Timestep Intervals and Timestep Sizes in case.sif.
SCHEDULE = ((10, 0.5), (20, 5.0), (24, 20.0))


def time_at(step):
    """Simulation time in seconds at a 1-based Elmer output index."""
    remaining = step
    elapsed = 0.0
    for count, size in SCHEDULE:
        take = min(remaining, count)
        elapsed += take * size
        remaining -= take
        if remaining == 0:
            return elapsed
    raise RuntimeError("step %s is past the schedule" % step)


def main():
    vtu_dir = sys.argv[1]
    frame_dir = sys.argv[2]
    here = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(here, "images")
    os.makedirs(frame_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

    paths = sorted(glob.glob(os.path.join(vtu_dir, "case_t*.vtu")))
    if not paths:
        raise SystemExit("no case_t*.vtu files in " + vtu_dir)
    print("VTU files: %d" % len(paths), flush=True)

    reader = XMLUnstructuredGridReader(FileName=[paths[-1]])
    reader.UpdatePipeline()
    fetched = servermanager.Fetch(reader)
    temp = fetched.GetPointData().GetArray("temperature")
    last_low, last_high = temp.GetRange()
    print(
        "Last file %s, temperature %.4f C to %.4f C."
        % (os.path.basename(paths[-1]), last_low, last_high),
        flush=True,
    )
    # Early frames stay near the air temperature. Lock the bar to that floor
    # and to the hottest node of the run so the colors mean the same thing
    # in every frame.
    scale_low = 25.0
    scale_high = last_high

    view = GetActiveViewOrCreate("RenderView")
    view.ViewSize = [1280, 720]
    view.OrientationAxesVisibility = 0
    display = Show(reader, view)
    display.Representation = "Surface"
    ColorBy(display, ("POINTS", "temperature"))
    lut = GetColorTransferFunction("temperature")
    lut.RescaleTransferFunction(scale_low, scale_high)
    display.SetScalarBarVisibility(view, True)
    bar = GetScalarBar(lut, view)
    bar.Title = "Temperature (C)"
    bar.ComponentTitle = ""
    bar.TitleColor = [0.0, 0.0, 0.0]
    bar.LabelColor = [0.0, 0.0, 0.0]
    bar.WindowLocation = "Any Location"
    bar.Position = [0.88, 0.16]
    bar.ScalarBarLength = 0.68
    LoadPalette("WhiteBackground")
    bar.TitleColor = [0.0, 0.0, 0.0]
    bar.LabelColor = [0.0, 0.0, 0.0]

    clock = Text(registrationName="Clock")
    clock.Text = "t = 0 s"
    clock_display = Show(clock, view)
    clock_display.FontSize = 22
    clock_display.Color = [0.0, 0.0, 0.0]
    clock_display.Bold = 1
    clock_display.Justification = "Left"
    clock_display.WindowLocation = "Any Location"
    clock_display.Position = [0.04, 0.90]

    ResetCamera(view)
    camera = GetActiveCamera()
    camera.Azimuth(40)
    camera.Elevation(30)
    ResetCamera(view)
    camera.Zoom(1.05)
    camera.SetWindowCenter(0.16, 0.0)
    focal = tuple(camera.GetFocalPoint())
    position = tuple(camera.GetPosition())
    view_up = tuple(camera.GetViewUp())
    window_center = tuple(camera.GetWindowCenter())

    for index, path in enumerate(paths, start=1):
        elapsed = time_at(index)
        reader.FileName = [path]
        reader.UpdatePipeline()
        fetched = servermanager.Fetch(reader)
        low, high = fetched.GetPointData().GetArray("temperature").GetRange()
        if high > scale_high + 1.0e-6:
            raise SystemExit(
                "frame %d is hotter than the last frame (%.4f > %.4f)"
                % (index, high, scale_high)
            )
        clock.Text = "t = %.1f s" % elapsed
        camera.SetFocalPoint(*focal)
        camera.SetPosition(*position)
        camera.SetViewUp(*view_up)
        camera.SetWindowCenter(*window_center)
        lut.RescaleTransferFunction(scale_low, scale_high)
        Render(view)
        frame_path = os.path.join(frame_dir, "frame_%04d.png" % index)
        SaveScreenshot(frame_path, view, ImageResolution=[1280, 720])
        print(
            "frame %02d  t %7.1f s  %6.2f C to %6.2f C" % (index, elapsed, low, high),
            flush=True,
        )

    # The page stills use the last frame and the wider canvas.
    view.ViewSize = [1700, 950]
    bar.Position = [0.90, 0.16]
    camera.SetFocalPoint(*focal)
    camera.SetPosition(*position)
    camera.SetViewUp(*view_up)
    camera.SetWindowCenter(0.16, 0.0)
    Hide(clock, view)
    Render(view)
    SaveScreenshot(
        os.path.join(image_dir, "temperature.png"),
        view,
        ImageResolution=[1700, 950],
    )
    print("Saved images/temperature.png.", flush=True)

    camera.SetFocalPoint(0.0, 0.0, 0.0003)
    camera.SetPosition(0.009, -0.011, 0.010)
    camera.SetViewUp(0.0, 0.0, 1.0)
    camera.SetParallelProjection(False)
    view.CameraParallelScale = 0.006
    camera.SetWindowCenter(0.10, 0.0)
    Render(view)
    SaveScreenshot(
        os.path.join(image_dir, "temperature_chip.png"),
        view,
        ImageResolution=[1700, 950],
    )
    print("Saved images/temperature_chip.png.", flush=True)
    print(
        "Color scale locked at %.2f C to %.2f C." % (scale_low, scale_high),
        flush=True,
    )


if __name__ == "__main__":
    main()
