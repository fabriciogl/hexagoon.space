#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from bson import ObjectId
from starlette.responses import Response

from api.v1.artigo.model.artigo_model import Artigo
from api.v1.autenticacao.endpoint.autenticacao_endpoints import AutenticacaoEndpoints
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigo, ModalidadeArtigoInUpdate
from api.v1.role.model.role_model import Role
from api.v1.usuario.model.usuario_model import UsuarioHandlerToken, Usuario
from recursos.acoes_initiallizer import AcoesInitiallizer
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
        renderiza a tela de administracao de usuarios
        """

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
        artigo_data = self.handler.operacao.find_one(id=self._id, collection=Artigo.Config.title)
        self.data: Artigo = Artigo(**artigo_data)
        self.data.corpo = json.loads(self.data.corpo)

        # recupera todas as modalidades de artigo ordenando pela escolhida
        modalidades_artigo_data = self.handler.operacao.find_all(collection=ModalidadeArtigo.Config.title)
        modalidades_artigo: [ModalidadeArtigoInUpdate] = [ModalidadeArtigoInUpdate(**ma) for ma in modalidades_artigo_data]
        modalidades_ordenadas = [self.data.modalidade_artigo]
        modalidades_artigo.remove(self.data.modalidade_artigo)
        modalidades_ordenadas.extend(modalidades_artigo)

        # recupera todos os artigos de mesma modalidade
        artigos_data = self.handler.operacao.find_all(
            where={'modalidade_artigo._id': self.data.modalidade_artigo.id},
            projection=['titulo'],
            collection='artigos'
        )
        artigos = [Artigo(**a) for a in artigos_data]

        self.handler.sucesso = templates.TemplateResponse(
            "artigos/artigo_individual.html",
            {
                "request": self.handler.request,
                "artigo": self.data,
                "artigos": artigos,
                "modalidades_artigo": modalidades_ordenadas
            }
        )

    def acao_4(self):
        """ use : [articleAll-1]"""

        artigo = Artigo()
        lista_modalidade_artigo = [ModalidadeArtigo()]
        if artigos_data := self.handler.operacao.find_all(collection='artigos'):

            # artigo a ser exibido na página inicial
            artigos_ordenados = sorted(artigos_data, key=lambda x: x['criado_em'], reverse=True)
            primeiro_artigo = artigos_ordenados[-1]
            artigo: Artigo = Artigo(**primeiro_artigo)
            artigo.corpo = json.loads(artigo.corpo)

            # seleciona os últimos cinco artigos para serem apresetandos na tela inicial
            self.data = [Artigo(**a) for a in artigos_ordenados[:5]]

        # recupera todas as modalidades de artigo
        if modalidades_artigos_data := self.handler.operacao.find_all(collection=ModalidadeArtigo.Config.title):
            lista_modalidade_artigo: [ModalidadeArtigo] = [ModalidadeArtigo(**modalidade) for modalidade in
                                                           modalidades_artigos_data]

        self.handler.sucesso = templates.TemplateResponse(
            "artigos/landing_page_artigos.html",
            {
                "request": self.handler.request,
                "artigos": self.data,
                "artigo": artigo,
                "modalidades_artigo": lista_modalidade_artigo
            }
        )

    def acao_5(self):
        """ use : [articleGroup-1]"""

        # recupera todos os artigos de mesma modalidade
        artigos_data = self.handler.operacao.find_all(
            where={'modalidade_artigo._id': ObjectId(self._id)},
            projection=['titulo'],
            collection='artigos'
        )
        artigos = [Artigo(**a) for a in artigos_data]

        # recupera todas as modalidades de artigo ordenando pela escolhida
        modalidades_artigo_data = self.handler.operacao.find_all(collection=ModalidadeArtigo.Config.title)
        modalidades_artigo: [ModalidadeArtigoInUpdate] = [ModalidadeArtigoInUpdate(**ma) for ma in modalidades_artigo_data]
        # recupera o primeiro para ser exibido, se não existir gera um dinamicamente.
        if len(artigos) != 0:
            artigo: Artigo = Artigo(**self.handler.operacao.find_one(
            id=artigos[0].id,
            collection='artigos'
        ))
            modalidades_ordenadas = [artigo.modalidade_artigo]
            modalidades_artigo.remove(artigo.modalidade_artigo)
            modalidades_ordenadas.extend(modalidades_artigo)

        else:
            artigo = Artigo(
                titulo="Novo Artigo do Grupo",
                corpo=json.dumps({"blocks": [
                    {"data": {"level": 2, "text": "Bem Vindo ao Hexagoon"}, "id": "VlSDl34iWg", "type": "header"}]})
            )
            modalidades_ordenadas = [m for m in modalidades_artigo if str(m.id) == self._id]
            modalidades_ordenadas.extend([m for m in modalidades_artigo if str(m.id) != self._id])

        artigo.corpo = json.loads(artigo.corpo)

        self.handler.sucesso = templates.TemplateResponse(
            "artigos/artigo_individual.html",
            {
                "request": self.handler.request,
                "artigos": artigos,
                "artigo": artigo,
                "modalidades_artigo": modalidades_ordenadas
            }
        )
