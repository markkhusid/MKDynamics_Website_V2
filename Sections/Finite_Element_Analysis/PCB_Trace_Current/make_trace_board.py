#!/usr/bin/env python3
r"""Build the layout that the rest of the pipeline analyses.

This script is the stand-in for drawing a board by hand. A later project
can start from a KiCad schematic, assign footprints, and route the copper.
The export below does not care how the board was drawn. It only needs a
.kicad_pcb and a net name.

What this file produces is the layout only. It does not solve current or
temperature. The copper solid that Salome meshes comes from the next
command, run in the KiCad 9 container from this directory:

    kicad-cli pcb export xao --output trace.xao \
        --no-board-body --no-components \
        --include-tracks --include-pads --include-zones \
        --fuse-shapes --net-filter TRACE trace.kicad_pcb

--no-board-body leaves the FR4 out. --fuse-shapes joins the pads, tracks,
and via into one solid. --net-filter TRACE drops every other net. A thermal
model needs the dielectric as its own solid, so that export would keep the
board body. This current-only model does not.

Geometry, millimetres, board origin at the lower left:
  outline 12 x 8 on Edge.Cuts (not in the XAO)
  pad A   F.Cu  2 x 2 at (3, 4)     net TRACE
  track   F.Cu  0.4 wide, (3, 4) to (6, 4)
  via     through, drill 0.3, pad 0.6, at (6, 4)
  track   B.Cu  0.4 wide, (6, 4) to (9, 4)
  pad B   B.Cu  2 x 2 at (9, 4)     net TRACE

Copper thickness is written into the stackup as 0.035 mm (1 oz).
Running the script again replaces trace.kicad_pcb and gives the objects
new ids.
"""
import pathlib
import pcbnew


def say(line):
    # One line of the run log. Flushed so a piped capture keeps the order.
    print(line, flush=True)


# Board file written beside this script. pcbnew is the KiCad 9 Python module,
# so this runs inside the KiCad environment, not the system interpreter.
OUT = pathlib.Path(__file__).resolve().parent / "trace.kicad_pcb"
say(f"KiCad pcbnew {pcbnew.Version()}")
say(f"Writing the layout to {OUT}")
say("This step draws copper only. It does not export the XAO or solve a field.")


def mm(v):
    # KiCad stores coordinates as integer nanometres. FromMM does that conversion.
    return pcbnew.FromMM(v)


def xy(x, y):
    # One board point. x grows right and y grows down, origin at the lower left
    # of the outline drawn below.
    return pcbnew.VECTOR2I(mm(x), mm(y))


# Create an empty two-layer board at the output path.
board = pcbnew.NewBoard(str(OUT))
settings = board.GetDesignSettings()
# F.Cu and B.Cu. A later thermal model still wants this layer count, plus the
# dielectric between them.
settings.SetCopperLayerCount(2)
# Finished board thickness, copper plus core. The core thickness is written
# into the stackup text after the save.
settings.SetBoardThickness(mm(1.6))
say("Board has 2 copper layers and a finished thickness of 1.6 mm.")

# One net. The XAO export keeps copper whose net name matches TRACE.
net = pcbnew.NETINFO_ITEM(board, "TRACE")
board.Add(net)
say("Added net TRACE. The XAO export keeps copper on this net and drops the rest.")


def edge(x1, y1, x2, y2):
    # One straight segment of the board outline. Edge.Cuts is the KiCad layer
    # for that outline. The current XAO export skips it because the board body
    # is turned off. Draw it anyway so the file is a real board, and so a later
    # export can turn the outline into an FR4 solid.
    shape = pcbnew.PCB_SHAPE(board)
    shape.SetShape(pcbnew.SHAPE_T_SEGMENT)
    shape.SetLayer(pcbnew.Edge_Cuts)
    shape.SetStart(xy(x1, y1))
    shape.SetEnd(xy(x2, y2))
    # Line width of the outline graphic, not a copper width.
    shape.SetWidth(mm(0.05))
    board.Add(shape)


# Close the 12 mm by 8 mm rectangle. The last segment returns to the first point.
edge(0, 0, 12, 0)
edge(12, 0, 12, 8)
edge(12, 8, 0, 8)
edge(0, 8, 0, 0)
say("Outline is a 12 mm by 8 mm rectangle on Edge.Cuts. The current XAO export leaves this outline out.")

# KiCad stores pads inside a footprint. J1 is that holder. Both pads share it,
# so the XAO face names contain J1: Pad_F_J1_A_TRACE and Pad_B_J1_B_TRACE.
fp = pcbnew.FOOTPRINT(board)
fp.SetReference("J1")
fp.SetValue("trace-pads")
fp.SetPosition(xy(0, 0))
board.Add(fp)
say("Footprint J1 holds both pads. KiCad will name the XAO faces from J1, the pad, and the net.")


def smd_pad(number, layer, x, y):
    # A surface pad on one copper layer. number becomes the pad name in the
    # XAO group. The pad is the face Elmer will drive or sink.
    pad = pcbnew.PAD(fp)
    pad.SetNumber(number)
    pad.SetName(number)
    # SMD keeps the pad on the single layer selected below. A through-hole pad
    # would also drill the board, which this terminal does not do.
    pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
    pad.SetShape(pcbnew.PAD_SHAPE_RECT)
    # 2 mm by 2 mm. Salome reports the face area as 4 mm^2.
    pad.SetSize(pcbnew.VECTOR2I(mm(2.0), mm(2.0)))
    # The layer set says which copper sheet the pad occupies. SetLayer is the
    # pad's primary layer and must name the same sheet.
    layers = pcbnew.LSET()
    layers.AddLayer(layer)
    pad.SetLayerSet(layers)
    pad.SetLayer(layer)
    # (x, y) is the pad center, not a corner.
    pad.SetPosition(xy(x, y))
    pad.SetNet(net)
    fp.Add(pad)
    return pad


# Front terminal at the left, back terminal at the right.
smd_pad("A", pcbnew.F_Cu, 3.0, 4.0)
say("Pad A is 2 mm by 2 mm on F.Cu, centered at (3 mm, 4 mm), on net TRACE.")
smd_pad("B", pcbnew.B_Cu, 9.0, 4.0)
say("Pad B is 2 mm by 2 mm on B.Cu, centered at (9 mm, 4 mm), on net TRACE.")


def track(layer, x1, y1, x2, y2, width):
    # A straight copper trace. The centerline runs from (x1, y1) to (x2, y2),
    # and width is the copper width across that line. These 0.4 mm traces are
    # the narrow part of the path, so the current density and the heating peak
    # there.
    item = pcbnew.PCB_TRACK(board)
    item.SetStart(xy(x1, y1))
    item.SetEnd(xy(x2, y2))
    item.SetWidth(mm(width))
    item.SetLayer(layer)
    item.SetNet(net)
    board.Add(item)


# Front trace from pad A to the via, then back trace from the via to pad B.
track(pcbnew.F_Cu, 3.0, 4.0, 6.0, 4.0, 0.4)
say("Front trace is 0.4 mm wide on F.Cu, from (3 mm, 4 mm) to the via at (6 mm, 4 mm).")
track(pcbnew.B_Cu, 6.0, 4.0, 9.0, 4.0, 0.4)
say("Back trace is 0.4 mm wide on B.Cu, from the via at (6 mm, 4 mm) to (9 mm, 4 mm).")

# The via is the copper barrel that joins the front trace to the back trace.
# Drill is the hole. Width is the annular pad diameter. A through via spans
# F.Cu to B.Cu, so the fused XAO solid is one conductor.
via = pcbnew.PCB_VIA(board)
via.SetPosition(xy(6.0, 4.0))
via.SetDrill(mm(0.3))
via.SetWidth(mm(0.6))
via.SetViaType(pcbnew.VIATYPE_THROUGH)
via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
via.SetNet(net)
board.Add(via)
say("Through via at (6 mm, 4 mm): drill 0.3 mm, pad 0.6 mm, from F.Cu to B.Cu, on net TRACE.")

# Write the board KiCad can open. The stackup thicknesses are not part of that
# save in this pcbnew binding, so they are inserted into the file text next.
pcbnew.SaveBoard(str(OUT), board)
text = OUT.read_text()
# 0.035 mm is 1 oz copper on each outer layer. 1.53 mm of FR4 fills the rest
# of the 1.6 mm board. The dielectric line records the board for a later
# thermal model. This XAO export does not turn that line into a solid.
stackup = """\t\t(stackup
\t\t\t(layer "F.Cu" (type "copper") (thickness 0.035))
\t\t\t(layer "dielectric 1" (type "core") (thickness 1.53) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
\t\t\t(layer "B.Cu" (type "copper") (thickness 0.035))
\t\t\t(copper_finish "None")
\t\t\t(dielectric_constraints no)
\t\t)
"""
# Insert the stackup once, directly under the setup block KiCad already wrote.
needle = "\t(setup\n"
if needle not in text:
    raise SystemExit("setup section not found")
text = text.replace(needle, needle + stackup, 1)
OUT.write_text(text)
say("Stackup written under setup: F.Cu 0.035 mm copper, 1.53 mm FR4 core, B.Cu 0.035 mm copper.")
say(f"Wrote {OUT.name}: {OUT.stat().st_size} bytes.")
say("Next command is the XAO export. It fuses the TRACE copper and leaves the FR4 behind.")
say("  kicad-cli pcb export xao --output trace.xao --no-board-body --no-components \\")
say("      --include-tracks --include-pads --include-zones --fuse-shapes \\")
say("      --net-filter TRACE trace.kicad_pcb")
