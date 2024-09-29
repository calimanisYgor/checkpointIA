# Detecção de Sono em Tempo Real

Este projeto é uma aplicação em Python que utiliza a webcam para capturar vídeo em tempo real, processa as imagens usando um modelo de detecção fornecido pelo Roboflow e exibe o vídeo com as predições sobrepostas em uma interface gráfica construída com Tkinter.

## Descrição 📄
A aplicação captura frames da webcam do usuário, envia periodicamente esses frames para um modelo de detecção de sono hospedado no Roboflow, e exibe as predições (como retângulos e labels) sobre o vídeo em tempo real na janela do Tkinter.

## Requisitos 📌
- Python 3.6 ou superior
- Webcam conectada ao computador

## Instalação 🚀

1. Clone o repositório ou faça o download dos arquivos do projeto.

2. Instale as dependências necessárias:

3. Utilize o pip para instalar as bibliotecas requeridas:

```
pip install opencv-python requests Pillow
```

## Como Usar 🖥️

1. Obtenha as credenciais da API do Roboflow:

- Crie uma conta no Roboflow.
- Faça o upload ou treine um modelo de detecção.
- Obtenha a sua API_KEY e MODEL_ID.

2. Configure o código:

-  Abra o arquivo Python do projeto.
-  Substitua "YOUR_API_KEY" pela sua chave de API.
- Substitua "YOUR_MODEL_ID" pelo ID do seu modelo (geralmente no formato "nome-do-modelo/versão").

3. Execute a aplicação:
```
python checkpoint.py
```