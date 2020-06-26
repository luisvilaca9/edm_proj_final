# main.py
import sys
from secrets import mqtt_pass, api_key
from utime import sleep
from umqttsimple import MQTTClient
import ubinascii
import urequests
from ujson import dumps
from machine import unique_id, reset
from led import Led
from button import Button

bleft = Button(23)
bright = Button(18)
green = Led(19)
yellow = Led(22)
red = Led(21)

green.state(False)
yellow.state(False)
red.state(False)

location = 'Porto'
mode = 'None'
mqtt_server = 'edm2020.ddns.net'
client_id = ubinascii.hexlify(unique_id())

def leds_off():
    green.state(False)
    yellow.state(False)
    red.state(False)

def prettify(s):
    i = 0
    for c in s:
        if c in ['[', '{']:
            print(c)
            i += 2
            print(i*' ', end='')
        elif c in [']', '}']:
            print("")
            i -= 2
            print(i*' ', end='')
            print(c, end='')
        elif c == ',':
            print(c)
            print((i-1)*' ', end='')
        else:
            print(c, end='')
    print("")

def clock_api():
    url = "http://worldtimeapi.org/api/ip"
    t = urequests.get(url).json()
    # prettify(dumps(s))
    return t

def weather_api():
    try:
        global location     
        url = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}" .format(location, api_key)
        r = urequests.get(url).json()
        # prettify(dumps(r))
        return r
    except KeyError:
        print("City not found!")

def time():
    leds_off()
    r = weather_api()
    t = clock_api()
    utc_time = t['unixtime'] - t['dst_offset']   
    if (utc_time >= int(r["sys"]["sunrise"]) and utc_time < int(r["sys"]["sunset"])):
        green.state(True)
    else:
        yellow.state(True)

def beach():
    leds_off()
    r = weather_api()
    count = 0
    count += temp_count(r["main"]["temp"])
    count += wind_count(r["wind"]["speed"]) 
    count += uv_count(r["coord"]["lat"], r["coord"]["lon"])
    count += humidity_count(r["main"]["humidity"])

    if count >= 4 and count < 7:
        red.state(True)
    elif count >= 7 and count < 10:
        print("Press the right button to terminate intermitent mode")
        while True():
            yellow.blink(500)
            if bright.state() == 1:
                break
    elif count <= 10 and count < 13:
        yellow.state(True)
    else:
        green.state(True)

def temp_count(temp):
    if temp > 33 or temp < 18:
        count = 1
    elif temp >= 18 and temp <= 23:
        count = 2
    elif temp == 24 or temp >= 31 and temp <= 33:
        count = 3
    else:
        count = 4
    return count

def wind_count(speed):
    if speed >= 5.55:
        count = 1
    elif speed < 5.55 and speed >= 3.61:
        count = 2
    elif speed >= 1.94 and speed < 3.61:
        count = 3
    else:
        count = 4
    return count

def uv_count(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/uvi?appid={0}&lat={1}&lon={2}" .format(api_key, lat, lon)
    r = urequests.get(url).json()
    # prettify(dumps(r))
    value = r['value']

    if value >= 10:
        count = 1
    elif value >= 8 and value < 10:
        count = 2
    elif value >= 5 and value < 8:
        count = 3
    else:
        count = 4
    return count

def humidity_count(humidity):
    if humidity >= 80 and humidity <= 15:
        count = 1
    elif humidity > 15 and humidity <= 30 or humidity >= 70 and humidity < 80:
        count = 2
    elif humidity > 30 and humidity <= 40:
        count = 3
    else:
        count = 4
    return count

def info():
    r = weather_api()
    message = "Weather in location {0}, {1}:\n\
            Wind Speed: {2} m/s\n\
            Temperature: {3} C\n\
            Max Temp: {4} C\n\
            Min Temp: {5} C\n\
            Humidity: {6}%\n\
            Pressure: {7} hPa\n"\
            .format(r["name"], r["sys"]["country"], r["wind"]["speed"], r["main"]["temp"], r["main"]["temp_max"], r["main"]["temp_min"], r["main"]["humidity"], r["main"]["pressure"])
    client.publish('Info', message)

def sub_cb(topic, message):
    print("Received MQTT message: topic '{0}', message '{1}'".format(topic.decode("utf-8"), message.decode("utf-8")))
    topic = topic.decode("utf-8")
    global location
    if topic == 'City':
        location = message.decode("utf-8")
        print("Selected Location: {0}." .format(location))
        info()

    if topic == 'Mode':
        global mode
        mode = message.decode("utf-8")
        print("Active mode in {0}: {1}" .format(location, mode.upper()))
        if mode.lower() == 'time':
            time()
        if mode.lower() == 'beach':
            beach()
    
def connect_and_subscribe():
    mqtt_client = MQTTClient(client_id, mqtt_server, user='edm', password=mqtt_pass)
    mqtt_client.set_callback(sub_cb)
    mqtt_client.connect()
    mqtt_client.subscribe('City')
    mqtt_client.subscribe('Mode')
    print('Connected to {0} MQTT broker'.format(mqtt_server))
    return mqtt_client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

def loop():
    try:
        client.check_msg()
        global mode
        if bright.state() == 1:
            leds_off()
            print('Programa Interrompido por Botão Direito')
            sys.exit()

    except OSError:
        restart_and_reconnect()

try:
    while True:
        loop()
except KeyboardInterrupt: 
    leds_off()
    print('Programa Interrompido por Ctrl-C')
    sys.exit()
