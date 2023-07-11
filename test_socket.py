
import asyncio
from websockets.server import serve
from faker import Faker
import random
import json
from time import sleep

# ws://127.0.0.1:8765

fake = Faker()

def get_random_message():
    msg = {
        "name": fake.name(),
        "email": fake.email(),
        "text": fake.text(),
        "id": random.randint(0, 10000)
    }

    return msg

async def echo(websocket):
    print("Connected")

    while True:
        msg = get_random_message()
        print(f"Msg {msg}")
        await websocket.send(json.dumps(msg))
        sleep(1)


async def main():
    async with serve(echo, "localhost", 8765):
        print("Started")
        await asyncio.Future()  # run forever

asyncio.run(main())