#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from bson import ObjectId
from fastapi.testclient import TestClient

from api.v1.artigo.model.artigo_model import Artigo
from api.v1.modalidade_artigo.model.modalidade_artigo_model import ModalidadeArtigo
from config import settings
from main import app

client = TestClient(app)


class TestModalidadeArtigoEndpoints:
    token = None
    id_artigo = None
    novo_id = None

    @staticmethod
    def test_find(client: TestClient, operacao):
        TestModalidadeArtigoEndpoints.token = client.post(
            "/autenticacao",
            json={"email": settings.root_email, "senha": settings.root_pass}
        ).json().get('token')

        response = client.get(
            f"modalidade_artigo/{TestModalidadeArtigoEndpoints.id_artigo}",
            headers={'Authorization': f'Bearer {TestModalidadeArtigoEndpoints.token}'}
        )
        assert response.status_code == 200
        assert response.json().get('_id') == TestModalidadeArtigoEndpoints.id_artigo

    @staticmethod
    def test_create(client: TestClient, operacao):
        response = client.post(
            "modalidade_artigo",
            json={
                "nome": "Hexagoon MongoDB"
            },
            headers={'Authorization': f'Bearer {TestModalidadeArtigoEndpoints.token}'}
        )

        novo_modalidade_artigo = ModalidadeArtigo(**operacao.find_one(
            collection='modalidadeArtigos',
            where={'nome': 'Hexagoon MongoDB'}
        ))
        TestModalidadeArtigoEndpoints.novo_id = str(novo_modalidade_artigo.id)

        assert response.status_code == 201
        assert response.json().get('_id') == str(novo_modalidade_artigo.id)

    @staticmethod
    def test_update(client: TestClient, operacao):
        response = client.put(
            f"modalidade_artigo/{TestModalidadeArtigoEndpoints.novo_id}",
            json={"nome": "João do Pulo"},
            headers={'Authorization': f'Bearer {TestModalidadeArtigoEndpoints.token}'}
        )

        update_modalidade_artigo = ModalidadeArtigo(**operacao.find_one(collection='modalidadeArtigos', id=TestModalidadeArtigoEndpoints.novo_id))

        assert response.status_code == 200
        assert update_modalidade_artigo.nome == "João do Pulo"

    @staticmethod
    def test_delete(client: TestClient, operacao):
        response = client.delete(
            f"modalidade_artigo/{TestModalidadeArtigoEndpoints.novo_id}",
            headers={'Authorization': f'Bearer {TestModalidadeArtigoEndpoints.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        delete_modalide_artigo = ModalidadeArtigo(
            **operacao.find_one(collection='modalidadeArtigos', id=TestModalidadeArtigoEndpoints.novo_id, soft_deleteds=True))

        assert response.status_code == 200
        assert delete_modalide_artigo.deletado_em is not None
        assert delete_modalide_artigo.deletado_por is not None

    @staticmethod
    def test_modalidade_not_found(client: TestClient, operacao):
        response = client.get(
            f"modalidade_artigo/{ObjectId(b'123456789012')}",
            headers={'Authorization': f'Bearer {TestModalidadeArtigoEndpoints.token}'}
        )

        assert response.status_code == 406

    @staticmethod
    def test_delete_again(client: TestClient, operacao):
        response = client.delete(
            f"modalidade_artigo/{TestModalidadeArtigoEndpoints.novo_id}",
            headers={'Authorization': f'Bearer {TestModalidadeArtigoEndpoints.token}'}
        )

        assert response.status_code == 406
