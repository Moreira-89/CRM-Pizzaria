from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.usuario import Usuario
import logging

logger = logging.getLogger(__name__)

class UsuarioDAO(FirebaseDAO):
    """
    DAO responsável por manipulações CRUD de usuários, agora incluindo senha_hash.
    Collection padrão: "usuarios".
    """

    def __init__(self):
        super().__init__(collection="usuarios")

    def criar(self, usuario: Usuario) -> Optional[str]:
        """
        Cria um novo usuário. Deve ter 'usuario.id' e campo 'senha_hash' já preenchido.

        Args:
            usuario: Instância de Usuario (ou subclasse) com todos os campos, inclusive senha_hash.

        Returns:
            str: ID do usuário criado, ou None se falhou.
        """
        try:
            if not isinstance(usuario, Usuario):
                raise ValueError("Parâmetro deve ser uma instância de Usuario")
            if not usuario.id:
                raise ValueError("Usuário precisa ter um ID antes de criar")
            if not usuario.senha_hash:
                raise ValueError("Usuário precisa ter senha_hash preenchido antes de criar")

            sucesso = super().criar(usuario.id, usuario.to_dict())
            if sucesso:
                return usuario.id
            return None
        except Exception as e:
            logger.error(f"[usuarios] Erro ao criar usuário: {e}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Usuario]:
        """
        Busca usuário pelo ID. Retorna instância de Usuario, com o campo senha_hash carregado.
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
        Lista todos os usuários. Cada dicionário virá com senha_hash, mas não exponha em lista final.
        """
        try:
            dados = super().listar_todos()
            return [Usuario.from_dict(item) for item in dados if item]
        except Exception as e:
            logger.error(f"[usuarios] Erro ao listar usuários: {e}")
            return []

    def atualizar(self, usuario: Usuario) -> bool:
        """
        Atualiza dados de um usuário existente. Inclui possibilidade de trocar senha_hash.
        """
        try:
            if not isinstance(usuario, Usuario):
                raise ValueError("Parâmetro deve ser uma instância de Usuario")
            if not usuario.id:
                raise ValueError("ID do usuário não informado para atualização")
            if not usuario.senha_hash:
                raise ValueError("Usuário deve ter senha_hash válido ao atualizar")

            return super().atualizar(usuario.id, usuario.to_dict())
        except Exception as e:
            logger.error(f"[usuarios] Erro ao atualizar usuário '{getattr(usuario, 'id', None)}': {e}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Deleta um usuário pelo ID.
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"[usuarios] Erro ao deletar usuário '{id}': {e}")
            return False

    def autenticar(self, login_id: str, senha_plain: str) -> bool:
        """
        Verifica se o usuário existe e se o hash de senha corresponde ao hash armazenado.
        login_id: corresponde ao campo 'id' do usuário (ou e-mail, se você trocar id por e-mail).
        """
        try:
            usuario = self.buscar_por_id(login_id)
            if not usuario:
                return False
            # Gera hash da senha fornecida e compara
            hash_fornecido = Usuario._gerar_hash(senha_plain)
            return usuario.senha_hash == hash_fornecido
        except Exception as e:
            logger.error(f"[usuarios] Erro ao autenticar usuário '{login_id}': {e}")
            return False
