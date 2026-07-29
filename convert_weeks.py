from pathlib import Path
import re

CALENDAR = Path("calendar")

INPUT = CALENDAR / "WEEKS_2026_2027.txt"
OUTPUT = CALENDAR / "WEEKS_2026_2027_NEW.txt"

MONTHS = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}

year = 2026

with open(INPUT, "r", encoding="utf-8") as fin, \
     open(OUTPUT, "w", encoding="utf-8") as fout:

    for line in fin:

        line = line.strip()

        if not line:
            continue

        # Skip year headers
        if line == "2026":
            year = 2026
            continue

        if line == "2027":
            year = 2027
            continue

        if line == "20027":
            year = 2027
            continue

        # Remove emoji circles

line = line.strip()

        parts = re.split(r"\s{2,}|\t+", line)

        if len(parts) != 3:
            print("SKIPPED:", line)
            continue

        week_text = parts[0].strip()
        description = parts[1].strip().upper()
        confidence = parts[2].strip().upper()

        m = re.match(
            r"([A-Za-z]{3})\s+(\d+)-(?:(?P<endmonth>[A-Za-z]{3})\s*)?(\d+)",
            week_text,
        )

        if not m:
            print("SKIPPED:", line)
            continue

        start_month_name = m.group(1)
        end_month_name = m.group("endmonth")

        start_month = MONTHS[start_month_name]

        if end_month_name:
            end_month = MONTHS[end_month_name]
        else:
            end_month = start_month

        start_day = int(m.group(2))
        end_day = int(m.group(4))

        start_year = year
        end_year = year

        if start_month == "12" and end_month == "01":
            end_year += 1

        start_date = f"{start_year}-{start_month}-{start_day:02d}"
        end_date = f"{end_year}-{end_month}-{end_day:02d}"

        fout.write(
            f"{start_date}|{end_date}|{confidence}|{description}\n"
        )

print()
print("DONE")
print("Output:", OUTPUT)