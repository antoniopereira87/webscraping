import requests
from bs4 import BeautifulSoup
import pandas as pd

url_base = "https://www.cbf.com.br/futebol-brasileiro/times/campeonato-brasileiro-serie-a/2023"
req = requests.get(url_base)

# Le o html
soup = BeautifulSoup(req.text, 'html.parser')


times = []
for time in soup.find_all('div', class_='col-md-3'):
	link = time.div.a['href']
	nome = time.find('span').contents[0]
	
	times.append((nome, link))

df = pd.DataFrame(data=times, columns=['nome','link'])
df.to_csv('times.csv', index=False)
