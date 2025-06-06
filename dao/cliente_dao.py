# dao/cliente_dao.py

import uuid
from typing import List, Optional, Dict
from dao.firebase_dao import FirebaseDAO
from models.cliente import Cliente
import logging

logger = logging.getLogger(__name__)


class ClienteDAO(FirebaseDAO):
    """
    DAO para operações CRUD de clientes no Firebase RTDB.
    Collection padrão: "clientes".
    """

    def __init__(self):
        super().__init__(collection="clientes")

    def criar(self, cliente: Cliente) -> Optional[str]:
        """
        Cria um novo cliente.

        Args:
            cliente: Instância de Cliente.

        Returns:
            str: ID gerado ou None se falhou.
        """
        try:
            if not isinstance(cliente, Cliente):
                raise ValueError("Parâmetro deve ser uma instância de Cliente")

            if not cliente.id:
                cliente.id = str(uuid.uuid4())

            # Verifica existência por CPF ou e-mail antes de criar
            if self._cliente_existe_por_cpf_ou_email(cliente.cpf, cliente.email):
                raise ValueError("Já existe cliente com este CPF ou e-mail")

            sucesso = super().criar(cliente.id, cliente.to_dict())
            if sucesso:
                return cliente.id
            return None

        except Exception as e:
            logger.error(f"[clientes] Erro ao criar cliente: {e}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Cliente]:
        """
        Busca cliente pelo ID.

        Args:
            id: ID do cliente.

        Returns:
            Cliente: Instância ou None se não encontrado.
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Cliente.from_dict(data)
            return None
        except Exception as e:
            logger.error(f"[clientes] Erro ao buscar cliente por ID '{id}': {e}")
            return None

    def buscar_por_nome(self, nome: str) -> Optional[Cliente]:
        """
        Busca primeiro cliente com nome exato (case-insensitive).

        Args:
            nome: Nome do cliente.

        Returns:
            Cliente: Instância ou None se não encontrado.
        """
        try:
            if not nome or not isinstance(nome, str):
                return None

            todos = self.listar_todos()
            for c in todos:
                if c.nome.lower() == nome.lower():
                    return c
            return None
        except Exception as e:
            logger.error(f"[clientes] Erro ao buscar cliente por nome '{nome}': {e}")
            return None

    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """
        Busca cliente pelo e-mail (case-insensitive).

        Args:
            email: E-mail do cliente.

        Returns:
            Cliente: Instância ou None se não encontrado.
        """
        try:
            if not email or not isinstance(email, str):
                return None

            todos = self.listar_todos()
            for c in todos:
                if c.email.lower() == email.lower():
                    return c
            return None
        except Exception as e:
            logger.error(f"[clientes] Erro ao buscar cliente por e-mail '{email}': {e}")
            return None

    def buscar_por_cpf(self, cpf: str) -> Optional[Cliente]:
        """
        Busca cliente pelo CPF (ignora formatação, compara somente dígitos).

        Args:
            cpf: CPF do cliente.

        Returns:
            Cliente: Instância ou None se não encontrado.
        """
        try:
            if not cpf or not isinstance(cpf, str):
                return None

            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            todos = self.listar_todos()
            for c in todos:
                c_cpf_limpo = ''.join(filter(str.isdigit, c.cpf))
                if c_cpf_limpo == cpf_limpo:
                    return c
            return None
        except Exception as e:
            logger.error(f"[clientes] Erro ao buscar cliente por CPF '{cpf}': {e}")
            return None

    def listar_todos(self) -> List[Cliente]:
        """
        Lista todos os clientes.

        Returns:
            List[Cliente]: Lista de instâncias de Cliente.
        """
        try:
            dados = super().listar_todos()
            return [Cliente.from_dict(item) for item in dados if item]
        except Exception as e:
            logger.error(f"[clientes] Erro ao listar clientes: {e}")
            return []

    def listar_por_cidade(self, cidade: str) -> List[Cliente]:
        """
        Lista clientes cujo campo 'endereco' contém a cidade informada (case-insensitive).
        Considera que 'endereco' pode ser string ou dicionário.

        Args:
            cidade: Nome da cidade.

        Returns:
            List[Cliente]: Clientes da cidade.
        """
        try:
            if not cidade or not isinstance(cidade, str):
                return []

            todos = self.listar_todos()
            resultado = []
            for c in todos:
                # Supondo que c.endereco seja string: extrair nome da cidade
                endereco = c.endereco.lower()
                if cidade.lower() in endereco:
                    resultado.append(c)
            return resultado

        except Exception as e:
            logger.error(f"[clientes] Erro ao listar clientes por cidade '{cidade}': {e}")
            return []

    def listar_com_opt_in(self, canal: str) -> List[Cliente]:
        """
        Lista clientes que aceitaram receber comunicações por um canal específico.

        Args:
            canal: 'email', 'sms' ou 'whatsapp'.

        Returns:
            List[Cliente]: Clientes com opt-in ativo no canal.
        """
        try:
            if not canal or not isinstance(canal, str):
                return []

            todos = self.listar_todos()
            return [c for c in todos if c.aceitar_marketing(canal)]
        except Exception as e:
            logger.error(f"[clientes] Erro ao listar clientes com opt-in '{canal}': {e}")
            return []

    def atualizar(self, cliente: Cliente) -> bool:
        """
        Atualiza dados de um cliente existente.

        Args:
            cliente: Instância de Cliente com ID preenchido.

        Returns:
            bool: True se atualizado com sucesso, False caso contrário.
        """
        try:
            if not isinstance(cliente, Cliente):
                raise ValueError("Parâmetro deve ser uma instância de Cliente")
            if not cliente.id:
                raise ValueError("ID do cliente não informado para atualização")

            return super().atualizar(cliente.id, cliente.to_dict())
        except Exception as e:
            logger.error(f"[clientes] Erro ao atualizar cliente '{getattr(cliente, 'id', None)}': {e}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Deleta um cliente pelo ID.

        Args:
            id: ID do cliente.

        Returns:
            bool: True se excluído com sucesso, False caso contrário.
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"[clientes] Erro ao deletar cliente '{id}': {e}")
            return False

    def _cliente_existe_por_cpf_ou_email(self, cpf: str, email: str) -> bool:
        """
        Verifica se já existe cliente com CPF ou e-mail fornecidos.

        Args:
            cpf: CPF a verificar.
            email: E-mail a verificar.

        Returns:
            bool: True se já existir, False caso contrário.
        """
        try:
            return (self.buscar_por_cpf(cpf) is not None) or (self.buscar_por_email(email) is not None)
        except Exception:
            return False

    def contar_por_cidade(self) -> Dict[str, int]:
        """
        Conta quantos clientes há em cada cidade (extraída do campo 'endereco').

        Returns:
            Dict[cidade, quantidade]: Dicionário de contagem por cidade.
        """
        try:
            todos = self.listar_todos()
            contador: Dict[str, int] = {}
            for c in todos:
                endereco = c.endereco.lower()
                # Supõe-se que a cidade esteja no endereço separado por vírgulas, ex: "Rua X, Bairro Y, Cidade Z"
                partes = [parte.strip() for parte in endereco.split(",")]
                cidade = partes[-1] if partes else "Não informado"
                contador[cidade] = contador.get(cidade, 0) + 1
            return contador
        except Exception as e:
            logger.error(f"[clientes] Erro ao contar clientes por cidade: {e}")
            return {}
