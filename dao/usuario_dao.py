from typing import Optional, List
from dao.firebase_dao import FirebaseDAO
from models.usuario import Usuario

class UsuarioDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="usuarios")

    def criar(self, usuario: Usuario) -> Optional[str]:
        if not usuario.id:
            raise ValueError("Usuário precisa de um ID")
        if super().criar(usuario.id, usuario.to_dict()):
            return usuario.id
        return None

    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        data = super().buscar_por_id(id)
        if data:
            return Usuario.from_dict(data)
        return None

    def listar_todos(self) -> List[Usuario]:
        dados = super().listar_todos()
        return [Usuario.from_dict(item) for item in dados if item]

    def atualizar(self, usuario: Usuario) -> bool:
        if not usuario.id:
            raise ValueError("ID do usuário não informado para atualização.")
        return super().atualizar(usuario.id, usuario.to_dict())

    def deletar(self, id: str) -> bool:
        return super().deletar(id)