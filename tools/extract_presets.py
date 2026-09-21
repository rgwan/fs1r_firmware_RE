#!/usr/bin/env python3
"""Pull the preset voices, from PLG150-DX Image

    python tools/extract_presets.py   -> presets/native/NNN_Name.syx       (256 native 608-byte voices)
                                         presets/dx7/NNN_Name.syx          (1152 DX7-format 155-byte voices, as VCED)
                                         presets/performances/NNN_Name.syx (384 400-byte performances)
                                         presets/fseq/NN_Name.syx          (90 preset formant sequences)
                                         presets/index.csv

ROM layout :
  0x5461A - PLG150-DX

"""
import csv
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "dmps" / "plg150-dx" / "PLG150-DX.BIN"
OUT = ROOT / "presets"
BASE = 0x0
DX7_AT, DX7_N = 0x5461B - BASE, 1012
NAT_AT, NAT_N = 0x25C280 - BASE, 256
PERF_AT, PERF_N = 0x20A000 - BASE, 384
FSEQ_LONG_AT, FSEQ_LONG_N = 0x300A00 - BASE, 10       # 512 frames each
FSEQ_SHORT_AT, FSEQ_SHORT_N = 0x283000 - BASE, 80     # 128 frames each
# The three performance banks, in the order the table holds them.
PERF_BANKS = [(0, "PrA"), (128, "PrB"), (256, "PrC")]


def yamaha_bulk(addr_h, addr_m, addr_l, data):
    """FS1R native bulk dump: F0 43 0n 5E bc bc ah am al data cs F7 (device 1)."""
    bc = len(data)
    body = [bc >> 7 & 0x7F, bc & 0x7F, addr_h, addr_m, addr_l] + list(data)
    cs = (-sum(body)) & 0x7F
    return bytes([0xF0, 0x43, 0x00, 0x5E] + body + [cs, 0xF7])


def dx7_vced(vced155):
    body = list(vced155)
    cs = (-sum(body)) & 0x7F
    return bytes([0xF0, 0x43, 0x00, 0x00, 0x01, 0x1B] + body + [cs, 0xF7])


def safe(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip()) or "voice"


def main():
    rom = ROM.read_bytes()
    rows = []
    (OUT / "dx7").mkdir(parents=True, exist_ok=True)

    for i in range(DX7_N):
        r = rom[DX7_AT + i * 206: DX7_AT + (i + 1) * 206]
        name = r[196:206].decode("latin1")
        vced = r[51:206]          # DX7 VCED order: 6 ops, common, then name
        p = OUT / "dx7" / f"{i:03d}_{safe(name)}.syx"
        p.write_bytes(dx7_vced(vced))
        rows.append(("dx7", i, name, "", vced[134] + 1, str(p.relative_to(ROOT))))

    with open(OUT / "index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bank", "index", "name", "category", "algorithm", "file"])
        w.writerows(rows)
    print(f"wrote  {DX7_N} dx7 voices to {OUT}")


if __name__ == "__main__":
    main()
