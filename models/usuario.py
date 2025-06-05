class Usuario:
    def __init__(self, id, nome, cpf, telefone):
        self.id = id
        self.nome = nome
        self.cpf = cpf  
        self.telefone = telefone

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id=data.get("id"),
            nome=data.get("nome"),
            cpf=data.get("cpf"),
            telefone=data.get("telefone")
        )
