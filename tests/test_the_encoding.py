"""
THE ENCODING TEST âœ“âœ“.

**=> THE PEER SAW **THE WHOLE UI** WITH **BROKEN ICONS** âœ“âœ“ â€” **=> `Ã°Å¸â€œâ€¹` INSTEAD
OF `ðŸ“‹` âœ“âœ“, **=> AND `Ã¢â€žÂ¹Ã¯Â¸` INSTEAD OF `ðŸ` âœ“âœ“.**

**=> AND THE CAUSE WAS **MY OWN** âœ“âœ“ â€” **=> A POWERSHELL WRITE THAT USED **THE
**=> WRONG ENCODING** âœ“âœ“, **=> WHICH TURNED EVERY UTF-8 BYTE INTO **TWO
**=> CHARACTERS** âœ“âœ“ â€” **=> AND **THE FILE LOOKED FINE** âœ“âœ“ â€” **=> AND **THE TEST
**=> SUITE PASSED** âœ“âœ“.**

**=> AND **THAT IS **THE MOST IMPORTANT THING ABOUT THIS FILE** âœ“âœ“ â€” **=> THE
**=> DEFECT WAS **INVISIBLE** TO EVERY CHECK âœ“âœ“, **=> EXCEPT **A HUMAN LOOKING AT
**=> THE SCREEN** âœ“âœ“.**

**=> SO THIS TEST IS **THE HUMANS EYES** âœ“âœ“ â€” **=> IT LOOKS FOR **THE SIGNATURE**
**=> OF THE DAMAGE** âœ“âœ“, **=> AND IT IS **THE ONLY** TEST THAT WOULD HAVE CAUGHT
**=> IT** âœ“âœ“.**
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# **=> THE SIGNATURE âœ“âœ“ â€” **=> TWO CP1252 CHARACTERS IN A ROW âœ“âœ“, **=> WHERE A
# **=> SINGLE UTF-8 CHARACTER WAS MEANT âœ“âœ“.**
MOJIBAKE = re.compile(r"[\u00c0-\u00ff][\u0080-\u00bf]")

# **=> AND THE FILES THAT MATTER âœ“âœ“ â€” **=> THE ONES A HUMAN READS âœ“âœ“.**
READABLE = [
    "ui/index.html",
    "README.md",
    "00_README.md",
    "PRODUCT_DOCUMENTATION.md",
]


def test_no_file_has_mojibake():
    """
    **=> EVERY FILE âœ“âœ“ â€” **=> NOT JUST THE UI** âœ“âœ“, **=> BECAUSE **THE DAMAGE
    **=> LANDED IN A **PYTHON** FILE TOO** âœ“âœ“ â€” **=> `services/gate.py` **HAD
    **THIRTY** MANGLED CHARACTERS** âœ“âœ“, **=> AND **NOBODY WOULD HAVE SEEN IT**
    **=> UNLESS **THEY READ IT** âœ“âœ“.**
    """
    offenders = []
    for directory, subdirs, files in os.walk(ROOT):
        subdirs[:] = [
            d for d in subdirs if d not in (".git", "__pycache__", "node_modules", ".venv")
        ]
        for name in files:
            if not name.endswith((".html", ".py", ".md", ".json", ".sh")):
                continue
            path = os.path.join(directory, name)
            # THIS FILE HOLDS THE PATTERN ITSELF, SO IT WOULD FIND ITSELF.
            if os.path.abspath(path) == os.path.abspath(__file__):
                continue
            with open(path, "rb") as handle:
                text = handle.read().decode("utf-8", errors="replace")
            hits = MOJIBAKE.findall(text)
            if hits:
                offenders.append("{}: {}".format(os.path.relpath(path, ROOT), len(hits)))
    assert not offenders, "mojibake in:\n  " + "\n  ".join(offenders)


def test_the_readable_files_are_valid_utf8():
    """
    **=> AND **THE ONES **THE PEER READS** âœ“âœ“ **MUST BE **VALID UTF-8** âœ“âœ“ â€”
    **=> NOT JUST **MOJIBAKE-FREE** âœ“âœ“ â€” **=> BECAUSE **A FILE WITH A BROKEN
    **=> BYTE** IS **NOT UTF-8** âœ“âœ“, **=> AND **THAT** **IS **WHAT THE BROWSER
    **=> CHOKES ON** âœ“âœ“.**
    """
    for relative in READABLE:
        path = os.path.join(ROOT, relative)
        if not os.path.exists(path):
            continue
        with open(path, "rb") as handle:
            raw = handle.read()
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise AssertionError(
                "{} is not valid UTF-8: {}".format(relative, error)
            ) from error


def test_the_icons_are_real_emoji():
    """
    **=> AND **THE NAV ICONS** âœ“âœ“ **MUST BE **THE EMOJI** âœ“âœ“ â€” **=> NOT **THE
    **=> MOJIBAKE** âœ“âœ“ â€” **=> AND **THIS IS **THE EXACT THING **THE PEER SAW**
    **=> âœ“âœ“.**
    """
    path = os.path.join(ROOT, "ui", "index.html")
    with open(path, encoding="utf-8") as handle:
        ui = handle.read()
    icons = re.findall(r'<span class="nav-icon">(.*?)</span>', ui, re.S)
    assert icons, "the nav has no icons"
    for icon in icons:
        assert not MOJIBAKE.search(icon), (
            "the icon {} is mojibake - it should be the character itself".format(
                repr(icon)
            )
        )
        assert any(ord(char) > 0x2000 for char in icon), (
            "the icon {} is not an emoji".format(repr(icon))
        )
