"""
SumoX-26 -- Main chassis deck, redesigned for printability + real fitment.
Everything here is a flat plate + vertical walls/posts -> prints flat on the
bed with ZERO overhangs beyond 90 deg, so zero support material, period.

Coordinate system: X = width (left/right), Y = depth (0 = front, meets the
wedge), Z = height above the playing surface (ring).

VERIFY BEFORE PRINTING: motor length, motor face-hole spacing, battery
holder size, and BTS7960 hole spacing are estimates from public spec pages,
not measurements of your actual parts. Adjust the flagged constants below.
"""
import cadquery as cq

# ============================= PARAMETERS (mm) =============================
CORE_W        = 130.0
CORE_Y0       = 6.0
CORE_Y1       = 152.0
DECK_T        = 4.0
DECK_Z0       = 2.0

FLANGE_W      = 186.0
FLANGE_T      = 6.0
FLANGE_Z1     = 30.0
HOLE_D        = 3.4
N_HOLES       = 6
HOLE_INSET    = 14.0
HOLE_Z        = 16.0

MOTOR_D          = 37.0     # confirmed (JSumo/generic Titan-family 37mm-body spec sheets)
MOTOR_LENGTH     = 85.0     # ESTIMATE: no page gives the 60:1/200RPM length directly. Cross-referenced
                             # the same 37mm-diameter motor family (5-500 RPM variants): lengths run
                             # 77-79mm across that whole range, so 85mm is a deliberately safe
                             # (slightly long) placeholder -- measure yours, shorten if you can
PILOT_BORE_D     = 16.0     # clearance for the motor's shaft + center pilot spigot only --
                             # this is a FACE-MOUNT bulkhead (motor bolts to the outside via
                             # its own 6x M3 face holes), it does NOT need to pass through
WHEEL_D          = 52.0     # confirmed: JS5230
WHEEL_X          = 78.0
BULK_X           = 60.0
BULK_T           = 6.0
BULK_Z_TOP       = 48.0
AXLE_Z           = WHEEL_D / 2.0
LEFT_Y0, LEFT_Y1   = 9.0, 41.0
RIGHT_Y0, RIGHT_Y1 = 45.0, 77.0
FACE_HOLE_OFFSETS = [(-13, -13), (13, -13), (-13, 13), (13, 13)]
FACE_HOLE_D = 3.4

# 3x18650 series holder -- confirmed via multiple listings (Tayda A-5393/A-3264, DFRobot FIT0539,
# generic "3-cell side-by-side" holders): consistently ~75-81 x 59-62 x 20-22mm. Using 78x60x21.
# Mounted with the holder's LENGTH (78mm) along X (plenty of room) and WIDTH (60mm) along Y.
BATT_HOLDER_L, BATT_HOLDER_W = 78.0, 60.0
BATT_CLR = 4.0                              # clearance added around the holder
BATT_W = BATT_HOLDER_L + BATT_CLR           # inner cavity X
BATT_Y0, BATT_Y1 = 84.0, 84.0 + BATT_HOLDER_W + BATT_CLR   # inner cavity Y
BATT_WALL_T = 3.0
BATT_WALL_Z1 = 26.0

# electronics shelf: NOT printed as an overhang -- just 4 mounting holes on top of the
# battery-box walls. Bolt a separately-printed (flat, no-support) or laser-cut acrylic
# plate here on M3 standoffs to carry the Arduino UNO Q + screw shield above the battery.
UNO_W, UNO_L = 68.6, 53.4     # confirmed: UNO Q uses the standard Uno footprint
SHELF_HOLE_D = 3.2

# BTS7960 driver module -- confirmed 50x50mm board (consistent across Besomi/generic listings,
# Besomi being a UAE supplier). Hole spacing itself isn't published; 44x44mm assumes a typical
# ~3mm inset from each edge -- verify against your actual board before drilling final holes.
DRV_W, DRV_L = 44.0, 44.0
DRV_POST_D   = 6.0
DRV_HOLE_D   = 3.0
DRV1_CENTER  = (42.0, 25.0)
DRV2_CENTER  = (-42.0, 61.0)
DRV_POST_Z0  = DECK_Z0 + DECK_T
DRV_POST_Z1  = DRV_POST_Z0 + 6.0

EDGE_POST_D  = 6.0
EDGE_HOLE_D  = 2.5
EDGE_POST_Z0 = DECK_Z0 + DECK_T
EDGE_POST_Z1 = EDGE_POST_Z0 + 5.0
EDGE_INSET_X = 12.0
EDGE_INSET_Y = 10.0

CORNER_FILLET = 6.0
# ============================================================================


def box(cx, cy, z0, z1, w, l):
    return (
        cq.Workplane("XY")
        .box(w, l, z1 - z0, centered=(True, True, False))
        .translate((cx, cy, z0))
    )


def cyl_z(cx, cy, z0, z1, d):
    """Cylinder with axis along Z."""
    return cq.Workplane("XY").circle(d / 2.0).extrude(z1 - z0).translate((cx, cy, z0))


def cyl_y(cx, y0, y1, cz, d):
    """Cylinder with axis along Y (for holes through Y-thin walls)."""
    return (
        cq.Workplane("XZ")
        .circle(d / 2.0)
        .extrude(y1 - y0)
        .translate((cx, y0, cz))
    )


def cyl_x(x0, x1, cy, cz, d):
    """Cylinder with axis along X (for holes through bulkheads)."""
    return (
        cq.Workplane("YZ")
        .circle(d / 2.0)
        .extrude(x1 - x0)
        .translate((x0, cy, cz))
    )


# ---------------------------------------------------------------- core plate
deck = box(0, (CORE_Y0 + CORE_Y1) / 2, DECK_Z0, DECK_Z0 + DECK_T, CORE_W, CORE_Y1 - CORE_Y0)
deck = deck.edges("|Z").fillet(CORNER_FILLET)
print("core plate ok")

# ---------------------------------------------------------------- front flange
flange = box(0, FLANGE_T / 2, DECK_Z0, FLANGE_Z1, FLANGE_W, FLANGE_T)
deck = deck.union(flange)
print("flange union ok")

half_span = FLANGE_W / 2 - HOLE_INSET
xs = [-half_span + i * (2 * half_span) / (N_HOLES - 1) for i in range(N_HOLES)]
for x in xs:
    cutter = cyl_y(x, -1, FLANGE_T + 1, HOLE_Z, HOLE_D)
    deck = deck.cut(cutter)
print("flange holes ok")

cq.exporters.export(deck, "/home/claude/cad/deck_stage1.stl")
print("stage1 exported")

# ---------------------------------------------------------------- motor bulkheads
def add_bulkhead(deck, side, y0, y1):
    x = side * BULK_X
    ycen = (y0 + y1) / 2.0
    wall = box(x, ycen, DECK_Z0, BULK_Z_TOP, BULK_T, y1 - y0)
    deck = deck.union(wall)
    bore = cyl_x(x - BULK_T - 1, x + BULK_T + 1, ycen, AXLE_Z, PILOT_BORE_D)
    deck = deck.cut(bore)
    for dy, dz in FACE_HOLE_OFFSETS:
        h = cyl_x(x - BULK_T, x + BULK_T, ycen + dy, AXLE_Z + dz, FACE_HOLE_D)
        deck = deck.cut(h)
    return deck

deck = add_bulkhead(deck, -1, LEFT_Y0, LEFT_Y1)
print("left bulkhead ok")
deck = add_bulkhead(deck, +1, RIGHT_Y0, RIGHT_Y1)
print("right bulkhead ok")

cq.exporters.export(deck, "/home/claude/cad/deck_stage2.stl")
print("stage2 exported")

# ---------------------------------------------------------------- battery bay (open-top box)
batt_ycen = (BATT_Y0 + BATT_Y1) / 2.0
batt_l = BATT_Y1 - BATT_Y0
outer = box(0, batt_ycen, DECK_Z0 + DECK_T, BATT_WALL_Z1, BATT_W + 2 * BATT_WALL_T, batt_l + 2 * BATT_WALL_T)
inner = box(0, batt_ycen, DECK_Z0 + DECK_T - 0.1, BATT_WALL_Z1 + 0.1, BATT_W, batt_l)
batt_box = outer.cut(inner)
deck = deck.union(batt_box)
print("battery bay ok")

cq.exporters.export(deck, "/home/claude/cad/deck_stage3.stl")
print("stage3 exported")

# ---------------------------------------------------------------- electronics shelf mounting holes
# Drilled into the TOP of the battery-box walls (flat, already-printed surface --
# no new overhang). Bolt a separate flat shelf plate here on M3 standoffs to carry
# the Arduino UNO Q + screw shield above the battery. See write-up for why this is
# a separate part rather than a printed bridge.
def post(cx, cy, z0, z1, d, hole_d):
    p = cyl_z(cx, cy, z0, z1, d)
    h = cyl_z(cx, cy, z0 - 1, z1 + 1, hole_d)
    return p.cut(h)

# place holes ON the 3mm-thick battery-box wall corners (solid material), not the open cavity
wall_x = BATT_W / 2 + BATT_WALL_T / 2      # mid-thickness of the side walls
wall_y = batt_l / 2 + BATT_WALL_T / 2      # mid-thickness of the front/back walls
shelf_hole_xy = [(-wall_x, batt_ycen - wall_y), (wall_x, batt_ycen - wall_y),
                  (-wall_x, batt_ycen + wall_y), (wall_x, batt_ycen + wall_y)]
for (px, py) in shelf_hole_xy:
    hole = cyl_z(px, py, BATT_WALL_Z1 - 4, BATT_WALL_Z1 + 1, SHELF_HOLE_D)
    deck = deck.cut(hole)
print("shelf mounting holes ok")

cq.exporters.export(deck, "/home/claude/cad/deck_stage4.stl")
print("stage4 exported")

# ---------------------------------------------------------------- driver standoffs
def add_driver_standoffs(deck, center):
    cx, cy = center
    hx, hy = DRV_W / 2, DRV_L / 2
    pts = [(cx - hx, cy - hy), (cx + hx, cy - hy), (cx - hx, cy + hy), (cx + hx, cy + hy)]
    for (px, py) in pts:
        deck = deck.union(post(px, py, DRV_POST_Z0, DRV_POST_Z1, DRV_POST_D, DRV_HOLE_D))
    return deck

deck = add_driver_standoffs(deck, DRV1_CENTER)
deck = add_driver_standoffs(deck, DRV2_CENTER)
print("driver standoffs ok")

cq.exporters.export(deck, "/home/claude/cad/deck_stage5.stl")
print("stage5 exported")

# ---------------------------------------------------------------- edge sensor corner posts
corner_pts = [
    (-CORE_W / 2 + EDGE_INSET_X, CORE_Y0 + EDGE_INSET_Y),
    (CORE_W / 2 - EDGE_INSET_X, CORE_Y0 + EDGE_INSET_Y),
    (-CORE_W / 2 + EDGE_INSET_X, CORE_Y1 - EDGE_INSET_Y),
    (CORE_W / 2 - EDGE_INSET_X, CORE_Y1 - EDGE_INSET_Y),
]
for (px, py) in corner_pts:
    deck = deck.union(post(px, py, EDGE_POST_Z0, EDGE_POST_Z1, EDGE_POST_D, EDGE_HOLE_D))
print("edge sensor posts ok")

cq.exporters.export(deck, "/home/claude/cad/deck_final.stl")
print("FINAL deck exported")
