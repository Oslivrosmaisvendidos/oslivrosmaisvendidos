Este repositório descreve o funcionamento de um robô que coleta a lista dos livros mais vendidos do Brasil de 2010 até o presente. Seu funcionamento parte de uma amostra coletada pelo portal PublishNews e a divulgação é feita por meio da Geração de Língua Natural.

A primeira parte do código, para a coleta dos dados, é composto da seguinte maneira:


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
        

A segunda parte é responsável por criar as frases por meio da Inteligência Artificial. A seguir, transcrevemos o código. Para esta etapa, utilizamos o Google Colab.


    !git clone https://github.com/ThiagoCF05/Any2Some

    import os os.chdir('Any2Some')

    !pip3 install -r requirements.txt

    !python3 train.py --tokenizer facebook/bart-large
    --model facebook/bart-large
    --src_train 'trainsrc.txt'
    --trg_train 'traintrg.txt'
    --src_dev 'devsrc.txt'
    --trg_dev 'devtrg.txt'
    --epochs 30
    --learning_rate 1e-5
    --batch_size 2
    --early_stop 5
    --max_length 180
    --write_path bart
    --language portuguese
    --verbose
    --batch_status 2
    --cuda

    !python3 evaluate.py --tokenizer facebook/bart-large
    --model bart/model
    --src_test 'testesrc.txt'
    --trg_test 'testetrg.txt'
    --batch_size 4
    --max_length 180
    --write_dir results
    --language portuguese
    --verbose
    --batch_status 16
    --cuda

    from models.bartgen import BARTGen
    batch_size = 4 batch_status = 15 language = 'portuguese' verbose = False device = 'cpu'
    # model
    max_length = 180 tokenizer_path = 'facebook/bart-large' model_path = 'bart/model'
    src_lang = 'pt_XX' trg_lang = 'pt_XX' generator = BARTGen(tokenizer_path, model_path, max_length, device, False)
    import csv import random import pandas import pandas as df aleat = random.randint(2010, 2021)
    with open(f'ano {aleat}.csv', 'r') as file: reader = csv.reader(file, delimiter = '\t') n = 20 #número de linhas do arquivo s = 1 #Número de linhas desejadas filename = f'ano {aleat}.csv' skip = sorted(random.sample(range(n),n-s)) df = pandas.read_csv(file, skiprows=skip) df.to_csv('temp.csv')
    with open('temp.csv', 'r') as file: reader = csv.reader(file, delimiter = '\t') for row in reader: output = generator(row)
    novoTuite = str(output) char_remov = ["[", "]", "'"] for char in char_remov: novoTuite = novoTuite.replace(char, "") print(novoTuite)
