from config.firebase_config import FirebaseConfig


class FirebaseDAO:
    def __init__(self, collection):
        self.db = FirebaseConfig.get_instance().rtdb.child(collection)
        self.collection = collection

    def criar(self, id, data):
        self.db.child(id).set(data)

    def buscar_por_id(self, id):
        snapshot = self.db.child(id).get()
        return snapshot if snapshot else None

    def listar_todos(self):
        snapshot = self.db.get()
        return snapshot if snapshot else {}

    def atualizar(self, id, data):
        self.db.child(id).update(data)

    def deletar(self, id):
        self.db.child(id).delete()
