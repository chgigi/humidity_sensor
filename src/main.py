import Adafruit_DHT as dht

humidite, temperature = dht.read_retry(dht.DHT22, 2)
if humidite is not None and temperature is not None:
    print('Température = {0:0.1f}*  Humidité = {1:0.1f}%'.format(temperature, humidite))
else:
    print('Échec de lecture du capteur !')