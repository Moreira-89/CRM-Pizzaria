from models.usuario import Usuario
from typing import List, Union

class Motoboy(Usuario):
    """Modelo representando motoboys cadastrados."""
    def __init__(self, id: str, nome: str, cpf: str, telefone: str,
                 cnh: str, status_operacional: str, zonas_atuacao: List[str] = None, 
                 horarios_disponiveis: List[str] = None, avaliacao_media: float = 0.0, 
                 tempo_medio_entrega: int = 0):
        
        # Chama o construtor da classe pai
        super().__init__(id, nome, "Motoboy", cpf, telefone)
        
        # Atributos específicos do Motoboy
        self._cnh = cnh
        self._status_operacional = status_operacional
        self._zonas_atuacao = zonas_atuacao or []
        self._horarios_disponiveis = horarios_disponiveis or []
        self._avaliacao_media = avaliacao_media
        self._tempo_medio_entrega = tempo_medio_entrega

    # Propriedades específicas do Motoboy
    @property
    def cnh(self) -> str:
        return self._cnh
    
    @cnh.setter
    def cnh(self, value: str):
        if not self._validar_cnh(value):
            raise ValueError("CNH inválida")
        self._cnh = value

    @property
    def status_operacional(self) -> str:
        return self._status_operacional
    
    @status_operacional.setter
    def status_operacional(self, value: str):
        status_validos = ["Ativo", "Inativo", "Pausado", "Em Entrega"]
        if value not in status_validos:
            raise ValueError(f"Status deve ser um dos seguintes: {status_validos}")
        self._status_operacional = value

    @property
    def zonas_atuacao(self) -> List[str]:
        return self._zonas_atuacao.copy()
    
    @zonas_atuacao.setter
    def zonas_atuacao(self, value: List[str]):
        if not isinstance(value, list):
            raise ValueError("Zonas de atuação devem ser uma lista")
        self._zonas_atuacao = value.copy()

    @property
    def horarios_disponiveis(self) -> List[str]:
        return self._horarios_disponiveis.copy()
    
    @horarios_disponiveis.setter
    def horarios_disponiveis(self, value: List[str]):
        if not isinstance(value, list):
            raise ValueError("Horários disponíveis devem ser uma lista")
        self._horarios_disponiveis = value.copy()

    @property
    def avaliacao_media(self) -> float:
        return self._avaliacao_media
    
    @avaliacao_media.setter
    def avaliacao_media(self, value: Union[int, float]):
        if not isinstance(value, (int, float)) or value < 0 or value > 5:
            raise ValueError("Avaliação média deve ser um número entre 0 e 5")
        self._avaliacao_media = float(value)

    @property
    def tempo_medio_entrega(self) -> int:
        return self._tempo_medio_entrega
    
    @tempo_medio_entrega.setter
    def tempo_medio_entrega(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Tempo médio de entrega deve ser um número inteiro positivo")
        self._tempo_medio_entrega = value

    def to_dict(self) -> dict:
        """Sobrescreve o método da classe pai para incluir atributos específicos"""
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
        """Cria instância de Motoboy a partir de dicionário"""
        # Cria instância sem validação inicial (dados do banco)
        instance = cls.__new__(cls)
        
        # Inicializa atributos da classe pai
        instance._id = data.get("id")
        instance._nome = data.get("nome")
        instance._perfil = "Motoboy"
        instance._cpf = data.get("cpf")
        instance._telefone = data.get("telefone")
        
        # Inicializa atributos específicos
        instance._cnh = data.get("cnh")
        instance._status_operacional = data.get("status_operacional")
        instance._zonas_atuacao = data.get("zonas_atuacao", [])
        instance._horarios_disponiveis = data.get("horarios_disponiveis", [])
        instance._avaliacao_media = data.get("avaliacao_media", 0.0)
        instance._tempo_medio_entrega = data.get("tempo_medio_entrega", 0)
        
        return instance

    @staticmethod
    def _validar_cnh(cnh: str) -> bool:
        """Validação básica de CNH"""
        if not cnh or not isinstance(cnh, str):
            return False
        # Remove caracteres não numéricos
        cnh_nums = ''.join(filter(str.isdigit, cnh))
        return len(cnh_nums) == 11

    def esta_disponivel(self) -> bool:
        """Verifica se o motoboy está disponível para entregas"""
        return self._status_operacional == "Ativo"

    def pode_atender_zona(self, zona: str) -> bool:
        """Verifica se o motoboy pode atender uma zona específica"""
        return zona in self._zonas_atuacao

    def adicionar_zona_atuacao(self, zona: str) -> None:
        """Adiciona uma nova zona de atuação"""
        if zona and zona not in self._zonas_atuacao:
            self._zonas_atuacao.append(zona)

    def remover_zona_atuacao(self, zona: str) -> None:
        """Remove uma zona de atuação"""
        if zona in self._zonas_atuacao:
            self._zonas_atuacao.remove(zona)

    def atualizar_avaliacao(self, nova_avaliacao: float) -> None:
        """Atualiza a avaliação média (implementar lógica de cálculo se necessário)"""
        if 0 <= nova_avaliacao <= 5:
            self._avaliacao_media = nova_avaliacao

    def __str__(self) -> str:
        return f"Motoboy(id={self._id}, nome={self._nome}, status={self._status_operacional})"
