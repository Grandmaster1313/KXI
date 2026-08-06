def get_macro_bias(gold, dxy, us10y, wti, vix):

    # -------------------------
    # Prevent crashes if any feed is unavailable
    # -------------------------

    if gold is None:
        gold = {"change": 0}

    if dxy is None:
        dxy = {"change": 0}

    if us10y is None:
        us10y = {"change": 0}

    if wti is None:
        wti = {"change": 0}

    if vix is None:
        vix = {"change": 0}

    score = 0

    print()
    print("=" * 50)
    print("MACRO BIAS DIAGNOSTICS")
    print("=" * 50)

    # -------------------------
    # DXY (30%)
    # -------------------------

    if dxy["change"] > 0:
        dxy_score = -30
    else:
        dxy_score = 30

    score += dxy_score

    print(
        f"DXY    Change: {dxy['change']:>7.2f}   "
        f"Contribution: {dxy_score:+d}"
    )

    # -------------------------
    # US10Y (20%)
    # -------------------------

    if us10y["change"] > 0:
        us10y_score = -20
    else:
        us10y_score = 20

    score += us10y_score

    print(
        f"US10Y  Change: {us10y['change']:>7.2f}   "
        f"Contribution: {us10y_score:+d}"
    )

    # -------------------------
    # WTI (10%)   <-- APPROVED CHANGE
    # -------------------------

    if wti["change"] > 0:
        wti_score = 10
    else:
        wti_score = -10

    score += wti_score

    print(
        f"WTI    Change: {wti['change']:>7.2f}   "
        f"Contribution: {wti_score:+d}"
    )

    # -------------------------
    # VIX (10%)
    # -------------------------

    if vix["change"] > 0:
        vix_score = 10
    else:
        vix_score = -10

    score += vix_score

    print(
        f"VIX    Change: {vix['change']:>7.2f}   "
        f"Contribution: {vix_score:+d}"
    )

    print("-" * 50)
    print(f"TOTAL SCORE : {score:+d}")

    # -------------------------
    # Final Classification
    # -------------------------

    if score >= 60:
        bias = "Strong Bullish"

    elif score >= 20:
        bias = "Bullish"

    elif score <= -60:
        bias = "Strong Bearish"

    elif score <= -20:
        bias = "Bearish"

    else:
        bias = "Neutral"

    confidence = abs(score)

    print(f"BIAS        : {bias}")
    print(f"CONFIDENCE  : {confidence}%")
    print("=" * 50)
    print()

    return bias, confidence