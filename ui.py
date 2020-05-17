#!/usr/bin/env python

# Based on the following tutorial / documentation:
# https://websockets.readthedocs.io/en/stable/intro.html

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import pantilt

logging.basicConfig()

STATE = {"horizontal_angle": 0,
         "vertical_angle" : 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "left":
                STATE["horizontal_angle"] -= 0.5
                pantilt.set_horizontal_angle(STATE["horizontal_angle"])
                await notify_state()
            elif data["action"] == "right":
                STATE["horizontal_angle"] += 0.5
                pantilt.set_horizontal_angle(STATE["horizontal_angle"])
                await notify_state()
            elif data["action"] == "up":
                STATE["vertical_angle"] += 0.5
                pantilt.set_vertical_angle(STATE["vertical_angle"])
                await notify_state()
            elif data["action"] == "down":
                STATE["vertical_angle"] -= 0.5
                pantilt.set_vertical_angle(STATE["vertical_angle"])
                await notify_state()
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, None, 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
