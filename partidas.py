import requests
from bs4 import BeautifulSoup
import pandas as pd

pd_rows = []

def grab_url(numero):
	try:
		req = requests.get(f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023/{numero}')
	except:
		print(f"Erro em {numero}")
		return None

	page = BeautifulSoup(req.text, 'html.parser')
	
	meta = page.find('meta', attrs={'itemprop':'description'})
	description = meta['content'].split('/')
	if len(description) != 4: return None
	_, pontos, data, lugar = description
		
	mandante, visitante = pontos.strip().split('x')
	ponto_visitante, visitante = visitante.split(' ', 1)
	*mandante, ponto_mandante = mandante.split(' ')
	mandante = ' '.join(mandante)
	
	if not ponto_visitante.isnumeric() or ponto_mandante.isnumeric():
		row = (numero, mandante, visitante, None, None, lugar.strip(), data.strip())
		pd_rows.append(row)
		return row
	
	row = (numero, mandante, visitante, int(ponto_mandante), int(ponto_visitante), lugar.strip(), data.strip())
	pd_rows.append(row)
	
	return row

for i in range(1, 380):
	row = grab_url(i)
	print(row)
	
	
df = pd.DataFrame(data=pd_rows, columns=['Numero', 'Mandante', 'Visitante', "PontosMandante", "PontosVisitante", "Local", "Data"])
print(df)
df.to_csv("partidas.csv", index=False)
