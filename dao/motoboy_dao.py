# dao/motoboy_dao.py

import uuid
from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.motoboy import Motoboy
import logging

logger = logging.getLogger(__name__)


class MotoboyDAO(FirebaseDAO):
    """
    DAO para operações CRUD de motoboys no Firebase RTDB.
    Collection padrão: "motoboys".
    """

    def __init__(self):
        super().__init__(collection="motoboys")

    def criar(self, motoboy: Motoboy) -> Optional[str]:
        """
        Cria um novo motoboy.

        Args:
            motoboy: Instância de Motoboy.

        Returns:
            str: ID gerado ou None se falhou.
        """
        try:
            if not isinstance(motoboy, Motoboy):
                raise ValueError("Parâmetro deve ser uma instância de Motoboy")

            if not motoboy.id:
                motoboy.id = str(uuid.uuid4())

            # Verifica existência por CPF ou CNH
            if self._motoboy_existe_por_cpf_ou_cnh(motoboy.cpf, motoboy.cnh):
                raise ValueError("Já existe motoboy com este CPF ou CNH")

            sucesso = super().criar(motoboy.id, motoboy.to_dict())
            if sucesso:
                return motoboy.id
            return None
        except Exception as e:
            logger.error(f"[motoboys] Erro ao criar motoboy: {e}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Motoboy]:
        """
        Busca motoboy pelo ID.

        Args:
            id: ID do motoboy.

        Returns:
            Motoboy: Instância ou None se não encontrado.
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Motoboy.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"[motoboys] Erro ao buscar motoboy por ID '{id}': {e}")
            return None

    def buscar_por_nome(self, nome: str) -> Optional[Motoboy]:
        """
        Busca primeiro motoboy com nome exato (case-insensitive).

        Args:
            nome: Nome do motoboy.

        Returns:
            Motoboy: Instância ou None se não encontrado.
        """
        try:
            if not nome or not isinstance(nome, str):
                return None
            todos = self.listar_todos()
            for m in todos:
                if m.nome.lower() == nome.lower():
                    return m
            return None
        except Exception as e:
            logger.error(f"[motoboys] Erro ao buscar motoboy por nome '{nome}': {e}")
            return None

    def buscar_por_cpf(self, cpf: str) -> Optional[Motoboy]:
        """
        Busca motoboy pelo CPF (ignora formatação, compara apenas dígitos).

        Args:
            cpf: CPF do motoboy.

        Returns:
            Motoboy: Instância ou None se não encontrado.
        """
        try:
            if not cpf or not isinstance(cpf, str):
                return None

            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            todos = self.listar_todos()
            for m in todos:
                m_cpf_limpo = ''.join(filter(str.isdigit, m.cpf))
                if m_cpf_limpo == cpf_limpo:
                    return m
            return None
        except Exception as e:
            logger.error(f"[motoboys] Erro ao buscar motoboy por CPF '{cpf}': {e}")
            return None

    def buscar_por_cnh(self, cnh: str) -> Optional[Motoboy]:
        """
        Busca motoboy pela CNH (ignora formatação, compara apenas dígitos).

        Args:
            cnh: CNH do motoboy.

        Returns:
            Motoboy: Instância ou None se não encontrado.
        """
        try:
            if not cnh or not isinstance(cnh, str):
                return None

            cnh_limpa = ''.join(filter(str.isdigit, cnh))
            todos = self.listar_todos()
            for m in todos:
                m_cnh_limpa = ''.join(filter(str.isdigit, m.cnh))
                if m_cnh_limpa == cnh_limpa:
                    return m
            return None
        except Exception as e:
            logger.error(f"[motoboys] Erro ao buscar motoboy por CNH '{cnh}': {e}")
            return None

    def listar_todos(self) -> List[Motoboy]:
        """
        Lista todos os motoboys.

        Returns:
            List[Motoboy]: Lista de instâncias.
        """
        try:
            dados = super().listar_todos()
            return [Motoboy.from_dict(item) for item in dados if item]
        except Exception as e:
            logger.error(f"[motoboys] Erro ao listar motoboys: {e}")
            return []

    def listar_ativos(self) -> List[Motoboy]:
        """
        Lista apenas motoboys com status 'Online'.

        Returns:
            List[Motoboy]: Motoboys ativos.
        """
        try:
            todos = self.listar_todos()
            return [m for m in todos if m.esta_disponivel()]
        except Exception as e:
            logger.error(f"[motoboys] Erro ao listar motoboys ativos: {e}")
            return []

    def listar_por_status(self, status: str) -> List[Motoboy]:
        """
        Lista motoboys por status operacional exato.

        Args:
            status: "Online" ou "Offline".

        Returns:
            List[Motoboy]: Motoboys que correspondem ao status.
        """
        try:
            if not status or not isinstance(status, str):
                return []
            todos = self.listar_todos()
            return [m for m in todos if m.status_operacional == status]
        except Exception as e:
            logger.error(f"[motoboys] Erro ao listar por status '{status}': {e}")
            return []

    def listar_por_zona(self, zona: str) -> List[Motoboy]:
        """
        Lista motoboys que atendem a uma zona específica.

        Args:
            zona: Nome da zona.

        Returns:
            List[Motoboy]: Motoboys que podem atuar na zona.
        """
        try:
            if not zona or not isinstance(zona, str):
                return []
            todos = self.listar_todos()
            return [m for m in todos if m.pode_atender_zona(zona)]
        except Exception as e:
            logger.error(f"[motoboys] Erro ao listar por zona '{zona}': {e}")
            return []

    def atualizar(self, motoboy: Motoboy) -> bool:
        """
        Atualiza dados de um motoboy existente.

        Args:
            motoboy: Instância de Motoboy com ID preenchido.

        Returns:
            bool: True se atualizado com sucesso.
        """
        try:
            if not isinstance(motoboy, Motoboy):
                raise ValueError("Parâmetro deve ser uma instância de Motoboy")
            if not motoboy.id:
                raise ValueError("ID do motoboy não informado para atualização")

            return super().atualizar(motoboy.id, motoboy.to_dict())
        except Exception as e:
            logger.error(f"[motoboys] Erro ao atualizar motoboy '{getattr(motoboy, 'id', None)}': {e}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Deleta um motoboy pelo ID.

        Args:
            id: ID do motoboy.

        Returns:
            bool: True se excluído com sucesso.
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"[motoboys] Erro ao deletar motoboy '{id}': {e}")
            return False

    def _motoboy_existe_por_cpf_ou_cnh(self, cpf: str, cnh: str) -> bool:
        """
        Verifica se já existe motoboy com CPF ou CNH fornecidos.

        Args:
            cpf: CPF a verificar.
            cnh: CNH a verificar.

        Returns:
            bool: True se já existir, False caso contrário.
        """
        try:
            return (self.buscar_por_cpf(cpf) is not None) or (self.buscar_por_cnh(cnh) is not None)
        except Exception:
            return False

    def obter_estatisticas(self) -> dict:
        """
        Retorna estatísticas gerais sobre motoboys:
         - total
         - ativos, inativos
         - avaliação média geral
         - tempo médio de entrega

        Returns:
            dict: Estatísticas calculadas.
        """
        try:
            todos = self.listar_todos()
            total = len(todos)
            if total == 0:
                return {}

            ativos = len([m for m in todos if m.esta_disponivel()])
            inativos = total - ativos
            # Avaliação média geral (considera apenas valores > 0)
            avals = [m.avaliacao_media for m in todos if m.avaliacao_media > 0]
            media_geral = sum(avals) / len(avals) if avals else 0.0
            # Tempo médio de entrega geral (≥0)
            tempos = [m.tempo_medio_entrega for m in todos if m.tempo_medio_entrega > 0]
            tempo_medio_geral = sum(tempos) / len(tempos) if tempos else 0.0

            return {
                "total": total,
                "ativos": ativos,
                "inativos": inativos,
                "avaliacao_media_geral": round(media_geral, 2),
                "tempo_medio_entrega_geral": round(tempo_medio_geral, 2)
            }
        except Exception as e:
            logger.error(f"[motoboys] Erro ao obter estatísticas gerais: {e}")
            return {}
