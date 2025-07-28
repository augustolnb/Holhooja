# Documentação do Projeto Holhooja (ESP32)

Esta documentação descreve o firmware do ESP32 para o projeto Holhooja, um sistema de automação residencial e monitoramento de ambiente.

## Visão Geral

O código do ESP32 é responsável por:

*   Conectar-se a uma rede Wi-Fi.
*   Conectar-se a um broker MQTT para comunicação com a aplicação de controle.
*   Ler dados de sensores de temperatura, umidade, luminosidade, qualidade do ar e presença.
*   Controlar um ar-condicionado via infravermelho (IR).
*   Controlar uma lâmpada e uma porta (relé).
*   Publicar os dados dos sensores em tópicos MQTT.
*   Subscrever-se a tópicos MQTT para receber comandos.

## Estrutura do Código

O firmware está dividido em dois arquivos principais:

*   `main.ino`: Contém a lógica principal do programa, incluindo a função `setup()` e `loop()`.
*   `holhooja.h`: Contém as definições de constantes, variáveis globais, e as funções auxiliares.

## Funcionalidades

### Conectividade

*   **Wi-Fi:** O ESP32 se conecta a uma rede Wi-Fi usando as credenciais definidas em `main.ino`.
*   **MQTT:** O ESP32 se conecta a um broker MQTT no endereço IP e porta definidos em `main.ino`.

### Sensores

*   **DHT11:** Lê a temperatura e a umidade do ambiente.
*   **LDR:** Mede a luminosidade do ambiente.
*   **MQ-135:** Detecta a presença de gases nocivos no ar.
*   **HC-SR602:** Detecta movimento no ambiente.
*   **SCT-013:** Mede o consumo de corrente do ar-condicionado.

### Atuadores

*   **Emissor IR:** Envia sinais infravermelhos para controlar o ar-condicionado (ligar/desligar, ajustar temperatura).
*   **Relé:** Controla o acionamento de uma lâmpada e de uma porta.

## Tópicos MQTT

### Tópicos de Subscrição (Comandos)

*   `/comando/esp32/AC`: Recebe comandos para o ar-condicionado ("on", "off", "up", "down", "left", "right").
*   `/comando/esp32/porta`: Recebe comandos para a porta ("porta").
*   `/comando/esp32/lampada`: Recebe comandos para a lâmpada.
*   `/esp32/verificarConexao`: Tópico para verificar a conexão do ESP32.
*   `/esp32/enviarComando`: Tópico para enviar comandos genéricos ao ESP32.

### Tópicos de Publicação (Sensores)

*   `/sensores/DHT`: Publica os dados de temperatura e umidade.
*   `/sensores/LDR`: Publica os dados de luminosidade.
*   `/sensores/SR602`: Publica o status de detecção de movimento.
*   `/sensores/SCT`: Publica os dados de consumo de corrente do ar-condicionado.
*   `/sensores/MQ135`: Publica os dados de qualidade do ar.

## Pinos Utilizados

| Pino | Componente          |
| :--- | :------------------ |
| 1    | MQ-135 (Analógico)  |
| 2    | MQ-135 (Digital)    |
| 10   | Receptor IR         |
| 15   | Relé                |
| 18   | LED (Teste)         |
| 19   | Sensor de Movimento |
| 20   | LDR                 |
| 21   | DHT11               |
| 40   | Emissor IR          |

## Funções Principais

### `setup()`

*   Inicializa a comunicação serial.
*   Configura os pinos dos sensores e atuadores.
*   Inicializa o receptor e emissor IR.
*   Conecta-se à rede Wi-Fi.
*   Conecta-se ao broker MQTT e subscreve-se aos tópicos de comando.
*   Configura o sensor de corrente.

### `loop()`

*   Mantém a conexão com o broker MQTT.
*   Verifica se há sinais IR recebidos.
*   Lê os dados dos sensores em intervalos de tempo definidos.
*   Publica os dados dos sensores nos respectivos tópicos MQTT.

### `callback(char* topic, byte* message, unsigned int length)`

*   Função chamada quando uma mensagem é recebida em um dos tópicos de subscrição.
*   Processa os comandos recebidos e aciona os atuadores correspondentes.
