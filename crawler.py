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

-Funcoes:
    crawl(html, machines, atList, atDict): 
        
    webpage(url):
        
    runCrawler(url): verifica se a URL inserida eh suportada pelo web crawler. Se for, ela baixa o arquivo 
    HTML da pagina web e executa o crawler, chamando a funcao crawl(html, machines, atList, atDict) para extrair os atributos desejados
das paginas web. Se a URL inserida nao for suportada pelo crawler, chama a funcao 
errorUrl() para imprimir uma mensagem de erro.

    errorUrl(): imprime ensagem de erro caso o URL inserido nao seja suportado por este  web crawler.
"""

from bs4 import BeautifulSoup
import requests
import json, csv


#url = "https://www.vultr.com/products/cloud-compute/#pricing"
url = "https://www.digitalocean.com/pricing/"

    
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

# a partir daqui ainda falta polir e documentar melhor:

def printMachines(machines):
    i = 1
    print("\nMAQUINAS:\n")
    for mac in machines:
        print("--Maquina " + str(i) + "--\n")
        i += 1
        for item in mac.items():
            print(item[0] + ": " + item[1] + "\n")
        print("\n")
            

def runCrawler(url):
    if url == "https://www.vultr.com/products/cloud-compute/#pricing" or url == "https://www.digitalocean.com/pricing/":
        # Chama a funcao webpage(url) para baixar o html da pagina web:
        html = webpage(url)
        # Chama a função crawl, paa fazer a extração e armazenamento dos dados da pagina web:
        crawl(html, machines, atList, atDict)
        printMachines(machines)
        saveToJson(machines)
        saveToCsv(machines)
    else:
        errorUrl()

def webpage(url):
    response = requests.get(url)
    html = BeautifulSoup(response.text, "html.parser")
    return html

def crawl(html, machines, atList, atDict):
    # Limpa as listas para eliminar qualquer lixo de outra iteracao do programa:
    machines.clear()
    atList.clear()
    # Para a pagina-alvo 1:
    if url == "https://www.vultr.com/products/cloud-compute/#pricing":
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
                    atDict["STORAGE/SSD DISK"]= atList[0]    
                    atDict["CPU/VCPU"]= atList[1]
                    atDict["MEMORY"]= atList[2]
                    atDict["BANDWIDTH/TRANSFER"]= atList[3]
                    atDict["PRICE[$/mo]"]= atList[4]
                        
                    atList.clear() #limpa a lista temporaria atList
                    machines.append(atDict.copy())
    # Para a pagina-alvo 2:
    elif url == "https://www.digitalocean.com/pricing/":
        # Acessando a tabela "Basic droplets":
        """
        for container in html.find_all("div", {"id": "basic-droplets"}, class_="container"):
            print("a")
        """
        # Acessando os boxes (cada box tem os atributos de uma maquina):
        #for box in container.find_all("li", class_="priceBoxItem"):
        for box in html.find_all("li", class_="priceBoxItem"):
            #print("b")
            price = box.find("span", class_= "largePrice").get_text()
            atDict["PRICE[$/mo]"] = price
            #print(atDict["PRICE[$/mo]"])
            content = box.find_all("li")
            #print(content[2])
            array0 = content[0].get_text().split(" / ")
            #print(array0)
            atDict["MEMORY"] = array0[0]
            atDict["CPU/VCPU"] = array0[1]
            
            array1 = content[1].get_text().split(" ")
            #print(array1)
            atDict["STORAGE/SSD DISK"] = array1[0]+ " " +array1[1]
            
            array2 = content[2].get_text().split(" ")
            atDict["BANDWIDTH/TRANSFER"] = array2[0] + " " + array2[1]
            #print(array2)
            print("")
            print(atDict)
            machines.append(atDict.copy())
            
                
        

def errorUrl():
    message = """Erro: url invalido.
    As paginas-alvo suportadas por esse programa sao:
    1) "https://www.vultr.com/products/cloud-compute/#pricing"
    2) "https://www.digitalocean.com/pricing/"
    """
    print(message)
    
    
def saveToJson(data):
    with open("crawler_data.json", 'w') as file:
        json.dump(data, file)
        
def saveToCsv(data):
    csvColumns = [
       "CPU/VCPU",
       "MEMORY",
       "STORAGE/SSD DISK",
       "BANDWIDTH/TRANSFER",
       "PRICE[$/mo]"            
    ]
    with open("crawler_data.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvColumns)
        writer.writeheader()
        for value in data:
            writer.writerow(value)
        

#Script:
runCrawler(url)