from abc import ABC, abstractmethod
import re
import hashlib

class Usuario(ABC):
    """
    Classe base abstrata para representar usuários do sistema.
    Agora inclui também o campo 'senha_hash' para autenticação.
    """

    _PERFIS_VALIDOS = {"Funcionário", "Cliente", "Motoboy"}

    def __init__(self, 
                 id: str, 
                 nome: str, 
                 perfil: str, 
                 cpf: str, 
                 telefone: str, 
                 senha_plain: str = None,
                 senha_hash: str = None):
        """
        ou:
          - se fornecer senha_plain, gera internamente o hash, 
          - ou, se já tiver senha_hash, atribui diretamente (ex: ao carregar do BD).
        """
        self.id = id
        self.nome = nome
        self.perfil = perfil
        self.cpf = cpf
        self.telefone = telefone

        if senha_plain is not None:
            self.senha_hash = Usuario._gerar_hash(senha_plain)
        elif senha_hash is not None:
            self._senha_hash = senha_hash
        else:
            self._senha_hash = None

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
        pattern = re.compile(r'^[\d\-\s\(\)\+]+$')
        if not pattern.match(value):
            raise ValueError("Telefone contém caracteres inválidos")
        self._telefone = value.strip()

    @property
    def senha_hash(self) -> str:
        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, plain_or_hash: str):
        """
        Se for “já hash” (comprimento 64 hex) e conter apenas [0-9a-f],
        atribui diretamente. Senão, trata como senha “plana” e gera hash.
        """
        if not isinstance(plain_or_hash, str) or not plain_or_hash.strip():
            raise ValueError("Senha (ou hash) deve ser uma string não vazia")
        candidate = plain_or_hash.strip()
        if re.fullmatch(r"[0-9a-f]{64}", candidate):
            self._senha_hash = candidate
        else:
            self._senha_hash = Usuario._gerar_hash(candidate)

    @staticmethod
    def _gerar_hash(plain: str) -> str:
        """
        Gera um SHA256 hexdigest a partir da senha 'plain'.
        """
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria instância de Usuario (ou subclasse) a partir de dicionário,
        usando o campo 'senha_hash' direto.
        """
        instance = cls.__new__(cls)
        instance._id = data.get("id")
        instance._nome = data.get("nome")
        instance._perfil = data.get("perfil")
        instance._cpf = data.get("cpf")
        instance._telefone = data.get("telefone")
        instance._senha_hash = data.get("senha_hash", None)
        return instance

    def to_dict(self) -> dict:
        """
        Serializa o usuário para um dicionário, incluindo 'senha_hash'.
        """
        return {
            "id": self._id,
            "nome": self._nome,
            "perfil": self._perfil,
            "cpf": self._cpf,
            "telefone": self._telefone,
            "senha_hash": self._senha_hash
        }

    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
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
