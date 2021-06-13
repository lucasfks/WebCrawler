Esse projeto é um web crawler capaz de acessar duas páginas ("https://www.vultr.com/products/cloud-compute/#pricing"
e "https://www.digitalocean.com/pricing/") e extrair delas os seguintes atributos das máquinas disponíveis:
CPU/VCPU, Memory, Storage/SSD Disk, Bandwidth/Transfer e Price[$/mo].


-Instruções para o usuário-

	Para executar o programa, o usuário deve fazer o download dos arquivos contidos nesse repositório e deve ter o Python instalado em versão 3.7.3 para que haja garantia de funcionamento.
	É preciso também ter as seguintes bibliotecas do python instaladas: Requests, BeautifulSoup, json, csv, sys.
	Então o usuário deve abrir o prompt de comando (ou aplicativo semelhante) e, no mesmo diretório em que estão os arquivos do repositório, chamar o web crawler no seguinte formato:

        python crawler.py <comando> <url>

Onde:
	<comando> pode ser:
		--print : imprime resultados na tela
		--save_csv : salva dados em arquivo csv
		--save_json : salva dados em arquivo json
		OBS.: --save_csv e --save_json salvam os arquivos na mesma pasta em que estiver o arquivo crawler.py

<url> deve ser um dos URLs suportados pelo crawler:
	"https://www.vultr.com/products/cloud-compute/#pricing"
	"https://www.digitalocean.com/pricing/"
