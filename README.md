# <strong>Projeto Final de Eletrónica Digital e Microprocessadores</strong>  
<p>Este projeto consiste na utilização de 3 <i>Application Programming Interface</i>, nomeadamente, a API do <i>World Time</i>, a API do <i>OpenWeather</i> e a API do index ultravioleta que também pertence ao Open Weather.  
O intuito deste projeto é retirar os dados do formato <i>json</i> destes API's de forma a ser possível a determinação de diferentes modos consoante os parâmetros pré-selecionados.  
  Criaram-se para o efeito 2 modos: Mode <strong>Beach</strong>, Mode <strong>Time</strong>, e um tópico <strong>City</strong>. Em <strong>City</strong> podemos escolher a cidade pretendida e obter a informação metereológica nesse mesmo instante. O Mode <strong>Time</strong> permite indicar se numa cidade selecionada já ocorreu o nascer do sol ou o pôr do sol. Por último, existe o Mode <strong>Beach</strong> que permite saber se uma ida à praia nesse dia é adequada ou não.</p>
                   
### <strong>Pré-requesitos</strong>
Instalação do micropy no Visual Studio Code  
Instalação do broker Mosquitto  
Instalação de um programa que possa subscrever/publicar mensagens MQTT:
* Windows/Mac OSX/Linux [MQTT.fx](http://www.mqttfx.org/)
* Android [MQTT Dash](https://play.google.com/store/apps/details?id=net.routix.mqttdash&hl=pt_PT)
* IOS [MQTT Tool](https://apps.apple.com/us/app/mqttool/id1085976398)  

### <strong>Utilização geral do programa</strong>
Depois da instalação dos programas acima referidos, deve-se ir ao Visual Studio Code, selecionar View, Command Pallete, escrever Git: Clone, e colar o seguinte URL <https://github.com/luisvilaca9/edm_proj_final>. Posto isto, terá acesso a todos os códigos desenvolvidos ao longo do projeto.  

<strong>Nota:</strong> Antes de correr os programas deverá ter o cuidado de alterar o SSID e a password, no ficheiro Secrets.py, consoante a rede wi-fi que estiver a utilizar, bem como, selecionar a porta COM que deverá estar conetada à sua placa ESP32, no ficheiro pymakr.conf.

De seguida deve abrir o programa que pemite subscrever/publicar mensagens MQTT.  
Ao abrir esse programa deverá adicionar um novo servidor, colocando o mqtt_server = ‘edm2020.ddns.net’, mqtt_user = ‘edm’ e a mqtt_pass='M0squit0'. Deste modo já é possível a conexão ao broker.
De seguida, no Subscribe escreve-se Info no espaço a branco antes do Subscribe e depois carrega-se no botão localizado à frente no Subscribe.
Na zona do Publish, na parte maior representada a cor branca, carrega-se no botão direito do rato, carrega-se na zona que diz Add to Messages Clipboard, e escreve-se City. Repete-se o mesmo procedimento para o Mode.  

Na página do Subscribe deve obter o seguinte:  

<img src="https://user-images.githubusercontent.com/65592500/85929077-b2626c80-b8a9-11ea-896a-4cfbfeca3056.png" width="700" height="400" />  

Na página do Publish deve obter o seguinte:  

<img src="https://user-images.githubusercontent.com/65592500/85924841-b0d67b80-b88c-11ea-889c-8f598ac8f8a9.png" width="700" height="400" />  

### <strong>Execução prática do programa</strong>
#### <strong>City</strong>  
Para receber a informação meteorológica de um determinado local, deve-se inicialmente subscrever o bloco Info, carregar em City e na caixa de mensagem digitar o nome do local desejado. Posteriormente deve-se carregar no botão Publish.  

<img src="https://user-images.githubusercontent.com/65592500/86240494-4168d080-bb99-11ea-909d-a243466c5448.png" width="700" height="400" />

Seguidamente vai-se ao Subscribe, onde a informação climatérica do local pode ser visualizada em Info, no painel do broker. Esse painel irá conter a localização, a velocidade do vento, a temperatura máxima, a temperatura mínima e a pressão atmosférica.

<img src="https://user-images.githubusercontent.com/65592500/85932653-d2078e00-b8c5-11ea-9d7c-62ec174c0778.png" width="700" height="400" />  

#### <strong>Mode - Time</strong>  
Este modo consiste na verificação do período do dia em que uma cidade se encontra, através da visualização do LED verde aceso quando o dia está entre o nascer do sol e o pôr do sol, e de um LED amarelo aceso caso a hora seja posterior ao pôr do sol e anterior ao nascer do novo dia, na placa ESP32.  

Depois de ter subscrito o bloco Info na parte do Subscribe e escolher a cidade pretendida da forma explicada anteriormente, tem que se ir ao Publish, selecionar Mode, no notepad escrever 'time' (não sensível a capitalização) e depois carregar em Publish.  

<img src="https://user-images.githubusercontent.com/65592500/85958339-c03cee00-b98c-11ea-8b44-238d1636b1a9.png" width="700" height="400" />  

Na placa deverá obter o LED aceso consoante a altura do dia indicado.  
A título exemplificativo fica esta imagem da placa:  

<img src="https://user-images.githubusercontent.com/65592500/85958499-cf706b80-b98d-11ea-9d4b-d557227cea88.jpg" width="700" height="400" />  

Por esta imagem percebe-se que no local selecionado é de dia.  

#### <strong>Mode - Beach</strong>
Este modo consiste na visualização de um LED, na placa ESP32, indicativo do estado de tempo de modo a viabilizar uma ida à praia. Para isso, recorre-se aos parâmetros da temperatura atual, da velocidade do vento, do índice ultravioleta e a humidade relativa do ar. Cada parâmetro encontra-se quantificado no código main.py de 1 (pior estado) a 4 (condição ideal).  

<strong>Nota:</strong> Os intervalos escolhidos para os critérios tem por base a informação presente na bibliografia.  

A soma dos 4 parâmetros vai definir os estados do LED:  
* <strong>LED vermelho: </strong> 4<=count<7;
* <strong>LED amarelo no modo intermitente: </strong> 7<=count<10;
* <strong>LED amarelo: </strong> 10<=count<13
* <strong>LED verde: </strong> 13<=count<=16  

<strong>Nota: </strong>De referir que para sair do modo amarelo intermitente é necessário carregar no botão esquerdo do circuito.  

Primeiramente, para se visualizar o LED aceso na placa, no modo 'Beach', tem de se subscrever o bloco Info e escolher a cidade pretendida da forma explicada anteriormente.  
Seguidamente, ir ao Publish, carregar em Mode, na caixa de mensagem escrever 'Beach' (não sensível a capitalização) e depois carregar em Publish.  

No Visual Studio Code e na placa deve aparecer algo semelhante, respetivamente, a estas imagens:  

<img src="https://user-images.githubusercontent.com/65592500/86066281-a7563a80-ba69-11ea-81de-1517cb72c12e.png" width="400" height="230" /> <img src="https://user-images.githubusercontent.com/65592500/86067561-0c5f5f80-ba6d-11ea-91dd-99cfd61a4a50.jpg" width="400" height="230" />  

Por último, para terminar o funcionamento do código global é necessário carregar no botão direito do circuito ligado à placa ESP32 que irá, deste modo, sair do programa.


### <strong>Conclusão</strong>  
<p>Este projeto permitiu consolidar as bases do Micropy e aprender a utilizar a funcionalidade Wi-fi da placa de modo a poder interagir com diversas API's.  Também permitiu tirar partido dos LEDs e botões do circuito ligados à placa e das API's de modo a ser possível a criação deste código que fornece uma panóplia de informação ao seu utilizador, consoante o efeito pretendido. O código descrito é versátil podendo cada utilizador futuro fazer alterações de acordo com o seu gosto pessoal (nomeadamente no Mode 'Beach'). Em suma, os objetivos deste trabalho foram cumpridos.</p>


### <strong>Autores</strong>  
André João Fernandes Aguiar  
Luís Miguel de Sá Vilaça  
### <strong>Bibliografia</strong>  
[Link para o Ipma](https://www.ipma.pt/pt/educativa/faq/meteorologia/previsao/faqdetail.html?f=/pt/educativa/faq/meteorologia/previsao/faq_0032.html)  
[link para a API do índice ultravioleta](https://openweathermap.org/api/uvi#current)  
[link para a API do OpenWeather](https://openweathermap.org/api/one-call-api?gclid=CjwKCAjwxev3BRBBEiwAiB_PWNLlnx1aMDdf5oOwvEuOlTt6Lu5DAMMu-sp7PMyc9PzAAbbG4qwSWhoCRKQQAvD_BwE)  
[link para a API do World Time](http://worldtimeapi.org/)  
[link realacionado com a humidade relativa](https://pt.wikipedia.org/wiki/Umidade_relativa)









