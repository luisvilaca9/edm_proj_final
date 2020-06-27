# **Projeto Final de Eletrónica Digital e Microprocessadores**  
<p>Este projeto consiste na utilização de 3 <i>Application Programming Interface</i>, nomeadamente, a API do <i>World Time</i>, a API do <i>OpenWeather</i> e a API do index ultravioleta que também pertence ao Open Weather.  
O intuito deste projeto é retirar os dados do formato <i>json</i> destes API de modo a podermos determinar diferentes modos consoante os parâmetros pré-selecionados.  
Utilizaram-se 3 modos: mode beach, mode time e mode City. Com base no mode City podemos escolher a cidade pretendida e obter o tempo meteorológico nesse mesmo instante. O mode Time permite indicar se numa cidade selecionda já houve o nascer do sol ou o pôr do sol. Por último existe o mode beach que permite sabermos se uma ida à praia nesse dia é adequado ou não.</p>
                   
### Pré-requesitos
Instalação do micropy no Visual Studio Code
Instalação do broker Mosquitto  
Instalação de um programa que possa subscrever/publicar mensagens MQTT:
* Windows/Mac OSX/Linux [MQTT.fx](http://www.mqttfx.org/)
* Android [MQTT Dash](https://play.google.com/store/apps/details?id=net.routix.mqttdash&hl=pt_PT)
* IOS [MQTT Tool](https://apps.apple.com/us/app/mqttool/id1085976398)  Ter uma placa esp32 com  ligação a 3 leds e 2 botões
