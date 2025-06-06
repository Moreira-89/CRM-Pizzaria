# dao/usuario_dao.py

from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.usuario import Usuario
import logging

logger = logging.getLogger(__name__)


class UsuarioDAO(FirebaseDAO):
    """
    DAO responsável por manipulações CRUD de usuários.
    Collection padrão: "usuarios".
    """

    def __init__(self):
        super().__init__(collection="usuarios")

    def criar(self, usuario: Usuario) -> Optional[str]:
        """
        Cria um novo usuário.

        Args:
            usuario: Instância de Usuario (ou subclasse).

        Returns:
            str: ID do usuário ou None se falhou.
        """
        try:
            if not isinstance(usuario, Usuario):
                raise ValueError("Parâmetro deve ser uma instância de Usuario")
            if not usuario.id:
                raise ValueError("Usuário precisa de um ID antes de criar")

            sucesso = super().criar(usuario.id, usuario.to_dict())
            if sucesso:
                return usuario.id
            return None
        except Exception as e:
            logger.error(f"[usuarios] Erro ao criar usuário: {e}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """
        Busca usuário pelo ID.

        Args:
            id: ID do usuário.

        Returns:
            Usuario: Instância ou None se não encontrado.
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Usuario.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"[usuarios] Erro ao buscar usuário por ID '{id}': {e}")
            return None

    def listar_todos(self) -> List[Usuario]:
        """
        Lista todos os usuários.

        Returns:
            List[Usuario]: Lista de instâncias de Usuario.
        """
        try:
            dados = super().listar_todos()
            return [Usuario.from_dict(item) for item in dados if item]
        except Exception as e:
            logger.error(f"[usuarios] Erro ao listar usuários: {e}")
            return []

    def atualizar(self, usuario: Usuario) -> bool:
        """
        Atualiza dados de um usuário existente.

        Args:
            usuario: Instância de Usuario com ID preenchido.

        Returns:
            bool: True se atualizado com sucesso, False caso contrário.
        """
        try:
            if not isinstance(usuario, Usuario):
                raise ValueError("Parâmetro deve ser uma instância de Usuario")
            if not usuario.id:
                raise ValueError("ID do usuário não informado para atualização")

            return super().atualizar(usuario.id, usuario.to_dict())
        except Exception as e:
            logger.error(f"[usuarios] Erro ao atualizar usuário '{getattr(usuario, 'id', None)}': {e}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Deleta um usuário pelo ID.

        Args:
            id: ID do usuário.

        Returns:
            bool: True se excluído com sucesso, False caso contrário.
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"[usuarios] Erro ao deletar usuário '{id}': {e}")
            return False
