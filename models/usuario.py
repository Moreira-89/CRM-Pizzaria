from abc import ABC

class Usuario(ABC):
    """Classe base para representar usuários do sistema."""
    def __init__(self, id: str, nome: str,  perfil: str, cpf: str, telefone: str):
        self._id = id
        self._nome = nome
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
        """Serializa o usuário para um dicionário simples."""
        return {
            "id": self._id,
            "nome": self._nome,
            "perfil": self._perfil,
            "cpf": self._cpf,
            "telefone": self._telefone
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Cria instância de ``Usuario`` a partir de um dicionário."""
        instance = cls.__new__(cls)
        instance._id = data.get("id")
        instance._nome = data.get("nome")
        instance._perfil = data.get("perfil")
        instance._cpf = data.get("cpf")
        instance._telefone = data.get("telefone")
        return instance

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
