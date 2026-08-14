def scaled_score(change_pct, levels, weights, inverse=False):
    """
    change_pct : daily percentage change
    levels     : threshold percentages
    weights    : score values
    inverse    : True for DXY / US10Y / VIX
    """

    c = abs(change_pct)
    score = 0

    for level, weight in zip(levels, weights):
        if c >= level:
            score = weight

    if change_pct < 0:
        direction = -1
    elif change_pct > 0:
        direction = 1
    else:
        direction = 0

    score *= direction

    if inverse:
        score *= -1

    return score


def get_macro_bias(gold, dxy, us10y, wti, vix):

    gold = gold or {"change_pct": 0}
    dxy = dxy or {"change_pct": 0}
    us10y = us10y or {"change_pct": 0}
    wti = wti or {"change_pct": 0}
    vix = vix or {"change_pct": 0}

    print()
    print("=" * 60)
    print("MACRO ENGINE V2")
    print("=" * 60)

    GOLD_LEVELS = [0.10, 0.25, 0.40, 0.60, 0.80]
    GOLD_WEIGHTS = [2, 4, 6, 8, 10]

    DXY_LEVELS = [0.05, 0.15, 0.30, 0.50]
    DXY_WEIGHTS = [8, 15, 25, 35]

    US10Y_LEVELS = [0.05, 0.15, 0.30, 0.50]
    US10Y_WEIGHTS = [5, 10, 18, 25]

    WTI_LEVELS = [0.10, 0.30, 0.60, 1.00]
    WTI_WEIGHTS = [3, 6, 10, 15]

    VIX_LEVELS = [0.20, 0.50, 1.00]
    VIX_WEIGHTS = [4, 8, 15]

    gold_score = scaled_score(
        gold.get("change_pct", 0),
        GOLD_LEVELS,
        GOLD_WEIGHTS,
        inverse=False,
    )

    dxy_score = scaled_score(
        dxy.get("change_pct", 0),
        DXY_LEVELS,
        DXY_WEIGHTS,
        inverse=True,
    )

    us10y_score = scaled_score(
        us10y.get("change_pct", 0),
        US10Y_LEVELS,
        US10Y_WEIGHTS,
        inverse=True,
    )

    # WTI DOWN = bearish
    wti_score = scaled_score(
        wti.get("change_pct", 0),
        WTI_LEVELS,
        WTI_WEIGHTS,
        inverse=False,
    )

    # VIX UP = bearish
    vix_score = scaled_score(
        vix.get("change_pct", 0),
        VIX_LEVELS,
        VIX_WEIGHTS,
        inverse=True,
    )

    score = (
        gold_score
        + dxy_score
        + us10y_score
        + wti_score
        + vix_score
    )

    print(f"Gold  : {gold_score:+3}")
    print(f"DXY   : {dxy_score:+3}")
    print(f"US10Y : {us10y_score:+3}")
    print(f"WTI   : {wti_score:+3}")
    print(f"VIX   : {vix_score:+3}")

    print("-" * 60)
    print(f"TOTAL : {score:+3}")

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

    confidence = min(abs(score), 100)

    print(f"BIAS       : {bias}")
    print(f"CONFIDENCE : {confidence}%")
    print("=" * 60)
    print()

    return bias, confidence