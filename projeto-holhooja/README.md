# Documentação Geral do Projeto Holhooja

## 1. Introdução

O Projeto Holhooja é um sistema de Internet das Coisas (IoT) projetado para o monitoramento e controle de ambientes. A solução combina hardware embarcado (ESP32) para coleta de dados e atuação, uma aplicação web (Flask) como interface de usuário e o protocolo MQTT para comunicação em tempo real entre os componentes.

O objetivo principal é fornecer uma plataforma centralizada para visualizar dados de sensores (como temperatura, umidade, luminosidade, movimento e qualidade do ar) e controlar dispositivos remotamente (como ar-condicionado e iluminação).

**Tecnologias Utilizadas:**

*   **Hardware:** ESP32
*   **Firmware:** C/C++ (Arduino Framework)
*   **Backend e Frontend:** Python com Flask
*   **Banco de Dados:** MariaDB
*   **Comunicação:** MQTT (Broker Mosquitto)
*   **Bibliotecas Principais:** `paho-mqtt`, `Flask-SQLAlchemy`, `Flask-Login`, `Flask-SocketIO`.

## 2. Arquitetura do Sistema

O sistema é composto por três partes principais que se comunicam de forma assíncrona:

1.  **ESP32 (Nó Sensor/Atuador):** O cérebro da operação em campo. É responsável por ler os dados dos sensores conectados e enviar sinais de controle para os atuadores. Ele se conecta à rede Wi-Fi e atua como um cliente MQTT, publicando os dados dos sensores e se inscrevendo em tópicos de comando.

2.  **Broker MQTT (Intermediário):** Atua como o servidor de mensagens central. O Mosquitto é o broker utilizado. Ele recebe as mensagens publicadas pelo ESP32 e as encaminha para os clientes inscritos (a aplicação Flask) e vice-versa. Isso desacopla o hardware do software, permitindo que eles operem de forma independente.

3.  **Aplicação Flask (Interface do Usuário):** A aplicação web fornece a interface para o usuário final. Ela se conecta ao broker MQTT para receber os dados dos sensores e exibi-los em um dashboard. Também permite que os usuários enviem comandos (por exemplo, ligar o ar-condicionado) que são publicados em tópicos MQTT e recebidos pelo ESP32. Além disso, gerencia a autenticação de usuários e armazena dados históricos em um banco de dados MariaDB.

## 3. Firmware do ESP32

O firmware do ESP32, escrito em C/C++ com o framework Arduino, é responsável pela interação direta com o ambiente físico. Suas principais funcionalidades estão detalhadas no arquivo `esp32.md`.

*   **Conectividade:** Conecta-se à rede Wi-Fi e ao broker MQTT.
*   **Sensores:** Realiza a leitura de múltiplos sensores (DHT11, LDR, MQ-135, HC-SR602, SCT-013).
*   **Atuadores:** Controla um ar-condicionado via IR e relés para outros dispositivos.
*   **Comunicação MQTT:** Publica dados dos sensores e se inscreve em tópicos para receber comandos da aplicação Flask.

## 4. Aplicação Flask

A aplicação web, desenvolvida com o framework Flask em Python, serve como o ponto central de controle e visualização para o usuário. Suas funcionalidades estão detalhadas no arquivo `flask-python.md`.

*   **Interface Web:** Fornece dashboards para visualização de dados e páginas para controle dos atuadores.
*   **Gerenciamento de Usuários:** Sistema completo de registro, login e gerenciamento de permissões (administrador vs. usuário padrão).
*   **Comunicação MQTT:** Atua como um cliente MQTT para se inscrever nos tópicos dos sensores e publicar nos tópicos de comando.
*   **Persistência de Dados:** Utiliza SQLAlchemy para mapear e salvar os dados em um banco de dados MariaDB, incluindo leituras de sensores, informações de usuários e logs de acesso/comandos.
*   **Tempo Real:** Emprega Flask-SocketIO para atualizar a interface do usuário em tempo real à medida que novos dados dos sensores chegam via MQTT.

## 5. Configuração e Instalação

As anotações em `Comandos pertinentes.md` fornecem a base para configurar o ambiente de desenvolvimento da aplicação Flask.

### Configurando o Ambiente Virtual

É recomendado usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Crie um ambiente virtual chamado 'venv'
python -m venv venv

# Ative o ambiente virtual
# No Linux/macOS:
source venv/bin/activate
# No Windows:
.\venv\Scripts\activate
```

### Instalando as Dependências

Com o ambiente ativado, instale os pacotes necessários a partir do arquivo `requirements.txt`.

```bash
pip install -r mega-tutorial/requirements.txt
```

### Executando a Aplicação Flask

Para iniciar o servidor de desenvolvimento do Flask:

```bash
# Navegue até o diretório do projeto
cd mega-tutorial

# Exporte a variável de ambiente para o aplicativo Flask
export FLASK_APP=holhooja.py

# (Opcional) Ative o modo de depuração para recarregamento automático
export FLASK_DEBUG=1

# Execute a aplicação
flask run
```

## 6. Protocolo MQTT

Conforme detalhado em `esp32.md`, o MQTT é a espinha dorsal da comunicação do sistema. Ele garante a entrega de mensagens entre o ESP32 e a aplicação Flask de forma eficiente e com baixo consumo de banda.

*   **Broker:** Utiliza-se o Mosquitto como broker.
*   **Tópicos:** A comunicação é organizada por tópicos, separando os dados de cada sensor e os comandos para cada atuador.
*   **QoS (Qualidade de Serviço):** O sistema pode ser configurado para diferentes níveis de QoS para garantir a entrega das mensagens conforme a criticidade da informação.
