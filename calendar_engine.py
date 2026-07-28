from datetime import datetime, date


def get_calendar_status():

    today = datetime.now().date()

    # ---------------------------------
    # Trading Month
    # ---------------------------------

    if today.month in [8, 9]:
        trading_month = "STRONG"

    elif today.month in [12, 1, 2]:
        trading_month = "WEAK"

    else:
        trading_month = "NEUTRAL"

    # ---------------------------------
    # Default
    # ---------------------------------

    trading_week = "HIGH"

    # ---------------------------------
    # LOW CONFIDENCE WEEKS
    # ---------------------------------

    low_weeks = [

        (date(2026, 7, 13), date(2026, 7, 17)),
        (date(2026, 9, 14), date(2026, 9, 18)),
        (date(2026, 10, 26), date(2026, 10, 30)),
        (date(2026, 11, 23), date(2026, 11, 27)),
        (date(2026, 12, 21), date(2026, 12, 25)),
        (date(2026, 12, 28), date(2027, 1, 1)),

    ]

    # ---------------------------------
    # VERY LOW CONFIDENCE WEEKS
    # ---------------------------------

    very_low_weeks = [

        (date(2026, 7, 27), date(2026, 7, 31)),
        (date(2026, 12, 7), date(2026, 12, 11)),

    ]

    # ---------------------------------
    # Determine current trading week
    # ---------------------------------

    for start, end in very_low_weeks:
        if start <= today <= end:
            trading_week = "VERY LOW CONFIDENCE"
            break

    if trading_week != "VERY LOW CONFIDENCE":
        for start, end in low_weeks:
            if start <= today <= end:
                trading_week = "LOW CONFIDENCE"
                break

    # ---------------------------------
    # Session Status
    # ---------------------------------

    if trading_week in (
        "LOW CONFIDENCE",
        "VERY LOW CONFIDENCE",
    ):
        session_status = "=== DO NOT TRADE ASIA/EUROPE SESSION ==="
    else:
        session_status = "TRADING"

    return (
        trading_month,
        trading_week,
        session_status,
    )