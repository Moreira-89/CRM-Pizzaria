from typing import List, Union
from models.usuario import Usuario


class Motoboy(Usuario):
    """
    Modelo representando motoboys cadastrados.
    Estende Usuario e adiciona atributos específicos de motoboys.
    """

    _STATUS_VALIDOS = {"Online", "Offline"}

    def __init__(
        self,
        id: str,
        nome: str,
        cpf: str,
        telefone: str,
        cnh: str,
        status_operacional: str,
        zonas_atuacao: List[str] = None,
        horarios_disponiveis: List[str] = None,
        avaliacao_media: float = 0.0,
        tempo_medio_entrega: int = 0
    ):
        super().__init__(id, nome, "Motoboy", cpf, telefone)
        self.cnh = cnh
        self.status_operacional = status_operacional
        self.zonas_atuacao = zonas_atuacao or []
        self.horarios_disponiveis = horarios_disponiveis or []
        self.avaliacao_media = avaliacao_media
        self.tempo_medio_entrega = tempo_medio_entrega

    @property
    def cnh(self) -> str:
        return self._cnh

    @cnh.setter
    def cnh(self, value: str):
        if not isinstance(value, str) or not Motoboy._validar_cnh(value):
            raise ValueError("CNH inválida")
        self._cnh = ''.join(filter(str.isalnum, value))

    @property
    def status_operacional(self) -> str:
        return self._status_operacional

    @status_operacional.setter
    def status_operacional(self, value: str):
        if not isinstance(value, str) or value not in Motoboy._STATUS_VALIDOS:
            raise ValueError(f"Status deve ser um dos seguintes: {Motoboy._STATUS_VALIDOS}")
        self._status_operacional = value

    @property
    def zonas_atuacao(self) -> List[str]:
        return self._zonas_atuacao.copy()

    @zonas_atuacao.setter
    def zonas_atuacao(self, value: List[str]):
        if not isinstance(value, list) or any(not isinstance(z, str) for z in value):
            raise ValueError("Zonas de atuação devem ser uma lista de strings")
        self._zonas_atuacao = value.copy()

    @property
    def horarios_disponiveis(self) -> List[str]:
        return self._horarios_disponiveis.copy()

    @horarios_disponiveis.setter
    def horarios_disponiveis(self, value: List[str]):
        if not isinstance(value, list) or any(not isinstance(h, str) for h in value):
            raise ValueError("Horários disponíveis devem ser uma lista de strings")
        self._horarios_disponiveis = value.copy()

    @property
    def avaliacao_media(self) -> float:
        return self._avaliacao_media

    @avaliacao_media.setter
    def avaliacao_media(self, value: Union[int, float]):
        if not isinstance(value, (int, float)) or not (0.0 <= float(value) <= 5.0):
            raise ValueError("Avaliação média deve ser um número entre 0 e 5")
        self._avaliacao_media = float(value)

    @property
    def tempo_medio_entrega(self) -> int:
        return self._tempo_medio_entrega

    @tempo_medio_entrega.setter
    def tempo_medio_entrega(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Tempo médio de entrega deve ser um inteiro não-negativo")
        self._tempo_medio_entrega = value

    def to_dict(self) -> dict:
        """
        Serializa os atributos do Motoboy, incluindo os herdados de Usuario.
        """
        base = super().to_dict()
        base.update({
            "cnh": self._cnh,
            "status_operacional": self._status_operacional,
            "zonas_atuacao": self._zonas_atuacao,
            "horarios_disponiveis": self._horarios_disponiveis,
            "avaliacao_media": self._avaliacao_media,
            "tempo_medio_entrega": self._tempo_medio_entrega
        })
        return base

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria instância de Motoboy a partir de um dicionário.
        Usa __new__ para não chamar diretamente __init__.
        """
        instance = cls.__new__(cls)
        instance._id = data.get("id")
        instance._nome = data.get("nome")
        instance._perfil = "Motoboy"
        instance._cpf = data.get("cpf")
        instance._telefone = data.get("telefone")
        instance._cnh = data.get("cnh")
        instance._status_operacional = data.get("status_operacional")
        instance._zonas_atuacao = data.get("zonas_atuacao", [])
        instance._horarios_disponiveis = data.get("horarios_disponiveis", [])
        instance._avaliacao_media = data.get("avaliacao_media", 0.0)
        instance._tempo_medio_entrega = data.get("tempo_medio_entrega", 0)
        return instance

    @staticmethod
    def _validar_cnh(cnh: str) -> bool:
        """
        Validação básica de CNH: deve conter exatamente 11 caracteres numéricos.
        """
        nums = ''.join(filter(str.isdigit, cnh))
        return len(nums) == 11

    def esta_disponivel(self) -> bool:
        """
        Retorna True se o motoboy estiver com status 'Online'.
        """
        return self._status_operacional == "Online"

    def pode_atender_zona(self, zona: str) -> bool:
        """
        Verifica se o motoboy pode atender uma zona específica.
        """
        return zona in self._zonas_atuacao

    def adicionar_zona_atuacao(self, zona: str) -> None:
        """
        Adiciona uma nova zona de atuação, se não estiver já presente.
        """
        if isinstance(zona, str) and zona not in self._zonas_atuacao:
            self._zonas_atuacao.append(zona)

    def remover_zona_atuacao(self, zona: str) -> None:
        """
        Remove uma zona de atuação, se existir.
        """
        if zona in self._zonas_atuacao:
            self._zonas_atuacao.remove(zona)

    def atualizar_avaliacao(self, nova_nota: float) -> None:
        """
        Atualiza a avaliação média do motoboy com base em uma nova nota fornecida.
        Exemplo de lógica: média ponderada (simplificada como média simples).
        """
        if not isinstance(nova_nota, (int, float)) or not (0.0 <= float(nova_nota) <= 5.0):
            raise ValueError("Nova nota deve ser um número entre 0 e 5")
        # Implementação simplificada: assume que há apenas esta nota como base.
        # Em um cenário real, somar notas anteriores, contar número de avaliações etc.
        self._avaliacao_media = float(nova_nota)

    def __str__(self) -> str:
        return f"Motoboy(id={self._id}, nome={self._nome}, status={self._status_operacional})"
