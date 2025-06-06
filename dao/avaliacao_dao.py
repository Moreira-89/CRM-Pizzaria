import uuid
from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.avaliacao import Avaliacao
import logging

logger = logging.getLogger(__name__)

class AvaliacaoDAO(FirebaseDAO):
    """DAO para operações com avaliações"""
    
    def __init__(self):
        super().__init__(collection="avaliacoes")

    def criar(self, avaliacao: Avaliacao) -> Optional[str]:
        """
        Cria uma nova avaliação
        
        Args:
            avaliacao: Instância de Avaliacao
            
        Returns:
            str: ID da avaliação criada ou None se falhou
        """
        try:
            if not isinstance(avaliacao, Avaliacao):
                raise ValueError("Parâmetro deve ser uma instância de Avaliacao")
            
            if not avaliacao.id:
                avaliacao.id = str(uuid.uuid4())
            
            if super().criar(avaliacao.id, avaliacao.to_dict()):
                return avaliacao.id
            return None
            
        except Exception as e:
            logger.error(f"Erro ao criar avaliação: {str(e)}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Avaliacao]:
        """
        Busca avaliação por ID
        
        Args:
            id: ID da avaliação
            
        Returns:
            Avaliacao: Instância da avaliação ou None se não encontrado
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Avaliacao.from_dict(data)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar avaliação por ID {id}: {str(e)}")
            return None

    def listar_todos(self) -> List[Avaliacao]:
        """
        Lista todas as avaliações
        
        Returns:
            List[Avaliacao]: Lista de avaliações
        """
        try:
            dados = super().listar_todos()
            return [Avaliacao.from_dict(item) for item in dados if item]
            
        except Exception as e:
            logger.error(f"Erro ao listar avaliações: {str(e)}")
            return []

    def listar_por_avaliador(self, avaliador: str) -> List[Avaliacao]:
        """
        Lista avaliações feitas por um avaliador específico
        
        Args:
            avaliador: ID ou nome do avaliador
            
        Returns:
            List[Avaliacao]: Lista de avaliações do avaliador
        """
        try:
            if not avaliador:
                return []
            
            avaliacoes = self.listar_todos()
            return [
                avaliacao for avaliacao in avaliacoes 
                if avaliacao.avaliador == avaliador
            ]
            
        except Exception as e:
            logger.error(f"Erro ao listar avaliações por avaliador {avaliador}: {str(e)}")
            return []

    def listar_por_avaliado(self, avaliado: str) -> List[Avaliacao]:
        """
        Lista avaliações recebidas por um avaliado específico
        
        Args:
            avaliado: ID ou identificador do avaliado
            
        Returns:
            List[Avaliacao]: Lista de avaliações do avaliado
        """
        try:
            if not avaliado:
                return []
            
            avaliacoes = self.listar_todos()
            return [
                avaliacao for avaliacao in avaliacoes 
                if avaliacao.avaliado == avaliado
            ]
            
        except Exception as e:
            logger.error(f"Erro ao listar avaliações por avaliado {avaliado}: {str(e)}")
            return []

    def listar_por_nota(self, nota_minima: float, nota_maxima: float = 5.0) -> List[Avaliacao]:
        """
        Lista avaliações dentro de um intervalo de notas
        
        Args:
            nota_minima: Nota mínima (inclusive)
            nota_maxima: Nota máxima (inclusive)
            
        Returns:
            List[Avaliacao]: Lista de avaliações filtradas
        """
        try:
            avaliacoes = self.listar_todos()
            return [
                avaliacao for avaliacao in avaliacoes 
                if nota_minima <= avaliacao.nota <= nota_maxima
            ]
            
        except Exception as e:
            logger.error(f"Erro ao listar avaliações por nota: {str(e)}")
            return []

    def listar_positivas(self) -> List[Avaliacao]:
        """
        Lista avaliações positivas (nota >= 4)
        
        Returns:
            List[Avaliacao]: Lista de avaliações positivas
        """
        try:
            avaliacoes = self.listar_todos()
            return [avaliacao for avaliacao in avaliacoes if avaliacao.eh_positiva()]
            
        except Exception as e:
            logger.error(f"Erro ao listar avaliações positivas: {str(e)}")
            return []

    def listar_negativas(self) -> List[Avaliacao]:
        """
        Lista avaliações negativas (nota <= 2)
        
        Returns:
            List[Avaliacao]: Lista de avaliações negativas
        """
        try:
            avaliacoes = self.listar_todos()
            return [avaliacao for avaliacao in avaliacoes if avaliacao.eh_negativa()]
            
        except Exception as e:
            logger.error(f"Erro ao listar avaliações negativas: {str(e)}")
            return []

    def listar_recentes(self, limite: int = 10) -> List[Avaliacao]:
        """
        Lista as avaliações mais recentes
        
        Args:
            limite: Número máximo de avaliações a retornar
            
        Returns:
            List[Avaliacao]: Lista de avaliações ordenadas por data (mais recente primeiro)
        """
        try:
            avaliacoes = self.listar_todos()
            # Ordena por data/hora (mais recente primeiro)
            avaliacoes_ordenadas = sorted(
                avaliacoes, 
                key=lambda x: x.data_hora, 
                reverse=True
            )
            return avaliacoes_ordenadas[:limite]
            
        except Exception as e:
            logger.error(f"Erro ao listar avaliações recentes: {str(e)}")
            return []

    def atualizar(self, avaliacao: Avaliacao) -> bool:
        """
        Atualiza uma avaliação existente
        
        Args:
            avaliacao: Instância da avaliação com dados atualizados
            
        Returns:
            bool: True se atualizado com sucesso
        """
        try:
            if not isinstance(avaliacao, Avaliacao):
                raise ValueError("Parâmetro deve ser uma instância de Avaliacao")
            
            if not avaliacao.id:
                raise ValueError("ID da avaliação não informado para atualização")
            
            return super().atualizar(avaliacao.id, avaliacao.to_dict())
            
        except Exception as e:
            logger.error(f"Erro ao atualizar avaliação {avaliacao.id}: {str(e)}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Remove uma avaliação
        
        Args:
            id: ID da avaliação
            
        Returns:
            bool: True se removido com sucesso
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"Erro ao deletar avaliação {id}: {str(e)}")
            return False

    def calcular_media_por_avaliado(self, avaliado: str) -> float:
        """
        Calcula a média das avaliações de um avaliado
        
        Args:
            avaliado: ID ou identificador do avaliado
            
        Returns:
            float: Média das avaliações ou 0 se não houver avaliações
        """
        try:
            avaliacoes = self.listar_por_avaliado(avaliado)
            
            if not avaliacoes:
                return 0.0
            
            total_notas = sum(avaliacao.nota for avaliacao in avaliacoes)
            return round(total_notas / len(avaliacoes), 2)
            
        except Exception as e:
            logger.error(f"Erro ao calcular média de avaliações para {avaliado}: {str(e)}")
            return 0.0

    def obter_estatisticas_gerais(self) -> dict:
        """
        Obtém estatísticas gerais das avaliações
        
        Returns:
            dict: Estatísticas das avaliações
        """
        try:
            avaliacoes = self.listar_todos()
            
            if not avaliacoes:
                return {}
            
            total = len(avaliacoes)
            positivas = len([a for a in avaliacoes if a.eh_positiva()])
            negativas = len([a for a in avaliacoes if a.eh_negativa()])
            neutras = total - positivas - negativas
            
            # Calcula média geral
            media_geral = sum(a.nota for a in avaliacoes) / total
            
            # Distribução por nota
            distribuicao_notas = {}
            for i in range(1, 6):
                distribuicao_notas[str(i)] = len([a for a in avaliacoes if int(a.nota) == i])
            
            return {
                "total": total,
                "positivas": positivas,
                "negativas": negativas,
                "neutras": neutras,
                "media_geral": round(media_geral, 2),
                "distribuicao_notas": distribuicao_notas,
                "percentual_positivas": round((positivas / total) * 100, 1) if total > 0 else 0,
                "percentual_negativas": round((negativas / total) * 100, 1) if total > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas gerais de avaliações: {str(e)}")
            return {}

    def obter_avaliacoes_com_comentarios(self) -> List[Avaliacao]:
        """
        Lista avaliações que possuem comentários
        
        Returns:
            List[Avaliacao]: Lista de avaliações com comentários
        """
        try:
            avaliacoes = self.listar_todos()
            return [
                avaliacao for avaliacao in avaliacoes 
                if avaliacao.comentario and avaliacao.comentario.strip()
            ]
            
        except Exception as e:
            logger.error(f"Erro ao listar avaliações com comentários: {str(e)}")
            return []