#!/usr/bin/env python3

import asyncio
import itertools
import time

from aioify import aioify
from phue import Bridge, Group, Light, PhueRegistrationException
from concurrent.futures import ThreadPoolExecutor

_HOSTNAME: str = '10.20.2.11'

speed: float = 0.3 # Configurable speed
RED: int = 2000
CYAN: int = 39000
PURPLE: int = 55000
YELLOW: int = 10000

def connect(ip: str) -> Bridge:
    try:
        return Bridge(ip)
    except PhueRegistrationException:
        raise RuntimeError("Go press the button on your Bridge and try again! Quick!")


def set_group_setting(group_id: int, *args, **kwargs):
    if b.set_group(group_id, *args, **kwargs) is None:
        raise ValueError(f"Unknown group id {group_id}")

def main():
    global b
    b = connect(_HOSTNAME)
    _group = 'Office'

    group_id = b.get_group_id_by_name(_group)
    if group_id is False:
        raise ValueError(f"Unknown light group {group_name}")

    preflight_settings = {
        #'transitiontime': speed,
        'on': True,
        'bri': 254,
        #'saturation': 254,
        'hue': YELLOW
    }
    for setting, value in preflight_settings.items():
        set_group_setting(group_id, setting, value)

    for hue in itertools.cycle([YELLOW, RED, CYAN, PURPLE]):
        set_group_setting(group_id, 'hue', hue, transitiontime=0.1)
        time.sleep(speed)


if __name__ == "__main__":
    main()
