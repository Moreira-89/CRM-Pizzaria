from models.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, id:str, nome: str, cpf: str, email: str, telefone: str,
                 endereco: dict, preferencias: dict, opt_in: dict):
      
        super().__init__(id, nome, cpf, telefone)  
        self.email = email
        self.endereco = endereco
        self.preferencias = preferencias
        self.opt_in = opt_in

    #Transformando o objeto Cliente em um dicionario para armazenar dados no Firebase
    def to_dict(self):
        base = super().to_dict()
        base.update({
                "email": self.email,
                "telefone": self.telefone,
                "endereco": self.endereco,
                "preferencias": self.preferencias,
                "opt_in": self.opt_in
            })
        return base
    
    #Metodo estatico que cria obj Cliente a partir de um dicionario (fonte do Firebase)
    @staticmethod
    def from_dict(data):
        return Cliente(
            id=data.get("id"),
            nome=data.get("nome"),
            cpf=data.get("cpf"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            endereco=data.get("endereco"),
            preferencias=data.get("preferencias"),
            opt_in=data.get("opt_in"),
        )