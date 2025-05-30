import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import logging

logger = logging.getLogger(__name__)

class FirebaseConfig:
    _instance = None

    def __init__(self):
        if not firebase_admin._apps:
            self._initialize_firebase()

    def _initialize_firebase(self):
        try:
            # Verifica se todas as chaves necessárias estão presentes
            required_keys = ["PROJECT_ID", "DATABASE_SECRET", "CLIENT_EMAIL", "DATABASE_URL"]
            for key in required_keys:
                if key not in st.secrets["FIREBASE"]:
                    raise KeyError(f"Chave secreta ausente: FIREBASE.{key}")

            # Configuração das credenciais
            cred_dict = {
                "type": "service_account",
                "project_id": st.secrets["FIREBASE"]["PROJECT_ID"],
                "private_key": st.secrets["FIREBASE"]["DATABASE_SECRET"],
                "client_email": st.secrets["FIREBASE"]["CLIENT_EMAIL"],
                "token_uri": "https://oauth2.googleapis.com/token"
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(
                cred,
                { 'databaseURL': st.secrets["FIREBASE"]["DATABASE_URL"] }
            )
            logger.info("Firebase configurado com sucesso (sem Storage)!")
            
        except Exception as e:
            logger.error(f"Falha na inicialização do Firebase: {str(e)}")
            raise RuntimeError(f"Erro no Firebase: {str(e)}")
    
    @property
    def rtdb(self):
        """Retorna a referência do Realtime Database"""
        return db.reference()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = FirebaseConfig()
        return cls._instance