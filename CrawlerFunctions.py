#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawler Functions

"""

from bs4 import BeautifulSoup
import requests
import json, csv

# printMachines(machines): imprime os atributos de cada maquina.
# Recebe como parametro a lista de dicionarios (machines).
def printMachines(machines):
    i = 1
    print("\nMAQUINAS:\n")
    for mac in machines:
        print("--Maquina " + str(i) + "--\n")
        i += 1
        for item in mac.items():
            print(item[0] + ": " + item[1] + "\n")
        print("\n")
            

# runCrawler(url, machines, atList, atDict): verifica se o URL corresponde com um dos que sao suportados 
# pelo crawler. Recebe como parametros o comando inserido pelo usuario (command), o URL, a lista de dicionarios com os atributos das maquinas
#(machines), a lista de atributos (atList) e o dicionario de atributos (atDict).
def runCrawler(command, url, machines, atList, atDict):
    # Chama a função crawl, para fazer a extração e armazenamento dos dados da pagina web:
    crawl(url, machines, atList, atDict)
    # Dependendo do comando, faz diferentes acoes:
    if command == "--print":
        printMachines(machines)
    if command == "--save_csv":
        saveToCsv(machines)
    if command == "--save_json":
        saveToJson(machines)
    

# webpage(url): baixa o HTML da pagina-alvo. Recebe como parametro o URL da pagina (url).
def webpage(url):
    response = requests.get(url)
    html = BeautifulSoup(response.text, "html.parser")
    return html

# crawl(url, machines, atList, atDict): extrai os dados desejados da pagina web.
#Recebe como parametros o URL da página (url), a lista de dicionarios com os atributos das maquinas 
#(machines), a lista de atributos (atList) e o dicionario de atributos (atDict).
def crawl(url, machines, atList, atDict):
    # Limpa as listas para garantir que vao estar vazias:
    machines.clear()
    atList.clear()
    # Chama a funcao webpage(url) para baixar o html da pagina web:
    html = webpage(url)
    # Para a pagina-alvo 1:
    if url == "https://www.vultr.com/products/cloud-compute/#pricing":
        #separando por maquina (e entao organizando uma lista de atributos pra cada maquina):
        for row in html.find_all("div", class_="pt__row-content"): # cada linha de atributos (cada linha representa UMA maquina diferente)
            for cell in row.find_all("div", class_="pt__cell"): #para cada celula dentro de uma linha (para cada atributo de um computador)
                content = cell.find_all("strong")
                if len(content) != 0:
                    atList.append(content[0].get_text())
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
        # Acessando os boxes (cada box tem os atributos de uma maquina):
        #for box in container.find_all("li", class_="priceBoxItem"):
        for box in html.find_all("li", class_="priceBoxItem"):
            price = box.find("span", class_= "largePrice").get_text()
            atDict["PRICE[$/mo]"] = price
            content = box.find_all("li")
            
            array0 = content[0].get_text().split(" / ")
            atDict["MEMORY"] = array0[0]
            atDict["CPU/VCPU"] = array0[1]
            
            array1 = content[1].get_text().split(" ")
            atDict["STORAGE/SSD DISK"] = array1[0]+ " " +array1[1]
            
            array2 = content[2].get_text().split(" ")
            atDict["BANDWIDTH/TRANSFER"] = array2[0] + " " + array2[1]
            machines.append(atDict.copy())
    else:
        errorUrl()
        
    
# saveToJson(data): salva dados da lista de dicionarios no formato json.
def saveToJson(data):
    with open("crawler_data.json", 'w') as file:
        json.dump(data, file)
    
# saveToCsv(data): salva dados da lista de dicionarios no formato csv.
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
            
            
# errorUrl(): imprime mensagem de erro se o URL nao for suportado pelo web crawler.
# Na atual configuracao do crawler, a mensagem de ajuda help() vai ser chamada antes que 
# o errorUrl() possa ser chamado. Mesmo assim mantive essa funcao no codigo caso as funcoes desse 
# arquivo sejam usadas em outro contexto no futuro.
def errorUrl():
    message = """Erro: url invalido.
    As paginas-alvo suportadas por esse programa sao:
    1) "https://www.vultr.com/products/cloud-compute/#pricing"
    2) "https://www.digitalocean.com/pricing/"
    """
    print(message)
 
    
# Mensagem de ajuda.
def help():
    message = """
    --crawler.py--
        Help:
            
    Como chamar o programa:
        python crawler.py <comando> <url> 
        
    <comando> pode ser:
        --print : imprime resultados na tela
        --save_csv : salva dados em arquivo csv
        --save_json : salva dados em arquivo json
    OBS.: --save_csv e --save_json salvam os arquivos
    na mesma pasta em que estiver o arquivo crawler.py
    
    <url> deve ser um dos URLs suportados pelo crawler:
        "https://www.vultr.com/products/cloud-compute/#pricing"
        "https://www.digitalocean.com/pricing/"
    """
    print(message)
        