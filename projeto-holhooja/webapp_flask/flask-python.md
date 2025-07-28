# Documentação do Projeto Holhooja (Flask)

Esta documentação descreve a aplicação web Flask para o projeto Holhooja, um sistema de automação residencial e monitoramento de ambiente.

## Visão Geral

A aplicação Flask é responsável por:

*   Fornecer uma interface web para os usuários interagirem com o sistema.
*   Autenticar e autorizar usuários.
*   Exibir os dados dos sensores em tempo real.
*   Permitir o controle dos atuadores (ar-condicionado, lâmpada, porta).
*   Armazenar os dados dos sensores e os registros de acesso em um banco de dados.

## Estrutura do Projeto

O projeto Flask está estruturado da seguinte forma:

*   `holhooja.py`: Arquivo principal da aplicação.
*   `config.py`: Contém as configurações da aplicação, como a chave secreta e a URI do banco de dados.
*   `mqtt.py`: Contém a lógica para a comunicação com o broker MQTT.
*   `app/`: Diretório que contém o código da aplicação.
    *   `__init__.py`: Inicializa a aplicação Flask e as extensões.
    *   `routes.py`: Define as rotas da aplicação.
    *   `models.py`: Define os modelos do banco de dados.
    *   `forms.py`: Define os formulários da aplicação.
    *   `sockets.py`: Define a lógica para a comunicação com os clientes via Socket.IO.
    *   `templates/`: Contém os templates HTML da aplicação.

## Funcionalidades

### Autenticação de Usuários

*   Os usuários podem se registrar e fazer login na aplicação.
*   A aplicação utiliza o Flask-Login para gerenciar a autenticação dos usuários.
*   As senhas dos usuários são armazenadas de forma segura no banco de dados usando hashes.

### Visualização de Dados

*   A aplicação exibe os dados dos sensores em tempo real em um dashboard.
*   Os dados são atualizados automaticamente usando Socket.IO.

### Controle de Atuadores

*   Os usuários podem controlar o ar-condicionado, a lâmpada e a porta através da interface web.
*   Os comandos são enviados para o ESP32 via MQTT.

### Banco de Dados

*   A aplicação utiliza o SQLAlchemy para interagir com um banco de dados MariaDB.
*   O banco de dados armazena as seguintes informações:
    *   Usuários
    *   Registros de acesso
    *   Dados dos sensores
    *   Comandos enviados

## Tópicos MQTT

### Tópicos de Subscrição (Sensores)

*   `/sensores/DHT`: Recebe os dados de temperatura e umidade do ESP32.
*   `/sensores/LDR`: Recebe os dados de luminosidade do ESP32.
*   `/sensores/SR602`: Recebe o status de detecção de movimento do ESP32.

### Tópicos de Publicação (Comandos)

*   `/esp32/verificarConexao`: Envia comandos para o ar-condicionado.

## Modelos do Banco de Dados

*   **User:** Armazena as informações dos usuários.
*   **Acesso:** Armazena os registros de acesso dos usuários.
*   **Sensores:** Armazena os dados dos sensores.
*   **Comandos:** Armazena os comandos enviados pelos usuários.
