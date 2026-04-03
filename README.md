# CRUD FastAPI

Uma aplicação simples de API REST construída com **FastAPI** e containerizada com **Docker**.

## 📋 Índice

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Execução](#execução)
- [Docker](#docker)
- [Endpoints](#endpoints)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## 📦 Requisitos

- Python 3.11+
- Docker (opcional, para containerização)
- Docker Compose (opcional)

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd crud-fastapi
```

### 2. Crie um ambiente virtual

```powershell
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Execução

### Localmente (sem Docker)

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

### Documentação interativa

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🐳 Docker

### Build da imagem

```powershell
docker build -t crud-fastapi .
```

### Rodar o container

```powershell
docker run -p 8000:8000 crud-fastapi
```

### Rodar com volume (desenvolvimento)

```powershell
docker run -p 8000:8000 -v "C:\Users\dario\PycharmProjects\crud-fastapi\app:/app/app" crud-fastapi
```

### Usar Docker Compose

```powershell
docker-compose up
```

Para parar:

```powershell
docker-compose down
```

---

## 🔌 Endpoints

### GET `/`

Retorna uma mensagem simples.

**Resposta:**
```json
"Hello World!"
```

**Exemplo:**
```powershell
curl http://localhost:8000
```

---

## 📁 Estrutura do Projeto

```
crud-fastapi/
├── app/
│   └── main.py          # Aplicação FastAPI principal
├── .gitignore           # Arquivos ignorados pelo Git
├── Dockerfile           # Configuração Docker
├── docker-compose.yaml  # Orquestração de containers
├── requirements.txt     # Dependências Python
└── README.md            # Este arquivo
```

### `app/main.py`

Arquivo principal da aplicação contendo:
- Instância do FastAPI
- Rotas e endpoints

### `Dockerfile`

Imagem Docker baseada em `python:3.11-slim` que:
- Instala dependências Python
- Copia o código da aplicação
- Inicia o servidor Uvicorn na porta 8000

### `requirements.txt`

Lista de pacotes Python necessários:
- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI

---

## 🛠️ Desenvolvimento

### Adicionar uma nova rota

Edite `app/main.py`:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Com `--reload` ativo, a mudança será refletida automaticamente.

### Instalar novos pacotes

```bash
pip install <nome-do-pacote>
pip freeze > requirements.txt
```

Depois rebuild a imagem Docker:

```powershell
docker build -t crud-fastapi .
```

---

## 📝 Notas

- O projeto usa `--reload` no Dockerfile para desenvolvimento
- Em produção, remova a flag `--reload` do `Dockerfile`
- Certifique-se de que a porta 8000 está disponível

---

## 📄 Licença

MIT

---

## 🤝 Contribuindo

Sinta-se livre para abrir issues e pull requests!

