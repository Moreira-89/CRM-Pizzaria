from datetime import datetime
from typing import List, Optional

class Campanha:
    """Modelo que representa dados de uma campanha de marketing."""
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
        self._id = id
        self._nome = nome
        self._objetivo = objetivo
        self._data_inicio = data_inicio
        self._data_fim = data_fim
        self._canais = canais or []
        self._publicos_segmentados = publicos_segmentados or []
        self._clientes_atingidos = clientes_atingidos
        self._taxa_resposta = taxa_resposta
        self._conversao = conversao
        self._roi = roi
        self._data_criacao = data_criacao or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, value: str):
        self._nome = value

    @property
    def objetivo(self) -> str:
        return self._objetivo

    @objetivo.setter
    def objetivo(self, value: str):
        self._objetivo = value

    @property
    def data_inicio(self) -> str:
        return self._data_inicio

    @data_inicio.setter
    def data_inicio(self, value: str):
        self._data_inicio = value

    @property
    def data_fim(self) -> str:
        return self._data_fim

    @data_fim.setter
    def data_fim(self, value: str):
        self._data_fim = value

    @property
    def canais(self) -> List[str]:
        return self._canais.copy()

    @canais.setter
    def canais(self, value: List[str]):
        self._canais = value.copy()

    @property
    def publicos_segmentados(self) -> List[str]:
        return self._publicos_segmentados.copy()

    @publicos_segmentados.setter
    def publicos_segmentados(self, value: List[str]):
        self._publicos_segmentados = value.copy()

    @property
    def clientes_atingidos(self) -> int:
        return self._clientes_atingidos

    @clientes_atingidos.setter
    def clientes_atingidos(self, value: int):
        self._clientes_atingidos = value

    @property
    def taxa_resposta(self) -> float:
        return self._taxa_resposta

    @taxa_resposta.setter
    def taxa_resposta(self, value: float):
        self._taxa_resposta = value

    @property
    def conversao(self) -> float:
        return self._conversao

    @conversao.setter
    def conversao(self, value: float):
        self._conversao = value

    @property
    def roi(self) -> float:
        return self._roi

    @roi.setter
    def roi(self, value: float):
        self._roi = value

    @property
    def data_criacao(self) -> str:
        return self._data_criacao

    @data_criacao.setter
    def data_criacao(self, value: str):
        self._data_criacao = value

    def to_dict(self) -> dict:
        """Converte o objeto em um dicionário."""
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
        """Cria uma instância de ``Campanha`` a partir de um dicionário."""
        return cls(
            id=data.get("id"),
            nome=data.get("nome"),
            objetivo=data.get("objetivo"),
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            canais=data.get("canais", []),
            publicos_segmentados=data.get("publicos_segmentados", []),
            clientes_atingidos=data.get("clientes_atingidos", 0),
            taxa_resposta=data.get("taxa_resposta", 0.0),
            conversao=data.get("conversao", 0.0),
            roi=data.get("roi", 0.0),
            data_criacao=data.get("data_criacao")
        )
