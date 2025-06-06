from abc import ABC, abstractmethod
import re


class Usuario(ABC):
    """
    Classe base abstrata para representar usuários do sistema.
    Define campos e validações comuns a todos os tipos de usuários.
    """

    _PERFIS_VALIDOS = {"Funcionário", "Cliente", "Motoboy"}

    def __init__(self, id: str, nome: str, perfil: str, cpf: str, telefone: str):
        self.id = id
        self.nome = nome
        self.perfil = perfil
        self.cpf = cpf
        self.telefone = telefone

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("ID deve ser uma string não vazia")
        self._id = value

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Nome deve ser uma string não vazia")
        self._nome = value

    @property
    def perfil(self) -> str:
        return self._perfil

    @perfil.setter
    def perfil(self, value: str):
        if not isinstance(value, str) or value not in Usuario._PERFIS_VALIDOS:
            raise ValueError(f"Perfil deve ser um dos seguintes: {Usuario._PERFIS_VALIDOS}")
        self._perfil = value

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value: str):
        if not Usuario._validar_cpf(value):
            raise ValueError("CPF inválido")
        self._cpf = ''.join(filter(str.isdigit, value))

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Telefone deve ser uma string não vazia")
        # Validação simples: permitir dígitos, espaços, traços e parênteses
        pattern = re.compile(r'^[\d\-\s\(\)\+]+$')
        if not pattern.match(value):
            raise ValueError("Telefone contém caracteres inválidos")
        self._telefone = value.strip()

    def to_dict(self) -> dict:
        """
        Serializa o usuário para um dicionário.
        """
        return {
            "id": self._id,
            "nome": self._nome,
            "perfil": self._perfil,
            "cpf": self._cpf,
            "telefone": self._telefone
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria instância de Usuario a partir de um dicionário.
        Note: como Usuario é abstrato, deve ser chamado em subclasses.
        """
        instance = cls.__new__(cls)
        instance._id = data.get("id")
        instance._nome = data.get("nome")
        instance._perfil = data.get("perfil")
        instance._cpf = data.get("cpf")
        instance._telefone = data.get("telefone")
        return instance

    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """
        Validação básica de CPF: 11 dígitos e não todos iguais.
        """
        if not cpf or not isinstance(cpf, str):
            return False
        nums = ''.join(filter(str.isdigit, cpf))
        if len(nums) != 11 or nums == nums[0] * 11:
            return False
        return True

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, nome={self._nome}, perfil={self._perfil})"

    def __repr__(self) -> str:
        return self.__str__()