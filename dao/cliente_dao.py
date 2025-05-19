from firebase_admin import db
from models.cliente import Cliente

class ClienteDAO:
    def __init__(self):
        self.ref = db.reference('/clientes')

    def criarCliente() -> str:
        novo_cliente_ref = self.ref.push(cliente.to_dict())
        return novo_cliente_ref.key
    
    def buscarPorId(self, id:str) -> Cliente:
        snapshot = self.ref.get()
        return  Cliente(id=id, **snapshot) if snapshot else None
    
    def buscarTodos(self) -> list[Cliente]:
        snapshot = self.ref.get()
        return [Cliente(id=key, **value) for key, value in snapshot.items()] if snapshot else []
    