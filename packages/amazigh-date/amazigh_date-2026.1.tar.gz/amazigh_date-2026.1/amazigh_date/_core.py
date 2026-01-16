import datetime
import calendar as cal

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
