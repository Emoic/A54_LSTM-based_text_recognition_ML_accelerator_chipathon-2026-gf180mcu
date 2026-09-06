#!/usr/bin/env python3
"""Add nested Metal5 VDD/VSS rings and robust pad-to-ring via stacks.

The organizer provides six Metal2 access rectangles for each supply. Each
rectangle is extended only inside the 20 um boundary margin and connected to
its Metal5 ring through a 3x3 array at every level (Via2, Via3, and Via4).
The horizontal Metal5 ring rails connect to every existing vertical Metal4
PDN stripe through separate 3x3 Via4 arrays. Signal routing is not modified.
"""

import sys

import odb
from openroad import Design, Tech


if len(sys.argv) != 4:
    raise SystemExit("usage: connect_power_ring.py INPUT.odb OUTPUT.odb OUTPUT.def")

input_odb, output_odb, output_def = sys.argv[1:]

tech = Tech()
design = Design(tech)
design.readDb(input_odb)
db = tech.getDB()
block = db.getChip().getBlock()

layers = {
    name: db.getTech().findLayer(name)
    for name in ("Metal2", "Metal3", "Metal4", "Metal5")
}
vias = {
    name: db.getTech().findVia(name)
    for name in ("Via2_HH", "Via3_HH", "Via4_HH")
}
if any(value is None for value in (*layers.values(), *vias.values())):
    raise RuntimeError("Required Metal2-Metal5 layers or single-cut vias are missing")

# OpenDB units: 2000 DBU/um. Rings are 5 um wide and lie entirely in the
# organizer's 20 um boundary margin. VSS is the outer ring and VDD the inner.
half_width = 5000
ring_tracks = {
    "VSS": {"left": 10000, "right": 2210000, "bottom": 10000, "top": 2210000},
    "VDD": {"left": 26000, "right": 2194000, "bottom": 26000, "top": 2194000},
}

# Three-by-three single-cut arrays. The 1.5 um pitch is larger than the PDK
# cut spacing while fitting inside a 5 um landing shape.
array_offsets = (-3000, 0, 3000)


def add_via_array(swire, via, x, y, shape_type):
    count = 0
    for dx in array_offsets:
        for dy in array_offsets:
            odb.dbSBox_create(swire, via, x + dx, y + dy, shape_type)
            count += 1
    return count


for net_name in ("VDD", "VSS"):
    net = block.findNet(net_name)
    bterm = block.findBTerm(net_name)
    if net is None or bterm is None:
        raise RuntimeError(f"Missing required power net or BTerm: {net_name}")

    swires = net.getSWires()
    if not swires:
        raise RuntimeError(f"No generated PDN special wire found for {net_name}")
    swire = swires[0]

    pin_boxes = sorted(
        [box for bpin in bterm.getBPins() for box in bpin.getBoxes()],
        key=lambda box: (box.yMin(), box.xMin()),
    )
    if len(pin_boxes) != 6:
        raise RuntimeError(f"Expected six {net_name} access rectangles, found {len(pin_boxes)}")
    if any(box.getTechLayer().getName() != "Metal2" for box in pin_boxes):
        raise RuntimeError(f"Expected all {net_name} access rectangles on Metal2")

    # Remove only the earlier direct Metal2-to-Metal1 ECO, if present.
    pin_y_min = min(box.yMin() for box in pin_boxes)
    pin_y_max = max(box.yMax() for box in pin_boxes)
    removed = []
    for box in list(swire.getWires()):
        layer_name = box.getTechLayer().getName() if box.getTechLayer() else None
        via_name = box.getTechVia().getName() if box.isVia() and box.getTechVia() else None
        in_old_entry_window = (
            box.xMin() < 100000
            and box.xMax() < 100000
            and box.yMax() >= pin_y_min
            and box.yMin() <= pin_y_max
        )
        if in_old_entry_window and (
            layer_name == "Metal2" or via_name == "Via1_2CUT_H"
        ):
            removed.append(box)
    for box in removed:
        odb.dbSBox_destroy(box)

    tracks = ring_tracks[net_name]
    # Closed nested ring on otherwise unused Metal5.
    odb.dbSBox_create(
        swire, layers["Metal5"],
        tracks["left"] - half_width, tracks["bottom"] - half_width,
        tracks["left"] + half_width, tracks["top"] + half_width,
        "RING",
    )
    odb.dbSBox_create(
        swire, layers["Metal5"],
        tracks["right"] - half_width, tracks["bottom"] - half_width,
        tracks["right"] + half_width, tracks["top"] + half_width,
        "RING",
    )
    for rail_y in (tracks["bottom"], tracks["top"]):
        odb.dbSBox_create(
            swire, layers["Metal5"],
            tracks["left"] - half_width, rail_y - half_width,
            tracks["right"] + half_width, rail_y + half_width,
            "RING",
        )

    # All full-height vertical Metal4 stripes are part of the existing PDN.
    m4_stripes = sorted(
        [
            box for box in swire.getWires()
            if not box.isVia()
            and box.getTechLayer() is not None
            and box.getTechLayer().getName() == "Metal4"
            and box.yMin() == block.getDieArea().yMin()
            and box.yMax() == block.getDieArea().yMax()
        ],
        key=lambda box: box.xMin(),
    )
    if len(m4_stripes) < 2:
        raise RuntimeError(f"Expected multiple full-height Metal4 stripes on {net_name}")

    via4_ring_count = 0
    for stripe in m4_stripes:
        stripe_x = (stripe.xMin() + stripe.xMax()) // 2
        for rail_y in (tracks["bottom"], tracks["top"]):
            via4_ring_count += add_via_array(
                swire, vias["Via4_HH"], stripe_x, rail_y, "RING"
            )

    # Six independent entries, each with nine parallel cuts at every level.
    entry_counts = {"Via2": 0, "Via3": 0, "Via4": 0}
    for pin_box in pin_boxes:
        pin_y = (pin_box.yMin() + pin_box.yMax()) // 2
        entry_x = tracks["left"]
        odb.dbSBox_create(
            swire, layers["Metal2"],
            pin_box.xMin(), pin_y - half_width,
            entry_x + half_width, pin_y + half_width,
            "STRIPE",
        )
        for layer_name in ("Metal3", "Metal4"):
            odb.dbSBox_create(
                swire, layers[layer_name],
                entry_x - half_width, pin_y - half_width,
                entry_x + half_width, pin_y + half_width,
                "STRIPE",
            )
        entry_counts["Via2"] += add_via_array(
            swire, vias["Via2_HH"], entry_x, pin_y, "STRIPE"
        )
        entry_counts["Via3"] += add_via_array(
            swire, vias["Via3_HH"], entry_x, pin_y, "STRIPE"
        )
        entry_counts["Via4"] += add_via_array(
            swire, vias["Via4_HH"], entry_x, pin_y, "STRIPE"
        )

    print(
        f"{net_name}: removed {len(removed)} old entry shapes; "
        f"Metal5 ring=({tracks['left']},{tracks['bottom']}).."
        f"({tracks['right']},{tracks['top']}); "
        f"entry cuts Via2/Via3/Via4={entry_counts['Via2']}/"
        f"{entry_counts['Via3']}/{entry_counts['Via4']}; "
        f"ring Via4 cuts={via4_ring_count}"
    )

design.writeDb(output_odb)
design.writeDef(output_def)
