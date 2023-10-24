

import requests
from bs4 import BeautifulSoup
import pandas as pd

pd_rows = []

def grab_url(url):
	url_base = url
	req = requests.get(url_base)

	page = BeautifulSoup(req.text, 'html.parser')
	table = page.find('table', class_='m-t-30')

	for row in table.find_all('tr'):
		nomes = row.find_all('a')
		if not nomes or len(nomes) < 2: continue
		nome, apelido = nomes[0], nomes[1]
		nome = nome.contents[0].strip()
		apelido = apelido.contents[0].strip()
		clube = row.find('img')
		if clube:
			clube = clube['title'].strip()
		else:
			clube = None
		pd_rows.append([nome, apelido, clube])

	prox = page.find_all(attrs={'rel': 'next'})
	if not prox: return None
	return prox[0]['href']

url = 'https://www.cbf.com.br/futebol-brasileiro/atletas/campeonato-brasileiro-serie-a/2023'

page = 0
print("Baixando dados")
while url:
	url = grab_url(url)
	page += 1
	
	p = int(page/45*100)
	print(f'\r['+'#'*p+' '*(100-p)+']', end='')
	
df = pd.DataFrame(data=pd_rows, columns=['Nome', 'Apelido', "Clube"])
print(df)
df.to_csv("jogadores.csv", index=False)
