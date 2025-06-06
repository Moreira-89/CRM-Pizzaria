from typing import List, Any
from models.usuario import Usuario
import re


class Cliente(Usuario):
    """
    Modelo que representa um cliente da pizzaria.
    Estende Usuario e agrega e-mail, endereço (textual), preferências e opt-in de canais.
    """

    _EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

    def __init__(
        self,
        id: str,
        nome: str,
        cpf: str,
        telefone: str,
        email: str,
        endereco: str,
        preferencias: List[str] = None,
        opt_in: dict = None
    ):
        super().__init__(id, nome, "Cliente", cpf, telefone)
        self.email = email
        self.endereco = endereco
        self.preferencias = preferencias or []
        self.opt_in = opt_in or {}

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not isinstance(value, str) or not Cliente._EMAIL_REGEX.match(value):
            raise ValueError("E-mail inválido")
        self._email = value.strip()

    @property
    def endereco(self) -> str:
        return self._endereco

    @endereco.setter
    def endereco(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Endereço deve ser uma string não vazia")
        self._endereco = value.strip()

    @property
    def preferencias(self) -> List[str]:
        return self._preferencias.copy()

    @preferencias.setter
    def preferencias(self, value: List[str]):
        if not isinstance(value, list):
            raise ValueError("Preferências devem ser uma lista de strings")
        for pref in value:
            if not isinstance(pref, str):
                raise ValueError("Cada preferência deve ser uma string")
        self._preferencias = value.copy()

    @property
    def opt_in(self) -> dict:
        return self._opt_in.copy()

    @opt_in.setter
    def opt_in(self, value: dict):
        if not isinstance(value, dict):
            raise ValueError("Opt-in deve ser um dicionário")
        for canal, aceito in value.items():
            if not isinstance(canal, str) or not isinstance(aceito, bool):
                raise ValueError("Opt-in deve mapear canal (str) para bool")
        self._opt_in = value.copy()

    def to_dict(self) -> dict:
        """
        Sobrescreve to_dict da classe pai para incluir atributos próprios.
        """
        base = super().to_dict()
        base.update({
            "email": self._email,
            "endereco": self._endereco,
            "preferencias": self._preferencias,
            "opt_in": self._opt_in
        })
        return base

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria instância de Cliente a partir de um dicionário.
        Utiliza __new__ para não chamar __init__ diretamente.
        """
        instance = cls.__new__(cls)
        # Inicializa atributos de Usuario
        instance._id = data.get("id")
        instance._nome = data.get("nome")
        instance._perfil = "Cliente"
        instance._cpf = data.get("cpf")
        instance._telefone = data.get("telefone")
        # Atributos específicos
        instance._email = data.get("email")
        instance._endereco = data.get("endereco", "")
        instance._preferencias = data.get("preferencias", [])
        instance._opt_in = data.get("opt_in", {})
        return instance

    def aceitar_marketing(self, canal: str) -> bool:
        """
        Verifica se o cliente aceitou receber marketing por um canal específico.
        """
        return self._opt_in.get(canal, False)

    def atualizar_preferencia(self, chave: str, valor: Any) -> None:
        """
        Atualiza ou adiciona uma preferência associada ao cliente.
        """
        if not isinstance(chave, str):
            raise ValueError("Chave de preferência deve ser string")
        self._preferencias.append(str(valor))

    def __str__(self) -> str:
        return f"Cliente(id={self._id}, nome={self._nome}, email={self._email})"
