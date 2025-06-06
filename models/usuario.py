import hashlib
from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, id: str, nome: str, senha: str, perfil: str, cpf: str, telefone: str):
        self._id = id
        self._nome = nome
        self._senha = self._gerar_hash(senha) if senha else None
        self._perfil = perfil
        self._cpf = cpf  
        self._telefone = telefone

    # Propriedades (getters e setters)
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
    def senha(self) -> str:
        return self._senha
    
    @senha.setter
    def senha(self, value: str):
        if not value:
            raise ValueError("Senha não pode ser vazia")
        self._senha = self._gerar_hash(value)

    @property
    def perfil(self) -> str:
        return self._perfil
    
    @perfil.setter
    def perfil(self, value: str):
        perfis_validos = ["Funcionário", "Cliente", "Motoboy"]
        if value not in perfis_validos:
            raise ValueError(f"Perfil deve ser um dos seguintes: {perfis_validos}")
        self._perfil = value

    @property
    def cpf(self) -> str:
        return self._cpf
    
    @cpf.setter
    def cpf(self, value: str):
        if not self._validar_cpf(value):
            raise ValueError("CPF inválido")
        self._cpf = value

    @property
    def telefone(self) -> str:
        return self._telefone
    
    @telefone.setter
    def telefone(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Telefone deve ser uma string não vazia")
        self._telefone = value

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "senha": self._senha,
            "perfil": self._perfil,
            "cpf": self._cpf,
            "telefone": self._telefone
        }

    @classmethod
    def from_dict(cls, data: dict):
        # Cria instância sem hash da senha (já está hasheada no banco)
        instance = cls.__new__(cls)
        instance._id = data.get("id")
        instance._nome = data.get("nome")
        instance._senha = data.get("senha")  # Já hasheada
        instance._perfil = data.get("perfil")
        instance._cpf = data.get("cpf")
        instance._telefone = data.get("telefone")
        return instance

    @staticmethod
    def _gerar_hash(senha: str) -> str:
        """Gera hash SHA256 da senha"""
        if not senha:
            raise ValueError("Senha não pode ser vazia")
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def validar_senha(self, senha: str) -> bool:
        """Valida se a senha fornecida corresponde à senha armazenada"""
        if not senha:
            return False
        return self._senha == self._gerar_hash(senha)

    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """Validação básica de CPF"""
        if not cpf or not isinstance(cpf, str):
            return False
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        return len(cpf) == 11 and not cpf == cpf[0] * 11

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, nome={self._nome}, perfil={self._perfil})"

    def __repr__(self) -> str:
        return self.__str__()