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
