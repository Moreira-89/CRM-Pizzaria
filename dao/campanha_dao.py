from typing import Optional, List
import uuid
from dao.firebase_dao import FirebaseDAO
from models.campanha import Campanha

class CampanhaDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="campanhas")

    def criar(self, campanha: Campanha) -> Optional[str]:
        if not campanha.id:
            campanha.id = str(uuid.uuid4())
        if super().criar(campanha.id, campanha.to_dict()):
            return campanha.id
        return None

    def buscar_por_id(self, id: str) -> Optional[Campanha]:
        data = super().buscar_por_id(id)
        if data:
            return Campanha.from_dict(data)
        return None

    def listar_todos(self) -> List[Campanha]:
        dados = super().listar_todos()
        return [Campanha.from_dict(item) for item in dados if item]

    def atualizar(self, campanha: Campanha) -> bool:
        if not campanha.id:
            raise ValueError("ID da campanha não informado para atualização.")
        return super().atualizar(campanha.id, campanha.to_dict())

    def deletar(self, id: str) -> bool:
        return super().deletar(id)