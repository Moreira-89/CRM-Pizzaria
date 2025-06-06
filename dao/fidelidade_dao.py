from typing import Optional, List
import uuid
from dao.firebase_dao import FirebaseDAO
from models.fidelidade import Fidelidade

class FidelidadeDAO(FirebaseDAO):
    def __init__(self):
        super().__init__(collection="fidelidade")

    def criar(self, fidelidade: Fidelidade) -> Optional[str]:
        if not fidelidade.id:
            fidelidade.id = str(uuid.uuid4())
        if super().criar(fidelidade.id, fidelidade.to_dict()):
            return fidelidade.id
        return None

    def buscar_por_id(self, id: str) -> Optional[Fidelidade]:
        data = super().buscar_por_id(id)
        if data:
            return Fidelidade.from_dict(data)
        return None

    def listar_todos(self) -> List[Fidelidade]:
        dados = super().listar_todos()
        return [Fidelidade.from_dict(item) for item in dados if item]

    def atualizar(self, fidelidade: Fidelidade) -> bool:
        if not fidelidade.id:
            raise ValueError("ID da fidelidade não informado para atualização.")
        return super().atualizar(fidelidade.id, fidelidade.to_dict())

    def deletar(self, id: str) -> bool:
        return super().deletar(id)