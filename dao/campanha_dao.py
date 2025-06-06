import uuid
from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.campanha import Campanha
import logging

logger = logging.getLogger(__name__)


class CampanhaDAO(FirebaseDAO):
    """
    DAO responsável por CRUD de campanhas de marketing no Firebase RTDB.
    Collection padrão: "campanhas".
    """

    def __init__(self):
        super().__init__(collection="campanhas")

    def criar(self, campanha: Campanha) -> Optional[str]:
        """
        Cria uma nova campanha.

        Args:
            campanha: Instância de Campanha.

        Returns:
            str: ID gerado ou None se falhou.
        """
        try:
            if not isinstance(campanha, Campanha):
                raise ValueError("Parâmetro deve ser uma instância de Campanha")

            if not campanha.id:
                campanha.id = str(uuid.uuid4())

            sucesso = super().criar(campanha.id, campanha.to_dict())
            if sucesso:
                return campanha.id
            return None
        except Exception as e:
            logger.error(f"[campanhas] Erro ao criar campanha: {e}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Campanha]:
        """
        Busca campanha pelo ID.

        Args:
            id: ID da campanha.

        Returns:
            Campanha: Instância ou None se não encontrada.
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Campanha.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"[campanhas] Erro ao buscar campanha por ID '{id}': {e}")
            return None

    def listar_todos(self) -> List[Campanha]:
        """
        Lista todas as campanhas.

        Returns:
            List[Campanha]: Lista de instâncias.
        """
        try:
            dados = super().listar_todos()
            return [Campanha.from_dict(item) for item in dados if item]
        except Exception as e:
            logger.error(f"[campanhas] Erro ao listar campanhas: {e}")
            return []

    def atualizar(self, campanha: Campanha) -> bool:
        """
        Atualiza dados de uma campanha existente.

        Args:
            campanha: Instância de Campanha com ID preenchido.

        Returns:
            bool: True se atualizado com sucesso.
        """
        try:
            if not isinstance(campanha, Campanha):
                raise ValueError("Parâmetro deve ser uma instância de Campanha")
            if not campanha.id:
                raise ValueError("ID da campanha não informado para atualização")

            return super().atualizar(campanha.id, campanha.to_dict())
        except Exception as e:
            logger.error(f"[campanhas] Erro ao atualizar campanha '{getattr(campanha, 'id', None)}': {e}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Deleta uma campanha pelo ID.

        Args:
            id: ID da campanha.

        Returns:
            bool: True se excluído com sucesso.
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"[campanhas] Erro ao deletar campanha '{id}': {e}")
            return False
