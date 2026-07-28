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

    # -------------------------
    # DXY (30%)
    # -------------------------
    if dxy["change"] > 0:
        score -= 30
    else:
        score += 30

    # -------------------------
    # US10Y (20%)
    # -------------------------
    if us10y["change"] > 0:
        score -= 20
    else:
        score += 20

    # -------------------------
    # WTI (40%)
    # -------------------------
    if wti["change"] > 0:
        score += 40
    else:
        score -= 40

    # -------------------------
    # VIX (10%)
    # -------------------------
    if vix["change"] > 0:
        score += 10
    else:
        score -= 10

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

    return bias, confidence