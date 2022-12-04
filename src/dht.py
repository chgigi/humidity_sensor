import Adafruit_DHT

MAX_SUCCESS_TRY = 8
MAX_TRY = 12

def get_temperature_from_dht22_local(pin, sensor_type, temperature_return=True, humidity_return=True):
    if sensor_type == 'DHT_11':
        sensor = Adafruit_DHT.DHT11
    if sensor_type == 'DHT_22':
        sensor = Adafruit_DHT.DHT22
    else:
        return None
    
    json_response = None
    try_succeed = 0
    _try = 0
    while try_succeed < MAX_SUCCESS_TRY and _try < MAX_TRY:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if temperature is not None and humidity is not None:
            json_response = {}
            if temperature_return:
                json_response['temperature'] = temperature
            if humidity_return:
                json_response['humidity'] = humidity
            try_succeed += 1
        _try += 1
    return json_response
    