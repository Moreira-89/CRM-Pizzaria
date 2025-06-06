# dao/firebase_dao.py

from abc import ABC
from typing import Any, Dict, List, Optional
from config.firebase_config import FirebaseConfig
import logging

logger = logging.getLogger(__name__)


class FirebaseDAO(ABC):
    """
    Classe abstrata base para operações CRUD com Firebase Realtime Database.
    Todas as DAOs específicas herdam desta classe e fornecem o nome da coleção.
    """

    def __init__(self, collection: str):
        if not collection or not isinstance(collection, str):
            raise ValueError("Nome da coleção deve ser uma string não vazia")
        self._collection = collection
        self._db = FirebaseConfig.get_instance().rtdb.child(collection)

    @property
    def collection(self) -> str:
        """Retorna o nome da coleção no Firebase."""
        return self._collection

    @property
    def db(self):
        """Retorna a referência ao nó da coleção no RTDB."""
        return self._db

    def criar(self, id: str, data: Dict[str, Any]) -> bool:
        """
        Cria um novo registro no Firebase.

        Args:
            id: Identificador único do registro (chave).
            data: Dicionário com os campos a serem salvos.

        Returns:
            bool: True se criado com sucesso, False caso contrário.
        """
        try:
            if not id or not isinstance(id, str):
                raise ValueError("ID deve ser uma string não vazia")

            if not isinstance(data, dict):
                raise ValueError("Data deve ser um dicionário")

            self._db.child(id).set(data)
            logger.info(f"[{self._collection}] Registro criado com sucesso: {id}")
            return True

        except Exception as e:
            logger.error(f"[{self._collection}] Erro ao criar registro '{id}': {e}")
            return False

    def buscar_por_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Busca um registro pelo ID.

        Args:
            id: Identificador do registro.

        Returns:
            Dict com os dados do registro, ou None se não encontrado.
        """
        try:
            if not id or not isinstance(id, str):
                raise ValueError("ID deve ser uma string não vazia")

            snapshot = self._db.child(id).get()
            if snapshot and snapshot.val():
                return snapshot.val()
            return None

        except Exception as e:
            logger.error(f"[{self._collection}] Erro ao buscar registro '{id}': {e}")
            return None

    def listar_todos(self) -> List[Dict[str, Any]]:
        """
        Lista todos os registros da coleção.

        Returns:
            Lista de dicionários com os dados de cada registro.
        """
        try:
            snapshot = self._db.get()
            if snapshot and snapshot.val():
                dados = snapshot.val()
                if isinstance(dados, dict):
                    # Os valores do dicionário representam cada registro
                    return list(dados.values())
            return []

        except Exception as e:
            logger.error(f"[{self._collection}] Erro ao listar registros: {e}")
            return []

    def atualizar(self, id: str, data: Dict[str, Any]) -> bool:
        """
        Atualiza um registro existente.

        Args:
            id: Identificador do registro a ser atualizado.
            data: Dicionário com os campos a atualizar.

        Returns:
            bool: True se atualização bem-sucedida, False caso contrário.
        """
        try:
            if not id or not isinstance(id, str):
                raise ValueError("ID deve ser uma string não vazia")

            if not isinstance(data, dict):
                raise ValueError("Data deve ser um dicionário")

            # Verifica se o registro existe antes de atualizar
            if not self.buscar_por_id(id):
                logger.warning(f"[{self._collection}] Tentativa de atualizar registro inexistente: {id}")
                return False

            self._db.child(id).update(data)
            logger.info(f"[{self._collection}] Registro atualizado com sucesso: {id}")
            return True

        except Exception as e:
            logger.error(f"[{self._collection}] Erro ao atualizar registro '{id}': {e}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Remove um registro pelo ID.

        Args:
            id: Identificador do registro a ser removido.

        Returns:
            bool: True se remoção bem-sucedida, False caso contrário.
        """
        try:
            if not id or not isinstance(id, str):
                raise ValueError("ID deve ser uma string não vazia")

            # Verifica se o registro existe antes de deletar
            if not self.buscar_por_id(id):
                logger.warning(f"[{self._collection}] Tentativa de deletar registro inexistente: {id}")
                return False

            self._db.child(id).delete()
            logger.info(f"[{self._collection}] Registro deletado com sucesso: {id}")
            return True

        except Exception as e:
            logger.error(f"[{self._collection}] Erro ao deletar registro '{id}': {e}")
            return False

    def existe(self, id: str) -> bool:
        """
        Verifica se um registro existe.

        Args:
            id: Identificador do registro.

        Returns:
            bool: True se existe, False caso contrário.
        """
        return self.buscar_por_id(id) is not None

    def contar_registros(self) -> int:
        """
        Conta o número total de registros na coleção.

        Returns:
            int: Quantidade de registros.
        """
        try:
            snapshot = self._db.get()
            if snapshot and snapshot.val():
                dados = snapshot.val()
                if isinstance(dados, dict):
                    return len(dados)
            return 0

        except Exception as e:
            logger.error(f"[{self._collection}] Erro ao contar registros: {e}")
            return 0
