from typing import Optional, List

class Fidelidade:
    def __init__(
        self,
        id: Optional[str],
        cliente_id: str,
        cliente_nome: str,
        pontos: int,
        nivel: str,
        validade: str,
        historico: Optional[List[str]] = None
    ):
        self._id = id
        self._cliente_id = cliente_id
        self._cliente_nome = cliente_nome
        self._pontos = pontos
        self._nivel = nivel
        self._validade = validade
        self._historico = historico or []

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def cliente_id(self) -> str:
        return self._cliente_id

    @cliente_id.setter
    def cliente_id(self, value: str):
        self._cliente_id = value

    @property
    def cliente_nome(self) -> str:
        return self._cliente_nome

    @cliente_nome.setter
    def cliente_nome(self, value: str):
        self._cliente_nome = value

    @property
    def pontos(self) -> int:
        return self._pontos

    @pontos.setter
    def pontos(self, value: int):
        self._pontos = value

    @property
    def nivel(self) -> str:
        return self._nivel

    @nivel.setter
    def nivel(self, value: str):
        self._nivel = value

    @property
    def validade(self) -> str:
        return self._validade

    @validade.setter
    def validade(self, value: str):
        self._validade = value

    @property
    def historico(self) -> List[str]:
        return self._historico.copy()

    @historico.setter
    def historico(self, value: List[str]):
        self._historico = value.copy()

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "cliente_id": self._cliente_id,
            "cliente_nome": self._cliente_nome,
            "pontos": self._pontos,
            "nivel": self._nivel,
            "validade": self._validade,
            "historico": self._historico
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            cliente_id=data.get("cliente_id"),
            cliente_nome=data.get("cliente_nome"),
            pontos=data.get("pontos"),
            nivel=data.get("nivel"),
            validade=data.get("validade"),
            historico=data.get("historico", [])
        )