import argparse

def run():
    parser = argparse.ArgumentParser(
                    prog = 'TempSensorServer',
                    description = 'Server for temperature and humidity sensor with DHT22',
                    )