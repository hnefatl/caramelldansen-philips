#!/usr/bin/env python3

import asyncio
import itertools
import time

from aioify import aioify
from phue import Bridge, Group, Light, PhueRegistrationException

_HOSTNAME: str = '10.20.2.11'

speed: float = 0.2 # Configurable speed
RED: int = 2000
CYAN: int = 39000
PURPLE: int = 55000
YELLOW: int = 10000

def connect(ip: str) -> Bridge:
    try:
        return Bridge(ip)
    except PhueRegistrationException:
        raise RuntimeError("Go press the button on your Bridge and try again! Quick!")


def get_group_lights(group_name: str) -> list[Light]:
    group_id = b.get_group_id_by_name(group_name)

    # TODO: work out if it's guaranteed to be this index
    group = b.groups[group_id]

    return group.lights


async def set_group_hue(lights: list[Light], hue: int):
    ops = list(map(lambda x: b.aio_set_light(x.light_id, 'hue', hue, transitiontime=0.1), lights))
    await asyncio.gather(*ops)


async def party_time(lights: list[Light]):
    preflight_command = {
        'transitiontime': speed,
        'on': True,
        'bri': 254,
        'saturation': 254,
        'hue': YELLOW
    }

    for light in lights:
        light.on = preflight_command['on']
        light.transitiontime = preflight_command['transitiontime']
        light.bri = preflight_command['bri']
        light.saturation = preflight_command['saturation']
        light.hue = preflight_command['hue']

    for hue in itertools.cycle([YELLOW, RED, CYAN, PURPLE]):
        await set_group_hue(lights, hue)
        time.sleep(speed)


async def main():
    global b
    b = connect(_HOSTNAME)
    b.aio_set_light = aioify(obj=b.set_light)

    _group = 'lights.office'

    lights = get_group_lights(group_name=_group)
    await party_time(lights)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
