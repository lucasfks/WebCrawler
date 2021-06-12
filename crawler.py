#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Crawler

-Geral:
    O web crawler armazena os atributos de cada maquina em um dicionario (atDict), 
o qual eh adicionado a uma lista de maquinas (machines). A lista de maquinas tem como 
elementos, os dicionarios das maquinas encontradas na pagina web. Antes de armazenar os 
atributos de uma maquina no dicionario, eles sao armazenados em uma lista de atributos (atList).
Essa lista facilita o armazenamento de atributos durante a execucao dos loops que foram 

-Bibliotecas:
    Para extrair informacao do arquivo html da pagina web, foi usada a biblioteca BeautifulSoup.

-Funcoes:
    crawl(html, machines, atList, atDict): 
    webpage(url):
    runCrawler(url): verifica se a URL inserida eh suportada pelo web crawler. Se for, ela 
executa o web crawler, chamando a funcao webpage(url) para armazenar html da pagina, e entao 
chama a funcao crawl crawl(html, machines, atList, atDict) para extrair os atributos desejados
das paginas web. Se a URL inserida nao for suportada pelo web crawler, chama a funcao 
errorUrl() para imprimir uma mensagem de erro.
    errorUrl(): imprime ensagem de erro caso o URL inserido nao seja suportado por este  web crawler.
"""

from bs4 import BeautifulSoup
import requests
import os, os.path, csv

url = "https://www.vultr.com/products/cloud-compute/#pricing"

    
# maquinas: Lista de maquinas. Cada elemento da lista e um dicionario de atributos para uma maquina especifica.
machines = []

# atList (attributes list): Lista temporaria de atributos para uma maquina especifica. Essa lista facilita o monitoramento da extracao de dados da pagina html para cada maquina. 
atList = []

# atDict (attributes dictionary): Dicionario de atributos de cada maquina. O dicionario de cada maquina sera adicionado a lista de maquinas (machList).
atDict = {
       "CPU" : "",
       "MEMORY" : "",
       "STORAGE" : "",
       "BANDWIDTH" : "",
       "PRICE[$/mo]" : ""
}

# a partir daqui ainda falta polir e documentar melhor:

def printMachines(machines):
    print("\nMAQUINAS:\n")
    """
    for i in range(len(machines)):
        print("--Maquina " + str(i+1) + "--\n")
        for item in machines[i].items():
            print(item[0] + ": " + item[1] + "\n")
        print("\n")
        """
    i = 1
    for mac in machines:
        print("--Maquina " + str(i) + "--\n")
        i += 1
        for item in mac.items():
            print(item[0] + ": " + item[1] + "\n")
        print("\n")
            

def runCrawler(url):
    if url == "https://www.vultr.com/products/cloud-compute/#pricing" or url == "https://www.digitalocean.com/pricing/":
        html = webpage(url)
        crawl(html, machines, atList, atDict)  
        #print(machines) #teste para ver se funciona
        printMachines(machines)
    else:
        errorUrl()

def webpage(url):
    response = requests.get(url)
    html = BeautifulSoup(response.text, "html.parser")
    return html

def crawl(html, machines, atList, atDict):
    #separando por maquina (e entao organizando uma lista de atributos pra cada maquina):
    for row in html.find_all("div", class_="pt__row-content"): # cada linha de atributos (cada linha representa UMA maquina diferente)
        #print(row)
        #print("-------//------")
        for cell in row.find_all("div", class_="pt__cell"): #para cada celula dentro de uma linha (para cada atributo de um computador)
            #print(cell)
            #print("-------//------")
            content = cell.find_all("strong")
            #print(content)
            #print("-------//------")
            if len(content) != 0:
                atList.append(content[0].get_text())
                #print(atList)
            if len(atList) == 5:  # numero de atributos extraidos para cada maquina
                # passando os atributos da atList para o datDict:
                if url == "https://www.vultr.com/products/cloud-compute/#pricing": # para a pagina-alvo 1
                    atDict["STORAGE"]= atList[0]    
                    atDict["CPU"]= atList[1]
                    atDict["MEMORY"]= atList[2]
                    atDict["BANDWIDTH"]= atList[3]
                    atDict["PRICE[$/mo]"]= atList[4]
                #elif url == "https://www.digitalocean.com/pricing/": #pagina-alvo 2
                    
                atList.clear() #limpa a lista temporaria atList
                machines.append(atDict.copy())

def errorUrl():
    message = """Erro: url invalido.
    As paginas-alvo suportadas por esse programa sao:
    1) "https://www.vultr.com/products/cloud-compute/#pricing"
    2) "https://www.digitalocean.com/pricing/"
    """
    print(message)

#Script:
runCrawler(url)