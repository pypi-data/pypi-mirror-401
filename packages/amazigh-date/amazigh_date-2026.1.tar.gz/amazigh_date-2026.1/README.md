# amazigh-date

Lightweight Python library and CLI that converts Gregorian dates to the Amazigh (Berber) calendar.

## Install

    python -m pip install amazigh-date

## CLI

    amazigh-date
    amazigh-date --short
    amazigh-date --era
    amazigh-date --countdown
    amazigh-date --gui

## Library

    from amazigh_date import amazigh_date, MONTHS
    y, m, d, wd = amazigh_date()
    print(f"{d} {MONTHS[m-1]} {y}")
