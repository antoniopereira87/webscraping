

numeros = [10, 8, 6, 19, 2, 4, 18, 16, 20, 1, 11, 9, 15, 7, 17, 3, 5, 14, 13, 12]

import requests
from bs4 import BeautifulSoup
import pandas as pd

pd_rows = []

def grab_url(numero):
	try:
		req = requests.get(f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023/{numero}#escalacao')
	except requests.ConnectionError as e:
		print(f"Erro em {numero}: {e}")
		return None

	page = BeautifulSoup(req.text, 'html.parser')
	
	nomes = page.find_all('h3', 'time-nome')
	mand, vist = [n.string for n in nomes]

	cols = page.find_all('div', 'col-xs-6')
	cols = cols[4:8]

	# print(cols)
	data = []
	for col_i, col in enumerate(cols):
		numbers = col.find_all('span', 'list-number')
		data.extend([(mand if col_i % 2 == 0 else vist, n.string, n.next_sibling.next_sibling.a.string) for n in numbers])
	
	pd_rows.extend(data)
	return data


	# meta = page.find('meta', attrs={'itemprop':'description'})
	# if not meta:
	# 	print(f"Erro em {numero}: sem <meta>")
	# 	return None

	# description = meta['content'].split('/')
	# if len(description) != 4: return None
	# _, pontos, data, lugar = description
		
	# mandante, visitante = pontos.strip().split('x')
	# ponto_visitante, visitante = visitante.split(' ', 1)
	# *mandante, ponto_mandante = mandante.split(' ')
	# mandante = ' '.join(mandante)

	# print(numero, mandante, visitante, ponto_mandante, ponto_visitante, sep=',')
	
	# if not ponto_visitante.strip().isnumeric() or not ponto_mandante.strip().isnumeric():
	# 	row = (numero, mandante, visitante, None, None, lugar.strip(), data.strip())
	# 	pd_rows.append(row)
	# 	return row
	
	# row = (numero, mandante, visitante, int(ponto_mandante), int(ponto_visitante), lugar.strip(), data.strip())
	# pd_rows.append(row)
	
	# return row

for i in numeros:
	row = grab_url(i)
	print(row)
	
	
df = pd.DataFrame(data=pd_rows, columns=['Clube', 'Camisa', 'Apelido'])
print(df)
df.to_csv("camisas.csv", index=False)
