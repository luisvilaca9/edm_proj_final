# main.py
from secrets import mqtt_pass, api_key
from utime import sleep
from umqttsimple import MQTTClient
import ubinascii
import sys
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

mqtt_server = 'edm2020.ddns.net'
client_id = ubinascii.hexlify(unique_id())

def call_api():
  try:
    global location     
    url = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}" .format(location, api_key)
    r = urequests.get(url).json()
    message = "Weather in location {0}, {1}:\n\
              Wind Speed: {2} m/s\n\
              Temperature: {3} C\n\
              Max Temp: {4} C\n\
              Min Temp: {5} C\n\
              Humidity: {6}%\n\
              Pressure: {7} hPa\n"\
              .format(r["name"], r["sys"]["country"], r["wind"]["speed"], r["main"]["temp"], r["main"]["temp_max"], r["main"]["temp_min"], r["main"]["humidity"], r["main"]["pressure"])
    print(message)
    client.publish('Info', message)

  except KeyError:
    print("City not found!")

def sub_cb(topic, message):
    print("Received MQTT message: topic '{0}', message '{1}'".format(topic.decode("utf-8"), message.decode("utf-8")))
    topic = topic.decode("utf-8")
    if topic == 'City':
      global location
      location = message.decode("utf-8")

def connect_and_subscribe():
  mqtt_client = MQTTClient(client_id, mqtt_server, user='edm', password=mqtt_pass)
  mqtt_client.set_callback(sub_cb)
  mqtt_client.connect()
  mqtt_client.subscribe('City')
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
    if bleft.state() == 1:
      client.publish('bleft', 'Value = 1') 
      global location
      print('City:', location)
      sleep(0.25)

    if bright.state() == 1:
      call_api()
      sleep(0.25)
  except OSError as e:
    restart_and_reconnect()

try:
  while True:
    loop()
except KeyboardInterrupt: 
    print('Programa Interrompido por Ctrl-C')
    sys.exit(0)
    
  
