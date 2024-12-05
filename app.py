import pandas as pd
import time
import random
from flask import Flask, request, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading

app = Flask(__name__)

# Função para enviar mensagens via WhatsApp
def enviar_mensagens(numeros, mensagens):
    navegador = webdriver.Chrome()
    navegador.get('https://web.whatsapp.com')
    input("Escaneie o QR Code e pressione ENTER para continuar...")  # Remova isso e use uma lógica de espera

    random.shuffle(mensagens)  # Embaralhar mensagens para envio aleatório

    for numero in numeros:
        mensagem = random.choice(mensagens)  # Escolhe uma mensagem aleatória

        try:
            # Acessa o chat do contato pelo link direto do WhatsApp Web
            link = f"https://web.whatsapp.com/send?phone={numero}"
            navegador.get(link)
            time.sleep(20)  # Aumentar o tempo para garantir que a página carregue

            # Verifica se a página carregou corretamente
            try:
                # Tenta encontrar o alerta de erro
                navegador.find_element(By.XPATH, '//div[@role="alert"]')
                print(f"Erro ao abrir conversa para {numero}. O número pode estar incorreto.")
                continue
            except:
                pass  # Se não encontrar o alerta, continue

            # Aguarda até que o campo de mensagem esteja disponível
            while True:
                try:
                    campo_mensagem = navegador.find_element(By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')
                    print(f"Campo de mensagem disponível para {numero}. Iniciando envio...")
                    break  # Campo encontrado, sai do loop
                except:
                    print("Aguardando o campo de mensagem...")
                    time.sleep(1)  # Aguarda um segundo antes de tentar novamente

            campo_mensagem.click()  # Foca no campo de mensagem

            print(f"Digitando a mensagem: {mensagem}")
            for letra in mensagem:
                campo_mensagem.send_keys(letra)
                time.sleep(random.uniform(0.05, 0.15))  # Atraso aleatório entre letras

            campo_mensagem.send_keys(Keys.ENTER)
            print(f"Mensagem enviada para {numero}")

            # Aguardar alguns segundos antes de enviar a próxima mensagem
            time.sleep(random.uniform(60, 300))  # Atraso aleatório entre mensagens

        except Exception as e:
            print(f"Erro ao enviar para {numero}: {str(e)}")

    navegador.quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    data = request.json
    numeros = data['telefones']
    mensagens = data['mensagens']

    # Executa a função de envio em uma thread separada
    threading.Thread(target=enviar_mensagens, args=(numeros, mensagens)).start()
    
    return jsonify({"status": "Mensagens enviadas com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
