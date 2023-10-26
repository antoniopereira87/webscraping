import requests
from bs4 import BeautifulSoup
import pandas as pd

url_base = "https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2023"
req = requests.get(url_base)

# Le o html
soup = BeautifulSoup(req.text, 'html.parser')

# Encontrar todos elementos <table>
for table in soup.find_all('table'):
	body = table.tbody # table tbody
	if body is None: continue
	rows = body.find_all('tr') # todos os <tr> (linhas)

	pd_rows = []
	for row in rows:
		cells = row.find_all(['td', 'th']) # todos os <td> <th> para cada linha
		if len(cells) < 12: continue
		# destruturar os valores
		nome, pts, j, v, e, d, gp, gc, sg, ca, cv, porc, *rest = cells
		
		# Nome esta dentro de um <span class='hidden-xs'>
		nome = nome.find('span', 'hidden-xs')

		# pegar o texto dentro dos elementos
		data = list(map(lambda x: x.contents[0], [nome, pts, j, v, e, d, gp, gc, sg, ca, cv, porc]))
		pd_rows.append(data)

	if not pd_rows: continue

	# fazer dataframe pandas
	df = pd.DataFrame(data=pd_rows, columns=['Nome', "PTS", "J", "V", "E", "D", "GP", "GC", "SG", "CA", "CV", "%"])

	print(df)
	df.to_csv("times.csv", index=False)
