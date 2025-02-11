# <strong>Projeto Final de Eletrónica Digital e Microprocessadores</strong>  
<p>Este projeto consiste na utilização de 3 <i>Application Programming Interface</i>, nomeadamente, a API do <i>World Time</i>, a API do <i>OpenWeather</i> e a API do index ultravioleta que também pertence ao Open Weather.  
O intuito deste projeto é retirar os dados do formato <i>json</i> destes API's de forma a ser possível a determinação de diferentes modos consoante os parâmetros pré-selecionados.  
  Criaram-se para o efeito 2 modos: Mode <strong>Beach</strong>, Mode <strong>Time</strong>, e um tópico <strong>City</strong>. Em <strong>City</strong> podemos escolher a cidade pretendida e obter a informação metereológica nesse mesmo instante. O Mode <strong>Time</strong> permite indicar se numa cidade selecionada já ocorreu o nascer do sol ou o pôr do sol. Por último, existe o Mode <strong>Beach</strong> que permite saber se uma ida à praia nesse dia é adequada ou não.</p>
                   
### <strong>Pré-requesitos</strong>
* Microcontrolador ESP32, 2 botões e 3 LEDs (Verde, Amarelo, Vermelho);
* Dois condensadores de 100 nF e seis resistências de 1 k<span>&#8486;</span>;
* Instalação do micropy no Visual Studio Code;  
* Instalação do broker Mosquitto;  
* Instalação de um programa que possa subscrever/publicar mensagens MQTT:
  * Windows/Mac OSX/Linux [MQTT.fx](http://www.mqttfx.org/)
  * Android [MQTT Dash](https://play.google.com/store/apps/details?id=net.routix.mqttdash&hl=pt_PT)
  * IOS [MQTT Tool](https://apps.apple.com/us/app/mqttool/id1085976398)  

### <strong>Esquema do Hardware</strong>
Para a execução deste programa foi utilizado o microcontrolador ESP32, cujo esquema pode ser visualizado na imagem seguinte:

<p align="center"> 
  <img src="https://paginas.fe.up.pt/~hsm/wp-content/uploads/2020/04/ESP32-Pico-Kit-624x252.png" width="400" height="180" />
</p>  

Qualquer controlador que seja semelhante ao ESP32 pode ser utilizado para correr este programa, contudo há que ter a devida atenção de mudar no código a enumeração dos pinos dos LEDs e botões caso estas ligações sejam alteradas. No desenvolvimento deste trabalho, as ligações dos LEDs e botões aos pinos da ESP32 foram realizadas consoante o seguinte esquema:
<p align="center">
  <img src="https://paginas.fe.up.pt/~hsm/wp-content/uploads/2018/04/modulo-624x191.jpg" width="400" height="190" />   <img src="https://paginas.fe.up.pt/~hsm/wp-content/uploads/2020/04/ledButBoardPins-624x398.png" width="400" height="190" />
</p>

Os LEDs vermelho, amarelo e verde serão ligados respetivamente aos pinos 21, 22 e 19 da placa ESP32. Cada LED é ativo a nível alto devido a uma diferença de tensão que irá provocar uma corrente que atravessa o LED. Cada LED está protegido por uma resistência de 1 k<span>&#8486;</span>  de modo a não queimar.  
O botão esquerdo será ligado ao pino 23 e o direito ao pino 18. Os botões são ativos ao nível baixo, ou seja, quando o botão é premido, o pino da placa ESP32 correspondente assume o valor 0. Os botões estão também protegidos por resistências de 1 k<span>&#8486;</span>, sendo que para cada um deles existe um condensador de 100 nF, em paralelo com a resistência, funcionando como mecanismo de anti-bouncing.

### <strong>Utilização geral do programa</strong>
Depois da instalação dos programas acima referidos, deve-se ir ao Visual Studio Code, selecionar View, Command Pallete, escrever Git: Clone, e colar o seguinte URL <https://github.com/luisvilaca9/edm_proj_final>. Posto isto, terá acesso a todos os códigos desenvolvidos ao longo do projeto.  

<strong>Nota:</strong> Antes de correr os programas deverá ter o cuidado de alterar o SSID e a password, no ficheiro Secrets.py, consoante a rede wi-fi que estiver a utilizar, bem como, selecionar a porta COM que deverá estar conetada à sua placa ESP32, no ficheiro pymakr.conf.

De seguida deve abrir o programa que pemite subscrever/publicar mensagens MQTT.  
Ao abrir esse programa deverá adicionar um novo servidor, colocando o mqtt_server = ‘edm2020.ddns.net’, mqtt_user = ‘edm’ e a mqtt_pass='M0squit0'. Deste modo já é possível a conexão ao broker.
De seguida, no Subscribe escreve-se Info no espaço a branco antes do Subscribe e depois carrega-se no botão localizado à frente no Subscribe.
Na zona do Publish, na parte maior representada a cor branca, carrega-se no botão direito do rato, carrega-se na zona que diz Add to Messages Clipboard, e escreve-se City. Repete-se o mesmo procedimento para o Mode.  

Na página do Subscribe deve-se obter o seguinte:  

<p align="center">
  <img src="https://user-images.githubusercontent.com/65592500/85929077-b2626c80-b8a9-11ea-896a-4cfbfeca3056.png" width="700" height="400" />
</p>

Na página do Publish deve-se obter o seguinte:  

<p align="center">
  <img src="https://user-images.githubusercontent.com/65592500/85924841-b0d67b80-b88c-11ea-889c-8f598ac8f8a9.png" width="700" height="400" />
</p>

### <strong>Execução prática do programa</strong>
#### <strong>City</strong>  
Para receber a informação meteorológica de um determinado local, deve-se inicialmente subscrever o bloco Info, carregar em City e na caixa de mensagem digitar o nome do local desejado. Posteriormente deve-se carregar em Publish.  

<p align="center">
  <img src="https://user-images.githubusercontent.com/65592500/86240494-4168d080-bb99-11ea-909d-a243466c5448.png" width="700" height="400" />
</p>

Seguidamente vai-se ao separador Subscribe, onde a informação climatérica do local pode ser visualizada no tópico Info. Esse painel irá conter a velocidade do vento, a temperatura máxima, a temperatura mínima e a pressão atmosférica para a localização selecionada.

<p align="center">
  <img src="https://user-images.githubusercontent.com/65592500/85932653-d2078e00-b8c5-11ea-9d7c-62ec174c0778.png" width="700" height="400" />
</p>

 

#### <strong>Mode - Time</strong>  
Este modo consiste na verificação do período do dia em que uma cidade se encontra, através da visualização do LED verde aceso quando o dia está entre o nascer do sol e o pôr do sol, e de um LED amarelo aceso caso a hora seja posterior ao pôr do sol e anterior ao nascer do novo dia.  

Depois de ter subscrito o bloco Info na parte do Subscribe e escolher a cidade pretendida da forma explicada anteriormente, tem que se ir ao Publish, selecionar Mode, no notepad escrever 'time' (não sensível a capitalização) e depois carregar em Publish.  

<p align="center">
  <img src="https://user-images.githubusercontent.com/65592500/85958339-c03cee00-b98c-11ea-8b44-238d1636b1a9.png" width="700" height="400" />
</p>

Na placa deverá obter o LED aceso consoante a altura do dia indicado.  
A título exemplificativo fica esta imagem da placa:  

<p align="center">
  <img src="https://user-images.githubusercontent.com/65592500/85958499-cf706b80-b98d-11ea-9d4b-d557227cea88.jpg" width="700" height="400" />
</p>

Por esta imagem percebe-se que no local selecionado é de dia.  

O modo <strong>Time</strong> pode ser útil no caso de haver membros familiares noutro fuso horário, e com um simples clique no Broker, fica-se a saber que altura do dia é nessa zona, sendo possível avaliar se é a altura ideal para estabelecer algum tipo de ligação. Também pode ser útil no caso de estar longe de casa e querer que a luz acenda para iluminar a entrada de casa (através da sincronização da placa com o sistema de iluminação inteligente da habitação).

#### <strong>Mode - Beach</strong>
Este modo consiste na visualização de um LED, na placa ESP32, indicativo do estado de tempo de modo a viabilizar uma ida à praia. Para isso, recorre-se aos parâmetros da temperatura atual, da velocidade do vento, do índice ultravioleta e a humidade relativa do ar. Cada parâmetro encontra-se quantificado no código main.py de 1 (pior estado) a 4 (condição ideal).  

<strong>Nota:</strong> Os intervalos escolhidos para os critérios tem por base a informação presente na bibliografia.  

A soma dos 4 parâmetros vai definir os estados do LED:  
* <strong>LED vermelho: </strong> 4<=count<8;
* <strong>LED amarelo no modo intermitente: </strong> 8<=count<11;
* <strong>LED amarelo: </strong> 11<=count<14;
* <strong>LED verde: </strong> 14<=count<=16.  

<strong>Nota: </strong>De referir que para sair do modo amarelo intermitente é necessário carregar no botão esquerdo do circuito.  

Primeiramente, para se visualizar o LED aceso na placa, no modo <strong>Beach</strong>, tem de se subscrever o bloco Info e escolher a cidade pretendida da forma explicada anteriormente.  
Seguidamente, ir ao separador Publish, carregar em Mode, na caixa de mensagem escrever 'Beach' (não sensível a capitalização) e depois carregar em Publish.  

No Visual Studio Code e na placa deve aparecer algo semelhante, respetivamente, a estas imagens:  

<p align="center">
  <img src="https://user-images.githubusercontent.com/65592500/86515010-04f1da80-be0e-11ea-9512-f4dfe8613327.png" width="400" height="230" /> <img src="https://user-images.githubusercontent.com/65592500/86067561-0c5f5f80-ba6d-11ea-91dd-99cfd61a4a50.jpg" width="400" height="230" />
</p>

Por último, para encerrar o programa é necessário carregar no botão direito do circuito ligado à placa ESP32. O encerramento do programa também pode ser feito através de Ctrl-C no Visual Studio Code.


### <strong>Conclusão</strong>  
<p>Este projeto permitiu consolidar as bases do Micropy e aprender a utilizar a funcionalidade Wi-fi da placa de modo a poder interagir com diversas API's.  Também permitiu tirar partido dos LEDs e botões do circuito ligados à placa e das API's de modo a ser possível a criação deste código que fornece uma panóplia de informação ao seu utilizador, consoante o efeito pretendido. O código descrito é versátil podendo cada utilizador futuro fazer alterações de acordo com o seu gosto pessoal (nomeadamente no Mode 'Beach'). Em suma, os objetivos deste trabalho foram cumpridos.</p>


### <strong>Autores</strong>  
André João Fernandes Aguiar  
Luís Miguel de Sá Vilaça  
### <strong>Bibliografia</strong>  
[Site do Ipma](https://www.ipma.pt/pt/educativa/faq/meteorologia/previsao/faqdetail.html?f=/pt/educativa/faq/meteorologia/previsao/faq_0032.html)  
[API do índice ultravioleta](https://openweathermap.org/api/uvi#current)  
[API do OpenWeather](https://openweathermap.org/api/one-call-api?gclid=CjwKCAjwxev3BRBBEiwAiB_PWNLlnx1aMDdf5oOwvEuOlTt6Lu5DAMMu-sp7PMyc9PzAAbbG4qwSWhoCRKQQAvD_BwE)  
[API do World Time](http://worldtimeapi.org/)  
[Link informativo acerca da humidade relativa](https://pt.wikipedia.org/wiki/Umidade_relativa)  
[Link relativo ao índice ultravioleta](https://pt.wikipedia.org/wiki/Índice_ultravioleta)  
[Apontamentos de Eletrónica Digital e Microprocessadores](https://paginas.fe.up.pt/~hsm/docencia/edm/edm-201920/gpio/)









