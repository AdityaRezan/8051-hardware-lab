import csv, collections, io

CATS = [
    ("Semiconductors and ICs", ["U1", "U2", "U3", "U4", "U5", "U6", "U7"]),
    ("Discretes (transistors, diodes, LEDs)", ["Q1", "Q2", "Q3", "Q4", "D1", "D2", "D3-D10", "D11"]),
    ("Displays, modules and output devices", ["LCD1", "DSP1", "RLY1", "BZ1"]),
    ("Switches and input devices", ["SW1", "PB1", "PB2", "PB3"]),
    ("Resistors and networks", ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
                                "RN1", "RN2", "RN3", "RN4"]),
    ("Capacitors", ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]),
    ("Crystal and timing", ["Y1"]),
    ("Sockets, connectors and jumpers", ["S1", "S2", "S3", "J1", "J2", "J3", "J4", "J5", "JP1"]),
    ("Power, PCB and tooling", ["HS1", "PCB1", "WR1", "PWR1", "PRG1", "PRG2"]),
]

LOOKUP = {}
for _name, _refs in CATS:
    for _r in _refs:
        LOOKUP[_r] = _name

def cat_of(ref):
    if ref in LOOKUP:
        return LOOKUP[ref]
    stem = ref.rstrip("0123456789")
    for _name, _refs in CATS:
        if any(_r.startswith(stem) for _r in _refs):
            return _name
    return "Other"

rows = []
with open("hardware/BOM.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        r["qty"] = int(r["Qty"])
        r["unit"] = float(r["Unit INR"])
        r["total"] = r["qty"] * r["unit"]
        r["cat"] = cat_of(r["Ref"])
        rows.append(r)

groups = collections.OrderedDict()
for r in rows:
    groups.setdefault(r["cat"], []).append(r)

out = io.StringIO()
out.write("# Bill of Materials - 8051 Hardware Lab Board\n\n")
out.write("Prices are indicative retail rates in India for the 2025-26 academic year and vary by vendor and quantity.\n")
out.write("A single unit is populated per board; the two programmer entries (PRG1, PRG2) are shared lab tools, not per-board parts.\n\n")

grand = 0.0
board_only = 0.0
for name, items in groups.items():
    sub = sum(i["total"] for i in items)
    grand += sub
    if name != "Power, PCB and tooling":
        board_only += sub
    out.write("## {0}\n\n".format(name))
    out.write("| Ref | Item | Value / part | Package | Qty | Unit (INR) | Line (INR) |\n")
    out.write("|---|---|---|---|---:|---:|---:|\n")
    for i in items:
        out.write("| {0} | {1} | {2} | {3} | {4} | {5:.0f} | {6:.0f} |\n".format(
            i["Ref"], i["Item"], i["Value or Part Number"], i["Package"],
            i["qty"], i["unit"], i["total"]))
    out.write("\n**Subtotal: INR {0:,.0f}**\n\n".format(sub))

out.write("## Cost summary\n\n")
out.write("| Item | Amount (INR) |\n|---|---:|\n")
out.write("| Components on one board | {0:,.0f} |\n".format(board_only))
out.write("| Power supply, PCB, wire and programmers | {0:,.0f} |\n".format(grand - board_only))
out.write("| **Total for one complete working setup** | **{0:,.0f}** |\n\n".format(grand))
out.write("The recurring cost of a second board is about INR {0:,.0f} because the adapter and programmers are reused.\n\n".format(board_only))
out.write("## Notes on sourcing\n\n")
out.write("- AT89S52 is chosen over AT89C51 because it is programmed through SPI with a USBasp, which costs about INR 250, instead of a parallel programmer that costs several thousand rupees.\n")
out.write("- 74HC573 is a transparent latch; the 74HC373 or 74LS573 also work but HC is preferred for CMOS 5 V logic and low loading on the P0 bus.\n")
out.write("- Substitute MAX232A and use 0.1 uF charge pump capacitors, or use MAX3232 with 0.1 uF capacitors for 3.3 V tolerant operation.\n")
out.write("- Any 16x2 HD44780 compatible display works; JHD162A, WH1602 and generic blue or green backlight modules are interchangeable.\n")
out.write("- Any common cathode 2 digit 0.56 inch display works. A common anode display does not work with this driver and must not be substituted without changing the segment table and digit driver polarity.\n")

open("hardware/BOM.md", "w", encoding="utf-8").write(out.getvalue())
print(out.getvalue()[:1200])
print("...\ngrand total:", round(grand))
