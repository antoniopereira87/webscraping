

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
	cols = cols[4:6]

	# print(cols)
	data = ([],[],[])
	for col_i, col in enumerate(cols):
		substituidos_el = col.find_all('path', attrs={'fill':'#FA1200'})
		substituicoes = [
			(mand if col_i % 2 == 0 else vist,
			s.parent.parent.parent.a.string,
			s.parent.parent.parent.parent.next_sibling.next_sibling.a.string)
			for s in substituidos_el
		]


		cartoes_amarelo = col.find_all('i', 'icon-yellow-card')
		cartoes_vermelho = col.find_all('i', 'icon-red-card')
		cartoes = [
			(mand if col_i % 2 == 0 else vist,c.parent.a.string,'Y') for c in cartoes_amarelo
		] + [
			(mand if col_i % 2 == 0 else vist,c.parent.a.string,'R') for c in cartoes_vermelho
		]

		gols = [
			(mand if col_i % 2 == 0 else vist,
				c.parent.a.string,
				c['title'])
			for c in col.find_all('i', 'icon') if 'title' in c.attrs]
		
		print(substituicoes)
		print(cartoes)
		print(gols)

		data[0].extend(substituicoes)
		data[1].extend(cartoes)
		data[2].extend(gols)

	pd_rows.extend(data)
	return data

for i in [3]:
	row = grab_url(i)
	print(row)
	
	
# df = pd.DataFrame(data=pd_rows, columns=['Clube', 'Camisa', 'Apelido'])
# print(df)
# df.to_csv("camisas.csv", index=False)
