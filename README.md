# <strong>Projeto Final de Eletrónica Digital e Microprocessadores</strong>  
<p>Este projeto consiste na utilização de 3 <i>Application Programming Interface</i>, nomeadamente, a API do <i>World Time</i>, a API do <i>OpenWeather</i> e a API do index ultravioleta que também pertence ao Open Weather.  
O intuito deste projeto é retirar os dados do formato <i>json</i> destes API de modo a podermos determinar diferentes modos consoante os parâmetros pré-selecionados.  
  Utilizaram-se 3 modos: Mode <strong>beach</strong>, Mode <strong>time</strong> e Mode <strong>City</strong>. Com base no Mode <strong>City</strong> podemos escolher a cidade pretendida e obter o tempo meteorológico nesse mesmo instante. O Mode <strong>time</strong> permite indicar se numa cidade selecionda já houve o nascer do sol ou o pôr do sol. Por último, existe o Mode <strong>beach</strong> que permite sabermos se uma ida à praia nesse dia é adequada ou não.</p>
                   
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
Ao abrir esse programa deverá colocar o mqtt_server = ‘edm2020.ddns.net’, mqtt_user = ‘edm’ e a mqtt_pass='M0squit0'. Deste modo já é possível se conectar ao broker.
De seguida, no Subscribe escreve-se Info no espaço a branco antes do Subscribe e depois carrega-se no botão localizado à frente no Subscribe.
Na zona do Publish, na parte maior representada a cor branca, carrega-se no botão direito do rato, carrega-se na zona que diz Add to Messages Clipboard, e escreve-se City. Repete-se o mesmo procedimento para o mode.  

Na página do Subscribe deve obter o seguinte:  

<img src="https://user-images.githubusercontent.com/65592500/85929077-b2626c80-b8a9-11ea-896a-4cfbfeca3056.png" width="700" height="400" />  

Na página do Publish deve obter o seguinte:  

<img src="https://user-images.githubusercontent.com/65592500/85924841-b0d67b80-b88c-11ea-889c-8f598ac8f8a9.png" width="700" height="400" />  

### <strong>Execução prática dos modos</strong>
#### <strong>Mode City</strong>
Para se visualizar a informação relativa à meteorologia numa determinada cidade tem que se selecionar mode, escrever City, escrever o nome da cidade (exemplo: Vila de Conde) no notepad e depois fazer Publish.  

<img src="https://user-images.githubusercontent.com/65592500/85932447-2ad62700-b8c4-11ea-865b-dd73b5c3d15b.png" width="700" height="400" />  

Seguidamente vai-se ao Subscribe, onde se escreve info e carrega-se no botão do Subscribe, fazendo com que a informação pretendida apareça nesse painel. Esse painel irá conter a localização, a velocidade do vento, a temperatura máxima a temperatura mínima e a pressão atmosférica.

<img src="https://user-images.githubusercontent.com/65592500/85932653-d2078e00-b8c5-11ea-9d7c-62ec174c0778.png" width="700" weight="400" />  

#### <strong>Mode time</strong>  
Este modo consiste na verificação do período do dia em que uma cidade se encontra, através da visualização do LED verde aceso quando o dia está entre o nascer do sol e o pôr do sol, e de um LED amarelo aceso caso a hora seja posterior ao pôr do sol e anterior ao nascer do novo dia, na placa ESP32.  

Depois de ter subscrito o bloco Info na parte do Subscribe e escolher a cidade pretendida da forma explicada anteriormente tem que se ir ao Publish, selecionar Mode, escrever Mode, no notepad escrever o time e depois carregar no botão do Publish.  

<img src="https://user-images.githubusercontent.com/65592500/85958339-c03cee00-b98c-11ea-8b44-238d1636b1a9.png" width="700" weight="400" />  

Na placa deverá obter o LED aceso consoante a altura do dia indicado.  
A título exemplificativo fica esta imagem da placa:  

<img src="https://user-images.githubusercontent.com/65592500/85958499-cf706b80-b98d-11ea-9d4b-d557227cea88.jpg" width="700" weight="400" />  

Por esta imagem percebe-se que no local selecionado é de dia.  

#### <strong>Mode beach</strong>
Este modo consiste na visualização de um LED, na placa ESP32, indicativo do estado de tempo de modo a viabilizar uma ida à praia ou não. Para isso, recorre-se aos parâmetros da temperatura atual, da velocidade do vento, do índice ultravioleta e a humidade relativa do ar. Cada parâmetro encontra-se quantificado no código main.py de 1 (estado pior) a 4 (condição ideal).  
<strong>Nota:</strong>Os intervalos escolhidos para os critérios tem por base a informação presente na bibliografia.  

A soma dos 4 parâmetros vai definir os estados do LED:  
* <strong>LED vermelho:</strong> 4<=count<7;
* <strong>LED amarelo no modo intermitente:</strong> 7<=count<10;
* <strong>LED amarelo:</strong> 10<=count<13
* <strong>LED verde:</strong> 13<=count<=16






