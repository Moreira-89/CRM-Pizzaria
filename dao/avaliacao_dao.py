# dao/avaliacao_dao.py

import uuid
from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.avaliacao import Avaliacao
import logging

logger = logging.getLogger(__name__)


class AvaliacaoDAO(FirebaseDAO):
    """
    DAO para operações CRUD sobre avaliações no Firebase Realtime Database.
    Collection padrão: "avaliacoes".
    """

    def __init__(self):
        super().__init__(collection="avaliacoes")

    def criar(self, avaliacao: Avaliacao) -> Optional[str]:
        """
        Cria uma nova avaliação.

        Args:
            avaliacao: Instância de Avaliacao.

        Returns:
            str: ID gerado da avaliação ou None se falhou.
        """
        try:
            if not isinstance(avaliacao, Avaliacao):
                raise ValueError("Parâmetro deve ser uma instância de Avaliacao")

            # Gera UUID se não existir
            if not avaliacao.id:
                avaliacao.id = str(uuid.uuid4())

            sucesso = super().criar(avaliacao.id, avaliacao.to_dict())
            if sucesso:
                return avaliacao.id
            return None

        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao criar avaliação: {e}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Avaliacao]:
        """
        Busca avaliação pelo ID.

        Args:
            id: ID da avaliação.

        Returns:
            Avaliacao: Instância ou None se não encontrado.
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Avaliacao.from_dict(data)
            return None

        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao buscar avaliação por ID '{id}': {e}")
            return None

    def listar_todos(self) -> List[Avaliacao]:
        """
        Lista todas as avaliações.

        Returns:
            List[Avaliacao]: Lista de instâncias de Avaliacao.
        """
        try:
            dados = super().listar_todos()
            return [Avaliacao.from_dict(item) for item in dados if item]
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao listar avaliações: {e}")
            return []

    def listar_por_avaliador(self, avaliador: str) -> List[Avaliacao]:
        """
        Lista avaliações feitas por determinado avaliador.

        Args:
            avaliador: Nome ou identificador do avaliador.

        Returns:
            List[Avaliacao]: Avaliações correspondentes.
        """
        try:
            if not avaliador or not isinstance(avaliador, str):
                return []
            todas = self.listar_todos()
            return [a for a in todas if a.avaliador == avaliador]
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao listar por avaliador '{avaliador}': {e}")
            return []

    def listar_por_avaliado(self, avaliado: str) -> List[Avaliacao]:
        """
        Lista avaliações recebidas por determinado avaliado.

        Args:
            avaliado: Nome ou identificador do avaliado.

        Returns:
            List[Avaliacao]: Avaliações correspondentes.
        """
        try:
            if not avaliado or not isinstance(avaliado, str):
                return []
            todas = self.listar_todos()
            return [a for a in todas if a.avaliado == avaliado]
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao listar por avaliado '{avaliado}': {e}")
            return []

    def listar_por_nota(self, nota_minima: float, nota_maxima: float = 5.0) -> List[Avaliacao]:
        """
        Lista avaliações cujo valor da nota está num intervalo.

        Args:
            nota_minima: Nota mínima inclusive.
            nota_maxima: Nota máxima inclusive.

        Returns:
            List[Avaliacao]: Avaliações dentro do intervalo.
        """
        try:
            todas = self.listar_todos()
            return [a for a in todas if nota_minima <= a.nota <= nota_maxima]
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao listar por nota de {nota_minima} a {nota_maxima}: {e}")
            return []

    def listar_positivas(self) -> List[Avaliacao]:
        """
        Lista avaliações positivas (nota >= 4).

        Returns:
            List[Avaliacao]: Avaliações positivas.
        """
        try:
            return [a for a in self.listar_todos() if a.eh_positiva()]
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao listar avaliações positivas: {e}")
            return []

    def listar_negativas(self) -> List[Avaliacao]:
        """
        Lista avaliações negativas (nota <= 2).

        Returns:
            List[Avaliacao]: Avaliações negativas.
        """
        try:
            return [a for a in self.listar_todos() if a.eh_negativa()]
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao listar avaliações negativas: {e}")
            return []

    def listar_recentes(self, limite: int = 10) -> List[Avaliacao]:
        """
        Lista as N avaliações mais recentes (por data/hora).

        Args:
            limite: Máximo de avaliações a retornar (mais recentes primeiro).

        Returns:
            List[Avaliacao]: Lista de avaliações ordenadas.
        """
        try:
            todas = self.listar_todos()
            ordenadas = sorted(todas, key=lambda a: a.data_hora, reverse=True)
            return ordenadas[:limite]
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao listar avaliações recentes: {e}")
            return []

    def atualizar(self, avaliacao: Avaliacao) -> bool:
        """
        Atualiza uma avaliação existente.

        Args:
            avaliacao: Instância de Avaliacao com o mesmo ID.

        Returns:
            bool: True se atualizado com sucesso, False caso contrário.
        """
        try:
            if not isinstance(avaliacao, Avaliacao):
                raise ValueError("Parâmetro deve ser uma instância de Avaliacao")

            if not avaliacao.id:
                raise ValueError("ID da avaliação não informado para atualização")

            return super().atualizar(avaliacao.id, avaliacao.to_dict())
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao atualizar avaliação '{avaliacao.id}': {e}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Exclui uma avaliação pelo ID.

        Args:
            id: ID da avaliação a ser excluída.

        Returns:
            bool: True se excluído com sucesso, False caso contrário.
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao deletar avaliação '{id}': {e}")
            return False

    def calcular_media_por_avaliado(self, avaliado: str) -> float:
        """
        Calcula a média das notas de avaliações recebidas por um avaliado.

        Args:
            avaliado: Nome ou identificador do avaliado.

        Returns:
            float: Média arredondada para duas casas ou 0.0 se não houver avaliações.
        """
        try:
            lista = self.listar_por_avaliado(avaliado)
            if not lista:
                return 0.0
            total = sum(a.nota for a in lista)
            return round(total / len(lista), 2)
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao calcular média para '{avaliado}': {e}")
            return 0.0

    def obter_estatisticas_gerais(self) -> dict:
        """
        Retorna estatísticas gerais de todas as avaliações:
         - total
         - positivas, negativas, neutras
         - média geral
         - distribuição por nota (1 a 5)
         - percentuais de positivas e negativas

        Returns:
            dict: Estatísticas calculadas.
        """
        try:
            todas = self.listar_todos()
            total = len(todas)
            if total == 0:
                return {}

            positivas = sum(1 for a in todas if a.eh_positiva())
            negativas = sum(1 for a in todas if a.eh_negativa())
            neutras = total - positivas - negativas
            media_geral = sum(a.nota for a in todas) / total

            # Distribuição por nota inteira (1..5)
            distribuicao = {str(i): sum(1 for a in todas if int(a.nota) == i) for i in range(1, 6)}

            return {
                "total": total,
                "positivas": positivas,
                "negativas": negativas,
                "neutras": neutras,
                "media_geral": round(media_geral, 2),
                "distribuicao_notas": distribuicao,
                "percentual_positivas": round((positivas / total) * 100, 1),
                "percentual_negativas": round((negativas / total) * 100, 1)
            }
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao obter estatísticas gerais: {e}")
            return {}

    def obter_avaliacoes_com_comentarios(self) -> List[Avaliacao]:
        """
        Retorna todas as avaliações que possuem comentário (não vazio).

        Returns:
            List[Avaliacao]: Lista filtrada de avaliações.
        """
        try:
            return [a for a in self.listar_todos() if a.comentario.strip()]
        except Exception as e:
            logger.error(f"[avaliacoes] Erro ao buscar avaliações com comentários: {e}")
            return []
