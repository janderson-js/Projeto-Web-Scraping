import requests # Faz requisições HTTP para carregar a página.
import schedule # Faz a automação do codigo
import time # controla o tempo para a verificação
import smtplib
import json
from bs4 import BeautifulSoup #Analisa o HTML da página e permite extrair dados.
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


with open("config.json", "r") as f:
    config = json.load(f)


EMAIL_REMETENTE = config["EMAIL_REMETENTE"]
SENHA_EMAIL = config["SENHA_EMAIL"]
EMAIL_DESTINO = config["EMAIL_DESTINO"]


# Define a url do produto.
url = "https://www.kabum.com.br/produto/633107/ssd-kingston-1tb-padrao-nv3-m-2-2280-nvme-4-0-gen-4x4-leitura-6000-e-gravacao-4000mbps-ultra-rapido-snv3s-1000g"

# Usa um User-Agent para evitar bloqueios do site.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
preco_alvo = 600.00


ultimo_preco = None


def enviar_email(preco_atual):
    msg = MIMEMultipart()
    msg["from"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINO
    msg["Subject"] = "⚠️⚠️⚠️ Alerta preço Baixo - SSD Kingston"
    
    corpo = f"📌 O preço do SSD caiu para R$ {preco_atual:.2f}!\nConfira: {url}"
    msg.attach(MIMEText(corpo, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_EMAIL)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())
        
        print("✅ E-mail enviado com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao enviar e-mail: {e}")
    finally:
        server.quit()

def verificar_preco():
    global ultimo_preco  # Permite modificar a variável global

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("h4", class_="finalPrice")  # Ajustar a classe conforme necessário

        if price_tag:
            price_text = price_tag.get_text(strip=True)
            price_text = "".join(char for char in price_text if char.isdigit() or char in ",.")
            preco_atual = float(price_text.replace(".", "").replace(",", "."))

            print(f"Preço atual: R$ {preco_atual:.2f}")

            # Se for a primeira execução, apenas armazena o preço
            if ultimo_preco is None:
                ultimo_preco = preco_atual
                return

            # Enviar e-mail somente se o preço cair e for diferente do último registrado
            if preco_atual < ultimo_preco and preco_atual <= preco_alvo:
                print("🔔 Preço caiu! Enviando e-mail...")
                enviar_email(preco_atual)

            # Atualiza o último preço conhecido
            ultimo_preco = preco_atual
        else:
            print("⚠️ Preço não encontrado.")
    else:
        print(f"⚠️ Falha ao acessar o site. Status code: {response.status_code}")

# faz com que a função rode durante um determinado tempo
schedule.every(10).seconds.do(verificar_preco)

print("Monitor de preço iniciado...")
while True:
    schedule.run_pending() # roda o script 
    time.sleep(10) # Faz com que o programa espere um tempo antes de realiza uma proxima verificação de preço
    





