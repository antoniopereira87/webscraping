"""
Feito por:  Antonio Jorge Oliveira Pereira
            Julia Luiza Ferreira Santos
            Marco Antonio de Abreu Barbosa
            Renan Aguiar Chagas
            Vitor Luiz Reis do Carmo
            Wallace Barbosa Ferreira
"""
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'BRASILEIRAO'

TABLES = {}

TABLES['USUARIO'] = (
        "CREATE TABLE `USUARIO` ("
        "`nome` varchar(30) NOT NULL,"
        "`tipo` enum('ADMIN', 'NORMAL') NOT NULL,"
        "`login` varchar(30) NOT NULL,"
        "`senha` varchar(30) NOT NULL,"
        "PRIMARY KEY(`login`)"
        ") DEFAULT CHARSET = utf8"
        )

TABLES['CLUBE'] = (
        "CREATE TABLE `CLUBE` ("
         "`nome` varchar(50) NOT NULL,"
         "`vitorias` int,"
         "`derrotas` int,"
         "`empates` int,"
         "`tecnico` varchar(20) NOT NULL,"
         "PRIMARY KEY(`nome`)"
         ") DEFAULT CHARSET = utf8"
        )

TABLES['JOGADOR'] = (
        "CREATE TABLE `JOGADOR` ("
        "`id` int NOT NULL,"
        "`nome` varchar(50) NOT NULL,"
        "`camisa` int,"
        "`clube` varchar(50),"
        "PRIMARY KEY(`id`),"
        "FOREIGN KEY(`clube`) REFERENCES CLUBE(`nome`)"
        ") DEFAULT CHARSET = utf8"
        )

TABLES['PARTIDA'] = (
        "CREATE TABLE `PARTIDA` ("
        "`num_partida` int NOT NULL,"
        "`num_rodada` int NOT NULL,"
        "`local` varchar(50) NOT NULL,"
        "`time_mandante` varchar(50) NOT NULL,"
        "`time_visitante` varchar(50) NOT NULL,"
        "`data_partida` datetime,"
        "PRIMARY KEY(`num_partida`),"
        "FOREIGN KEY(`time_mandante`) REFERENCES CLUBE(`nome`),"
        "FOREIGN KEY(`time_visitante`) REFERENCES CLUBE(`nome`)"
        ") DEFAULT CHARSET = utf8"
        )

TABLES['ARBITRAGEM'] = (
        "CREATE TABLE `ARBITRAGEM` ("
        "`num_partida` int NOT NULL,"
        "`nome` varchar(50) NOT NULL,"
        "`funcao` varchar(50) NOT NULL,"
        "FOREIGN KEY(`num_partida`) REFERENCES PARTIDA(`num_partida`)"
        ") DEFAULT CHARSET = utf8"
        )

TABLES['SUBSTITUICAO'] = (
        "CREATE TABLE `SUBSTITUICAO` ("
        "`num_partida` int NOT NULL,"
        "`substituido` int,"
        "`substituto` int,"
        "`time_afetado` varchar(30) NOT NULL,"
        "FOREIGN KEY(`num_partida`) REFERENCES PARTIDA(`num_partida`),"
        "FOREIGN KEY(`substituido`) REFERENCES JOGADOR(`id`),"
        "FOREIGN KEY(`substituto`) REFERENCES JOGADOR(`id`),"
        "FOREIGN KEY(`time_afetado`) REFERENCES CLUBE(`nome`)"
        ") DEFAULT CHARSET = utf8"
        )

TABLES['CARTAO'] = (
        "CREATE TABLE `CARTAO` ("
        "`num_partida` int NOT NULL,"
        "`tipo_cartao` enum('Y', 'R'),"
        "`punido` int,"
        "`clube_punido` varchar(50),"
        "FOREIGN KEY(`num_partida`) REFERENCES PARTIDA(`num_partida`),"
        "FOREIGN KEY(`punido`) REFERENCES JOGADOR(`id`),"
        "FOREIGN KEY(`clube_punido`) REFERENCES CLUBE(`nome`)"
        ") DEFAULT CHARSET = utf8"
        )

TABLES['GOLS'] = (
        "CREATE TABLE `GOLS` ("
        "`num_partida` int NOT NULL,"
        "`jogador` int,"
        "`tempo_gol` int NOT NULL,"
        "`minuto_gol` int NOT NULL,"
        "`time_marcou` varchar(50) NOT NULL,"
        "FOREIGN KEY(`time_marcou`) REFERENCES CLUBE(`nome`),"
        "FOREIGN KEY(`num_partida`) REFERENCES PARTIDA(`num_partida`),"
        "FOREIGN KEY(`jogador`) REFERENCES JOGADOR(`id`)"
        ") DEFAULT CHARSET = utf8"
        )

TABLES['RELACIONADOS_PARA'] = (
        "CREATE TABLE `RELACIONADOS_PARA` ("
        "`id_jogador` int NOT NULL,"
        "`num_partida` int NOT NULL,"
        "FOREIGN KEY (`id_jogador`) REFERENCES JOGADOR(`id`),"  
        "FOREIGN KEY(`num_partida`) REFERENCES PARTIDA(`num_partida`)"
        ") DEFAULT CHARSET = utf8"
        )

cnx = mysql.connector.connect(user='root', host='localhost', port='3306', password='senha')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
