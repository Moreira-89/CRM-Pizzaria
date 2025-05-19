class Cliente:
    def __init__(self, id:str, nome: str, cpf: str, email: str, telefone: str,
                 endereco: dict, geolocalizacao: dict, preferencias: dict, opt_in: dict):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.geolocalizacao = geolocalizacao
        self.preferencias = preferencias
        self.opt_in = opt_in

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "geolocalizacao": self.geolocalizacao,
            "preferencias": self.preferencias,
            "opt_in": self.opt_in
        }