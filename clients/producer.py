import json
import time
# import asyncio
from websocket import create_connection

from utils import default_logger

logger = default_logger()

ws_client = create_connection("ws://localhost:8766/rebroadcast")
tic = time.time()

try:
    while True:
        
        ws_client.send( json.dumps( { "data": 'Naiiii Poios Einaiii'} ) )
        data = ws_client.recv()

        toc = time.time()
        delta = toc - tic
        tic = toc
        logger.debug(delta*1E3)     # ms
        # print(data)
        # await asyncio.sleep(1)
        # time.sleep(1)
        # asyncio.sleep(1)
except KeyboardInterrupt:
    ws_client.close()