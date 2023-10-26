import requests
from bs4 import BeautifulSoup
import pandas as pd

pd_rows = []

def grab_url(numero):
	try:
		req = requests.get(f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023/{numero}')
	except requests.ConnectionError as e:
		print(f"Erro em {numero}: {e}")
		return None

	page = BeautifulSoup(req.text, 'html.parser')
	
	meta = page.find('meta', attrs={'itemprop':'description'})
	if not meta:
		print(f"Erro em {numero}: sem <meta>")
		return None

	description = meta['content'].split('/')
	if len(description) != 4: return None
	_, pontos, data, lugar = description
		
	mandante, visitante = pontos.strip().split('x')
	ponto_visitante, visitante = visitante.split(' ', 1)
	*mandante, ponto_mandante = mandante.split(' ')
	mandante = ' '.join(mandante)

	print(numero, mandante, visitante, ponto_mandante, ponto_visitante, sep=',')
	
	if not ponto_visitante.strip().isnumeric() or not ponto_mandante.strip().isnumeric():
		row = (numero, mandante, visitante, None, None, lugar.strip(), data.strip())
		pd_rows.append(row)
		return row
	
	row = (numero//38+1, numero, mandante, visitante, int(ponto_mandante), int(ponto_visitante), lugar.strip(), data.strip())
	pd_rows.append(row)
	
	return row

for i in range(1, 380):
	row = grab_url(i)
	print(row)
	if row:
		print(row,sep=',', file=f)
	
	
df = pd.DataFrame(data=pd_rows, columns=['Rodada', 'Numero', 'Mandante', 'Visitante', "PontosMandante", "PontosVisitante", "Local", "Data"])
print(df)
df.to_csv("partidas.csv", index=False)
