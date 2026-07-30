from macro_engine import get_macro_bias
from dashboard_writer import write_dashboard
from yahoo_data import get_market_data, get_dxy_data
from datetime import datetime

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

current_time = datetime.now().strftime("%H:%M:%S CST")

last_update = datetime.now().strftime("%Y-%m-%d %H:%M CST")

def arrow(value):

    if value > 0:
        return "^"

    elif value < 0:
        return "v"


    else:
        return "-"

    def bias_text(bias):

    bias = bias.lower()

    if bias == "very bullish":
        return "<i>Very Bullish ^ ^ ^</i>"

    elif bias == "bullish":
        return "<i>Bullish ^</i>"

    elif bias == "bearish":
        return "v Bearish"

    elif bias == "very bearish":
        return "v v v Very Bearish"

    else:
        return bias.title()
    
print("=" * 50)
print("        GOLD COMMAND CENTER V1")
print("=" * 50)

print()

print(f"Gold   : {gold['price']:8.2f}   {arrow(gold['change'])} {gold['change']:>6.2f} ({gold['change_pct']}%)")
print(f"DXY    : {dxy['price']:8.2f}   {arrow(dxy['change'])} {dxy['change']:>6.2f} ({dxy['change_pct']}%)")
print(f"US10Y  : {us10y['price']:8.2f}   {arrow(us10y['change'])} {us10y['change']:>6.2f} ({us10y['change_pct']}%)")
print(f"WTI    : {wti['price']:8.2f}   {arrow(wti['change'])} {wti['change']:>6.2f} ({wti['change_pct']}%)")
print(f"VIX    : {vix['price']:8.2f}   {arrow(vix['change'])} {vix['change']:>6.2f} ({vix['change_pct']}%)")
print()

print("=" * 50)

python scheduler.py
 calendar_engine import get_calendar_status

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

<div class="container">

<pre>

+============================================================================+
| KXI COMMAND CENTER                                     CLIENT : LIVE        |
+============================================================================+

MARKET CONDITIONS

Macro Bias .............. {bias}
Confidence .............. {confidence}%

Trading Month ........... {trading_month}
Trading Week ............ {trading_week}
{session_status}

===============================================================================

MARKET SNAPSHOT

Gold .............. {gold['price']:8.2f}     {arrow(gold['change'])}{gold['change']:6.2f}
DXY ............... {dxy['price']:8.2f}      {arrow(dxy['change'])}{dxy['change']:6.2f}

US10Y ............. {us10y['price']:8.2f}    {arrow(us10y['change'])}{us10y['change']:6.2f}
WTI ............... {wti['price']:8.2f}      {arrow(wti['change'])}{wti['change']:6.2f}

VIX ............... {vix['price']:8.2f}      {arrow(vix['change'])}{vix['change']:6.2f}

===============================================================================

SYSTEM STATUS

System ..... OK                 Current Time ... {current_time}
Scheduler .. RUNNING            Last Update ... {last_update}
Dashboard .. UPDATED            Status ........ READY

+============================================================================+

</pre>

</div>

</body>

</html>

"""
write_dashboard(html)