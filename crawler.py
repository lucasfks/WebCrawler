#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Crawler

-Geral:
    O web crawler armazena os atributos de cada maquina em um dicionario (atDict), 
o qual eh adicionado a uma lista de maquinas (machines). A lista de maquinas tem, como 
elementos, os dicionarios das maquinas encontradas na pagina web. Antes de armazenar os 
atributos de uma maquina no dicionario, eles sao armazenados em uma lista de atributos (atList).
Essa lista facilita o armazenamento de atributos durante a execucao dos loops que buscam os atributos 
na pagina-alvo 1.

-Bibliotecas:
    Requests: serviu para acessar a pagina web pelo protocolo HTTP.
    BeautifulSoup: foi utilizada para extrair dados do arquivo HTML da pagina web.
    json: salva arquivos no formato json.
    csv: salva arquivos no formato csv.
    sys: permite o uso do sys.argv.

"""

#from CrawlerFunctions import *
import CrawlerFunctions as crawler
import sys


# lista de URLs suportados pelo crawler:
urls = ["https://www.vultr.com/products/cloud-compute/#pricing", 
        "https://www.digitalocean.com/pricing/"]


commands = ["--print", "--save_csv", "--save_json"]
    
# maquinas: Lista de maquinas. Cada elemento da lista e um dicionario de atributos para uma maquina especifica.
machines = []

# atList (attributes list): Lista temporaria de atributos para uma maquina especifica. Essa lista facilita o monitoramento da extracao de dados da pagina html para cada maquina. 
atList = []

# atDict (attributes dictionary): Dicionario de atributos de cada maquina. O dicionario de cada maquina sera adicionado a lista de maquinas (machList).
atDict = {
       "CPU/VCPU" : "",
       "MEMORY" : "",
       "STORAGE/SSD DISK" : "",
       "BANDWIDTH/TRANSFER" : "",
       "PRICE[$/mo]" : ""
}

#Script:
if len(sys.argv) == 3:
    if sys.argv[2] in urls and sys.argv[1] in commands:
        # Se o URL e o comando inserido pelo usuario sao suportado pelo crawler, executar o crawler:
        # sys.argv[1] é o comando desejado pelo usuario,
        # sys.argv[2] é o URL.
        crawler.runCrawler(sys.argv[1], sys.argv[2], machines, atList, atDict)
    else:
        crawler.help()
else:
    crawler.help()