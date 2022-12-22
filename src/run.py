import argparse
import logging
import os
import sys

from api import App


def run():
    parser = argparse.ArgumentParser(
                    prog = 'TempSensorServer',
                    description = 'Server for temperature and humidity sensor with DHT22',
                    )
    parser.add_argument('--port', type=int, help='Port of the API', default=3333)
    parser.add_argument('--db-address', type=str, help='Address of the DataBase', default="127.0.0.1")
    parser.add_argument('--db-port', type=int, help='Port of the DataBase', default=5432)
    parser.add_argument('--logfile', type=str, help='log file to store logs', default="logs/humiditySensor.log")

    args = parser.parse_args()

    if not os.path.exists("./logs"):
        os.mkdir("./logs")

    logging.basicConfig(format='%(asctime)s - %(message)s', filename=args.logfile, encoding='utf-8', level=logging.DEBUG)
    logger = logging.getLogger()

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    app = App(logger=logger, address="0.0.0.0", port=args.port, db_address=args.db_address, db_port=args.db_port)
    app.run()
    