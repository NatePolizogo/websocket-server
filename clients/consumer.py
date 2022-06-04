import json
import time
import asyncio
from websocket import create_connection

ws_client = create_connection("ws://localhost:8766/rebroadcast")
# for i in range(100):
tic = time.time()
while True:
    
    data = ws_client.recv()

    toc = time.time()
    delta = toc - tic
    tic = toc
    print(delta*1E3, data)
    # await asyncio.sleep(1)
    # time.sleep(1)
    # asyncio.sleep(1)

ws_client.close()