import requests # Faz requisições HTTP para carregar a página.
from bs4 import BeautifulSoup #Analisa o HTML da página e permite extrair dados.

# Define a URL do produto.
url = "https://www.kabum.com.br/produto/633107/ssd-kingston-1tb-padrao-nv3-m-2-2280-nvme-4-0-gen-4x4-leitura-6000-e-gravacao-4000mbps-ultra-rapido-snv3s-1000g"

# Usa um User-Agent para evitar bloqueios do site.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Faz a Requisição HTTP (Envia um GET para obter o conteúdo da página.)
response = requests.get(url, headers=headers)

# Verifica se a Página Carregou com Sucesso
if response.status_code == 200: # O código 200 significa sucesso.
    page_content = response.text
    print("\nPágina carregada com sucesso\n")
else:
    # Se falhar, exibe o código de erro.
    print(f"\nFalha ao carregar a página. Status code: {response.status_code}\n")

# Processa o HTML com BeautifulSoup e analisa a estrutura HTML da página.
soup = BeautifulSoup(page_content, 'html.parser')

# Busca a Tag do Preço e tenta encontrar um <h4> com a classe "finalPrice".
price_tag = soup.find('h4', class_='finalPrice')

# Processa o Preço
if price_tag:
    # Pega o texto do preço.
    price_text = price_tag.get_text(strip=True)
    # Filtra caracteres, mantendo apenas números e pontuação
    price_text = ''.join(char for char in price_text if char.isdigit() or char in ',.')
    # Formata para float, garantindo que fique no formato correto.
    price = float(price_text.replace('.', '').replace(',', '.'))
    
    print(f"\nPreço atual: R$ {price:.2f}\n")
    
else:
    print("\nNão foi possível encontrar o preço da pagina.\n")
    
