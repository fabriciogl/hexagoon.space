# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.
import json
import os
import sys
import time
import bs4
import random
import datetime
import pandas as pd
from Conexoes.Internet.Proxy import ConectorRequest


class QConcurso:
    """
    Classe para extração das questões e respostas do QConcurso
    """

    def __init__(self):
        """

        """
        self.connector = ConectorRequest(proxy=False, header=True, timeout=5)

    def crawler_paginas(self):
        """
        Função que extrai informações do site do QConcurso e salva em banco de dados
        """

        conector = ConectorRequest(proxy=True, header=True, timeout=5)

        for i in range(230, 997):
            try:
                resposta = conector.request_get(
                    f'https://www.qconcursos.com/questoes-de-concursos/questoes?institute_ids%5B%5D=58'
                    f'&page={i}')
                # Caso seja de sucesso salva o xml
                with open(f'Documentos/WebPages/itamaraty-{i}.html', mode='w') as localfile:
                    localfile.write(resposta.content.decode("utf-8"))

                print(i)
                time.sleep(random.randrange(10))
            except:
                print(f'Erro na página {i}')
                time.sleep(random.randrange(10))
                continue

    def extrai_questao(self):
        """
        Função que extrai as informações de cada questão
        """

        questoes = []
        for file in os.listdir('Documentos/WebPages/'):
            if file.endswith("html"):
                pagina = open(f'Documentos/WebPages/{file}', mode='r')
                paginaXML = bs4.BeautifulSoup(pagina.read(), 'lxml')
                for question in paginaXML.find_all('div', 'js-question-item'):
                    qId = question.find('div', 'q-id').find('a').text
                    qAssuntos = ",".join([assunto.text for assunto in
                                          question.find('div', 'q-question-breadcrumb').find_all('a', 'q-link')])
                    infos = [info.text for info in question.find('div', 'q-question-info').find_all('span')]
                    qConteudo = question.find('div', 'q-question-enunciation').text

                    questoes.append({'id': qId,
                                     'assuntos': qAssuntos.strip(),
                                     'ano': infos[0].split(':')[1].strip(),
                                     'banca': infos[1].split(':')[1].strip(),
                                     'orgao': infos[2].split(':')[1].strip(),
                                     'conteudo': qConteudo
                                     })

        arquivo_df = pd.Dataframe(questoes)
        arquivo_df.to_feather(f'{datetime.date.today().strftime("%Y%m%d")}-questoesItamaraty')

    def request_url(self, questao: str) -> str:
        """
        Funcao para ser usado no apply do dataframe de questoes
        :param questao: string da questão a ser consultada
        :return: string da resposta com certo ou errado
        """

        url = f'https://www.qconcursos.com/api/questions/{questao.replace("Q", "")}/answer?'
        data = {"answer": f"{random.choice(['C', 'E'])}"}
        cookie = {
            "remember_user_token": "W1sxMjE4MDkyXSwiQzZLWlBqVWc2WXVOQWlVMkZaMTQiLCIxNjI0Mjk0NDcxLjI2MjQxMzUiXQ%3D%3D--ddad0c5251ff9eddc8b7f7c84374d46946c3ecf5"}

        r = self.connector.request_post(url=url, formulario=data, cookies=cookie)

        if r.status_code == 200:
            r_json = json.loads(r.text).get('resolve')

            espera = random.randint(25, 35)
            print(f'{questao}-{data["answer"]}-{r_json}-{espera}')
            time.sleep(espera)

            if r_json["status"] == "correct":
                return "E"
            if r_json["status"] == "wrong":
                if r_json["right_answer"] == "X":
                    return "A"
                return "C"
        else:
            print(r.text)
            sys.exit(79)

    def crawler_resposta(self=None, inicio: int = 0, fim: int = 0):
        """
        Função para extrair as repostas das questões diretamente do site
        """

        arquivo_df = pd.read_feather('Documentos/WebPages/questoesItamaraty')

        arquivo_df_reduzido = arquivo_df.iloc[inicio:fim, :]

        arquivo_df_reduzido['respostas'] = arquivo_df_reduzido['id'].map(self.request_url)

        arquivo_df_reduzido.reset_index().to_feather(f'Documentos/WebPages/respotas-({inicio}-{fim})')


# qconcurso = QConcurso()
# qconcurso.crawler_resposta(inicio=1697, fim=2500)
