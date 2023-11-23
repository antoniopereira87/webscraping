from numpy import add
import pandas as pd
import re
import mysql.connector as sql
from math import ceil

conexao = sql.connect(
    #user='root', database='BRASILEIRAO', host='localhost', port='3306', password='senha'
    user="admdatabase",
    host="db4free.net",
    password="bb70044e",
    database='brasileirao2023',
)
cursor = conexao.cursor()

lista_tecnicos = [
        "Lúcio Flávio",
        "Pedro Caixinha",
        "Abel Ferreira",
        "Tite",
        "Wesley Carvalho",
        "Renato Portaluppi",
        "Luiz Felipe Scolari",
        "Fernando Diniz",
        "Juan Pablo Vojvoda",
        "Dorival Júnior",
        "Eduardo Coudet",
        "Toni Oliveira",
        "Zé Ricardo",
        "Mano Menezes",
        "Rogério Ceni",
        "Marcelo Fernandes",
        "Armando Evangelista",
        "Ramón Díaz",
        "Thiago Kosloski",
        "Fabián Bustos"
        ]

times = pd.read_csv("times2.csv")

times.insert(4, "tecnico", lista_tecnicos) 

# # Preenchendo tabela TIME
# add_time = ("INSERT INTO CLUBE VALUES"
#             "(%s, %s, %s, %s, %s)")
# try:
#     for linha in times.itertuples():
#         dados_time = (linha[1], linha[2], linha[3], linha[4], linha[5])
#         cursor.execute(add_time, dados_time)
#         conexao.commit()
# except:
#     print("Tabela CLUBE já criada")

# print("Tabela CLUBE criada")

# Preenchendo tabela JOGADOR
jogadores = pd.read_csv("jogadores2.csv")
jogadores["Clube"] = jogadores.Clube.fillna("SEM CLUBE")
# id, nome, camisa, time
# clube, camisa, apelido, nome
add_jogador = ("INSERT IGNORE INTO JOGADOR VALUES"
               "(%s, %s, %s, %s)")

for jogador in jogadores.itertuples():
    nome_erro = jogador.Clube if jogador.Clube != "SEM CLUBE" else None
    nome_clube = nome_erro if nome_erro in times["Nome"].values else None
    if nome_clube is not None:
        dados_jogador = (jogador[0], jogador.Nome, jogador.Camisa, nome_erro) 
        cursor.execute(add_jogador, dados_jogador)
        conexao.commit()

# print("Tabela JOGADOR criada")

# Preenchendo tabela PARTIDA
#np, nr, local, mand, vis, data
#Rodada,Numero,Mandante,Visitante,PontosMandante,PontosVisitante,Local,Data
partidas = pd.read_csv("partidas.csv")
add_partida = ("INSERT IGNORE INTO PARTIDA VALUES"
               "(%s, %s, %s, %s, %s, %s)")
DATE = re.compile(r'.+, (\d+) de ([A-Za-z]+) de (\d+) (\d+):(\d+)')
MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

for partida in partidas.itertuples():
    data_partida = DATE.match(partida.Data)
    if data_partida is not None:
        data = f"{data_partida[3]}-{MESES.index(data_partida.group(2)) + 1}-{data_partida[1]} {data_partida[4]}:{data_partida[5]}:00"
        dados_partida = (partida.Numero, ceil(partida.Numero / 10), partida.Local, partida.Mandante, partida.Visitante, data) 
    else:
        dados_partida = (partida.Numero, ceil(partida.Numero / 10), partida.Local, partida.Mandante, partida.Visitante, None) 
    cursor.execute(add_partida, dados_partida)
    conexao.commit()

print("PARTIDA criada")

# Preenchendo tabela GOLS
# np, j, tg, mg, tm
# np, c, a, m, n, c, id
add_gols = ("INSERT IGNORE INTO GOLS VALUES"
               "(%s, %s, %s, %s, %s)")
gols = pd.read_csv("gols2.csv")
TEMPO = re.compile(r'(\d+(?:\+\d+)?)\' \((\d)ºT\)')

for gol in gols.itertuples():
    tempo = TEMPO.match(gol.Momento)
    if not pd.isna(gol.id):
        dados_gols = (gol.NPartida, gol.id, eval(tempo[1]), tempo[2], gol.Clube)
    else:
        dados_gols = (gol.NPartida, None, eval(tempo[1]), tempo[2], gol.Clube)
    cursor.execute(add_gols, dados_gols)
    conexao.commit()

print("GOLS criada")

# Preenchendo tabela CARTAO
# np, tc, j
# np, cl, tc, j 
cartoes = pd.read_csv("cartoes2.csv")
add_cartao = ("INSERT INTO CARTAO VALUES"
              "(%s, %s, %s, %s)")

for cartao in cartoes.itertuples():
    if not pd.isna(cartao.Punido):
        dados_cartoes = (cartao.NPartida, cartao.Cartao, cartao.Punido, cartao.Clube)
    else:
        dados_cartoes = (cartao.NPartida, cartao.Cartao, None, cartao.Clube)
    cursor.execute(add_cartao, dados_cartoes)
    conexao.commit()

# Preenche SUBS
# np, sai, entra 
# NPartida,Clube,idSubstituido,idSubstituto

subs = pd.read_csv("subs2.csv")
add_subs = ("INSERT INTO SUBSTITUICAO VALUES"
            "(%s, %s, %s, %s)")

try:
    for sub in subs.itertuples():
        sai = sub.idSubstituido if not pd.isna(sub.idSubstituido) else None
        entra = sub.idSubstituto if not pd.isna(sub.idSubstituto) else None
        dados_subs = (sub.NPartida, sai, entra, sub.Clube)
        cursor.execute(add_subs, dados_subs)
        conexao.commit()
except:
    print("SUBS criada")

print("SUBS criada")

# Preenche ARBITRO
# np, nome, func
arbs = pd.read_csv("arbs/arb6.csv")
add_arbs = ("INSERT INTO ARBITRAGEM VALUES"
            "(%s, %s, %s)")
try:
    for arb in arbs.itertuples():
        dados_arbs = (arb.NPartida, arb.Nome, arb.Funcao)
        cursor.execute(add_arbs, dados_arbs)
        conexao.commit()
except:
    print("ARBITRAGEM criada")

print("ARBITRAGEM criada")

relac = pd.read_csv("relacionados2.csv")
add_relac = ("INSERT INTO RELACIONADOS_PARA VALUES"
             "(%s, %s)")

for rel in relac.itertuples():
    if not pd.isna(rel.Jogador):
        dados_rel = (rel.Jogador, rel.NPartida)
        cursor.execute(add_relac, dados_rel)
        conexao.commit()

print("RELACIONADOS criada")

# FIM

cursor.close()
conexao.close()
