from models.usuario import Usuario
from typing import Dict, Any

class Cliente(Usuario):
    """Modelo que representa um cliente da pizzaria."""
    def __init__(self, id: str, nome: str, cpf: str, email: str, 
                 telefone: str, endereco: Dict[str, str], preferencias: Dict[str, Any], 
                 opt_in: Dict[str, bool]):
        # Chama o construtor da classe pai
        super().__init__(id, nome, "Cliente", cpf, telefone)
        
        # Atributos específicos do Cliente
        self._email = email
        self._endereco = endereco or {}
        self._preferencias = preferencias or {}
        self._opt_in = opt_in or {}

    # Propriedades específicas do Cliente
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if not self._validar_email(value):
            raise ValueError("Email inválido")
        self._email = value

    @property
    def endereco(self) -> Dict[str, str]:
        return self._endereco.copy()  # Retorna cópia para evitar modificação direta
    
    @endereco.setter
    def endereco(self, value: Dict[str, str]):
        if not isinstance(value, dict):
            raise ValueError("Endereço deve ser um dicionário")
        
        # Validar campos obrigatórios do endereço
        campos_obrigatorios = ['rua', 'cidade', 'cep']
        for campo in campos_obrigatorios:
            if campo not in value or not value[campo]:
                raise ValueError(f"Campo '{campo}' é obrigatório no endereço")
        
        self._endereco = value.copy()

    @property
    def preferencias(self) -> Dict[str, Any]:
        return self._preferencias.copy()
    
    @preferencias.setter
    def preferencias(self, value: Dict[str, Any]):
        if not isinstance(value, dict):
            raise ValueError("Preferências devem ser um dicionário")
        self._preferencias = value.copy()

    @property
    def opt_in(self) -> Dict[str, bool]:
        return self._opt_in.copy()
    
    @opt_in.setter
    def opt_in(self, value: Dict[str, bool]):
        if not isinstance(value, dict):
            raise ValueError("Opt-in deve ser um dicionário")
        # Validar que todos os valores são booleanos
        for key, val in value.items():
            if not isinstance(val, bool):
                raise ValueError(f"Valor para '{key}' deve ser booleano")
        self._opt_in = value.copy()

    def to_dict(self) -> dict:
        """Sobrescreve o método da classe pai para incluir atributos específicos"""
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
        """Cria instância de Cliente a partir de dicionário"""
        # Cria instância sem validação inicial (dados do banco)
        instance = cls.__new__(cls)
        
        # Inicializa atributos da classe pai
        instance._id = data.get("id")
        instance._nome = data.get("nome")
        instance._perfil = "Cliente"
        instance._cpf = data.get("cpf")
        instance._telefone = data.get("telefone")
        
        # Inicializa atributos específicos
        instance._email = data.get("email")
        instance._endereco = data.get("endereco", {})
        instance._preferencias = data.get("preferencias", {})
        instance._opt_in = data.get("opt_in", {})
        
        return instance

    @staticmethod
    def _validar_email(email: str) -> bool:
        """Validação básica de email"""
        if not email or not isinstance(email, str):
            return False
        return "@" in email and "." in email.split("@")[-1]

    def aceitar_marketing(self, canal: str) -> bool:
        """Verifica se o cliente aceitou receber marketing por um canal específico"""
        return self._opt_in.get(canal, False)

    def atualizar_preferencia(self, chave: str, valor: Any) -> None:
        """Atualiza uma preferência específica"""
        self._preferencias[chave] = valor

    def __str__(self) -> str:
        return f"Cliente(id={self._id}, nome={self._nome}, email={self._email})"
