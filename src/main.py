# main.py
from secrets import mqtt_pass, api_key
from utime import sleep
from umqttsimple import MQTTClient
import ubinascii
import sys
import urequests
from ujson import dumps, load
from machine import unique_id, reset, RTC
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
  local_now = t['unixtime'] + r['timezone'] - 3600  
  if (local_now >= int(r["sys"]["sunrise"]) and local_now < int(r["sys"]["sunset"])):
    green.state(True)
  else:
    yellow.state(True)

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
  if topic == 'City':
    global location
    location = message.decode("utf-8")

  if topic == 'Mode':
    global mode
    mode = message.decode("utf-8")
    
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
    if bleft.state() == 1:
      if mode.lower() == 'time':
        time()
      sleep(0.5)

    if bright.state() == 1:
      info()
      sleep(0.25)
  
  except OSError as e:
    restart_and_reconnect()

try:
  while True:
    loop()
except KeyboardInterrupt: 
    print('Programa Interrompido por Ctrl-C')
    sys.exit(0)
    
  
