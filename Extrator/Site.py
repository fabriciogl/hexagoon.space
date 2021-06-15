# Copyright (c) 2021. QuickTest. App de estudo por questões. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.

import bs4
from Conexoes.Internet.Proxy import ConectorRequest




def qconcurso_crawler():
    """
    Função que extrai informações do site do QConcurso e salva em banco de dados

    :return: None
    """

    conector = ConectorRequest(proxy=False, header=True)

    for i in range(0, 996):
        pagina = '' if i == 0 else f'&page={i}'
        resultado = conector.request_get(f'https://www.qconcursos.com/questoes-de-concursos/questoes?institute_ids%5B%5D=58{pagina}')

        processo_cru = bs4.BeautifulSoup(resultado.content, 'lxml', from_encoding=resultado.encoding)


qconcurso_crawler()