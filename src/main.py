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

# Associação dos botões e LEDs aos respetivos Pins. Utilização de classes importadas dos ficheiros button.py e led.py
bleft = Button(23)
bright = Button(18)
green = Led(19)
yellow = Led(22)
red = Led(21)

# No início do programa os LEDs devem estar apagados
green.state(False)
yellow.state(False)
red.state(False)

location = 'Porto' # Localização padrão
mode = 'None' # Modo padrão (modos time e beach disponíveis)
mqtt_server = 'edm2020.ddns.net' # Servidor Broker
client_id = ubinascii.hexlify(unique_id()) # ID Cliente Broker

def leds_off():
    """Função para desligar todos os LEDs"""
    green.state(False)
    yellow.state(False)
    red.state(False)

def prettify(s):
    """Função para visualizar ficheiros JSON provenientes do API"""
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
    """API para obter relógio mundial consoante IP"""
    url = "http://worldtimeapi.org/api/ip"
    t = urequests.get(url).json() # Obter ficheiro JSON do API
    # prettify(dumps(s))
    return t

def weather_api():
    """API para obter informações sobre o tempo na localização selecionada"""
    global location # Constante global de location pois irá ser utilizada em várias funções      
    url = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}" .format(location, api_key) # URL para obter informação do tempo consoante a localização
    r = urequests.get(url).json() # Obter ficheiro JSON do API
    # prettify(dumps(r))
    return r
    

def time():
    """Função do modo Time, liga o LED verde ou amarelo consoante seja de dia ou de noite (nascer do sol, pôr-do-sol)"""
    leds_off() # Desligar LEDs para não existir interferência visual com funções previamente utilizadas
    r = weather_api() # Buscar informação do tempo na localidade selecionada
    t = clock_api() # Hora consoante o IP da rede
    utc_time = t['unixtime'] - t['dst_offset'] # Obter o tempo em UTC de modo a calcular nascer e pôr-do-sol, utilizando offset horário do IP em relação ao UTC.  
    if (utc_time >= int(r["sys"]["sunrise"]) and utc_time < int(r["sys"]["sunset"])): # Entre sunrise e sunset, no local selecionado é de dia
        green.state(True) # Ligar LED Verde
    else: # Caso seja de noite
        yellow.state(True) # Ligar LED amarelo

def beach():
    """Modo Beach que avalia as condições para um dia de praia na localidade selecionada através de um sistema de pontos"""
    leds_off()
    r = weather_api() # Informação sobre o tempo 
    count = 0 # Inicializar pontuação em 0
    # Avaliar em funções distintas as condições de: temperatura, vento, índice de UVs e humidade
    count += temp_count(r["main"]["temp"])
    count += wind_count(r["wind"]["speed"]) 
    count += uv_count(r["coord"]["lat"], r["coord"]["lon"])
    count += humidity_count(r["main"]["humidity"])

    # Consoante a pontuação das várias variáveis mencionadas anteriormente, é acendido o respetivo LED
    # Numa escala de melhores para piores condições, acender: LED Verde, LED Amarelo, LED Amarelo em modo intermitente, LED Vermelho
    if count >= 4 and count < 7:
        print("Red Alert!", "Total Score = {0}" .format(count))
        red.state(True)
    elif count >= 7 and count < 10:
        print("Not recommended.", "Press the left button to terminate intermitent mode.", "Total Score =", count) # Mensagem explicativa para terminar o modo amarelo intermitente
        while True: # Loop para modo amarelo intermitente
            yellow.blink(500) # Função da classe LED para o modo intermitente. Como argumento assume o periodo em ms para ligar e desligar o LED.
            if bleft.state() == 1: # Premir botão esquerdo para terminar modo intermitente
                yellow.state(False)  # Desliga LED Amarelo
                break
                
    elif count >= 10 and count < 13:
        print("Stable weather!", "Total score =", count)      
        yellow.state(True)
    else:
        print("Ideal weather!", "Total Score =", count)
        green.state(True)

def temp_count(temp):
    """Avalia temperatura ideal para um dia de praia, de 1 a 4 pontos"""
    if temp > 33 or temp < 18:
        count = 1
    elif temp >= 18 and temp <= 23:
        count = 2
    elif temp == 24 or temp >= 31 and temp <= 33:
        count = 3
    else:
        count = 4
    print("Temperature Score = {0}, Value = {1} \u00b0C" .format(count, temp))
    return count

def wind_count(speed):
    """Avalia velocidade do vento ideal para um dia de praia, de 1 a 4 pontos"""
    if speed >= 5.55:
        count = 1
    elif speed < 5.55 and speed >= 3.61:
        count = 2
    elif speed >= 1.94 and speed < 3.61:
        count = 3
    else:
        count = 4
    print("Wind Speed Score = {0}, Value = {1} m/s" .format(count, speed))    
    return count

def uv_count(lat, lon):
    """Avaliação do índice de UVs para um dia de praia. Utiliza um API distinto consoante a latitude e longitude do local selecionado, 
    visto que esta informação não se encontrar no API previamente utilizado para avaliação do clima."""
    url = "http://api.openweathermap.org/data/2.5/uvi?appid={0}&lat={1}&lon={2}" .format(api_key, lat, lon) # URL do API
    r = urequests.get(url).json() # Ficheiro JSON do API mencionado anteriormente
    # prettify(dumps(r))
    value = r['value'] # Valor do índice de UVs incidente no local selecionado
    if value >= 10:
        count = 1
    elif value >= 8 and value < 10:
        count = 2
    elif value >= 5 and value < 8:
        count = 3
    else:
        count = 4
    print("UV Index Score = {0}, Value = {1}" .format(count, value))
    return count

def humidity_count(humidity):
    """Função que avalia as condições de humidade para um dia de praia e retorna uma pontuação entre 1 e 4"""
    if humidity >= 80 and humidity <= 15:
        count = 1
    elif humidity > 15 and humidity <= 30 or humidity >= 70 and humidity < 80:
        count = 2
    elif humidity > 30 and humidity <= 40:
        count = 3
    else:
        count = 4
    print("Relative Humidity Score = {0}, Value = {1}%" .format(count, humidity))
    return count

def info():
    """Função que publica no broker a informação climatérica do local escolhido previamente"""
    r = weather_api() # API do clima de modo a obter as informações necessárias
    # Formatação de uma mensagem com toda a informação climatérica do local
    message = "Weather in location {0}, {1}:\n\
            Wind Speed: {2} m/s\n\
            Temperature: {3} C\n\
            Max Temp: {4} C\n\
            Min Temp: {5} C\n\
            Humidity: {6} %\n\
            Pressure: {7} hPa\n"\
            .format(r["name"], r["sys"]["country"], r["wind"]["speed"], r["main"]["temp"], r["main"]["temp_max"], r["main"]["temp_min"], r["main"]["humidity"], r["main"]["pressure"])
    client.publish('Info', message) # Publicar no broker a mensagem com tópico Info
        
def sub_cb(topic, message):
    """Função para o ESP receber informação a tópicos subscritos no broker"""
    try:
        print("Received MQTT message: topic '{0}', message '{1}'.".format(topic.decode("utf-8"), message.decode("utf-8"))) #Mesnagem para confirmar recepção da informação do broker
        topic = topic.decode("utf-8") # Descodificar nome do tópico para utf-8 pois a informação do broker vem em binário
        global location
        if topic == 'City': # Permite selecionar o local desejado
            location = message.decode("utf-8")
            print("Selected Location: {0}." .format(location)) # Mensagem que mostra o local selecionado através do broker
            info() # Execução da função info para publicar informação climatérica no broker
            print("See weather info of {0} on the Broker Client." .format(location)) # Mesnagem a avisar que a informação do tempo sobre o local selecionado pode ser vista no broker
            
        if topic == 'Mode': # Seleção do modo time ou beach
            global mode
            mode = message.decode("utf-8") # Descodificação da mensagem proveniente do broker que indica o modo escolhido
            print("Active mode in {0}: {1}" .format(location, mode.upper())) # Confirmação em mensagem no terminal que o modo foi escolhido para certo local
            if mode.lower() == 'time':
                time()
            if mode.lower() == 'beach':
                beach()
                
    except UnicodeError:
        print("Invalid Location. Remove special characters.")

    except KeyError:
        print("Location not found. Select another location.")
    
def connect_and_subscribe():
    """Função para ligar placa ESP ao broker e subscrever a tópicos no broker para receber informação do mesmo"""
    mqtt_client = MQTTClient(client_id, mqtt_server, user='edm', password=mqtt_pass) # Info cliente MQTT
    mqtt_client.set_callback(sub_cb) # Callback do MQTT para obter informação do broker
    mqtt_client.connect() # Ligar ESP ao cliente MQTT
    mqtt_client.subscribe('City') # Subscrição do tópico City
    mqtt_client.subscribe('Mode') # Subscrição do tópico Mode
    print('Connected to {0} MQTT broker'.format(mqtt_server)) # Mensagem de ligação ao broker
    return mqtt_client

def restart_and_reconnect():
    """Função para reconectar a placa ESP ao broker caso haja falha na ligação"""
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    reset()

# Iniciar ligação do ESP ao broker, caso não tenha sucesso -> restart e reconnect
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

def loop():
    """Main loop para correr o programa"""
    try:
        client.check_msg() # Cliente ESP sempre a verificar se recebe mensagens do broker 
        if bright.state() == 1: # Botão direito termina programa
            leds_off() # Desligar LEDs
            print('Program interrupted by Right Button')
            sys.exit()

    except OSError:
        restart_and_reconnect()

try:
    while True:
        loop()
except KeyboardInterrupt: # Interrupção do programa através de Ctrl-C
    leds_off() # Desligar LEDs
    print('Program Interrupted by Ctrl-C')
    sys.exit()
