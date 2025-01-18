import requests
from bs4 import BeautifulSoup


url = "https://www.kabum.com.br/produto/633107/ssd-kingston-1tb-padrao-nv3-m-2-2280-nvme-4-0-gen-4x4-leitura-6000-e-gravacao-4000mbps-ultra-rapido-snv3s-1000g"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    page_content = response.text
    print("\nPágina carregada com sucesso\n")
else:
    print(f"\nFalha ao carregar a página. Status code: {response.status_code}\n")


soup = BeautifulSoup(page_content, 'html.parser')

price_tag = soup.find('h4', class_='finalPrice')

if price_tag:

    price_text = price_tag.get_text(strip=True)

    price_text = ''.join(char for char in price_text if char.isdigit() or char in ',.')
    
    price = float(price_text.replace('.', '').replace(',', '.'))
    
    print(f"\nPreço atual: R$ {price:.2f}\n")
    
else:
    print("\nNão foi possível encontrar o preço da pagina.\n")
    
