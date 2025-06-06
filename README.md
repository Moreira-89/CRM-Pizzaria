# 🍕 CRM Pizzaria

Um sistema de CRM desenvolvido para uma pizzaria, com funcionalidades de gestão de clientes, motoboys, avaliações, campanhas de marketing e programa de fidelidade.

## 🚀 Tecnologias Utilizadas

- Python
- Streamlit (Interface Web)
- Firebase Realtime Database (Backend)
- Firebase Admin SDK (Autenticação e dados)
- Graphviz (Para diagramas - opcional)

## 🔥 Funcionalidades Principais

- 🔐 Login com senha e controle de acesso por perfil (**Funcionário**, **Motoboy**, **Cliente**)
- 🧑‍💼 Gestão de Clientes (CRUD)
- 🏍️ Gestão de Motoboys (CRUD)
- 💬 Avaliação 360° (feedback de clientes e da operação)
- 🏆 Programa de Fidelidade
- 📣 Campanhas de Marketing
- 📊 Dashboard consolidado de operação
- ✅ Cadastro interno de usuários

## 🗂️ Estrutura de Pastas

crm-pizzaria/
├── app.py # Ponto de entrada da aplicação
├── requirements.txt # Dependências
├── config/
│ └── firebase_config.py # Configurações do Firebase
├── models/ # Modelos de dados
│ ├── usuario.py
│ ├── cliente.py
│ ├── motoboy.py
│ ├── avaliacao.py
│ ├── fidelidade.py
│ └── campanha.py
├── dao/ # Acesso ao Firebase
│ ├── firebase_dao.py
│ ├── usuario_dao.py
│ ├── cliente_dao.py
│ ├── motoboy_dao.py
│ ├── avaliacao_dao.py
│ ├── fidelidade_dao.py
│ └── campanha_dao.py
├── views/ # Interfaces Streamlit
│ ├── login.py
│ ├── cadastro_usuario.py #AINDA NAO IMPLEMENTADO
│ ├── cliente_page.py
│ ├── motoboy_page.py
│ ├── avaliacao_page.py
│ ├── fidelidade_page.py
│ ├── campanha_page.py
│ └── dashboard_page.py


## 🔧 Configuração Inicial

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/crm-pizzaria.git
cd crm-pizzaria
```
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Configure o Firebase:
- Crie um arquivo `.streamlit/secrets.toml` com:
```bash
[FIREBASE]
PROJECT_ID = "seu-project-id"
DATABASE_SECRET = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL = "seu-email-do-firebase"
DATABASE_URL = "https://seu-projeto.firebaseio.com"

```

