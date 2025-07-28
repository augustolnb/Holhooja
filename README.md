# Projeto Holhooja: Um Sistema IoT para Automação Laboratorial e Controle de Acesso

## 📖 Sobre o Projeto

O Holhooja é um sistema integrado de automação e controle de acesso baseado em IoT, desenvolvido para o Laboratório de Práticas Autônomas (LPA) do IFTO - Campus Palmas. O projeto visa modernizar a gestão do laboratório, oferecendo uma solução prática e segura para o controle de acesso, automação de equipamentos e monitoramento em tempo real.

### 🎯 Objetivos

*   **Automatizar o controle de acesso:** Substituir o controle manual por um sistema de login online.
*   **Gerenciar o tempo de uso:** Registrar a permanência dos alunos para a emissão de certificados de horas complementares.
*   **Automação do ambiente:** Controlar remotamente a iluminação e o ar condicionado.
*   **Monitoramento em tempo real:** Fornecer dados sobre as condições do laboratório (temperatura, umidade, número de presentes, etc).
*   **Código Aberto:** Disponibilizar o projeto para que possa ser adaptado e implementado em outros ambientes.

## ✨ Funcionalidades Principais

*   ✅ **Autenticação Online:** Sistema de login para acesso ao laboratório.
*   ✅ **Registro de Acesso:** Gravação automática de entradas e saídas.
*   ✅ **Contagem de Horas:** Cálculo do tempo de permanência por usuário.
*   ✅ **Controle Remoto:** Gerenciamento do ar condicionado e iluminação via dashboard.
*   ✅ **Monitoramento de Sensores:** Acompanhamento em tempo real de temperatura, umidade, presença e qualidade do ar.
*   ✅ **Código Aberto:** Projeto disponível para a comunidade.

## 🛠️ Tecnologias Utilizadas

O projeto é dividido em duas partes principais: o **Hardware Embarcado** e a **Aplicação Web**.

### Hardware (ESP32)

*   **Microcontrolador:** ESP32-S3-WROOM-1
*   **Linguagem:** C++ (com framework Arduino)
*   **Sensores:**
    *   DHT11 (Sensor de Temperatura e Umidade)
    *   MQ-135 (Sensor de Gases Nocivos)
    *   SR602 (Sensor de Presença PIR)
    *   SCT-013 (Corrente Elétrica)
    *   LDR (Luminosidade)
*   **Atuadores:**
    *   Relé para controle da fechadura eletrônica.
    *   LED Infravermelho para controle do ar condicionado.
*   **Comunicação:** MQTT

### Aplicação Web (Servidor)

*   **Linguagem:** Python
*   **Framework:** Flask
*   **Banco de Dados:** MariaDB
*   **Servidor Web:** Nginx
*   **Servidor WSGI:** Gunicorn
*   **Comunicação em Tempo Real:** WebSockets (com Flask-SocketIO) e MQTT (com Paho-MQTT)
*   **Frontend:** HTML, CSS (com framework Bulma) e JavaScript.


### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/Holhooja.git
    ```
2.  **Aplicação Web:**
    *   Navegue até a pasta `App/V4.5`.
    *   Crie e ative um ambiente virtual.
    *   Instale as dependências: `pip install -r requirements.txt`.
    *   Configure o banco de dados...
    *   Execute a aplicação: `flask run`.
3.  **Firmware (ESP32):**
    *   Abra o projeto em `ESP32/firmware/V4.0/` na Arduino IDE.
    *   Instale as bibliotecas necessárias...
    *   Configure as credenciais de Wi-Fi e MQTT.
    *   Compile e envie o firmware para o ESP32.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
