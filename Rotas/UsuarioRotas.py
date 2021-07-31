from fastapi import APIRouter, HTTPException

from Acoes.UsuarioAcoes import UsuarioAcoes
from Model.Usuario import Usuario
from Repositorio.Mongo.Configuracao.MongoBasico import MongoBasico
from Repositorio.Mongo.UsuarioRepository import UsuarioRepository

router = APIRouter(
    prefix="/usuarios",
    responses={404: {"Descrição": "Não Encontrado"}},
)


@router.get("/{usuario_id}")
async def busca_usuario(usuario_id: str):
    # verificar posteriormente a possibilidade de criar e  validar um Usuário somente com id
    # para facilitar o processo de recuperar do banco de dados com base no nome da classe.
    resultado = UsuarioRepository.recupera_um(_id=usuario_id)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return {"usuario_id": resultado.__dict__}


@router.post("/")
async def salva_usuario(usuario: Usuario):

    # valida as regras necessárias no objeto

    # realiza as acoes necessárias no objeto
    UsuarioAcoes(usuario, 'create')

    # conclui as operacoes no banco
    resultado = MongoBasico.comitar()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Erro ao salvar o objeto.")
    return {"resultado": resultado[0].bulk_api_result}
