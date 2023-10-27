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
	
	tabela = page.find('table')
	arbritos = tabela.tbody('tr')

	# # print(cols)
	data = []
	for r in arbritos:
		func = r.th.string.strip().replace('\r\n', '')
		nome = ' '.join(r.a.string.strip().replace('\r\n', '').split())
		data.append((numero, nome, func))

	pd_rows.extend(data)
	return data

for j in range(10):
	for i in range(38):
		row = grab_url(j*38+i+1)
		print(row)
		

	df = pd.DataFrame(data=pd_rows, columns=['NPartida','Nome','Funcao'])
	df.to_csv(f"arbs/arb{j}.csv", index=False)