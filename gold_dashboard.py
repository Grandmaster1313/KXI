from macro_engine import get_macro_bias
from dashboard_writer import write_dashboard
from yahoo_data import get_market_data, get_dxy_data
from datetime import datetime
from calendar_engine import get_calendar_status
from macro_state import load_previous_bias, save_current_bias
from audio_alert import macro_bias_up, macro_bias_down


gold = get_market_data("GC=F")
dxy = get_dxy_data()
us10y = get_market_data("^TNX")
wti = get_market_data("CL=F")
vix = get_market_data("VIXY")


print("Gold :", gold)
print("DXY  :", dxy)
print("US10Y:", us10y)
print("WTI  :", wti)
print("VIX  :", vix)
print()


bias, confidence = get_macro_bias(
    gold,
    dxy,
    us10y,
    wti,
    vix
)


history = load_previous_bias()

previous_bias = None

if history:
    previous_bias = history[0].split("|")[1]


if previous_bias is not None and previous_bias != bias:

    print(
        f"Macro Bias changed: {previous_bias} -> {bias}"
    )

    bullish_states = [
        "Bullish",
        "Strong Bullish",
        "Very Bullish"
    ]

    bearish_states = [
        "Bearish",
        "Strong Bearish",
        "Very Bearish"
    ]


    if (
        bias in bullish_states
        and previous_bias not in bullish_states
    ):

        print("MACRO BIAS IMPROVED")
        macro_bias_up()


    elif (
        bias in bearish_states
        and previous_bias not in bearish_states
    ):

        print("MACRO BIAS WEAKENED")
        macro_bias_down()



save_current_bias(bias, confidence)


history = load_previous_bias()

macro_history = []

for entry in history:

    parts = entry.split("|")

    if len(parts) >= 3:

        timestamp = parts[0]
        status = parts[1]
        confidence_value = parts[2]

        time_only = timestamp.split()[1]

        if "Bullish" in status:
            symbol = "^"

        elif "Bearish" in status:
            symbol = "v"

        else:
            symbol = "="

        macro_history.append(
            f"{time_only:<10} {symbol} {status} ({confidence_value}%)"
        )

    elif len(parts) == 2:

        # Compatibility with old history entries

        timestamp = parts[0]
        status = parts[1]

        time_only = timestamp.split()[1]

        macro_history.append(
            f"{time_only:<10} {status}"
        )

current_time = datetime.now().strftime(
    "%H:%M:%S CST"
)

last_update = datetime.now().strftime(
    "%Y-%m-%d %H:%M CST"
)


def arrow(value):

    if value > 0:
        return "^"

    elif value < 0:
        return "v"

    else:
        return "-"



def bias_text(bias):

    text = bias.lower().strip()

    if text in ("strong bullish", "very bullish"):
        return "<i>Strong Bullish ^ ^ ^</i>"

    elif text == "bullish":
        return "<i>Bullish ^</i>"

    elif text == "bearish":
        return "v Bearish"

    elif text in ("strong bearish", "very bearish"):
        return "v v v Strong Bearish"

    else:
        return bias



print("=" * 50)
print("        GOLD COMMAND CENTER V1")
print("=" * 50)

print()

print(
    f"Gold   : {gold['price']:8.2f}   "
    f"{arrow(gold['change'])} {gold['change']:>6.2f} "
    f"({gold['change_pct']}%)"
)

print(
    f"DXY    : {dxy['price']:8.2f}   "
    f"{arrow(dxy['change'])} {dxy['change']:>6.2f} "
    f"({dxy['change_pct']}%)"
)

print(
    f"US10Y  : {us10y['price']:8.2f}   "
    f"{arrow(us10y['change'])} {us10y['change']:>6.2f} "
    f"({us10y['change_pct']}%)"
)

print(
    f"WTI    : {wti['price']:8.2f}   "
    f"{arrow(wti['change'])} {wti['change']:>6.2f} "
    f"({wti['change_pct']}%)"
)

print(
    f"VIX    : {vix['price']:8.2f}   "
    f"{arrow(vix['change'])} {vix['change']:>6.2f} "
    f"({vix['change_pct']}%)"
)

print()

print("=" * 50)



trading_month, trading_week, session_status = get_calendar_status()


html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta http-equiv="refresh" content="35">

<title>KXI Command Center</title>

<link rel="stylesheet" href="style.css">

</head>


<body>
<div class="container"><pre>
+=============================================================================+
| KXI COMMAND CENTER                                     CLIENT : LIVE        |
+=============================================================================+
Macro Bias ........ {bias_text(bias)}
Confidence ........ {confidence}%

Recent Changes
{chr(10).join(macro_history)}

Trading Month ........... {trading_month}
Trading Week ............ {trading_week}

{session_status}

===============================================================================
MARKET SNAPSHOT

Gold .............. {gold['price']:8.2f}    WTI ............... {wti['price']:8.2f}
DXY ............... {dxy['price']:8.2f}    VIX ............... {vix['price']:8.2f}
US10Y ............. {us10y['price']:8.2f}

===============================================================================
SYSTEM STATUS

System ..... OK
Scheduler .. RUNNING
Dashboard .. UPDATED

Current Time ... {current_time}
Last Update .... {last_update}

+============================================================================+

</pre></div>

</body>

</html>
"""


write_dashboard(html)