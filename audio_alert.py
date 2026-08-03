import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pygame


pygame.mixer.init(
    frequency=44100,
    size=-16,
    channels=2
)


LOG_FILE = Path("logs") / "audio_alert.log"

STATUS_FILE = Path("audio_alert_status.txt")



# ============================================================
# WRITE AUDIO HISTORY LOG
# ============================================================

def write_audio_log(event, frequency, duration, gap):

    LOG_FILE.parent.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S CST"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write(
            f"{timestamp} | "
            f"{event} | "
            f"{frequency}Hz | "
            f"duration={duration}s | "
            f"gap={gap}s\n"
        )



# ============================================================
# WRITE CURRENT ALERT STATUS
# ============================================================

def write_audio_status(event, frequency, duration, gap):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S CST"
    )

    with open(
        STATUS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"LAST ALERT: {event}\n"
        )

        f.write(
            f"TIME: {timestamp}\n"
        )

        f.write(
            f"FREQUENCY: {frequency}Hz\n"
        )

        f.write(
            f"DURATION: {duration}s\n"
        )

        f.write(
            f"GAP: {gap}s\n"
        )



# ============================================================
# PLAY BEEP
# ============================================================

def play_beep(
    frequency,
    duration,
    gap,
    event
):

    sample_rate = 44100

    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        False
    )

    wave = np.sin(
        2 * np.pi * frequency * t
    )


    stereo = np.column_stack(
        (wave, wave)
    )


    stereo = (
        stereo * 32767 * 0.50
    ).astype(np.int16)


    sound = pygame.sndarray.make_sound(
        stereo
    )


    write_audio_log(
        event,
        frequency,
        duration,
        gap
    )


    write_audio_status(
        event,
        frequency,
        duration,
        gap
    )


    for _ in range(3):

        channel = sound.play()

        while channel.get_busy():

            time.sleep(0.01)

        time.sleep(gap)



# ============================================================
# MACRO BIAS IMPROVES
# ============================================================

def macro_bias_up():

    play_beep(
        frequency=1200,
        duration=0.18,
        gap=0.25,
        event="MACRO BIAS UP"
    )



# ============================================================
# MACRO BIAS WEAKENS
# ============================================================

def macro_bias_down():

    play_beep(
        frequency=500,
        duration=0.30,
        gap=0.35,
        event="MACRO BIAS DOWN"
    )