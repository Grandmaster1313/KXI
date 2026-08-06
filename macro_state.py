from pathlib import Path
from datetime import datetime

from audio_alert import (
    macro_bias_up,
    macro_bias_down
)


STATE_FILE = Path("macro_bias_state.txt")


# ============================================================
# LOAD HISTORY
# ============================================================

def load_previous_bias():

    if not STATE_FILE.exists():
        return []

    return [
        line.strip()
        for line in STATE_FILE.read_text().splitlines()
        if line.strip()
    ]



# ============================================================
# BIAS VALUE
# ============================================================

def bias_strength(bias):

    values = {
        "Strong Bearish": -2,
        "Bearish": -1,
        "Neutral": 0,
        "Bullish": 1,
        "Strong Bullish": 2
    }

    return values.get(bias, 0)



# ============================================================
# CHECK CHANGE
# ============================================================

def check_bias_change(new_bias):

    history = load_previous_bias()

    if not history:
        return


    old_entry = history[0]


    if "|" not in old_entry:
        return


    old_bias = old_entry.split("|")[1]


    old_strength = bias_strength(old_bias)
    new_strength = bias_strength(new_bias)



    if new_strength > old_strength:

        print(
            f"MACRO BIAS IMPROVED: {old_bias} -> {new_bias}"
        )

        macro_bias_up()



    elif new_strength < old_strength:

        print(
            f"MACRO BIAS WEAKENED: {old_bias} -> {new_bias}"
        )

        macro_bias_down()



# ============================================================
# SAVE
# ============================================================

def save_current_bias(bias, confidence):

    check_bias_change(bias)


    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S CST"
    )


    entry = f"{timestamp}|{bias}|{confidence}"


    history = load_previous_bias()


    if history:

        previous = history[0].split("|")[1]

        if previous == bias:
            return



    history.insert(0, entry)


    history = history[:3]


    STATE_FILE.write_text(
        "\n".join(history)
    )