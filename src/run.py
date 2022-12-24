import argparse
import json
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
    parser.add_argument('--db-access', type=str, help='File access', required=True)

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

    # Get db access credentials
    db_user = None
    db_pass = None
    db_name = None
    try:
        with open(args.db_access) as f:
            json_file = json.load(f)
            db_user = json_file['user']
            db_pass = json_file['password']
            db_name = json_file['name']
    except Exception as e:
        logger.error("Can't read the logging access file for database", e)
        sys.exit(-1)
    app = App(logger=logger, address="0.0.0.0", port=args.port, db_address=args.db_address,
              db_port=args.db_port, db_user=db_user, db_pass=db_pass, db_name=db_name)
    app.run()
    