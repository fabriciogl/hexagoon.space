#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from bson import ObjectId
from fastapi.testclient import TestClient

from api.v1.artigo.model.artigo_model import Artigo
from config import settings
from main import app

client = TestClient(app)


class TestArtigoEndpoints:
    token = None
    id_artigo = None
    novo_id = None
    modalidade_artigo_id = None

    @staticmethod
    def test_find(client: TestClient, operacao):
        TestArtigoEndpoints.token = client.post(
            "/autenticacao",
            json={"email": settings.root_email, "senha": settings.root_pass}
        ).json().get('token')

        response = client.get(
            f"artigo/{TestArtigoEndpoints.id_artigo}",
            headers={'Authorization': f'Bearer {TestArtigoEndpoints.token}'}
        )
        assert response.status_code == 200
        assert response.json().get('_id') == TestArtigoEndpoints.id_artigo

    @staticmethod
    def test_create(client: TestClient, operacao):
        response = client.post(
            "artigo",
            json={
                "titulo": "Erick Hobsbawn",
                "corpo": json.dumps("eric@hexsaturn.space"),
                "modalidade_artigo_id": TestArtigoEndpoints.modalidade_artigo_id
            },
            headers={'Authorization': f'Bearer {TestArtigoEndpoints.token}'}
        )

        novo_artigo = Artigo(**operacao.find_one(collection='artigos', where={'titulo': 'Erick Hobsbawn'}))
        TestArtigoEndpoints.novo_id = str(novo_artigo.id)

        assert response.status_code == 201
        assert response.json().get('_id') == str(novo_artigo.id)

    @staticmethod
    def test_update(client: TestClient, operacao):
        response = client.put(
            f"artigo/{TestArtigoEndpoints.novo_id}",
            json={"titulo": "João do Pulo"},
            headers={'Authorization': f'Bearer {TestArtigoEndpoints.token}'}
        )

        update_usuario = Artigo(**operacao.find_one(collection='artigos', id=TestArtigoEndpoints.novo_id))

        assert response.status_code == 200
        assert update_usuario.titulo == "João do Pulo"

    @staticmethod
    def test_delete(client: TestClient, operacao):
        response = client.delete(
            f"artigo/{TestArtigoEndpoints.novo_id}",
            headers={'Authorization': f'Bearer {TestArtigoEndpoints.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        delete_usuario = Artigo(
            **operacao.find_one(collection='artigos', id=TestArtigoEndpoints.novo_id, soft_deleteds=True))

        assert response.status_code == 200
        assert delete_usuario.deletado_em is not None
        assert delete_usuario.deletado_por is not None

    @staticmethod
    def test_artigo_not_found(client: TestClient, operacao):
        response = client.get(
            f"artigo/{ObjectId(b'123456789012')}",
            headers={'Authorization': f'Bearer {TestArtigoEndpoints.token}'}
        )

        assert response.status_code == 406

    @staticmethod
    def test_delete_again(client: TestClient, operacao):
        response = client.delete(
            f"artigo/{TestArtigoEndpoints.novo_id}",
            headers={'Authorization': f'Bearer {TestArtigoEndpoints.token}'}
        )

        assert response.status_code == 406
