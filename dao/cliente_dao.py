import uuid
from typing import List, Optional
from dao.firebase_dao import FirebaseDAO
from models.cliente import Cliente
import logging

logger = logging.getLogger(__name__)

class ClienteDAO(FirebaseDAO):
    """DAO para operações com clientes"""
    
    def __init__(self):
        super().__init__(collection="clientes")

    def criar(self, cliente: Cliente) -> Optional[str]:
        """
        Cria um novo cliente
        
        Args:
            cliente: Instância de Cliente
            
        Returns:
            str: ID do cliente criado ou None se falhou
        """
        try:
            if not isinstance(cliente, Cliente):
                raise ValueError("Parâmetro deve ser uma instância de Cliente")
            
            if not cliente.id:
                cliente.id = str(uuid.uuid4())
            
            # Verifica se já existe cliente com mesmo CPF ou email
            if self._cliente_existe_por_cpf_ou_email(cliente.cpf, cliente.email):
                raise ValueError("Já existe cliente com este CPF ou email")
            
            if super().criar(cliente.id, cliente.to_dict()):
                return cliente.id
            return None
            
        except Exception as e:
            logger.error(f"Erro ao criar cliente: {str(e)}")
            return None

    def buscar_por_id(self, id: str) -> Optional[Cliente]:
        """
        Busca cliente por ID
        
        Args:
            id: ID do cliente
            
        Returns:
            Cliente: Instância do cliente ou None se não encontrado
        """
        try:
            data = super().buscar_por_id(id)
            if data:
                return Cliente.from_dict(data)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por ID {id}: {str(e)}")
            return None
    
    def buscar_por_nome(self, nome: str) -> Optional[Cliente]:
        """
        Busca cliente por nome (case-insensitive)
        
        Args:
            nome: Nome do cliente
            
        Returns:
            Cliente: Primeira ocorrência encontrada ou None
        """
        try:
            if not nome or not isinstance(nome, str):
                return None
            
            clientes = self.listar_todos()
            for cliente in clientes:
                if cliente.nome.lower() == nome.lower():
                    return cliente
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por nome {nome}: {str(e)}")
            return None

    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """
        Busca cliente por email
        
        Args:
            email: Email do cliente
            
        Returns:
            Cliente: Instância do cliente ou None se não encontrado
        """
        try:
            if not email or not isinstance(email, str):
                return None
            
            clientes = self.listar_todos()
            for cliente in clientes:
                if cliente.email.lower() == email.lower():
                    return cliente
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por email {email}: {str(e)}")
            return None

    def buscar_por_cpf(self, cpf: str) -> Optional[Cliente]:
        """
        Busca cliente por CPF
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            Cliente: Instância do cliente ou None se não encontrado
        """
        try:
            if not cpf or not isinstance(cpf, str):
                return None
            
            # Remove formatação do CPF
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            
            clientes = self.listar_todos()
            for cliente in clientes:
                cpf_cliente_limpo = ''.join(filter(str.isdigit, cliente.cpf))
                if cpf_cliente_limpo == cpf_limpo:
                    return cliente
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar cliente por CPF {cpf}: {str(e)}")
            return None

    def listar_todos(self) -> List[Cliente]:
        """
        Lista todos os clientes
        
        Returns:
            List[Cliente]: Lista de clientes
        """
        try:
            dados = super().listar_todos()
            return [Cliente.from_dict(item) for item in dados if item]
            
        except Exception as e:
            logger.error(f"Erro ao listar clientes: {str(e)}")
            return []

    def listar_por_cidade(self, cidade: str) -> List[Cliente]:
        """
        Lista clientes por cidade
        
        Args:
            cidade: Nome da cidade
            
        Returns:
            List[Cliente]: Lista de clientes da cidade
        """
        try:
            if not cidade:
                return []
            
            clientes = self.listar_todos()
            return [
                cliente for cliente in clientes 
                if cliente.endereco.get('cidade', '').lower() == cidade.lower()
            ]
            
        except Exception as e:
            logger.error(f"Erro ao listar clientes por cidade {cidade}: {str(e)}")
            return []

    def listar_com_opt_in(self, canal: str) -> List[Cliente]:
        """
        Lista clientes que aceitaram receber comunicação por um canal específico
        
        Args:
            canal: Canal de comunicação (email, sms, whatsapp, etc.)
            
        Returns:
            List[Cliente]: Lista de clientes com opt-in ativo
        """
        try:
            clientes = self.listar_todos()
            return [
                cliente for cliente in clientes 
                if cliente.aceitar_marketing(canal)
            ]
            
        except Exception as e:
            logger.error(f"Erro ao listar clientes com opt-in {canal}: {str(e)}")
            return []

    def atualizar(self, cliente: Cliente) -> bool:
        """
        Atualiza um cliente existente
        
        Args:
            cliente: Instância do cliente com dados atualizados
            
        Returns:
            bool: True se atualizado com sucesso
        """
        try:
            if not isinstance(cliente, Cliente):
                raise ValueError("Parâmetro deve ser uma instância de Cliente")
            
            if not cliente.id:
                raise ValueError("ID do cliente não informado para atualização")
            
            return super().atualizar(cliente.id, cliente.to_dict())
            
        except Exception as e:
            logger.error(f"Erro ao atualizar cliente {cliente.id}: {str(e)}")
            return False

    def deletar(self, id: str) -> bool:
        """
        Remove um cliente
        
        Args:
            id: ID do cliente
            
        Returns:
            bool: True se removido com sucesso
        """
        try:
            return super().deletar(id)
        except Exception as e:
            logger.error(f"Erro ao deletar cliente {id}: {str(e)}")
            return False

    def _cliente_existe_por_cpf_ou_email(self, cpf: str, email: str) -> bool:
        """
        Verifica se já existe cliente com o CPF ou email informado
        
        Args:
            cpf: CPF a verificar
            email: Email a verificar
            
        Returns:
            bool: True se já existe
        """
        try:
            return (self.buscar_por_cpf(cpf) is not None or 
                    self.buscar_por_email(email) is not None)
        except Exception:
            return False

    def contar_por_cidade(self) -> dict:
        """
        Conta clientes agrupados por cidade
        
        Returns:
            dict: Dicionário com cidade como chave e quantidade como valor
        """
        try:
            clientes = self.listar_todos()
            contador = {}
            
            for cliente in clientes:
                cidade = cliente.endereco.get('cidade', 'Não informado')
                contador[cidade] = contador.get(cidade, 0) + 1
            
            return contador
            
        except Exception as e:
            logger.error(f"Erro ao contar clientes por cidade: {str(e)}")
            return {}