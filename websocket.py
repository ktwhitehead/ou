import asyncio
import websockets
from threading import Thread

class WebSocket:
  def __init__(self):
    self.connected = set()

  async def server(self, websocket, path):
      # Register.
      self.connected.add(websocket)
      try:
        # Respond to each websocket connection here
        async for message in websocket:
          for conn in self.connected:
            await conn.send('bla')
      finally:
        # Unregister.
        self.connected.remove(websocket)

  async def send_message(self, message):
    for conn in self.connected:
      await conn.send(message)

  def start_loop(self, loop, server):
    loop.run_until_complete(server)
    loop.run_forever()

  def start(self):
    new_loop = asyncio.new_event_loop()

    start_server = websockets.serve(self.server, "172.19.229.37", 5000, loop=new_loop)

    t = Thread(target=self.start_loop, args=(new_loop, start_server))
    t.start()
