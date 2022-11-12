from aiohttp import web

class App:
    def __init__(self, address="127.0.0.1", port=3333):
        self._address = address
        self._port = 3333
        self._app = web.Application()
        self._handler = Handler()
        self._app.add_routes([web.get('/ping', self._handler._get_ping)])

    def run(self):
        web.run_app(self._app, host=self._address, port=self._port)

class Handler:
    def __init__(self):
        pass
        
    async def _get_ping(self, request):
        return web.Response(text="Pong")


app = App()
app.run()

