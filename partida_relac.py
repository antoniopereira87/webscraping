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
		data.extend([
			(   numero,
				mand if col_i % 2 == 0 else vist,
				n.string, n.next_sibling.next_sibling.a['href']
			)
			for n in numbers
		])
		

	pd_rows.extend(data)
	return data

for j in range(10):
	for i in range(38):
		row = grab_url(j*38+i+1)
		print(row)
		

	df = pd.DataFrame(data=pd_rows, columns=['NPartida','Time','Camisa','href'])
	df.to_csv(f"relac/relacionado{j}.csv", index=False)

"""
Associar apelido jogador com id

jogadores = pd.read_csv('jogadores2.csv')
relac = pd.read_csv('relac/relacionado9.csv.csv')
relac_j = relac.rename(columns={'Time': 'Clube'}).merge(jogadores, how='left')[['NPartida', 'id']].rename(columns={'id': 'Jogador'})
relac_j.to_csv('relacionados2.csv', index=False)
"""