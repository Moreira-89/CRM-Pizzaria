import uuid
from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.motoboy import Motoboy
import logging

logger = logging.getLogger(__name__)

class MotoboyDAO(FirebaseDAO):
    """DAO para operações com motoboys"""
    
    def __init__(self):
        super().__init__(collection="motoboys")

    def criar(self, motoboy: Motoboy) -> Optional[str]:
        """
        Cria um novo motoboy
        
        Args:
            motoboy: Instância de Motoboy
            
        Returns:
            str: ID do motoboy criado ou None se falhou
        """
        try:
            if not isinstance(motoboy, Motoboy):
                raise ValueError("Parâmetro deve ser uma instância de Motoboy")
            
            if not motoboy.id:
                motoboy.id = str(uuid.uuid4())
            
            # Verifica se já existe motoboy com mesmo CPF ou CNH
            if self._motoboy_existe_por_cpf_ou_cnh(motoboy.cpf, motoboy.cnh):
                raise ValueError("Já existe motoboy com este CPF ou CNH")
            
            if super().criar(motoboy.id, motoboy.to_dict()):
                return motoboy.id
            return None
            
        except Exception as e:
            logger.error(f"Erro ao criar motoboy: {str(e)}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Motoboy]:
        """
        Busca motoboy por ID
        
        Args:
            id: ID do motoboy
            
        Returns:
            Motoboy: Instância do motoboy ou None se não encontrado
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Motoboy.from_dict(data)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar motoboy por ID {id}: {str(e)}")
            return None

    def buscar_por_nome(self, nome: str) -> Optional[Motoboy]:
        """
        Busca motoboy por nome (case-insensitive)
        
        Args:
            nome: Nome do motoboy
            
        Returns:
            Motoboy: Primeira ocorrência encontrada ou None
        """
        try:
            if not nome or not isinstance(nome, str):
                return None
            
            motoboys = self.listar_todos()
            for motoboy in motoboys:
                if motoboy.nome.lower() == nome.lower():
                    return motoboy
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar motoboy por nome {nome}: {str(e)}")
            return None

    def buscar_por_cpf(self, cpf: str) -> Optional[Motoboy]:
        """
        Busca motoboy por CPF
        
        Args:
            cpf: CPF do motoboy
            
        Returns:
            Motoboy: Instância do motoboy ou None se não encontrado
        """
        try:
            if not cpf or not isinstance(cpf, str):
                return None
            
            # Remove formatação do CPF
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            
            motoboys = self.listar_todos()
            for motoboy in motoboys:
                cpf_motoboy_limpo = ''.join(filter(str.isdigit, motoboy.cpf))
                if cpf_motoboy_limpo == cpf_limpo:
                    return motoboy
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar motoboy por CPF {cpf}: {str(e)}")
            return None

    def buscar_por_cnh(self, cnh: str) -> Optional[Motoboy]:
        """
        Busca motoboy por CNH
        
        Args:
            cnh: CNH do motoboy
            
        Returns:
            Motoboy: Instância do motoboy ou None se não encontrado
        """
        try:
            if not cnh or not isinstance(cnh, str):
                return None
            
            # Remove formatação da CNH
            cnh_limpa = ''.join(filter(str.isdigit, cnh))
            
            motoboys = self.listar_todos()
            for motoboy in motoboys:
                cnh_motoboy_limpa = ''.join(filter(str.isdigit, motoboy.cnh))
                if cnh_motoboy_limpa == cnh_limpa:
                    return motoboy
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar motoboy por CNH {cnh}: {str(e)}")
            return None

    def listar_todos(self) -> List[Motoboy]:
        """
        Lista todos os motoboys
        
        Returns:
            List[Motoboy]: Lista de motoboys
        """
        try:
            dados = super().listar_todos()
            return [Motoboy.from_dict(item) for item in dados if item]
            
        except Exception as e:
            logger.error(f"Erro ao listar motoboys: {str(e)}")
            return []

    def listar_ativos(self) -> List[Motoboy]:
        """
        Lista apenas motoboys ativos
        
        Returns:
            List[Motoboy]: Lista de motoboys ativos
        """
        try:
            motoboys = self.listar_todos()
            return [motoboy for motoboy in motoboys if motoboy.esta_disponivel()]
            
        except Exception as e:
            logger.error(f"Erro ao listar motoboys ativos: {str(e)}")
            return []

    def listar_por_status(self, status: str) -> List[Motoboy]:
        """
        Lista motoboys por status operacional
        
        Args:
            status: Status operacional
            
        Returns:
            List[Motoboy]: Lista de motoboys com o status especificado
        """
        try:
            if not status:
                return []
            
            motoboys = self.listar_todos()
            return [
                motoboy for motoboy in motoboys 
                if motoboy.status_operacional == status
            ]
            
        except Exception as e:
            logger.error(f"Erro ao listar motoboys por status {status}: {str(e)}")
            return []

    def listar_por_zona(self, zona: str) -> List[Motoboy]:
        """
        Lista motoboys que atendem uma zona específica
        
        Args:
            zona: Nome da zona
            
        Returns:
            List[Motoboy]: Lista de motoboys que atendem a zona
        """
        try:
            if not zona:
                return []
            
            motoboys = self.listar_todos()
            return [
                motoboy for motoboy in motoboys 
                if motoboy.pode_atender_zona(zona)
            ]
            
        except Exception as e:
            logger.error(f"Erro ao listar motoboys por zona {zona}: {str(e)}")
            return []

    def atualizar(self, motoboy: Motoboy) -> bool:
        """
        Atualiza um motoboy existente
        
        Args:
            motoboy: Instância do motoboy com dados atualizados
            
        Returns:
            bool: True se atualizado com sucesso
        """
        try:
            if not isinstance(motoboy, Motoboy):
                raise ValueError("Parâmetro deve ser uma instância de Motoboy")
            
            if not motoboy.id:
                raise ValueError("ID do motoboy não informado para atualização")
            
            return super().atualizar(motoboy.id, motoboy.to_dict())
            
        except Exception as e:
            logger.error(f"Erro ao atualizar motoboy {motoboy.id}: {str(e)}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Remove um motoboy
        
        Args:
            id: ID do motoboy
            
        Returns:
            bool: True se removido com sucesso
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"Erro ao deletar motoboy {id}: {str(e)}")
            return False

    def _motoboy_existe_por_cpf_ou_cnh(self, cpf: str, cnh: str) -> bool:
        """
        Verifica se já existe motoboy com o CPF ou CNH informado
        
        Args:
            cpf: CPF a verificar
            cnh: CNH a verificar
            
        Returns:
            bool: True se já existe
        """
        try:
            return (self.buscar_por_cpf(cpf) is not None or 
                    self.buscar_por_cnh(cnh) is not None)
        except Exception:
            return False

    def obter_estatisticas(self) -> dict:
        """
        Obtém estatísticas dos motoboys
        
        Returns:
            dict: Estatísticas dos motoboys
        """
        try:
            motoboys = self.listar_todos()
            
            if not motoboys:
                return {}
            
            total = len(motoboys)
            ativos = len([m for m in motoboys if m.status_operacional == "Ativo"])
            inativos = len([m for m in motoboys if m.status_operacional == "Inativo"])
            em_entrega = len([m for m in motoboys if m.status_operacional == "Em Entrega"])
            
            # Calcula avaliação média geral
            avaliacoes = [m.avaliacao_media for m in motoboys if m.avaliacao_media > 0]
            avaliacao_media_geral = sum(avaliacoes) / len(avaliacoes) if avaliacoes else 0
            
            # Calcula tempo médio de entrega geral
            tempos = [m.tempo_medio_entrega for m in motoboys if m.tempo_medio_entrega > 0]
            tempo_medio_geral = sum(tempos) / len(tempos) if tempos else 0
            
            return {
                "total": total,
                "ativos": ativos,
                "inativos": inativos,
                "em_entrega": em_entrega,
                "avaliacao_media_geral": round(avaliacao_media_geral, 2),
                "tempo_medio_entrega_geral": round(tempo_medio_geral, 2)
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas dos motoboys: {str(e)}")
            return {}
