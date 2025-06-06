from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from config.firebase_config import FirebaseConfig
import logging

logger = logging.getLogger(__name__)

class FirebaseDAO(ABC):
    """Classe abstrata base para operações CRUD com Firebase Realtime Database"""
    
    def __init__(self, collection: str):
        if not collection:
            raise ValueError("Nome da coleção não pode ser vazio")
        
        self._collection = collection
        self._db = FirebaseConfig.get_instance().rtdb.child(collection)

    @property
    def collection(self) -> str:
        """Getter para o nome da coleção"""
        return self._collection

    @property
    def db(self):
        """Getter para a referência do banco de dados"""
        return self._db

    def criar(self, id: str, data: Dict[str, Any]) -> bool:
        """
        Cria um novo registro no Firebase
        
        Args:
            id: Identificador único do registro
            data: Dados a serem salvos
            
        Returns:
            bool: True se criado com sucesso, False caso contrário
        """
        try:
            if not id or not isinstance(id, str):
                raise ValueError("ID deve ser uma string não vazia")
            
            if not isinstance(data, dict):
                raise ValueError("Data deve ser um dicionário")
            
            self._db.child(id).set(data)
            logger.info(f"Registro criado com sucesso: {self._collection}/{id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar registro em {self._collection}/{id}: {str(e)}")
            return False

    def buscar_por_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Busca um registro pelo ID
        
        Args:
            id: Identificador do registro
            
        Returns:
            Dict ou None se não encontrado
        """
        try:
            if not id or not isinstance(id, str):
                raise ValueError("ID deve ser uma string não vazia")
            
            snapshot = self._db.child(id).get()
            
            if snapshot and snapshot.val():
                return snapshot.val()
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar registro {self._collection}/{id}: {str(e)}")
            return None

    def listar_todos(self) -> List[Dict[str, Any]]:
        """
        Lista todos os registros da coleção
        
        Returns:
            Lista de dicionários com os dados
        """
        try:
            snapshot = self._db.get()
            
            if snapshot and snapshot.val():
                dados = snapshot.val()
                if isinstance(dados, dict):
                    return list(dados.values())
                return []
            
            return []
            
        except Exception as e:
            logger.error(f"Erro ao listar registros de {self._collection}: {str(e)}")
            return []

    def atualizar(self, id: str, data: Dict[str, Any]) -> bool:
        """
        Atualiza um registro existente
        
        Args:
            id: Identificador do registro
            data: Dados a serem atualizados
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        try:
            if not id or not isinstance(id, str):
                raise ValueError("ID deve ser uma string não vazia")
            
            if not isinstance(data, dict):
                raise ValueError("Data deve ser um dicionário")
            
            # Verifica se o registro existe
            if not self.buscar_por_id(id):
                logger.warning(f"Tentativa de atualizar registro inexistente: {self._collection}/{id}")
                return False
            
            self._db.child(id).update(data)
            logger.info(f"Registro atualizado com sucesso: {self._collection}/{id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar registro {self._collection}/{id}: {str(e)}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Remove um registro
        
        Args:
            id: Identificador do registro
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        try:
            if not id or not isinstance(id, str):
                raise ValueError("ID deve ser uma string não vazia")
            
            # Verifica se o registro existe
            if not self.buscar_por_id(id):
                logger.warning(f"Tentativa de deletar registro inexistente: {self._collection}/{id}")
                return False
            
            self._db.child(id).delete()
            logger.info(f"Registro deletado com sucesso: {self._collection}/{id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar registro {self._collection}/{id}: {str(e)}")
            return False

    def existe(self, id: str) -> bool:
        """
        Verifica se um registro existe
        
        Args:
            id: Identificador do registro
            
        Returns:
            bool: True se existe, False caso contrário
        """
        return self.buscar_por_id(id) is not None

    def contar_registros(self) -> int:
        """
        Conta o número total de registros na coleção
        
        Returns:
            int: Número de registros
        """
        try:
            snapshot = self._db.get()
            if snapshot and snapshot.val():
                dados = snapshot.val()
                if isinstance(dados, dict):
                    return len(dados)
            return 0
        except Exception as e:
            logger.error(f"Erro ao contar registros de {self._collection}: {str(e)}")
            return 0