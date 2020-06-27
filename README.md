# <strong>Projeto Final de Eletrónica Digital e Microprocessadores</strong>  
<p>Este projeto consiste na utilização de 3 <i>Application Programming Interface</i>, nomeadamente, a API do <i>World Time</i>, a API do <i>OpenWeather</i> e a API do index ultravioleta que também pertence ao Open Weather.  
O intuito deste projeto é retirar os dados do formato <i>json</i> destes API de modo a podermos determinar diferentes modos consoante os parâmetros pré-selecionados.  
  Utilizaram-se 3 modos: mode <strong>beach</strong>, mode <strong>time</strong> e mode <strong>City</strong>. Com base no mode <strong>City</strong> podemos escolher a cidade pretendida e obter o tempo meteorológico nesse mesmo instante. O mode <strong>time</strong> permite indicar se numa cidade selecionda já houve o nascer do sol ou o pôr do sol. Por último existe o mode <strong>beach</strong> que permite sabermos se uma ida à praia nesse dia é adequada ou não.</p>
                   
### <strong>Pré-requesitos</strong>
Instalação do micropy no Visual Studio Code  
Instalação do broker Mosquitto  
Instalação de um programa que possa subscrever/publicar mensagens MQTT:
* Windows/Mac OSX/Linux [MQTT.fx](http://www.mqttfx.org/)
* Android [MQTT Dash](https://play.google.com/store/apps/details?id=net.routix.mqttdash&hl=pt_PT)
* IOS [MQTT Tool](https://apps.apple.com/us/app/mqttool/id1085976398)  

### <strong>Utilização geral do programa</strong>
Depois da instalação dos programas referidos em cima, deve-se ir ao Visual Studio Code, selecionar View, Command Pallete, escrever Git: Clone, e colar o seguinte URL <https://github.com/luisvilaca9/edm_proj_final>. Posto isto, deverá ter acesso a todos os códigos desenvolvidos ao longo do projeto.  
<strong>Nota:</strong> Antes de correr os programas deverá ter o cuidado de alterar o SSID e a password, no ficheiro Secrets.py, consoante a rede wi-fi que estiver a utilizar e ter ainda o cuidado de selecionar a porta COM adequada a qual a sua placa ESP32 estará conetada, no ficheiro pymakr.conf.

De seguida deve abrir o programa que pemite subscrever/publicar mensagens MQTT.  
Ao abrir esse programa deverá colocar o mqtt_server = ‘edm2020.ddns.net’, mqtt_user = ‘edm’ e a mqtt_pass='M0squit0'. Deste modo já é possível se conetar ao broker.
De seguida, no Subscribe escreve-se Info no espaço a branco antes do Subscribe e depois carrega-se no botão localizado à frente no Subscribe.
Na zona do Publish, na parte maior representada a cor branca, carrega-se no botão direito do rato, carrega-se na zona que diz Add to Messages Clipboard, e escreve-se City. Repete-se o mesmo procedimento para o mode.  

Na página do Subscribe deve obter o seguinte:  

<img src="https://user-images.githubusercontent.com/65592500/85929077-b2626c80-b8a9-11ea-896a-4cfbfeca3056.png" width="700" height="400" />  

Na página do Publish deve obter o seguinte:  

<img src="https://user-images.githubusercontent.com/65592500/85924841-b0d67b80-b88c-11ea-889c-8f598ac8f8a9.png" width="700" height="400" />  

### <strong>Execução prática dos modos</strong>
#### <strong>mode City</strong>
Para se visualizar a informação relativa à meteorologia numa determinada cidade tem que se selecional City, escrever City, escrever o nome da cidade no notepad e depois fazer Publish.
Seguidamente vai-se ao Subscribe, onde se escreve info e carrega-se no botão do Subscribe, fazendo com que a informação pretendida apareça nesse painel.
Agora será mostrado um exemplo do procedimento a seguir.  


