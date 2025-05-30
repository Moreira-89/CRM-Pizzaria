class Cliente:
    def __init__(self, id:str, nome: str, cpf_cnpj: str, email: str, telefone: str,
                 endereco: dict, geolocalizacao: dict, preferencias: dict, opt_in: dict):
        self.id = id
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.geolocalizacao = geolocalizacao
        self.preferencias = preferencias
        self.opt_in = opt_in

    #Transformando o objeto Cliente em um dicionario para armazenar dados no Firebase
    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf_cnpj": self.cpf_cnpj,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "geolocalizacao": self.geolocalizacao,
            "preferencias": self.preferencias,
            "opt_in": self.opt_in
        }
    #Metodo estatico que cria obj Cliente a partir de um dicionario (fonte do Firebase)
    @staticmethod
    def from_dict(data):
        return Cliente(
            id=data.get("id"),
            nome=data.get("nome"),
            cpf_cnpj=data.get("cpf_cnpj"),
            email=data.get("email"),
            telefone=data.get("telefone"),
            endereco=data.get("endereco"),
            geolocalizacao=data.get("geolocalizacao"),
            preferencias=data.get("preferencias"),
            opt_in=data.get("opt_in"),
            historico_pedidos=data.get("historico_pedidos")
        )