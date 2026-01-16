#!/usr/bin/env python3
"""
build_package.py – one-shot generator for amazigh-date Python package
Run:
    python build_package.py
Then:
    python -m pip install -e .
or:
    python -m build && twine upload dist/*
"""

import shutil
from pathlib import Path

PKG_NAME = "amazigh_date"
CLI_NAME = "amazigh-date"
EMAIL = "butterflyoffire+pypi@protonmail.com"

# ------------------------------------------------------------------ core code
CORE_CODE = '''\
import datetime
import calendar as cal
import json
from textwrap import dedent

MONTHS = [
    "Yennayer", "Fuṛar", "Meɣres", "Yebrir", "Mayyu", "Yunyu",
    "Yulyu", "Ɣuct", "Ctembeṛ", "Tubeṛ", "Wambeṛ", "Dujembeṛ"
]

DAYS = [
    "Acer", "Arim", "Aram", "Ahad", "Amhad", "Sem", "Sed"
]

def amazigh_date(greg=None, yennayer=12):
    """Return (year, month, day, weekday) of Amazigh calendar."""
    if greg is None:
        greg = datetime.date.today()

    year = greg.year + 950
    jan_first = datetime.date(greg.year, 1, 1)
    yday = (greg - jan_first).days + 1

    ystart = datetime.date(greg.year, 1, yennayer)
    ystart_doy = (ystart - jan_first).days + 1

    if yday < ystart_doy:
        year -= 1
        leap = cal.isleap(greg.year - 1)
        yday += 366 if leap else 365

    doy = yday - ystart_doy + 1

    month_lengths = [
        31,
        29 if cal.isleap(greg.year) else 28,
        31, 30, 31, 30,
        31, 31, 30, 31, 30, 31,
    ]

    m = 0
    d = doy
    while d > month_lengths[m]:
        d -= month_lengths[m]
        m += 1

    weekday = (greg.weekday() + 1) % 7
    return year, m + 1, d, weekday

def days_until_yennayer(today=None, yennayer=12):
    """Return (days_left, gregorian_yennayer_date)."""
    if today is None:
        today = datetime.date.today()

    this_year = today.year
    y_date = datetime.date(this_year, 1, yennayer)

    if today < y_date:
        delta = y_date - today
    else:
        y_date = datetime.date(this_year + 1, 1, yennayer)
        delta = y_date - today

    return delta.days, y_date

def era_format(year, month, day, weekday, show_era=False):
    base = f"{DAYS[weekday]} {day} {MONTHS[month-1]} {year}"
    return base + " Mz" if show_era else base

def as_dict(year, month, day, weekday, show_era=False):
    """Return dict ready for json.dumps."""
    return {
        "year": year,
        "month": month,
        "day": day,
        "weekday": DAYS[weekday],
        "era": "Mz" if show_era else None
    }

def ics_year(year_amazigh, yennayer=12):
    """Yield one VEVENT block per Amazigh day for the whole year."""
    g_year = year_amazigh - 950
    y_start = datetime.date(g_year, 1, yennayer)

    mlens = [31,
             29 if cal.isleap(g_year) else 28,
             31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    doy = 1
    for mon, l in enumerate(mlens, 1):
        for d in range(1, l + 1):
            g_date = y_start + datetime.timedelta(doy - 1)
            a_date = amazigh_date(g_date, yennayer=yennayer)
            summary = era_format(*a_date, show_era=True)
            uid = g_date.isoformat() + "@amazigh-date"
            yield dedent(f"""\
                BEGIN:VEVENT
                UID:{uid}
                DTSTART;VALUE=DATE:{g_date.strftime('%Y%m%d')}
                DTEND;VALUE=DATE:{g_date.strftime('%Y%m%d')}
                SUMMARY:{summary}
                END:VEVENT""")
            doy += 1
'''

# ------------------------------------------------------------------ __init__.py  (tray-free)
INIT_CODE = '''\
"""Amazigh-date: convert Gregorian ↔ Amazigh calendar."""
from ._core import (
    MONTHS, DAYS, amazigh_date, days_until_yennayer, era_format,
    as_dict, ics_year
)

__all__ = [
    "MONTHS", "DAYS", "amazigh_date", "days_until_yennayer", "era_format",
    "as_dict", "ics_year",
]
'''

# ------------------------------------------------------------------ CLI  (GTK-free)
CLI_CODE = '''\
#!/usr/bin/env python3
import argparse
from ._core import amazigh_date, days_until_yennayer, era_format, ics_year, as_dict


def main():
    parser = argparse.ArgumentParser(description="Amazigh (Berber) calendar")

    parser.add_argument(
        "--yennayer", type=int, choices=[12, 13, 14], default=12,
        help="Gregorian date that starts Yennayer (default: 12)")
    parser.add_argument(
        "--short", action="store_true",
        help='Short format: "dd-mm-yyyy"')
    parser.add_argument(
        "--era", action="store_true",
        help='Add "Mz" suffix')
    parser.add_argument(
        "--countdown", action="store_true",
        help="Show days remaining until next Yennayer")
    parser.add_argument(
        "--json", action="store_true",
        help="Machine-readable JSON output")
    parser.add_argument(
        "--export-cal", type=int, metavar="YEAR",
        help="Export entire Amazigh YEAR as iCalendar stream to stdout")

    args = parser.parse_args()

    if args.export_cal is not None:
        print("BEGIN:VCALENDAR")
        print("VERSION:2.0")
        print("PRODID:-//amazigh-date//EN")
        for block in ics_year(args.export_cal, yennayer=args.yennayer):
            print(block)
        print("END:VCALENDAR")
        return

    y, m, d, wd = amazigh_date(yennayer=args.yennayer)

    if args.json:
        import json
        print(json.dumps(as_dict(y, m, d, wd, show_era=args.era)))
        return

    if args.countdown:
        days, y_date = days_until_yennayer(yennayer=args.yennayer)
        if days == 0:
            print(f"Happy Yennayer! Today starts the year {y_date.year + 950}.")
        else:
            print(f"{days} days until Yennayer ({y_date.strftime('%d %b %Y')}).")
        return

    if args.short:
        print(f"{d:02d}-{m:02d}-{y:04d}")
    else:
        print(era_format(y, m, d, wd, show_era=args.era))


if __name__ == "__main__":
    main()
'''

# ------------------------------------------------------------------ pyproject.toml  (single script)
PYPROJECT_TOML = f'''\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "amazigh-date"
version = "2026.2"
description = "Amazigh (Berber) calendar library and CLI"
readme = "README.md"
license = "CC0-1.0"
authors = [{{name = "Athmane MOKRAOUI", email = "{EMAIL}"}}]
requires-python = ">=3.8"
keywords = ["amazigh", "berber", "calendar", "date", "yennayer"]
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "Intended Audience :: Developers",
]

[project.scripts]
{CLI_NAME} = "{PKG_NAME}.cli:main"
'''

# ------------------------------------------------------------------ README.md  (no tray)
README_MD = """\
# amazigh-date

Lightweight Python library and CLI that converts Gregorian dates to the Amazigh (Berber) calendar.

## Install

    python -m pip install amazigh-date

## CLI

    amazigh-date
    amazigh-date --short
    amazigh-date --era
    amazigh-date --countdown
    amazigh-date --json
    amazigh-date --export-cal 2976 > Yennayer2976.ics

## Library

    from amazigh_date import amazigh_date, MONTHS
    y, m, d, wd = amazigh_date()
    print(f"{d} {MONTHS[m-1]} {y}")
"""

# ------------------------------------------------------------------ builder
def build():
    root = Path(PKG_NAME)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()

    (root / "__init__.py").write_text(INIT_CODE)
    (root / "_core.py").write_text(CORE_CODE)
    (root / "cli.py").write_text(CLI_CODE)

    Path("pyproject.toml").write_text(PYPROJECT_TOML)
    Path("README.md").write_text(README_MD)

    print("Package tree created:")
    for p in sorted(Path().rglob("*")):
        print("  ", p)
    print("\nNext steps:")
    print("  python -m pip install -e .")
    print("  python -m build")
    print("  twine upload dist/")

if __name__ == "__main__":
    build()
