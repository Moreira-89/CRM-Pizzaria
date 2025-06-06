from typing import Optional, List
from datetime import datetime, date


class Fidelidade:
    """
    Armazena informações de programas de fidelidade dos clientes.
    Fornece métodos para adicionar pontos, resgatar e verificar status.
    """

    _NIVEIS_VALIDOS = {"bronze", "prata", "ouro"}

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
        self.id = id
        self.cliente_id = cliente_id
        self.cliente_nome = cliente_nome
        self.pontos = pontos
        self.nivel = nivel
        self.validade = validade
        self.historico = historico or []

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value: Optional[str]):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError("ID deve ser string não vazia ou None")
        self._id = None if value is None else value.strip()

    @property
    def cliente_id(self) -> str:
        return self._cliente_id

    @cliente_id.setter
    def cliente_id(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("cliente_id deve ser string não vazia")
        self._cliente_id = value

    @property
    def cliente_nome(self) -> str:
        return self._cliente_nome

    @cliente_nome.setter
    def cliente_nome(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("cliente_nome deve ser string não vazia")
        self._cliente_nome = value

    @property
    def pontos(self) -> int:
        return self._pontos

    @pontos.setter
    def pontos(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Pontos deve ser inteiro não negativo")
        self._pontos = value

    @property
    def nivel(self) -> str:
        return self._nivel

    @nivel.setter
    def nivel(self, value: str):
        if not isinstance(value, str) or value.lower() not in Fidelidade._NIVEIS_VALIDOS:
            raise ValueError(f"Nível deve ser um de {Fidelidade._NIVEIS_VALIDOS}")
        self._nivel = value.lower()

    @property
    def validade(self) -> str:
        return self._validade

    @validade.setter
    def validade(self, value: str):
        # Espera formato 'YYYY-MM-DD'
        try:
            dt = datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Validade deve ser string no formato 'YYYY-MM-DD'")
        self._validade = value

    @property
    def historico(self) -> List[str]:
        return self._historico.copy()

    @historico.setter
    def historico(self, value: List[str]):
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            raise ValueError("Histórico deve ser lista de strings")
        self._historico = value.copy()

    def to_dict(self) -> dict:
        """
        Serializa a instância em um dicionário.
        """
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
        """
        Cria instância de Fidelidade a partir de um dicionário.
        """
        return cls(
            id=data.get("id"),
            cliente_id=data.get("cliente_id", ""),
            cliente_nome=data.get("cliente_nome", ""),
            pontos=data.get("pontos", 0),
            nivel=data.get("nivel", "bronze"),
            validade=data.get("validade", date.today().strftime("%Y-%m-%d")),
            historico=data.get("historico", [])
        )

    def adicionar_pontos(self, quantidade: int, motivo: str = "") -> None:
        """
        Adiciona pontos ao cliente e registra no histórico.
        """
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Quantidade de pontos deve ser inteiro positivo")
        self._pontos += quantidade
        if motivo:
            self._historico.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: +{quantidade} pontos - {motivo}")

    def resgatar_pontos(self, quantidade: int, motivo: str = "") -> bool:
        """
        Tenta resgatar pontos. Se houver saldo suficiente, deduz e retorna True,
        caso contrário, retorna False.
        """
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Quantidade de pontos deve ser inteiro positivo")
        if quantidade > self._pontos:
            return False
        self._pontos -= quantidade
        if motivo:
            self._historico.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: -{quantidade} pontos - {motivo}")
        return True

    def esta_expirado(self) -> bool:
        """
        Retorna True se a validade já passou.
        """
        return datetime.strptime(self._validade, "%Y-%m-%d").date() < date.today()

    def __str__(self) -> str:
        return f"Fidelidade(id={self._id}, cliente={self._cliente_nome}, pontos={self._pontos}, nível={self._nivel})"
