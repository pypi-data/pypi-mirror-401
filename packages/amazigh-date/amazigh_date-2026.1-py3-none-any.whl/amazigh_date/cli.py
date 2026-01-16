#!/usr/bin/env python3
import argparse
from ._core import amazigh_date, days_until_yennayer, era_format


def main():
    parser = argparse.ArgumentParser(
        description="Amazigh (Berber) calendar"
    )

    parser.add_argument(
        "--yennayer",
        type=int,
        choices=[12, 13, 14],
        default=12,
        help="Gregorian date that starts Yennayer (default: 12)",
    )
    parser.add_argument(
        "--short",
        action="store_true",
        help='Short format: "dd-mm-yyyy"',
    )
    parser.add_argument(
        "--era",
        action="store_true",
        help='Add "Mz" suffix',
    )
    parser.add_argument(
        "--countdown",
        action="store_true",
        help="Show days remaining until next Yennayer",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Open small GTK window",
    )

    args = parser.parse_args()

    if args.countdown:
        days, y_date = days_until_yennayer(yennayer=args.yennayer)
        if days == 0:
            print(f"Happy Yennayer! Today starts the year {y_date.year + 950}.")
        else:
            print(f"{days} days until Yennayer ({y_date.strftime('%d %b %Y')}).")
        return

    y, m, d, wd = amazigh_date(yennayer=args.yennayer)

    if args.short:
        print(f"{d:02d}-{m:02d}-{y:04d}")
    else:
        print(era_format(y, m, d, wd, show_era=args.era))

    if args.gui:
        try:
            import gi
            gi.require_version("Gtk", "3.0")
            from gi.repository import Gtk
        except ImportError:
            print("GTK 3 not available")
            return

        win = Gtk.Window(title="Amazigh Calendar")
        win.set_border_width(10)

        label = Gtk.Label(
            label=f"<big><b>{era_format(y, m, d, wd, show_era=args.era)}</b></big>"
        )
        label.set_use_markup(True)

        win.add(label)
        win.show_all()
        Gtk.main()


if __name__ == "__main__":
    main()
