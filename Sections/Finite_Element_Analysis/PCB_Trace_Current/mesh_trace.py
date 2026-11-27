#!/usr/bin/env python3
"""Turn the KiCad XAO into a volume mesh Elmer can read.

Place in the pipeline, after trace.xao exists and before ElmerGrid:

    salome shell -- python3 mesh_trace.py
    ElmerGrid 8 2 trace.unv -scale 1.0e-3 1.0e-3 1.0e-3 -out mesh

Use Salome's Python. The system interpreter has no salome module. The
shell command needs the "--" so Salome does not drop the script name.

The XAO coordinates are millimetres, and so are the mesh sizes below.
ElmerGrid's scale of 0.001 is what converts the mesh to metres. Skip that
scale and the conductivity and the current density are applied to a board
a thousand times too large.

The mesh groups are renamed input and output. case.sif attaches the 12 V
pad and the current sink to those names. A different board can use this
same script once its pad-face names are set in FRONT and BACK.

This step does not compute temperature. It only fills the copper with
tetrahedra. Heating is computed later from the current.
"""
import os
import sys

import salome

# Start a Salome session in this process. geomBuilder and smeshBuilder import
# only after that session exists.
salome.salome_init()
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder
import SMESH

HERE = os.path.dirname(os.path.abspath(__file__))
XAO = os.path.join(HERE, "trace.xao")
UNV = os.path.join(HERE, "trace.unv")
LOG = os.path.join(HERE, "mesh_trace.log")

# Each pair is (maximum element size, minimum element size) in millimetres.
# The first pair is the one this board accepted. The minimum, 0.08 mm, is
# thicker than the 0.035 mm foil. Netgen still built a volume mesh. The later
# pairs are finer fallbacks for a board where the coarse pair produces no
# tetrahedra. SetFineness(5) below means "custom", so these two numbers are
# the ones Netgen uses.
CANDIDATES = (
    (0.20, 0.08),
    (0.10, 0.02),
    (0.05, 0.01),
    (0.035, 0.008),
)

# Face names KiCad wrote into the XAO. They name the front and back pads.
# mesh.GroupOnGeom copies them onto the mesh as input and output.
FRONT = "Pad_F_J1_A_TRACE"
BACK = "Pad_B_J1_B_TRACE"


def log(line):
    # Print and keep a copy. Salome's own console is easy to lose.
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def main():
    # Start a fresh log so a failed size is not mixed with an older run.
    if os.path.exists(LOG):
        os.remove(LOG)
    # geompy reads and measures the CAD solid. smesh meshes it.
    geompy = geomBuilder.New()
    smesh = smeshBuilder.New()

    # ImportXAO returns the solid, any sub-shapes, the named groups, and
    # fields. This file has one solid and two face groups. The fields are
    # unused. ok is false when the file is not a readable XAO.
    ok, shape, _sub, groups, _fields = geompy.ImportXAO(XAO)
    if not ok:
        raise SystemExit("ImportXAO failed for " + XAO)
    # Publish the solid in the Salome study under the name "trace".
    geompy.addToStudy(shape, "trace")
    log(f"Imported {os.path.basename(XAO)}.")
    log("The file holds one fused copper solid and the named pad faces. There is no FR4 in it.")
    # Box of the solid in millimetres. KiCad's Y axis is flipped in the
    # OpenCASCADE solid, so a board drawn at positive y can show a negative
    # y here. The log is the check that the export landed where expected.
    xmin, xmax, ymin, ymax, zmin, zmax = geompy.BoundingBox(shape)
    log(
        "Bounding box of the solid, millimetres: "
        f"x from {xmin:.6g} to {xmax:.6g}, "
        f"y from {ymin:.6g} to {ymax:.6g}, "
        f"z from {zmin:.6g} to {zmax:.6g}."
    )
    log("KiCad's Y axis is flipped in this solid, so the pads sit at negative y.")

    # Measure every named face. area from BasicProperties is mm^2. Elmer's
    # current density is A/m^2, and 1 mm^2 = 1e-6 m^2. For this board each
    # pad is 4 mm^2, so 0.5 A leaving the pad is -0.5/4e-6 = -125000 A/m^2.
    # A new board needs that division repeated. Do not reuse 125000.
    by_name = {}
    for group in groups:
        name = group.GetName()
        by_name[name] = group
        geompy.addToStudyInFather(shape, group, name)
        length, area, volume = geompy.BasicProperties(group)
        area_m2 = area * 1.0e-6
        log(
            f"Group {name}: length {length:.6g} mm, "
            f"area {area:.6g} mm^2 ({area_m2:.6g} m^2), "
            f"volume {volume:.6g} mm^3."
        )
        if name == BACK and area_m2 > 0.0:
            # 0.5 A leaves through the output pad. Negative density is the
            # Elmer sign for current leaving the solid. A new board must
            # recompute this from the measured area.
            density = -0.5 / area_m2
            log(
                "  The output pad sinks 0.5 A, so the boundary current density "
                f"is {density:.6g} A/m^2. case.sif must use this value."
            )

    if FRONT not in by_name or BACK not in by_name:
        raise SystemExit("pad groups missing: " + ", ".join(sorted(by_name)))

    chosen = None
    mesh = None
    for max_mm, min_mm in CANDIDATES:
        # A new mesh object for this size pair. The name records the sizes
        # that were tried.
        mesh = smesh.Mesh(shape, f"trace_{max_mm}_{min_mm}")
        # Netgen 1D-2D-3D builds the edges, then the surface triangles, then
        # the tetrahedra. One algorithm owns all three.
        algo = mesh.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
        # 5 is Netgen's custom fineness. Without it, SetMaxSize is ignored.
        algo.SetFineness(5)
        algo.SetMaxSize(max_mm)
        algo.SetMinSize(min_mm)
        # Linear tetrahedra have four nodes. Elmer's static-current solver
        # uses those. Second order would add mid-edge nodes and a much
        # larger system.
        algo.SetSecondOrder(False)
        # Copy each pad face onto the mesh and rename it. SMESH.FACE means
        # the group is a surface. Elmer boundary conditions can only target
        # a surface group. The names input and output must match case.sif.
        input_group = mesh.GroupOnGeom(by_name[FRONT], "input", SMESH.FACE)
        output_group = mesh.GroupOnGeom(by_name[BACK], "output", SMESH.FACE)
        log(
            f"Meshing with Netgen 1D-2D-3D. Maximum element {max_mm} mm, "
            f"minimum element {min_mm} mm, linear tetrahedra."
        )
        if min_mm > 0.035:
            log(
                f"  The minimum size {min_mm} mm is thicker than the "
                "0.035 mm foil. Netgen can still fill this solid."
            )
        computed = mesh.Compute()
        volumes = mesh.NbVolumes()
        log(
            f"  Compute returned {computed}. "
            f"Nodes {mesh.NbNodes()}, faces {mesh.NbFaces()}, "
            f"tetrahedra {volumes}."
        )
        # A mesh with no tetrahedra is not a copper volume. Try the next,
        # finer pair. GetLog keeps Netgen's reason.
        if not computed or volumes == 0:
            for err in mesh.GetLog():
                log("  " + str(err))
            continue
        log(
            f"  Mesh group input ({FRONT}) has {input_group.Size()} faces. "
            f"Mesh group output ({BACK}) has {output_group.Size()} faces."
        )
        log("  Those two names are the boundary names in case.sif.")
        chosen = (max_mm, min_mm)
        break

    if chosen is None:
        raise SystemExit("no volume mesh; see " + LOG)

    # ExportUNV writes trace.unv and returns None even when the file is good.
    # The header of that file says the units are metres, but the node
    # coordinates are still millimetres. ElmerGrid must scale them.
    mesh.ExportUNV(UNV)
    if not os.path.isfile(UNV) or os.path.getsize(UNV) < 1000:
        raise SystemExit("ExportUNV failed")
    log(
        f"Wrote {os.path.basename(UNV)} ({os.path.getsize(UNV)} bytes) "
        f"with element sizes {chosen[0]} mm maximum and {chosen[1]} mm minimum."
    )
    log("The UNV header says metres, but the node coordinates are still millimetres.")
    log("Next command: ElmerGrid 8 2 trace.unv -scale 1.0e-3 1.0e-3 1.0e-3 -out mesh")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)
