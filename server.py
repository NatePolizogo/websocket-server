import asyncio
import websockets
import threading

def default_logger(name:str='Default Logger'):
    import logging

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger

class WebsockerServer(threading.Thread):

    def __init__(self, host:str="0.0.0.0", port:int=8765, daemon:bool=True, logger=None):
        super().__init__(daemon=daemon)
        self.host = host
        self.port = port

        # Setup Logging
        if logger is None:
            self.logger = default_logger(self.__class__.__name__)
        else:
            self.logger = logger
        
        self.logger.info(f'Using websockets library version: {websockets.__version__}')
        self.logger.info('Initializing Websockets Server!')

        self.clients = set()

        self.loop = asyncio.get_event_loop()
        self.start_server = websockets.serve(self.handler, host, port, loop=self.loop)


    def run(self):

        def start_loop(loop, server):
            loop.run_until_complete(server)
            loop.run_forever()

        start_loop(self.loop, self.start_server)

    async def handler(self, websocket, path):

        def message_data(data):
            return data
        
        uid = websocket.id

        self.clients.add(websocket)
        self.logger.info(f'ws:client {uid} connected at path {path}')
        try:
            async for msg in websocket:
                websockets.broadcast(self.clients, message_data(msg))
        except websockets.exceptions.ConnectionClosedError:
            self.logger.warning(f'Removing client {uid} before exit ...')
            self.clients.remove(websocket)
        finally:
            self.logger.info('Terminating Connection!')

def main():

    server = WebsockerServer(daemon=True)
    
    server.start()
    server.join()

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('\nQuiting ...')