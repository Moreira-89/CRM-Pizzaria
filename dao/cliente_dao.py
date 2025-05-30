import uuid
from dao.firebase_dao import FirebaseDAO
from models.cliente import Cliente


class ClienteDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="clientes")

    def criar(self, cliente: Cliente):
        if not cliente.id:
            cliente.id = str(uuid.uuid4())
        self.db.child(self.collection).child(cliente.id).set(cliente.to_dict())
        return cliente.id

    def buscar_por_id(self, id):
        data = self.db.child(self.collection).child(id).get()
        if data:
            return Cliente.from_dict(data)
        return None
    
    def buscar_por_nome(self, nome):
        data = self.db.get()
        if data and data.val():
            for item in data.val().values():
                if item.get("nome", "").lower() == nome.lower():
                    return item  # Retorna o dicionário do cliente
        return None

    def listar_todos(self):
        data = self.db.child(self.collection).get()
        if data:
            return [Cliente.from_dict(item) for item in data.values()]
        return []

    def atualizar(self, cliente: Cliente):
        if not cliente.id:
            raise ValueError("ID do cliente não informado para atualização.")
        self.db.child(self.collection).child(cliente.id).update(cliente.to_dict())

    def deletar(self, id):
        self.db.child(self.collection).child(id).remove()