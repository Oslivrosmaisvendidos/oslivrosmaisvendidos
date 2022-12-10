import scrapy
import pandas
import pandas as pd
from pandas import ExcelWriter
from random import randint
import json
cont = 0

class PublishSpider(scrapy.Spider):
    name = "publish"
    allowed_urls = ["https://www.publishnews.com.br"]
    start_urls = ["https://www.publishnews.com.br/ranking/anual/0/{year}/0/0".format(year=year)
    for year in range(2010, 2022)]
    
    def parse(self, response, **kwargs):
        print("*************************DADOS REQUISITADOS*************************")
        titulos = response.css(".pn-ranking-livro-nome")
        vendas = response.css(".pn-ranking-livros-posicao-volume")
        autores = response.css(".pn-ranking-livro-autor")
        editora = response.css(".pn-ranking-livro-editora")
        posicao = response.css(".pn-ranking-livros-posicao-numero")
        global cont

        nomessalvos = []
        vendassalvas = []
        autoressalvos = []
        editorasalva = []
        posicaosalva = []

        lista = [posicaosalva] + [nomessalvos] + [autoressalvos] + [editorasalva] + [vendassalvas] 

        for title in titulos:
            title = title.css(".pn-ranking-livro-nome::text").get()
            nomessalvos += [title]
            cont += 1

        for sell in vendas:
            sell = sell.css(".pn-ranking-livros-posicao-volume::text").get()
            vendassalvas += [sell]

        for author in autores:
            author = author.css(".pn-ranking-livro-autor::text").get()
            autoressalvos += [author]

        for publisher in editora:
            publisher = publisher.css(".pn-ranking-livro-editora::text").get()
            editorasalva += [publisher]
        
        for position in posicao:
            position = position.css(".pn-ranking-livros-posicao-numero::text").get()
            posicaosalva += [position]


        pd.DataFrame(lista).to_csv(f'ano {cont}.csv')
#        pd.DataFrame(lista).to_excel(f'ano {cont}.xlsx')
#        pd.DataFrame(lista).to_json(f'ano {cont}.json')
#        pd.DataFrame(lista).to_tsv(f'ano {cont}.tsv', sep='t')
