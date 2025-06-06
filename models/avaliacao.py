from datetime import datetime
from typing import Optional, Union


class Avaliacao:
    """
    Representa uma avaliação registrada no sistema.
    """

    def __init__(
        self,
        id: Optional[str],
        avaliador: str,
        avaliado: str,
        nota: Union[int, float],
        comentario: str = "",
        data_hora: Optional[str] = None
    ):
        self.id = id
        self.avaliador = avaliador
        self.avaliado = avaliado
        self.nota = nota
        self.comentario = comentario
        self.data_hora = data_hora or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value: Optional[str]):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError("ID deve ser uma string não vazia ou None")
        self._id = value

    @property
    def avaliador(self) -> str:
        return self._avaliador

    @avaliador.setter
    def avaliador(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Avaliador deve ser uma string não vazia")
        self._avaliador = value.strip()

    @property
    def avaliado(self) -> str:
        return self._avaliado

    @avaliado.setter
    def avaliado(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Avaliado deve ser uma string não vazia")
        self._avaliado = value.strip()

    @property
    def nota(self) -> Union[int, float]:
        return self._nota

    @nota.setter
    def nota(self, value: Union[int, float]):
        if not isinstance(value, (int, float)) or not (1 <= float(value) <= 5):
            raise ValueError("Nota deve ser um número entre 1 e 5")
        self._nota = float(value)

    @property
    def comentario(self) -> str:
        return self._comentario

    @comentario.setter
    def comentario(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Comentário deve ser uma string")
        self._comentario = value.strip()

    @property
    def data_hora(self) -> str:
        return self._data_hora

    @data_hora.setter
    def data_hora(self, value: str):
        if not Avaliacao._validar_data_hora(value):
            raise ValueError("Data/hora deve estar no formato 'YYYY-MM-DD HH:MM:SS'")
        self._data_hora = value

    @staticmethod
    def _validar_data_hora(data_hora: str) -> bool:
        """
        Valida se a string está no formato 'YYYY-MM-DD HH:MM:SS'.
        """
        if not isinstance(data_hora, str):
            return False
        try:
            datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False

    def to_dict(self) -> dict:
        """
        Converte o objeto em dicionário para armazenamento ou serialização.
        """
        return {
            "id": self._id,
            "avaliador": self._avaliador,
            "avaliado": self._avaliado,
            "nota": self._nota,
            "comentario": self._comentario,
            "data_hora": self._data_hora
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria instância de Avaliacao a partir de um dicionário.
        """
        return cls(
            id=data.get("id"),
            avaliador=data.get("avaliador", ""),
            avaliado=data.get("avaliado", ""),
            nota=data.get("nota", 1),
            comentario=data.get("comentario", ""),
            data_hora=data.get("data_hora")
        )

    def eh_positiva(self) -> bool:
        """
        Retorna True se a avaliação é positiva (nota >= 4).
        """
        return self._nota >= 4

    def eh_negativa(self) -> bool:
        """
        Retorna True se a avaliação é negativa (nota <= 2).
        """
        return self._nota <= 2

    def get_categoria_avaliacao(self) -> str:
        """
        Classifica a avaliação em categorias (Excelente, Boa, Regular, Ruim).
        """
        if self._nota >= 4.5:
            return "Excelente"
        if self._nota >= 3.5:
            return "Boa"
        if self._nota >= 2.5:
            return "Regular"
        return "Ruim"

    def get_data_formatada(self) -> str:
        """
        Retorna a data/hora formatada em 'DD/MM/YYYY às HH:MM'.
        """
        try:
            dt = datetime.strptime(self._data_hora, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d/%m/%Y às %H:%M")
        except ValueError:
            return self._data_hora

    def __str__(self) -> str:
        return f"Avaliacao(id={self._id}, nota={self._nota}, avaliado={self._avaliado})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Avaliacao):
            return False
        return self._id == other._id
