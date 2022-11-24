import asyncio
import websockets


class _WebSocketClient:
    def __init__(self, ws_url, on_message=None, on_connect=None, on_error=None, on_close=None, on_update=None):
        self.ws_url = ws_url
        self.on_message = on_message if on_message is not None else self._on_message
        self.on_error = on_error if on_error is not None else self._on_error
        self.on_close = on_close if on_close is not None else self._on_close
        self.on_connect = on_connect if on_connect is not None else self._on_connect
        self.on_update = on_update if on_update is not None else lambda: None
        self.running = True
        self.websocket = None

    def run(self):
        self.main()

    def main(self):
        for websocket in websockets.connect(self.ws_url):
            self.websocket = websocket
            self.on_update()
            if not self.running:
                break
            if websocket.open:
                try:
                    self.on_connect(websocket)
                    for message in websocket:
                        if not self.running:
                            break
                        self.on_update()
                        self.on_message(websocket, message)
                except websockets.ConnectionClosed:
                    self.on_close(websocket)
                except Exception as exception:
                    self.on_error(websocket, exception)

    def close(self):
        self.websocket.close()
        self.running = False

    def _on_message(self, ws, msg):
        print("WS Msg:", msg)

    def _on_error(self, ws, error):
        print("WS Error:", error)

    def _on_connect(self, ws):
        ws.send("--start connection--")
        print("WS ### connected ###")

    def _on_close(self, ws):
        print("WS ### closed ###")


class WebSocketClient(_WebSocketClient):
    def run(self):
        asyncio.run(self.main())

    async def main(self):
        async for websocket in websockets.connect(self.ws_url):
            self.websocket = websocket
            self.on_update()
            if not self.running:
                break
            if websocket.open:
                try:
                    await self.on_connect(websocket)
                    async for message in websocket:
                        if not self.running:
                            break
                        self.on_update()
                        await self.on_message(websocket, message)
                except websockets.ConnectionClosed:
                    await self.on_close(websocket)
                except Exception as exception:
                    await self.on_error(websocket, exception)

    def close(self):
        self.websocket.close()
        self.running = False

    async def _on_message(self, ws, msg):
        print("WS Msg:", msg)

    async def _on_error(self, ws, error):
        print("WS Error:", error)

    async def _on_connect(self, ws):
        await ws.send("--start connection--")
        print("WS ### connected ###")

    async def _on_close(self, ws):
        print("WS ### closed ###")


if __name__ == '__main__':
    host = 'localhost'
    port = '80'
    websocket_resource_url = f"ws://{host}:{port}"
    ws_client = WebSocketClient(websocket_resource_url)
    ws_client.run()
