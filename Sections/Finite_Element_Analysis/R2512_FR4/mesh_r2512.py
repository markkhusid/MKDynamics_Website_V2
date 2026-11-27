#!/usr/bin/env python3
"""Mesh a 2512 chip, two copper traces, and an FR4 coupon for Elmer.

Run with Salome's Python, from this directory:

    salome shell -- python3 mesh_r2512.py

The chip is the official KiCad solid R_2512_6332Metric.step. Salome reads
that file in metres. This script scales it to millimetres so the mesh matches
the trace page, and ElmerGrid scales those millimetres back to metres.

The STEP is one solid. It has no separate film, glass, nickel, or tin, and it
has no board. The traces and the FR4 are built here from the dimensions below.
The 0.1 W is spread through the whole chip volume because the file has no film
volume to put it in. The case is transient so the temperature rise can be filmed.
"""
import os

import salome

salome.salome_init()
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder
import SMESH

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(HERE, "R_2512_6332Metric.step")
UNV = os.path.join(HERE, "r2512.unv")
SIF = os.path.join(HERE, "case.sif")
LOG = os.path.join(HERE, "mesh_r2512.log")

# 20 mil is 0.508 mm. One inch is 25.4 mm. Both are exact.
TRACE_WIDTH_MM = 20.0 * 0.0254
TRACE_LENGTH_MM = 25.4
# 1 oz copper, the same foil thickness as the trace page.
COPPER_MM = 0.035
# A standard finished-board thickness. The Vishay datasheet does not give one.
FR4_MM = 1.6
# Bare FR4 past each trace end, and past each side of the chip. The datasheet
# does not define this coupon. These two numbers are the board that was meshed.
END_MARGIN_MM = 2.0
SIDE_MARGIN_MM = 5.0
POWER_W = 0.1
# CoorsTek AD-96: 3.72 g/cm^3 (ASTM C20), 880 J/(kg K) at 100 C (ASTM E1269).
ALUMINA_RHO = 3720.0
ALUMINA_CP = 880.0
# Room-temperature pure copper, paired with the 401 W/(m K) conductivity.
COPPER_RHO = 8960.0
COPPER_CP = 385.0
# Isola 370HR does not publish density or specific heat. 1850 kg/m^3 is the
# usual FR-4 specific gravity, 1.85. 1000 J/(kg K) is a round glass-epoxy
# value. They set the time scale. The steady temperature does not use them.
FR4_RHO = 1850.0
FR4_CP = 1000.0
# Frames: 10 at 0.5 s, 20 at 5 s, 24 at 20 s. Last frame is at 585 s.
TIMESTEP_INTERVALS = (10, 20, 24)
TIMESTEP_SIZES = (0.5, 5.0, 20.0)

# Coarse pair first. The foil is thinner than the minimum size; Netgen still
# filled the 0.035 mm trace on the earlier board. The later pairs are fallbacks.
CANDIDATES = (
    (0.35, 0.08),
    (0.25, 0.05),
    (0.15, 0.03),
)


def log(line):
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def rect_face(geompy, x0, y0, z, x1, y1):
    # A planar rectangle used as a partition tool so the touching solids share
    # a face. Without the imprint, a zero-volume contact can be dropped.
    points = [
        geompy.MakeVertex(x0, y0, z),
        geompy.MakeVertex(x1, y0, z),
        geompy.MakeVertex(x1, y1, z),
        geompy.MakeVertex(x0, y1, z),
    ]
    edges = [
        geompy.MakeEdge(points[0], points[1]),
        geompy.MakeEdge(points[1], points[2]),
        geompy.MakeEdge(points[2], points[3]),
        geompy.MakeEdge(points[3], points[0]),
    ]
    return geompy.MakeFace(geompy.MakeWire(edges), True)


def write_sif(volume_m3):
    # Body names are the Salome groups. ElmerGrid writes mesh.names, and
    # ElmerSolver substitutes the $ names from that file.
    # HeatSolve multiplies Heat Source by Density, so the value in the body
    # force is watts per kilogram. Density times that value times volume is
    # the 0.1 W.
    source_w_kg = POWER_W / (ALUMINA_RHO * volume_m3)
    counts = " ".join(str(n) for n in TIMESTEP_INTERVALS)
    sizes = " ".join(f"{dt:.1f}" for dt in TIMESTEP_SIZES)
    nspan = len(TIMESTEP_INTERVALS)
    text = f"""! Transient heat conduction for one 2512 chip on FR4.
! The chip solid is R_2512_6332Metric.step, scaled to metres by ElmerGrid.
! It is one body. The 0.1 W is uniform in that volume. There is no separate
! resistive film in the CAD file.
!
! Chip conductivity is 24.7 W/(m K), CoorsTek ADD-96 96% alumina, ASTM C408.
! The tin terminations are not a separate solid, so they use that same value.
! Copper is 401 W/(m K), pure copper near 300 K. The foil is 0.035 mm (1 oz).
! FR4 is 0.4 W/(m K) in every direction, the single Isola 370HR value from
! ASTM E1952. That test is through the thickness. The glass fabric is
! anisotropic; this case does not add an in-plane conductivity.
! Alumina density is {ALUMINA_RHO:.0f} kg/m^3 and specific heat is {ALUMINA_CP:.0f} J/(kg K)
! at 100 C, CoorsTek AD-96, ASTM C20 and ASTM E1269.
! Copper density is {COPPER_RHO:.0f} kg/m^3 and specific heat is {COPPER_CP:.0f} J/(kg K).
! Isola does not publish a 370HR density or specific heat. This case uses
! {FR4_RHO:.0f} kg/m^3, the usual FR-4 specific gravity of 1.85, and
! {FR4_CP:.0f} J/(kg K). Those two numbers set how fast the board warms.
! They do not set the final temperature.
!
! Each trace is 20 mil wide and 1 inch long, measured from the outer end of
! the body. Under the part, the trace covers the bottom metal of that end cap
! and stays 20 mil wide. It does not widen into the Vishay land pattern.
! Open surfaces lose heat by a coefficient of 10 W/(m^2 K) to air at 25 C.
! That coefficient is a mid-range natural-convection value, not a measurement
! of this coupon.
!
! Chip volume {volume_m3:.8e} m^3. Alumina density {ALUMINA_RHO:.1f} kg/m^3.
! Heat source {source_w_kg:.8e} W/kg. Product {ALUMINA_RHO * source_w_kg * volume_m3:.6f} W.
! Steps: {counts} intervals of {sizes} seconds. The last frame is at 585 s.

Header
  Mesh DB "." "mesh"
End

! ElmerGrid writes these $ names. They have to be included before the
! Body sections. The solver does not load mesh.names until after this file
! is parsed, so a bare "$ chip" is an unknown MATC name without this line.
Include "mesh/mesh.names"

Simulation
  Max Output Level = 4
  Coordinate System = Cartesian
  Simulation Type = Transient
  Timestepping Method = BDF
  BDF Order = 2
  Timestep Intervals({nspan}) = {counts}
  Timestep Sizes({nspan}) = {sizes}
  Output Intervals({nspan}) = {" ".join(["1"] * nspan)}
  Post File = case.vtu
End

Body 1
  Name = chip
  Target Bodies(1) = $ chip
  Equation = 1
  Material = 1
  Body Force = 1
  Initial Condition = 1
End

Body 2
  Name = copper_left
  Target Bodies(1) = $ copper_left
  Equation = 1
  Material = 2
  Initial Condition = 1
End

Body 3
  Name = copper_right
  Target Bodies(1) = $ copper_right
  Equation = 1
  Material = 2
  Initial Condition = 1
End

Body 4
  Name = fr4
  Target Bodies(1) = $ fr4
  Equation = 1
  Material = 3
  Initial Condition = 1
End

Solver 1
  Equation = Heat Equation
  Variable = Temperature
  Variable Dofs = 1
  Procedure = "HeatSolve" "HeatSolver"
  Linear System Solver = Iterative
  Linear System Iterative Method = BiCGStab
  Linear System Preconditioning = ILU1
  Linear System Max Iterations = 2000
  Linear System Convergence Tolerance = 1.0e-10
  Nonlinear System Max Iterations = 1
  Nonlinear System Convergence Tolerance = 1.0e-8
  Steady State Convergence Tolerance = 1.0e-8
End

Equation 1
  Name = Heat
  Active Solvers(1) = 1
End

! HeatSolve multiplies Heat Source by Density. The source is therefore
! W/kg, and Density * Heat Source * volume is the electrical power.
! The storage term is Density * Heat Capacity * dT/dt.
Material 1
  Name = alumina
  Heat Conductivity = 24.7
  Density = {ALUMINA_RHO:.1f}
  Heat Capacity = {ALUMINA_CP:.1f}
End

Material 2
  Name = copper
  Heat Conductivity = 401.0
  Density = {COPPER_RHO:.1f}
  Heat Capacity = {COPPER_CP:.1f}
End

Material 3
  Name = fr4
  Heat Conductivity = 0.4
  Density = {FR4_RHO:.1f}
  Heat Capacity = {FR4_CP:.1f}
End

Body Force 1
  Name = chip_power
  Heat Source = {source_w_kg:.8e}
End

Initial Condition 1
  Name = ambient
  Temperature = 25.0
End

Boundary Condition 1
  Name = air
  Target Boundaries(1) = $ air
  Heat Transfer Coefficient = 10.0
  External Temperature = 25.0
End
"""
    with open(SIF, "w", encoding="utf-8") as handle:
        handle.write(text)
    log(
        f"Wrote case.sif. Heat source {source_w_kg:.6g} W/kg "
        f"in {volume_m3:.6g} m^3 at {ALUMINA_RHO:.0f} kg/m^3 "
        f"is {ALUMINA_RHO * source_w_kg * volume_m3:.6f} W."
    )


def main():
    if os.path.exists(LOG):
        os.remove(LOG)
    geompy = geomBuilder.New()
    smesh = smeshBuilder.New()

    chip = geompy.ImportSTEP(STEP)
    xmin, xmax, ymin, ymax, zmin, zmax = geompy.BoundingBox(chip)
    span = xmax - xmin
    log(f"Imported {os.path.basename(STEP)}.")
    log(
        "Bounding box as read: "
        f"x {xmin:.6g} to {xmax:.6g}, y {ymin:.6g} to {ymax:.6g}, "
        f"z {zmin:.6g} to {zmax:.6g}."
    )
    # A span near 6.3 is already millimetres. A span near 0.0063 is metres.
    if span < 0.1:
        origin = geompy.MakeVertex(0, 0, 0)
        chip = geompy.MakeScaleTransform(chip, origin, 1000.0)
        log("Scaled the solid by 1000. Later numbers are millimetres.")
    xmin, xmax, ymin, ymax, zmin, zmax = geompy.BoundingBox(chip)
    log(
        "Chip bounding box, millimetres: "
        f"x {xmin:.4f} to {xmax:.4f}, y {ymin:.4f} to {ymax:.4f}, "
        f"z {zmin:.4f} to {zmax:.4f}."
    )
    # Sit the lowest face of the end caps on top of the foil.
    chip = geompy.MakeTranslation(chip, 0, 0, COPPER_MM - zmin)
    xmin, xmax, ymin, ymax, zmin, zmax = geompy.BoundingBox(chip)
    length, area, volume = geompy.BasicProperties(chip)
    log(
        f"Chip after the lift: z {zmin:.4f} to {zmax:.4f}. "
        f"Volume {volume:.4f} mm^3, surface {area:.4f} mm^2."
    )

    # Bottom faces are the end-cap metal. The ceramic underside is higher,
    # at about 0.06 mm in the STEP, so it does not land on this list.
    bottom = []
    for face in geompy.SubShapeAll(chip, geompy.ShapeType["FACE"]):
        fx0, fx1, fy0, fy1, fz0, fz1 = geompy.BoundingBox(face)
        if fz1 > zmin + 0.02:
            continue
        face_area = geompy.BasicProperties(face)[1]
        if face_area < 0.05:
            continue
        bottom.append((fx0, fx1, fy0, fy1, face_area))
        log(
            "Bottom face, millimetres: "
            f"x {fx0:.4f} to {fx1:.4f}, y {fy0:.4f} to {fy1:.4f}, "
            f"area {face_area:.4f} mm^2."
        )
    if len(bottom) < 2:
        raise SystemExit("expected a bottom face on each end cap")

    left = [item for item in bottom if 0.5 * (item[0] + item[1]) < 0.0]
    right = [item for item in bottom if 0.5 * (item[0] + item[1]) > 0.0]
    if not left or not right:
        raise SystemExit("bottom faces are not one per end")
    # Inner edge of the metal is the end of the trace under the cap.
    # Outer edge of the body is where the 1 inch trace begins.
    left_inner = max(item[1] for item in left)
    left_outer = min(item[0] for item in left)
    right_inner = min(item[0] for item in right)
    right_outer = max(item[1] for item in right)
    half_w = 0.5 * TRACE_WIDTH_MM
    left_x0 = left_outer - TRACE_LENGTH_MM
    right_x1 = right_outer + TRACE_LENGTH_MM
    log(
        f"Left trace x {left_x0:.4f} to {left_inner:.4f} mm. "
        f"The outer {TRACE_LENGTH_MM:.4f} mm is the 1 inch run. "
        f"The inner part covers the end-cap bottom."
    )
    log(
        f"Right trace x {right_inner:.4f} to {right_x1:.4f} mm. "
        f"Width {TRACE_WIDTH_MM:.4f} mm (20 mil). Thickness {COPPER_MM} mm."
    )

    left_cu = geompy.MakeBox(left_x0, -half_w, 0.0, left_inner, half_w, COPPER_MM)
    right_cu = geompy.MakeBox(right_inner, -half_w, 0.0, right_x1, half_w, COPPER_MM)
    board_x0 = left_x0 - END_MARGIN_MM
    board_x1 = right_x1 + END_MARGIN_MM
    board_y0 = ymin - SIDE_MARGIN_MM
    board_y1 = ymax + SIDE_MARGIN_MM
    fr4 = geompy.MakeBox(board_x0, board_y0, -FR4_MM, board_x1, board_y1, 0.0)
    log(
        "FR4 coupon, millimetres: "
        f"x {board_x0:.4f} to {board_x1:.4f}, "
        f"y {board_y0:.4f} to {board_y1:.4f}, "
        f"z {-FR4_MM:.4f} to 0. Thickness {FR4_MM} mm. "
        f"Side margin {SIDE_MARGIN_MM} mm, end margin {END_MARGIN_MM} mm."
    )

    tools = [
        rect_face(geompy, left_x0, -half_w, 0.0, left_inner, half_w),
        rect_face(geompy, right_inner, -half_w, 0.0, right_x1, half_w),
        rect_face(geompy, left_x0, -half_w, COPPER_MM, left_inner, half_w),
        rect_face(geompy, right_inner, -half_w, COPPER_MM, right_x1, half_w),
    ]
    # Fuzzy tolerance is 0.0001 mm. It glues faces that the STEP rounded off
    # by less than that, and it does not bridge the 0.035 mm foil.
    partition = geompy.MakePartition(
        [chip, left_cu, right_cu, fr4],
        tools,
        theFuzzyParam=1.0e-4,
    )
    geompy.addToStudy(partition, "r2512")
    solids = geompy.SubShapeAll(partition, geompy.ShapeType["SOLID"])
    log(f"Partition produced {len(solids)} solids.")

    named = {}
    for solid in solids:
        sx0, sx1, sy0, sy1, sz0, sz1 = geompy.BoundingBox(solid)
        svol = geompy.BasicProperties(solid)[2]
        cx = 0.5 * (sx0 + sx1)
        if svol > 50.0:
            name = "fr4"
        elif (sz1 - sz0) > 0.2:
            name = "chip"
        elif cx < 0.0:
            name = "copper_left"
        else:
            name = "copper_right"
        if name in named:
            raise SystemExit("two solids classified as " + name)
        named[name] = solid
        geompy.addToStudyInFather(partition, solid, name)
        log(
            f"Solid {name}: volume {svol:.4f} mm^3, "
            f"x {sx0:.4f} to {sx1:.4f}, y {sy0:.4f} to {sy1:.4f}, "
            f"z {sz0:.4f} to {sz1:.4f}."
        )
    for required in ("chip", "copper_left", "copper_right", "fr4"):
        if required not in named:
            raise SystemExit("missing solid " + required)

    def shared_faces(name_a, name_b):
        # GetSharedShapes returns a list of faces, not one compound.
        return geompy.GetSharedShapes(
            named[name_a], named[name_b], geompy.ShapeType["FACE"]
        ) or []

    def area_of(faces):
        total = 0.0
        for face in faces:
            total += geompy.BasicProperties(face)[1]
        return total

    for copper_name in ("copper_left", "copper_right"):
        chip_area = area_of(shared_faces("chip", copper_name))
        log(f"Contact face, chip to {copper_name}: {chip_area:.4f} mm^2.")
        if chip_area < 0.05:
            raise SystemExit("chip does not share a face with " + copper_name)
        board_area = area_of(shared_faces("fr4", copper_name))
        log(f"Contact face, FR4 to {copper_name}: {board_area:.4f} mm^2.")
        if board_area < 1.0:
            raise SystemExit("FR4 does not share the trace footprint with " + copper_name)

    # External skin: every face that is not a chip/copper or FR4/copper contact.
    shared_keys = set()
    for left_name, right_name in (
        ("chip", "copper_left"),
        ("chip", "copper_right"),
        ("fr4", "copper_left"),
        ("fr4", "copper_right"),
    ):
        for face in shared_faces(left_name, right_name):
            bb = geompy.BoundingBox(face)
            center = tuple(round(0.5 * (bb[i] + bb[i + 1]), 4) for i in (0, 2, 4))
            shared_keys.add(center)
    air_faces = []
    for solid in named.values():
        for face in geompy.SubShapeAll(solid, geompy.ShapeType["FACE"]):
            bb = geompy.BoundingBox(face)
            center = tuple(round(0.5 * (bb[i] + bb[i + 1]), 4) for i in (0, 2, 4))
            if center not in shared_keys:
                air_faces.append(face)
    air = geompy.GetInPlace(partition, geompy.MakeCompound(air_faces))
    geompy.addToStudyInFather(partition, air, "air")
    log(f"Air skin has {len(air_faces)} faces.")

    chip_volume_m3 = geompy.BasicProperties(named["chip"])[2] * 1.0e-9
    write_sif(chip_volume_m3)

    chosen = None
    mesh = None
    for max_mm, min_mm in CANDIDATES:
        mesh = smesh.Mesh(partition, f"r2512_{max_mm}_{min_mm}")
        algo = mesh.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
        algo.SetFineness(5)
        algo.SetMaxSize(max_mm)
        algo.SetMinSize(min_mm)
        algo.SetSecondOrder(False)
        groups = {}
        for name, solid in named.items():
            groups[name] = mesh.GroupOnGeom(solid, name, SMESH.VOLUME)
        air_group = mesh.GroupOnGeom(air, "air", SMESH.FACE)
        log(
            f"Meshing with Netgen 1D-2D-3D. Maximum element {max_mm} mm, "
            f"minimum element {min_mm} mm, linear tetrahedra."
        )
        computed = mesh.Compute()
        volumes = mesh.NbVolumes()
        log(
            f"  Compute returned {computed}. Nodes {mesh.NbNodes()}, "
            f"faces {mesh.NbFaces()}, tetrahedra {volumes}."
        )
        if not computed or volumes == 0:
            for err in mesh.GetLog():
                log("  " + str(err))
            continue
        for name, group in groups.items():
            log(f"  Volume group {name}: {group.Size()} tetrahedra.")
        log(f"  Face group air: {air_group.Size()} triangles.")
        if air_group.Size() == 0 or any(group.Size() == 0 for group in groups.values()):
            log("  A group is empty. Trying a finer size.")
            continue
        chosen = (max_mm, min_mm)
        break

    if chosen is None:
        raise SystemExit("no volume mesh; see " + LOG)

    mesh.ExportUNV(UNV)
    if not os.path.isfile(UNV) or os.path.getsize(UNV) < 1000:
        raise SystemExit("ExportUNV failed")
    log(
        f"Wrote {os.path.basename(UNV)} ({os.path.getsize(UNV)} bytes), "
        f"element sizes {chosen[0]} mm maximum and {chosen[1]} mm minimum."
    )
    log("Node coordinates are millimetres. ElmerGrid must scale them by 0.001.")
    log("Next: ElmerGrid 8 2 r2512.unv -scale 1.0e-3 1.0e-3 1.0e-3 -autoclean -out mesh")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
