#!/usr/bin/env python3

import fontforge
import psMat

PROJECT_NAME = "ZUTOMOJI_HG"
PROJECT_VERSION = "0.1.0"


class Patcher:

    def __init__(self,
                 base_font_path: str,
                 ztmy_font_path: str,
                 font_name: str,
                 font_family_name: str,
                 base_start_code_point: int = 0x100000) -> None:
        self.__base_font = fontforge.open(base_font_path)
        self.__ztmy_font = fontforge.open(ztmy_font_path)
        self.__font_name = font_name
        self.__font_family_name = font_family_name
        self.__base_current_code_point = base_start_code_point

        assert self.__ztmy_font.is_cid, "{} is not CID font.".format(
            ztmy_font_path)
        subfont_count = self.__ztmy_font.cidsubfontcnt
        assert subfont_count == 1, "{} has {} subfonts. Expect only one.".format(
            ztmy_font_path, subfont_count)

        self.__em_scale: float = 0 if self.__base_font.em == self.__ztmy_font.em else (
            self.__base_font.em / self.__ztmy_font.em)

    def __patch_set(self):
        return [
            {
                "code_point_start": 0x3001,
                "code_point_end": 0x3002
            },
            {
                "code_point_start": 0xff1f,
                "code_point_end": 0xff1f
            },
            {
                "code_point_start": 0xff01,
                "code_point_end": 0xff01
            },
            {
                "code_point_start": 0x30fc,
                "code_point_end": 0x30fc
            },
            {
                "code_point_start": 0x300c,
                "code_point_end": 0x300d
            },
            {
                "code_point_start": 0x3041,
                "code_point_end": 0x308d
            },
            {
                "code_point_start": 0x308f,
                "code_point_end": 0x308f
            },
            {
                "code_point_start": 0x3092,
                "code_point_end": 0x3093
            },
            {
                "code_point_start": 0x30a1,
                "code_point_end": 0x30ed
            },
            {
                "code_point_start": 0x30ef,
                "code_point_end": 0x30ef
            },
            {
                "code_point_start": 0x30f2,
                "code_point_end": 0x30f4
            },
            {
                "code_point_start": 0x5f37,
                "code_point_end": 0x5f37
            },
            {
                "code_point_start": 0x6817,
                "code_point_end": 0x6817
            },
            {
                "code_point_start": 0x5263,
                "code_point_end": 0x5263
            },
            {
                "code_point_start": 0x9283,
                "code_point_end": 0x9283
            },
            {
                "code_point_start": 0x6ce5,
                "code_point_end": 0x6ce5
            },
            {
                "code_point_start": 0x571f,
                "code_point_end": 0x571f
            },
            {
                "code_point_start": 0x97ee,
                "code_point_end": 0x97ee
            },
            {
                "code_point_start": 0x732b,
                "code_point_end": 0x732b
            },
            {
                "code_point_start": 0x98ef,
                "code_point_end": 0x98ef
            },
            {
                "code_point_start": 0x591c,
                "code_point_end": 0x591c
            },
            {
                "code_point_start": 0x8e0a,
                "code_point_end": 0x8e0a
            },
        ]

    def __copy_glyphs(self, code_point_start: int,
                      code_point_end: int) -> None:
        self.__ztmy_font.selection.select(("ranges", "unicode"),
                                          code_point_start, code_point_end)
        glyphs = [
            g for g in self.__ztmy_font.selection.byGlyphs if g.unicode >= 0
        ]

        expect_glyph_count = code_point_end + 1 - code_point_start
        assert len(glyphs) == (
            expect_glyph_count
        ), "Invalid glyphs exist. Expected {} but actual {}.".format(
            expect_glyph_count, len(glyphs))

        for glyph in glyphs:
            print("Updating glyph: {}, at: 0x{:x}".format(
                glyph.glyphname, self.__base_current_code_point))

            self.__ztmy_font.selection.select(glyph.encoding)
            self.__ztmy_font.copy()
            self.__base_font.selection.select(self.__base_current_code_point)
            self.__base_font.paste()

            if self.__em_scale != 0:
                matrix = psMat.scale(self.__em_scale)
                self.__base_font[self.__base_current_code_point].transform(
                    matrix)

            self.__base_current_code_point += 1

    def __set_meta_data(self) -> None:
        print("Updating font metadata")

        copyright = self.__base_font.copyright
        copyright += "\n\n[{}]\n{}".format(self.__ztmy_font.cidfontname,
                                           self.__ztmy_font.cidcopyright)
        copyright += "\n\n[{}]\nCopyright (c) 2023, ohakutsu".format(
            PROJECT_NAME)
        self.__base_font.copyright = copyright

        self.__base_font.fontname = self.__font_name
        self.__base_font.familyname = self.__font_family_name
        self.__base_font.fullname = self.__font_name
        self.__base_font.appendSFNTName("English (US)", "Family",
                                        self.__base_font.familyname)

        self.__base_font.version = PROJECT_VERSION
        self.__base_font.sfntRevision = None
        self.__base_font.appendSFNTName("English (US)", "Version",
                                        PROJECT_VERSION)

        unique_id = "{}:{}".format(self.__font_name, PROJECT_VERSION)
        self.__base_font.appendSFNTName("English (US)", "UniqueID", unique_id)

    def patch(self) -> None:
        print("em scale: {}".format(self.__em_scale))

        for patch in self.__patch_set():
            code_point_start = patch["code_point_start"]
            code_point_end = patch["code_point_end"]

            self.__copy_glyphs(code_point_start, code_point_end)

        self.__set_meta_data()

    def generate(self, out_file_path: str) -> None:
        self.__base_font.generate(out_file_path)
        print("Generated {}".format(out_file_path))

    def close(self) -> None:
        self.__base_font.close()
        self.__ztmy_font.close()


def main():
    font_data = [
        {
            "base_font_path": "HackGenConsoleNF-Regular.ttf",
            "font_name": "ZUTOMOJI_HGC-Regular",
            "font_family_name": "ZUTOMOJI_HGC"
        },
        {
            "base_font_path": "HackGenConsoleNF-Bold.ttf",
            "font_name": "ZUTOMOJI_HGC-Bold",
            "font_family_name": "ZUTOMOJI_HGC"
        },
        {
            "base_font_path": "HackGen35ConsoleNF-Regular.ttf",
            "font_name": "ZUTOMOJI_HG35C-Regular",
            "font_family_name": "ZUTOMOJI_HG35C"
        },
        {
            "base_font_path": "HackGen35ConsoleNF-Bold.ttf",
            "font_name": "ZUTOMOJI_HG35C-Bold",
            "font_family_name": "ZUTOMOJI_HG35C"
        },
    ]
    ztmy_font_file = "ZTMY_MOJI-R.otf"

    for data in font_data:
        patcher = Patcher(data["base_font_path"], ztmy_font_file,
                          data["font_name"], data["font_family_name"])
        patcher.patch()

        out_file_path = "{}.ttf".format(data["font_name"])
        patcher.generate(out_file_path)
        patcher.close()


if __name__ == "__main__":
    main()
