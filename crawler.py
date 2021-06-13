#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Crawler

-Geral:
    O web crawler armazena os atributos de cada maquina em um dicionario (atDict), 
que tem uma copia (atDict.copy()) adicionada a uma lista de maquinas (machines). Assim, a lista de maquinas 
tem como elementos os dicionarios com os atributos das maquinas encontradas na pagina web.

-Bibliotecas:
    Requests: serviu para acessar a pagina web pelo protocolo HTTP.
    BeautifulSoup: foi utilizada para extrair dados do arquivo HTML da pagina web.
    json: salva arquivos no formato json.
    csv: salva arquivos no formato csv.
    sys: permite o uso do sys.argv.


-Executando o programa no prompt:

python crawler.py --print "https://www.vultr.com/products/cloud-compute/#pricing"
python crawler.py --save_json "https://www.vultr.com/products/cloud-compute/#pricing"
python crawler.py --save_csv "https://www.vultr.com/products/cloud-compute/#pricing"

python crawler.py --print "https://www.digitalocean.com/pricing/"
python crawler.py --save_json "https://www.digitalocean.com/pricing/"
python crawler.py --save_csv "https://www.digitalocean.com/pricing/"
"""


import CrawlerFunctions as crawler
import sys


# lista de URLs suportados pelo crawler:
urls = ["https://www.vultr.com/products/cloud-compute/#pricing", 
        "https://www.digitalocean.com/pricing/"]

# lista de comandos aceitos pelo crawler:
commands = ["--print", "--save_csv", "--save_json"]
    

# machines: Lista de maquinas. Cada elemento da lista eh um dicionario de atributos para uma maquina especifica.
machines = []

# atDict (attributes dictionary): Dicionario de atributos de cada maquina. 
# O dicionario de cada maquina sera adicionado a lista de maquinas (machines).
atDict = {
       "CPU/VCPU" : "",
       "MEMORY" : "",
       "STORAGE/SSD DISK" : "",
       "BANDWIDTH/TRANSFER" : "",
       "PRICE[$/mo]" : ""
}


if len(sys.argv) == 3:
    if sys.argv[2] in urls and sys.argv[1] in commands:
        # Se o URL e o comando inserido pelo usuario sao suportado pelo crawler, executar o crawler:
        # sys.argv[1] é o comando desejado pelo usuario,
        # sys.argv[2] é o URL.
        crawler.runCrawler(sys.argv[1], sys.argv[2], machines, atDict)
    else:
        crawler.help()
else:
    crawler.help()