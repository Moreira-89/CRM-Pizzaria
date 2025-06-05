import hashlib

class Usuario:
    def __init__(self, id, nome, senha, perfil,  cpf, telefone):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.perfil = perfil
        self.cpf = cpf  
        self.telefone = telefone

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "senha": self.senha,
            "perfil": self.perfil,
            "cpf": self.cpf,
            "telefone": self.telefone
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id=data.get("id"),
            nome=data.get("nome"),
            senha=data.get("senha"),
            perfil=data.get("perfil"),
            cpf=data.get("cpf"),
            telefone=data.get("telefone")
        )
    @staticmethod
    def gerar_hash(senha):
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def validar_senha(self, senha):
        return self.senha == Usuario.gerar_hash(senha)