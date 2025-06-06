# dao/fidelidade_dao.py

import uuid
from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.fidelidade import Fidelidade
import logging

logger = logging.getLogger(__name__)


class FidelidadeDAO(FirebaseDAO):
    """
    DAO responsável por operações de CRUD em programas de fidelidade.
    Collection padrão: "fidelidade".
    """

    def __init__(self):
        super().__init__(collection="fidelidade")

    def criar(self, fidelidade: Fidelidade) -> Optional[str]:
        """
        Cria um novo registro de fidelidade.

        Args:
            fidelidade: Instância de Fidelidade.

        Returns:
            str: ID gerado ou None se falhou.
        """
        try:
            if not isinstance(fidelidade, Fidelidade):
                raise ValueError("Parâmetro deve ser uma instância de Fidelidade")

            if not fidelidade.id:
                fidelidade.id = str(uuid.uuid4())

            sucesso = super().criar(fidelidade.id, fidelidade.to_dict())
            if sucesso:
                return fidelidade.id
            return None
        except Exception as e:
            logger.error(f"[fidelidade] Erro ao criar programa: {e}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Fidelidade]:
        """
        Busca programa de fidelidade pelo ID.

        Args:
            id: ID do programa.

        Returns:
            Fidelidade: Instância ou None se não encontrado.
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Fidelidade.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"[fidelidade] Erro ao buscar por ID '{id}': {e}")
            return None

    def listar_todos(self) -> List[Fidelidade]:
        """
        Lista todos os programas de fidelidade.

        Returns:
            List[Fidelidade]: Lista de instâncias.
        """
        try:
            dados = super().listar_todos()
            return [Fidelidade.from_dict(item) for item in dados if item]
        except Exception as e:
            logger.error(f"[fidelidade] Erro ao listar programas: {e}")
            return []

    def atualizar(self, fidelidade: Fidelidade) -> bool:
        """
        Atualiza um registro de fidelidade existente.

        Args:
            fidelidade: Instância com ID preenchido.

        Returns:
            bool: True se atualizado com sucesso.
        """
        try:
            if not isinstance(fidelidade, Fidelidade):
                raise ValueError("Parâmetro deve ser uma instância de Fidelidade")
            if not fidelidade.id:
                raise ValueError("ID da fidelidade não informado para atualização")

            return super().atualizar(fidelidade.id, fidelidade.to_dict())
        except Exception as e:
            logger.error(f"[fidelidade] Erro ao atualizar registro '{getattr(fidelidade, 'id', None)}': {e}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Deleta um registro de fidelidade pelo ID.

        Args:
            id: ID do registro.

        Returns:
            bool: True se excluído com sucesso.
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"[fidelidade] Erro ao deletar registro '{id}': {e}")
            return False
