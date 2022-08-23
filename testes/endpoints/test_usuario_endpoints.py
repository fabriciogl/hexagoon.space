#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from bson import ObjectId
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from api.v1.usuario.model.usuario_model import Usuario
from config import settings


class TestUsuarioEndpoint:

    token = None
    id_root = None
    novo_id = None

    @staticmethod
    def test_find(client: TestClient, operacao):

        TestUsuarioEndpoint.token = client.post(
            "/autenticacao",
            json={"email": settings.root_email, "senha": settings.root_pass}
        ).json().get('token')

        response = client.get(
            f"usuario/{TestUsuarioEndpoint.id_root}",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )
        assert response.status_code == 200
        assert response.json().get('_id') == TestUsuarioEndpoint.id_root
        assert response.json()['roles'][0]['sigla'] == 'root'

    @staticmethod
    def test_create(client: TestClient, operacao):

        response = client.post(
            "usuario",
            json={"nome": "Erick Hobsbawn", "email": "eric@hexsaturn.space", "senha": "extremo"},
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        novo_usuario = Usuario(**operacao.find_one(collection='usuarios', where={'email': 'eric@hexsaturn.space'}))
        TestUsuarioEndpoint.novo_id = str(novo_usuario.id)

        assert response.status_code == 201
        assert response.json().get('_id') == str(novo_usuario.id)
        assert response.json().get('roles') is None

    @staticmethod
    def test_update(client: TestClient, operacao):
        response = client.put(
            f"usuario/{TestUsuarioEndpoint.id_root}",
            json={"nome": "João do Pulo"},
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        update_usuario = Usuario(**operacao.find_one(collection='usuarios', id=TestUsuarioEndpoint.id_root))

        assert response.status_code == 200
        assert update_usuario.nome == "João do Pulo"

    @staticmethod
    def test_inactivate(client: TestClient, operacao):
        response = client.delete(
            f"usuario/{TestUsuarioEndpoint.novo_id}/inactivate",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        inactivate_usuario = Usuario(**operacao.find_one(collection='usuarios', id=TestUsuarioEndpoint.novo_id))

        assert response.status_code == 200
        assert inactivate_usuario.ativo == False
        assert response.json().get('resultado') == 'usuário inativado.'

    @staticmethod
    def test_delete(client: TestClient, operacao):
        response = client.delete(
            f"usuario/{TestUsuarioEndpoint.novo_id}",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        delete_usuario = Usuario(**operacao.find_one(collection='usuarios', id=TestUsuarioEndpoint.novo_id, soft_deleteds=True))

        assert response.status_code == 200
        assert delete_usuario.deletado_em is not None
        assert delete_usuario.deletado_por is not None

    @staticmethod
    def test_usuario_not_found(client: TestClient, operacao):
        response = client.get(
            f"usuario/{ObjectId(b'123456789012')}",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        assert response.status_code == 406

    @staticmethod
    def test_update_email(client: TestClient, operacao):
        response = client.put(
            f"usuario/{TestUsuarioEndpoint.id_root}",
            json={"email": "joao@hexjupiter.space"},
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        update_usuario = Usuario(**operacao.find_one(collection='usuarios', id=TestUsuarioEndpoint.id_root))

        assert response.status_code == 422
        assert update_usuario.email == settings.root_email

    @staticmethod
    def test_create_email_utilizado(client: TestClient, operacao):

        response = client.post(
            "usuario",
            json={"nome": "Erick Hobsbawn", "email": "eric@hexsaturn.space", "senha": "extremo"},
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        assert response.status_code == 422


    @staticmethod
    def test_delete_again(client: TestClient, operacao):
        response = client.delete(
            f"usuario/{TestUsuarioEndpoint.novo_id}",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        assert response.status_code == 406