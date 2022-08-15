#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from bson import ObjectId
from starlette.testclient import TestClient

from api.v1.role.model.role_model import Role
from config import settings


class TestRoleEndpoints:

    token = None
    id_root = None
    novo_id = None

    @staticmethod
    def test_find(client: TestClient, operacao):

        TestRoleEndpoints.token = client.post(
            "/autenticacao",
            json={"email": settings.root_email, "senha": settings.root_pass}
        ).json().get('token')

        response = client.get(
            f"role/{TestRoleEndpoints.id_root}",
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )
        assert response.status_code == 200
        assert response.json().get('_id') == TestRoleEndpoints.id_root
        assert response.json().get('sigla')
        assert response.json().get('descricao')

    @staticmethod
    def test_create(client: TestClient, operacao):

        response = client.post(
            "role",
            json={"sigla": "pro", "descricao": "acesso de conta paga"},
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        nova_role = Role(
            **operacao.find_one(collection='roles', where={'sigla': 'pro'})
        )
        TestRoleEndpoints.novo_id = nova_role.id

        assert response.status_code == 201
        assert response.json().get('_id') == str(nova_role.id)

    @staticmethod
    def test_update(client: TestClient, operacao):
        response = client.put(
            f"role/{TestRoleEndpoints.novo_id}",
            json={"sigla": "paid"},
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        update_role = Role(**operacao.find_one(collection='roles', id=TestRoleEndpoints.novo_id))

        assert response.status_code == 200
        assert update_role.sigla == "paid"

    @staticmethod
    def test_add_predencia(client: TestClient, operacao):
        response = client.put(
            f"role/{TestRoleEndpoints.id_root}/adiciona_sub_role",
            json={"sub_role": f"{TestRoleEndpoints.novo_id}"},
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        assert response.status_code == 201
        assert response.json().get('_id')
        assert {"sigla": "paid"} in response.json().get('sub_roles')

    @staticmethod
    def test_remove_predencia(client: TestClient, operacao):
        response = client.put(
            f"role/{TestRoleEndpoints.id_root}/remove_sub_role",
            json={"sub_role": f"{TestRoleEndpoints.novo_id}"},
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        assert response.status_code == 200
        assert response.json().get('_id')
        assert {"sigla": "paid"} not in response.json().get('sub_roles')

    @staticmethod
    def test_delete(client: TestClient, operacao):
        response = client.delete(
            f"role/{TestRoleEndpoints.novo_id}",
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        delete_role = Role(**operacao.find_one(collection='roles', id=TestRoleEndpoints.novo_id, soft_deleteds=True))

        assert response.status_code == 200
        assert delete_role.deletado_em is not None
        assert delete_role.deletado_por is not None

    @staticmethod
    def test_not_found(client: TestClient, operacao):
        response = client.get(
            f"role/{ObjectId(b'123456789012')}",
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        assert response.status_code == 406