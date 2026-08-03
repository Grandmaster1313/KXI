from datetime import datetime, timedelta
from pathlib import Path

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).parent
CALENDAR_DIR = BASE_DIR / "calendar"

# ==========================================================
# LOAD MONTH CLASSIFICATIONS
# ==========================================================

def load_months():

    months = {}

    file = CALENDAR_DIR / "MONTHS_CLASSIFICATION.txt"

    with open(file, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            month, classification = line.split("|")

            months[int(month)] = classification.upper()

    return months


# ==========================================================
# LOAD WEEK CLASSIFICATIONS
# ==========================================================

def load_weeks():

    weeks = []

    file = CALENDAR_DIR / "WEEKS_2026_2027.txt"

    with open(file, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            start, end, confidence, description = line.split("|")

            weeks.append({

                "start": datetime.strptime(
                    start,
                    "%Y-%m-%d"
                ).date(),

                "end": datetime.strptime(
                    end,
                    "%Y-%m-%d"
                ).date(),

                "confidence": confidence.upper(),

                "description": description

            })

    return weeks


# ==========================================================
# LOAD HOLIDAYS
# ==========================================================

def load_holidays():

    holidays = {}

    file = CALENDAR_DIR / "HOLIDAYS_2026_2027_2028.txt"

    with open(file, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            d, name = line.split("|")

            holidays[
                datetime.strptime(
                    d,
                    "%Y-%m-%d"
                ).date()
            ] = name

    return holidays


# ==========================================================
# LOAD FED DATES
# ==========================================================

def load_fed():

    fed = []

    file = CALENDAR_DIR / "RATEDECISSION_DATES.txt"

    with open(file, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if line:

                fed.append(

                    datetime.strptime(

                        line,

                        "%Y-%m-%d"

                    ).date()

                )

    return fed


# ==========================================================
# LOAD BLACKOUT
# ==========================================================




# ==========================================================
# LOAD CHINESE NEW YEAR
# ==========================================================

def load_blackout():

    file = CALENDAR_DIR / "BLACKOUT_DATES.txt"

    with open(file, "r", encoding="utf-8") as f:
        line = f.readline().strip()

    start_str, end_str = line.split("|")

    start = datetime.strptime(start_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_str, "%Y-%m-%d").date()

    return start, end

def load_cny():

    file = CALENDAR_DIR / "CHINESENEWYEAR_2027.txt"

    with open(file, "r", encoding="utf-8") as f:
        line = f.readline().strip()

    if not line:
        raise ValueError("CHINESENEWYEAR_2027.txt is empty")

    if "|" not in line:
        raise ValueError(
            "CHINESENEWYEAR_2027.txt must contain: YYYY-MM-DD|YYYY-MM-DD"
        )

    start_str, end_str = line.split("|", 1)

    start = datetime.strptime(start_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_str, "%Y-%m-%d").date()

    return start, end


# ==========================================================
# LOAD DATA
# ==========================================================

MONTHS = load_months()

WEEKS = load_weeks()

HOLIDAYS = load_holidays()

FED_DATES = load_fed()

BLACKOUT_START, BLACKOUT_END = load_blackout()

CNY_START, CNY_END = load_cny()

# ==========================================================
# MAIN FUNCTION
# ==========================================================

def get_calendar_status():

    today = datetime.now().date()

    # ------------------------------------------------------
    # MONTH
    # ------------------------------------------------------

    trading_month = MONTHS.get(
        today.month,
        "UNKNOWN"
    )

    # ------------------------------------------------------
    # DEFAULTS
    # ------------------------------------------------------

    trading_week = "HIGH CONFIDENCE"

    session_status = "TRADING"

    # ------------------------------------------------------
    # BLACKOUT
    # ------------------------------------------------------

    if BLACKOUT_START <= today <= BLACKOUT_END:

        return (

            trading_month,

            "BLACKOUT",

            "=== NO TRADING (BLACKOUT PERIOD) ==="

        )

    # ------------------------------------------------------
    # CHINESE NEW YEAR
    # ------------------------------------------------------

    if CNY_START <= today <= CNY_END:

        return (

            trading_month,

            "CHINESE NEW YEAR",

            "=== TRADE ONLY TUESDAY / WEDNESDAY ==="

        )

    # ------------------------------------------------------
    # FED
    # ------------------------------------------------------

    for fed_day in FED_DATES:

        if today == fed_day:

            return (

                trading_month,

                "FED DAY",

                "=== NO TRADING (FED DAY) ==="

            )

        if today == fed_day - timedelta(days=1):

            return (

                trading_month,

                "FED WARNING",

                "=== 1 DAY TO FED ==="

            )

        if today == fed_day - timedelta(days=2):

            return (

                trading_month,

                "FED WARNING",

                "=== 2 DAYS TO FED ==="

            )

    # ------------------------------------------------------
    # WEEKS
    # ------------------------------------------------------

    for week in WEEKS:

        if week["start"] <= today <= week["end"]:

            confidence = week["confidence"]

            if confidence == "VERY LOW":

                trading_week = "VERY LOW CONFIDENCE"

                session_status = "=== NO TRADING ==="

            elif confidence == "LOW":

                trading_week = "LOW CONFIDENCE"

                session_status = "=== LOW CONFIDENCE ==="

            elif confidence == "MEDIUM":

                trading_week = "MEDIUM CONFIDENCE"

                session_status = "=== MEDIUM CONFIDENCE ==="

            elif confidence == "HIGH":

                trading_week = "HIGH CONFIDENCE"

                session_status = "TRADING"

            else:

                trading_week = confidence

                session_status = "TRADING"

            break

    # ------------------------------------------------------
    # 1 DAY BEFORE VERY LOW WEEK
    # ------------------------------------------------------

    for week in WEEKS:

        if week["confidence"] == "VERY LOW":

            if today == week["start"] - timedelta(days=1):

                session_status = "=== 1 DAY TO VERY LOW CONFIDENCE WEEK ==="

                break

    # ------------------------------------------------------
    # HOLIDAY
    # ------------------------------------------------------

    if today in HOLIDAYS:

        session_status = f"=== HOLIDAY : {HOLIDAYS[today]} ==="

    # ------------------------------------------------------
    # RETURN
    # ------------------------------------------------------

    return (

        trading_month,

        trading_week,

        session_status

    )


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print(get_calendar_status())