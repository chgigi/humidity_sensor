from aiohttp import web
import psycopg2
from psycopg2 import Error
from http import HTTPStatus
import json

from db import DataBase
from dht import get_temperature_from_dht22_local

DB_USER = "chgigi"
DB_PASS = "dbaccess12345"
DB_NAME = "homeserver"


class App(web.Application):
    def __init__(self, logger, address="0.0.0.0", port=3333, db_address="127.0.0.1", db_port=5432):
        self._logger = logger
        self._address = address
        self._port = port
        self._app = web.Application()
        self._db = DataBase(DB_USER, DB_PASS, db_address, db_port, DB_NAME, self._logger)

        self._logger.info(f"configure api with address: http://{self._address}:{self._port}")
        self._logger.info(f"connect to DataBase at address: {db_address}:{db_port}")

        # Try a connection
        if not self._db.connect():
            self._logger.error("Check the DataBase conneciton, exit of API")
            exit(-1)
        
        self._logger.info(f"Successfully connected to DataBase: {db_address}:{db_port}")
        super().__init__()

        self.router.add_route('GET', '/ping', self._get_ping)
        self.router.add_route('POST', '/room', self._add_new_room)
        self.router.add_route('GET', '/room/{room_id}/temperature', self._get_temperature)

    def run(self):
        web.run_app(self, host=self._address, port=self._port)
        
    async def _get_ping(self, request):
        return web.Response(text="Pong")

    async def _add_new_room(self, request):
        # TBD
        return web.Response(text="Not implemented yet")

    async def _get_temperature(self, request):
        room_id = request.match_info['room_id']
        # With DHT22 in local
        pin = 2
        response = get_temperature_from_dht22_local(pin, 'DHT_22', temperature_return=True, humidity_return=False)
        if response is None:
            return web.HTTPServiceUnavailable()
        return web.HTTPOk(body=json.dumps(response), content_type="application/json")