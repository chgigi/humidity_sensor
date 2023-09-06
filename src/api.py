from aiohttp import web
import psycopg2
from psycopg2 import Error
from http import HTTPStatus
import json

from db import DataBase
from dht import get_temperature_from_dht22_local


class App(web.Application):
    def __init__(self, logger, address="0.0.0.0", port=3333, db_address="127.0.0.1", db_port=5432, db_user=None, db_pass=None, db_name=None):
        self._logger = logger
        self._address = address
        self._port = port
        self._app = web.Application()
        self._db = DataBase(db_user, db_pass, db_address, db_port, db_name, self._logger)

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
        self.router.add_route('GET', '/room/{room_id}/humidity', self._get_humidity)
        self.router.add_route('GET', '/room/{room_id}/temp_humi', self._get_temperature_and_humidity)

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

    async def _get_humidity(self, request):
        room_id = request.match_info['room_id']
        # With DHT22 in local
        pin = 2
        response = get_temperature_from_dht22_local(pin, 'DHT_22', temperature_return=False, humidity_return=True)
        if response is None:
            return web.HTTPServiceUnavailable()
        return web.HTTPOk(body=json.dumps(response), content_type="application/json")

    async def _get_temperature_and_humidity(self, request):
        room_id = request.match_info['room_id']
        # With DHT22 in local
        pin = 2
        response = get_temperature_from_dht22_local(pin, 'DHT_22', temperature_return=True, humidity_return=True)
        if response is None:
            return web.HTTPServiceUnavailable()
        return web.HTTPOk(body=json.dumps(response), content_type="application/json")
