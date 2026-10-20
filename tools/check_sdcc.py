#!/usr/bin/env python3
"""Compile all 13 firmware programs with SDCC, without touching the originals.

Why this exists:
    The source in firmware/ is deliberately written in Keil C51 style (sbit,
    interrupt n, REGX52.H), because that is what the project is specified
    against. SDCC uses slightly different syntax, so the sources will not
    compile under it unchanged.

    This script copies everything to a scratch directory, applies the small set
    of translations needed, compiles each program, and reports the code size.
    The files in firmware/ are never modified.

    It is a syntax and logic check, not a substitute for the real build. SDCC
    and Keil generate different code, and the pin aliases are approximated here
    as ordinary variables, so the behaviour on real hardware must still be
    verified with the Keil build.

Usage:
    python3 tools/check_sdcc.py            # compile all 13
    python3 tools/check_sdcc.py --keep     # leave the scratch dir for inspection
    python3 tools/check_sdcc.py 05 12      # only these programs

Requires:
    sdcc on PATH.  apt install sdcc / brew install sdcc / sdcc.sourceforge.net
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "firmware", "src")
INC = os.path.join(ROOT, "firmware", "inc")

FLASH_LIMIT = 8192      # AT89S52 on-chip flash, bytes
EVAL_LIMIT = 2048       # Keil C51 evaluation code size cap, bytes


def translate_header(text):
    """Rewrite board.h for SDCC."""
    text = text.replace("REGX52.H", "8052.h")
    text = text.replace("REG51.H", "8051.h")
    text = text.replace("STRING.H", "string.h")
    text = text.replace("INTRINS.H", "8052.h")
    text = text.replace("unsigned char code ", "unsigned char __code ")
    # sbit NAME = P2^0;  ->  a plain byte variable. The pin binding is lost,
    # which is fine: we are checking that the code compiles and the logic
    # holds together, not that the pins toggle.
    text = re.sub(r"^sbit\s+(\w+)\s*=.*?;\s*$",
                  r"static volatile unsigned char \1 = 0;",
                  text, flags=re.M)
    return text


def translate_source(text):
    """Rewrite a .c file for SDCC."""
    text = re.sub(r"interrupt\s+(\d+)", r"__interrupt(\1)", text)
    text = re.sub(r"using\s+(\d+)", r"__using(\1)", text)
    text = re.sub(r"^sbit\s+(\w+)\s*=.*?;\s*$",
                  r"static volatile unsigned char \1 = 0;",
                  text, flags=re.M)
    text = text.replace("unsigned char code ", "unsigned char __code ")
    return text


def ihx_bytes(path):
    """Count the payload bytes in an Intel HEX file."""
    total = 0
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if len(line) < 11 or not line.startswith(":"):
                continue
            try:
                total += int(line[1:3], 16)
            except ValueError:
                pass
    return total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keep = "--keep" in sys.argv

    if shutil.which("sdcc") is None:
        print("sdcc not found on PATH.")
        print("  Linux:   sudo apt install sdcc")
        print("  macOS:   brew install sdcc")
        print("  Windows: https://sdcc.sourceforge.net/")
        return 2

    programs = sorted(f for f in os.listdir(SRC) if f.endswith(".c"))
    if args:
        wanted = set()
        for a in args:
            for p in programs:
                if p.startswith(a):
                    wanted.add(p)
        programs = sorted(wanted)
        if not programs:
            print("no program matched: %s" % " ".join(args))
            return 2

    scratch = tempfile.mkdtemp(prefix="8051_sdcc_")
    shutil.copy(os.path.join(INC, "board.h"), scratch)
    for p in programs:
        shutil.copy(os.path.join(SRC, p), scratch)

    with open(os.path.join(scratch, "board.h")) as fh:
        body = translate_header(fh.read())
    with open(os.path.join(scratch, "board.h"), "w") as fh:
        fh.write(body)

    for p in programs:
        fp = os.path.join(scratch, p)
        with open(fp) as fh:
            body = translate_source(fh.read())
        with open(fp, "w") as fh:
            fh.write(body)

    print("scratch: %s" % scratch)
    print()
    print("%-26s %8s %8s  %-9s %s" %
          ("PROGRAM", "CODE B", "FLASH %", "KEIL EVAL", "RESULT"))
    print("-" * 74)

    failed = 0
    total = 0
    for p in programs:
        out = os.path.join(scratch, p[:-2] + ".ihx")
        cmd = ["sdcc", "-mmcs51", "-I" + scratch, "--out-fmt-ihx", "-o", out, p]
        r = subprocess.run(cmd, cwd=scratch, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            failed += 1
            print("%-26s %8s %8s  %-9s %s" % (p, "-", "-", "-", "FAIL"))
            tail = (r.stderr or r.stdout).strip().splitlines()
            for line in tail[-6:]:
                print("      %s" % line)
            continue

        size = ihx_bytes(out)
        total += size
        pct = 100.0 * size / FLASH_LIMIT
        verdict = "OK" if size <= FLASH_LIMIT else "TOO BIG"
        if size > EVAL_LIMIT:
            ev = "needs lic"
        else:
            ev = "fits"
        print("%-26s %8d %7.1f%%  %-9s %s" % (p, size, pct, ev, verdict))

    print("-" * 74)
    print("%d program(s), %d failed, %d bytes total" %
          (len(programs), failed, total))
    print()
    print("Keil eval limit is %d bytes. Programs marked 'needs lic' will not"
          % EVAL_LIMIT)
    print("build in the free Keil C51; they need a licensed machine.")
    print()
    print("Reminder: this is a syntax and logic check only. The real build is")
    print("Keil, and only the real build proves the hardware behaviour.")

    if keep:
        print("\nkept: %s" % scratch)
    else:
        shutil.rmtree(scratch, ignore_errors=True)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
