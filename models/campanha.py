from datetime import datetime
from typing import List, Optional
import re


class Campanha:
    """
    Modelo que representa dados de uma campanha de marketing.
    Contém validações de datas e canais, bem como métodos auxiliares para métricas.
    """

    _CANAL_VALIDOS = {"email", "whatsapp", "sms"}
    _DATA_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    def __init__(
        self,
        id: Optional[str],
        nome: str,
        objetivo: str,
        data_inicio: str,
        data_fim: str,
        canais: List[str],
        publicos_segmentados: List[str],
        clientes_atingidos: int = 0,
        taxa_resposta: float = 0.0,
        conversao: float = 0.0,
        roi: float = 0.0,
        data_criacao: Optional[str] = None
    ):
        self.id = id
        self.nome = nome
        self.objetivo = objetivo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.canais = canais
        self.publicos_segmentados = publicos_segmentados
        self.clientes_atingidos = clientes_atingidos
        self.taxa_resposta = taxa_resposta
        self.conversao = conversao
        self.roi = roi
        self.data_criacao = data_criacao or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value: Optional[str]):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError("ID deve ser uma string não vazia ou None")
        self._id = None if value is None else value.strip()

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Nome da campanha deve ser uma string não vazia")
        self._nome = value.strip()

    @property
    def objetivo(self) -> str:
        return self._objetivo

    @objetivo.setter
    def objetivo(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Objetivo da campanha deve ser uma string não vazia")
        self._objetivo = value.strip()

    @property
    def data_inicio(self) -> str:
        return self._data_inicio

    @data_inicio.setter
    def data_inicio(self, value: str):
        if not Campanha._validar_data(value):
            raise ValueError("Data de início deve estar no formato 'YYYY-MM-DD'")
        self._data_inicio = value

    @property
    def data_fim(self) -> str:
        return self._data_fim

    @data_fim.setter
    def data_fim(self, value: str):
        if not Campanha._validar_data(value):
            raise ValueError("Data de fim deve estar no formato 'YYYY-MM-DD'")
        # Verifica se data_fim >= data_inicio
        dt_inicio = datetime.strptime(self._data_inicio, "%Y-%m-%d")
        dt_fim = datetime.strptime(value, "%Y-%m-%d")
        if dt_fim < dt_inicio:
            raise ValueError("Data de fim não pode ser anterior à data de início")
        self._data_fim = value

    @property
    def canais(self) -> List[str]:
        return self._canais.copy()

    @canais.setter
    def canais(self, value: List[str]):
        if not isinstance(value, list) or any(not isinstance(c, str) or c not in Campanha._CANAL_VALIDOS for c in value):
            raise ValueError(f"Canais devem ser lista de strings em {Campanha._CANAL_VALIDOS}")
        self._canais = value.copy()

    @property
    def publicos_segmentados(self) -> List[str]:
        return self._publicos_segmentados.copy()

    @publicos_segmentados.setter
    def publicos_segmentados(self, value: List[str]):
        if not isinstance(value, list) or any(not isinstance(p, str) for p in value):
            raise ValueError("Públicos segmentados devem ser uma lista de strings")
        self._publicos_segmentados = value.copy()

    @property
    def clientes_atingidos(self) -> int:
        return self._clientes_atingidos

    @clientes_atingidos.setter
    def clientes_atingidos(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Clientes atingidos deve ser inteiro não negativo")
        self._clientes_atingidos = value

    @property
    def taxa_resposta(self) -> float:
        return self._taxa_resposta

    @taxa_resposta.setter
    def taxa_resposta(self, value: float):
        if not isinstance(value, (int, float)) or not (0.0 <= float(value) <= 100.0):
            raise ValueError("Taxa de resposta deve ser um número entre 0 e 100")
        self._taxa_resposta = float(value)

    @property
    def conversao(self) -> float:
        return self._conversao

    @conversao.setter
    def conversao(self, value: float):
        if not isinstance(value, (int, float)) or not (0.0 <= float(value) <= 100.0):
            raise ValueError("Taxa de conversão deve ser um número entre 0 e 100")
        self._conversao = float(value)

    @property
    def roi(self) -> float:
        return self._roi

    @roi.setter
    def roi(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError("ROI deve ser um número")
        self._roi = float(value)

    @property
    def data_criacao(self) -> str:
        return self._data_criacao

    @data_criacao.setter
    def data_criacao(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Data de criação deve ser string no formato 'YYYY-MM-DD HH:MM:SS'")
        self._data_criacao = value

    @staticmethod
    def _validar_data(data_str: str) -> bool:
        """
        Valida formato de data 'YYYY-MM-DD'.
        """
        if not isinstance(data_str, str):
            return False
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def duracao_dias(self) -> int:
        """
        Retorna a duração da campanha em dias.
        """
        início = datetime.strptime(self._data_inicio, "%Y-%m-%d")
        fim = datetime.strptime(self._data_fim, "%Y-%m-%d")
        return (fim - início).days + 1

    def to_dict(self) -> dict:
        """
        Converte o objeto em dicionário para serialização.
        """
        return {
            "id": self._id,
            "nome": self._nome,
            "objetivo": self._objetivo,
            "data_inicio": self._data_inicio,
            "data_fim": self._data_fim,
            "canais": self._canais,
            "publicos_segmentados": self._publicos_segmentados,
            "clientes_atingidos": self._clientes_atingidos,
            "taxa_resposta": self._taxa_resposta,
            "conversao": self._conversao,
            "roi": self._roi,
            "data_criacao": self._data_criacao
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria instância de Campanha a partir de um dicionário.
        """
        return cls(
            id=data.get("id"),
            nome=data.get("nome", ""),
            objetivo=data.get("objetivo", ""),
            data_inicio=data.get("data_inicio", ""),
            data_fim=data.get("data_fim", ""),
            canais=data.get("canais", []),
            publicos_segmentados=data.get("publicos_segmentados", []),
            clientes_atingidos=data.get("clientes_atingidos", 0),
            taxa_resposta=data.get("taxa_resposta", 0.0),
            conversao=data.get("conversao", 0.0),
            roi=data.get("roi", 0.0),
            data_criacao=data.get("data_criacao")
        )

    def __str__(self) -> str:
        return f"Campanha(id={self._id}, nome={self._nome}, período={self._data_inicio} a {self._data_fim})"

    def __repr__(self) -> str:
        return self.__str__()