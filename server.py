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
    
    def __init__(self, host:str="0.0.0.0", port:int=8765, daemon:bool=True, cfg:str='', logger=None):
        super().__init__(daemon=daemon)
        self.version = 'v0.1.0'
        self.host = host
        self.port = port

        # Setup Logging
        if logger is None:
            self.logger = default_logger(self.__class__.__name__)
        else:
            self.logger = logger
        
        self.logger.info(f'Using websockets library version: {websockets.__version__}')
        self.logger.info(f'Initializing Websockets Server {self.version} @ {self.host}:{self.port} !')

        self.clients = set()

        self.loop = asyncio.get_event_loop()
        self.start_server = websockets.serve(self.handler, self.host, self.port, loop=self.loop)


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

def main(opt):

    if opt.config == '':
        server = WebsockerServer(host=opt.host ,port=8766)
    else:
        server = WebsockerServer(opt.config)
    
    server.start()
    server.join()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simple Websocket Server')
    parser.add_argument('--config', '-cfg', type=str, default='', help='server configuration file')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='host ip')
    parser.add_argument('--port', '-p', type=int, default=8765, help='server port')
    opt = parser.parse_args()
    
    try:
        main(opt)
    except KeyboardInterrupt:
        print('\nQuiting ...')