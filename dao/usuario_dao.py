from typing import Optional, List
from dao.firebase_dao import FirebaseDAO
from models.usuario import Usuario
import logging

logger = logging.getLogger(__name__)

class UsuarioDAO(FirebaseDAO):
    """DAO responsável por manipular registros de usuários."""

    def __init__(self):
        super().__init__(collection="usuarios")

    def criar(self, usuario: Usuario) -> Optional[str]:
        """Cria um novo usuário."""
        try:
            if not usuario.id:
                raise ValueError("Usuário precisa de um ID")
            if super().criar(usuario.id, usuario.to_dict()):
                return usuario.id
            return None
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """Busca um usuário pelo ID."""
        try:
            data = super().buscar_por_id(id)
            if data:
                return Usuario.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por ID {id}: {str(e)}")
            return None

    def listar_todos(self) -> List[Usuario]:
        """Lista todos os usuários."""
        try:
            dados = super().listar_todos()
            return [Usuario.from_dict(item) for item in dados if item]
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {str(e)}")
            return []

    def atualizar(self, usuario: Usuario) -> bool:
        """Atualiza os dados de um usuário."""
        try:
            if not usuario.id:
                raise ValueError("ID do usuário não informado para atualização.")
            return super().atualizar(usuario.id, usuario.to_dict())
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário {usuario.id}: {str(e)}")
            return False

    def deletar(self, id: str) -> bool:
        """Remove um usuário pelo ID."""
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"Erro ao deletar usuário {id}: {str(e)}")
            return False
