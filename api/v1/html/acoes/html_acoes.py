#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from sqlalchemy import select, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from starlette.responses import Response

from api.v1.autenticacao.endpoint.autenticacao_endpoints import AutenticacaoEndpoints
from recursos.acoes_initiallizer import AcoesInitiallizer
from recursos.basic_exceptions.sql_exceptions import SQLException
from api.v1.usuario.model.usuario_model import UsuarioOut
from banco_dados.sql_alchemy.configuracao.oracle.data_oracle import Usuario, Artigo, Role, ModalidadeArtigo
from templates.Jinja2 import create_templates

templates = create_templates()


class HTMLAcoes(AcoesInitiallizer):
    # declara o tipo do model
    # model:
    # data:

    def acao_1(self):
        """ use : [login-1] """

        self.handler.sucesso = templates.TemplateResponse(
            "login.html",
            {
                "request": self.handler.request
            }
        )

    def acao_2(self):
        """ use : [admin-1] """

        try:
            if data := self.handler \
                    .sessao \
                    .query(Usuario) \
                    .options(
                joinedload(
                    Usuario.criado_por
                ),
                joinedload(
                    Usuario.alterado_por
                ),
                joinedload(
                    Usuario.deletado_por
                ),
                joinedload(
                    Usuario.a_roles
                )
            ) \
                    .all():
                self.data = data

        except NoResultFound:
            raise SQLException('Não há objetos do tipo usuário.')

        perfis: Role = self.handler.sessao.query(Role).all()

        self.model: UsuarioOut = self.data

        html_response = templates.TemplateResponse(
            "usuarios.html",
            {
                "request": self.handler.request,
                "usuarios": self.data,
                "perfis": perfis
            }
        )

        token = AutenticacaoEndpoints.create_token(self.handler)

        headers = {'authorization': token.token}

        self.handler.sucesso = Response(content=html_response.body, headers=headers, media_type="text/html")

    def acao_3(self):
        """ use : [article-1] """

        # recupera o artigo que será exibido
        select_query = select(Artigo).where((Artigo.id == self._id))
        self.data: Artigo = self.handler.sessao.execute(select_query).scalar_one()
        self.data.corpo = json.loads(self.data.corpo)

        # recupera todas as modalidades de artigo ordenando pela escolhida
        modalidade_artigo: ModalidadeArtigo = self.handler.sessao.query(ModalidadeArtigo).all()
        modalidade_escolhida_ordenada = [self.data.modalidade_artigo]
        modalidade_artigo.remove(self.data.modalidade_artigo)
        modalidade_escolhida_ordenada.extend(modalidade_artigo)

        self.handler.sucesso = templates.TemplateResponse(
            "artigos/artigo_individual.html",
            {
                "request": self.handler.request,
                "artigo": self.data,
                "artigos": self.data.modalidade_artigo.artigos,
                "modalidadesArtigo": modalidade_escolhida_ordenada
            }
        )

    def acao_4(self):
        """ use : [articleAll-1]"""

        # forma de se recuperar somente algumas colunas da tabela
        select_query = select(Artigo.id, Artigo.titulo).order_by(desc(Artigo.criado_em))

        if data := self.handler.sessao.execute(select_query).fetchall():
            self.data = [Artigo(id=a[0], titulo=a[1]) for a in data]

        # recupera o artigo 1, que será o artigo exibido na página principal
        select_query = select(Artigo).filter_by(id=1)

        artigo: Artigo = self.handler.sessao.execute(select_query).scalar_one()
        artigo.corpo = json.loads(artigo.corpo)

        # recupera todas as modalidades de artigo
        modalidade_artigo: ModalidadeArtigo = self.handler.sessao.query(ModalidadeArtigo).all()

        self.handler.sucesso = templates.TemplateResponse(
            "artigos/landing_page_artigos.html",
            {
                "request": self.handler.request,
                "artigos": self.data,
                "artigo": artigo,
                "modalidadesArtigo": modalidade_artigo
            }
        )

    def acao_5(self):
        """ use : [articleGroup-1]"""

        try:
            query = select(ModalidadeArtigo).filter_by(id=self._id)
            if data := self.handler.sessao.execute(query).scalar_one():
                self.data: ModalidadeArtigo = data

        except NoResultFound:
            raise SQLException('Não há grupos de artigos.')

        artigo: Artigo = self.data.artigos[0] if len(self.data.artigos) != 0 else Artigo(
            titulo="Novo Artigo do Grupo",
            corpo=json.dumps({"blocks": [{"data": {"level": 2, "text": "Bem Vindo ao Hexagoon"}, "id": "VlSDl34iWg", "type": "header"}]})
        )
        artigo.corpo = json.loads(artigo.corpo)

        # recupera todas as modalidades de artigo ordenando pela escolhida
        modalidade_artigo: ModalidadeArtigo = self.handler.sessao.query(ModalidadeArtigo).all()
        modalidade_escolhida_ordenada = [self.data]
        modalidade_artigo.remove(self.data)
        modalidade_escolhida_ordenada.extend(modalidade_artigo)

        self.handler.sucesso = templates.TemplateResponse(
            "artigos/artigo_individual.html",
            {
                "request": self.handler.request,
                "artigos": self.data.artigos,
                "artigo": artigo,
                "modalidadesArtigo": modalidade_escolhida_ordenada
            }
        )
