#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from sqlalchemy import select, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from starlette.responses import Response

from api.v1.artigo.model.artigo_model import Artigo
from api.v1.autenticacao.endpoint.autenticacao_endpoints import AutenticacaoEndpoints
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigo
from api.v1.role.model.role_model import Role
from recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioHandlerToken, Usuario
from templates.Jinja2 import create_templates

templates = create_templates()


class HTMLAcoes(AcoesInitiallizer):
    # declara o tipo do model

    def acao_1(self):
        """ use : [login-1] """

        self.handler.sucesso = templates.TemplateResponse(
            "login.html",
            {
                "request": self.handler.request
            }
        )

    def acao_2(self):
        """ use : [admin-1]
        renderiza a tela de administracao de usuarios"""

        usuarios_data = self.handler.operacao.find_all(collection='usuarios')
        usuarios = []
        # converte usuarios_data para usuario, populando campos None
        for usuario in usuarios_data:
            usuarios.append(Usuario(**usuario))

        roles_data = self.handler.operacao.find_all(collection='roles')
        roles = []
        for role in roles_data:
            roles.append(Role(**role))

        self.model: UsuarioHandlerToken = self.data

        html_response = templates.TemplateResponse(
            "usuarios.html",
            {
                "request": self.handler.request,
                "usuarios": usuarios,
                "roles": roles
            }
        )

        token = AutenticacaoEndpoints.create_token(self.handler)

        headers = {'authorization': token.token}

        self.handler.sucesso = Response(content=html_response.body, headers=headers, media_type="text/html")

    def acao_3(self):
        """ use : [article-1] """

        # recupera o artigo que será exibido
        # select_query = select(Artigo).where((Artigo.id == self._id))
        # self.data: Artigo = self.handler.sessao.execute(select_query).scalar_one()
        # self.data.corpo = json.loads(self.data.corpo)
        #
        # # recupera todas as modalidades de artigo ordenando pela escolhida
        # modalidade_artigo: ModalidadeArtigo = self.handler.sessao.query(ModalidadeArtigo).all()
        # modalidade_escolhida_ordenada = [self.data.modalidade_artigo]
        # modalidade_artigo.remove(self.data.modalidade_artigo)
        # modalidade_escolhida_ordenada.extend(modalidade_artigo)
        #
        # self.handler.sucesso = templates.TemplateResponse(
        #     "artigos/artigo_individual.html",
        #     {
        #         "request": self.handler.request,
        #         "artigo": self.data,
        #         "artigos": self.data.modalidade_artigo.artigos,
        #         "modalidadesArtigo": modalidade_escolhida_ordenada
        #     }
        # )

    def acao_4(self):
        """ use : [articleAll-1]"""

        artigo = Artigo()
        lista_modalidade_artigo = [ModalidadeArtigo()]
        if artigos_data := self.handler.operacao.find_all(collection='artigos'):
            self.data = [Artigo(**a) for a in artigos_data]

            # artigo a ser exibido na página inicial
            primeiro_artigo = sorted(artigos_data, key=lambda x: x['criado_em'])[0]
            artigo: Artigo = Artigo(**primeiro_artigo)
            artigo.corpo = json.loads(artigo.corpo)

        # recupera todas as modalidades de artigo
        if modalidades_artigos_data := self.handler.operacao.find_all(collection='modalidadeArtigos'):
            lista_modalidade_artigo: [ModalidadeArtigo] = [ModalidadeArtigo(**modalidade) for modalidade in modalidades_artigos_data]

        self.handler.sucesso = templates.TemplateResponse(
            "artigos/landing_page_artigos.html",
            {
                "request": self.handler.request,
                "artigos": self.data,
                "artigo": artigo,
                "modalidadesArtigo": lista_modalidade_artigo
            }
        )

    def acao_5(self):
        """ use : [articleGroup-1]"""

        # try:
        #     query = select(ModalidadeArtigo).filter_by(id=self._id)
        #     if data := self.handler.sessao.execute(query).scalar_one():
        #         self.data: ModalidadeArtigo = data
        #
        # except NoResultFound:
        #     raise SQLException('Não há grupos de artigos.')
        #
        # artigo: Artigo = self.data.artigos[0] if len(self.data.artigos) != 0 else Artigo(
        #     titulo="Novo Artigo do Grupo",
        #     corpo=json.dumps({"blocks": [{"data": {"level": 2, "text": "Bem Vindo ao Hexagoon"}, "id": "VlSDl34iWg", "type": "header"}]})
        # )
        # artigo.corpo = json.loads(artigo.corpo)
        #
        # # recupera todas as modalidades de artigo ordenando pela escolhida
        # modalidade_artigo: ModalidadeArtigo = self.handler.sessao.query(ModalidadeArtigo).all()
        # modalidade_escolhida_ordenada = [self.data]
        # modalidade_artigo.remove(self.data)
        # modalidade_escolhida_ordenada.extend(modalidade_artigo)
        #
        # self.handler.sucesso = templates.TemplateResponse(
        #     "artigos/artigo_individual.html",
        #     {
        #         "request": self.handler.request,
        #         "artigos": self.data.artigos,
        #         "artigo": artigo,
        #         "modalidadesArtigo": modalidade_escolhida_ordenada
        #     }
        # )