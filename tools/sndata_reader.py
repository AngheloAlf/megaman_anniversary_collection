#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2023 AngheloAlf
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import spimdisasm
from pathlib import Path
import struct


class SndataEntry:
    def __init__(self, bytedata: bytearray, vram: int, nameAddress: int, symbolAddress: int, unk_8: int):
        self.vram = vram

        self.symbolNameAddress = nameAddress
        self.symbolAddress = symbolAddress
        self.unk_8 = unk_8

        # self.symbolNameOffset = self.symbolNameAddress - self.vram

        decodedStrings, rawStringSize = spimdisasm.common.Utils.decodeString(bytedata, self.symbolNameOffset, "utf-8")
        assert len(decodedStrings) <= 1, len(decodedStrings)

        self.symName = decodedStrings[0] if len(decodedStrings) == 1 else ""

        # print(f"{self.symName}: 0x{symbolAddress:X} 0x{unk_8:X}")
        # print(f"  0x{self.symbolNameAddress-self.vram:X} 0x{unk_4-self.vram:X} 0x{unk_8-self.vram:X}")


    @property
    def symbolNameOffset(self) -> int:
        return self.symbolNameAddress - self.vram


class SndataSection:
    def __init__(self, bytedata: bytearray, vram: int):
        self.vram = vram

        structformat = ">BBBB"
        temp = list(struct.unpack_from(structformat, bytedata, 0))

        self.magic = temp[0:4]

        structformat = "<IIII"
        temp = list(struct.unpack_from(structformat, bytedata, 4))
        self.unk_04 = temp[0]
        self.unk_08 = temp[1]
        self.unk_0C = temp[2] # table address
        self.unk_10 = temp[3] # number of symbols

        # print(f"unk_04: 0x{self.unk_04:08X}")
        # print(f"unk_08: 0x{self.unk_08:08X}")
        # print(f"unk_0C: 0x{self.unk_0C:08X}")
        # print(f"unk_10: 0x{self.unk_10:08X}")

        self.entries: list[SndataEntry] = []

        tableOffset = self.unk_0C - self.vram

        for i in range(self.unk_10):
            structformat = "<III"
            temp = list(struct.unpack_from(structformat, bytedata, tableOffset + i*0xC))
            self.entries.append(SndataEntry(bytedata, vram, *temp))
        # tableStart = table + 0xC

        # print(f"{tableOffset + self.unk_10*0xC:X}")


def sndataReaderMain():
    description = ""
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("sndata", help="path to sndata.bin")
    parser.add_argument("vram", help="addr from the elf file")

    args = parser.parse_args()

    sndataPath = Path(args.sndata)
    vram = int(args.vram, 0)

    sndataBytes = spimdisasm.common.Utils.readFileAsBytearray(sndataPath)
    sndata = SndataSection(sndataBytes, vram)

    sortedEntries = sorted(sndata.entries, key=lambda x: x.symbolAddress)

    for entry in sortedEntries:
        if entry.symbolAddress == 0:
            continue
        print(f"{entry.symName} = 0x{entry.symbolAddress:08X};")


if __name__ == "__main__":
    sndataReaderMain()
