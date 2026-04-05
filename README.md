# CRUD FastAPI

Uma aplicacao simples de API REST construida com **FastAPI** e containerizada com **Docker**.

## Indice

- [Requisitos](#requisitos)
- [Instalacao](#instalacao)
- [Execucao](#execucao)
- [Docker](#docker)
- [Endpoints](#endpoints)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## Requisitos

- Python 3.11+
- Docker (opcional, para containerizacao)
- Docker Compose (opcional)

---

## Instalacao

### 1. Clone o repositorio

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

### 4. Instale as dependencias

```bash
pip install -r requirements.txt
```

---

## Execucao

### Localmente (sem Docker)

```bash
uvicorn app.main:app --reload
```

A API estara disponivel em: `http://localhost:8000`

### Documentacao interativa

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Docker

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

### SonarQube local

O `docker-compose.yaml` inclui um servico `sonarqube` para analise local.

#### 1. Suba o SonarQube

```powershell
docker compose up -d sonarqube
```

Acesse:

```text
http://localhost:9000
```

Login inicial padrao:

- usuario: `admin`
- senha: `admin`

#### 2. Gere um token no SonarQube

No SonarQube, gere um token de usuario e use esse valor no arquivo `.env`.

#### 3. Crie o arquivo `.env`

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Preencha estes valores no `.env`:

```dotenv
SONAR_HOST_URL=http://localhost:9000
SONAR_PROJECT_KEY=crud-fastapi
SONAR_TOKEN=<seu_token>
```

#### 4. Gere a cobertura antes da analise

O projeto usa o arquivo [`.coveragerc`](C:\Users\dario\PycharmProjects\crud-fastapi\.coveragerc) para gerar `coverage.xml` com caminhos relativos. Isso e importante para o SonarQube conseguir importar a cobertura corretamente.

```powershell
pytest --cov=app --cov-report=xml
```

Isso gera o arquivo `coverage.xml` na raiz do projeto.

#### 5. Execute a analise

Opcao 1, usando o scanner em container:

```powershell
$env:SONAR_DOCKER_HOST_URL="http://sonarqube:9000"
docker compose run --rm sonar-scanner
```

Opcao 2, usando `pysonar` localmente, se ele estiver instalado na sua maquina:

```powershell
pysonar `
  --sonar-host-url=$env:SONAR_HOST_URL `
  --sonar-token=$env:SONAR_TOKEN `
  --sonar-project-key=$env:SONAR_PROJECT_KEY
```

O `pysonar` local usa `http://localhost:9000`. O scanner em container precisa usar `http://sonarqube:9000`, porque `localhost` dentro do container aponta para ele mesmo.

#### 6. Abra o resultado no dashboard

Depois da execucao bem-sucedida, abra:

```text
http://localhost:9000/dashboard?id=crud-fastapi
```

#### Fluxo completo recomendado

```powershell
docker compose up -d sonarqube
pytest --cov=app --cov-report=xml
$env:SONAR_DOCKER_HOST_URL="http://sonarqube:9000"
docker compose run --rm sonar-scanner
```

#### Script pronto

O projeto inclui o script [`run-sonar.ps1`](C:\Users\dario\PycharmProjects\crud-fastapi\run-sonar.ps1) para automatizar o processo.

Fluxo padrao, com testes, cobertura e scanner em container:

```powershell
.\run-sonar.ps1
```

Pular a geracao da cobertura:

```powershell
.\run-sonar.ps1 -SkipTests
```

Usar `pysonar` local em vez do scanner em container:

```powershell
.\run-sonar.ps1 -UsePysonar
```

#### Solucao de problemas

- Se o projeto nao aparecer na interface, abra diretamente `http://localhost:9000/dashboard?id=crud-fastapi`.
- Se a analise subir mas a cobertura nao aparecer, rode novamente `pytest --cov=app --cov-report=xml` antes do scanner.
- Se o `coverage.xml` tiver caminho absoluto do Windows, o SonarQube ignora a cobertura. O [`.coveragerc`](C:\Users\dario\PycharmProjects\crud-fastapi\.coveragerc) ja foi ajustado para evitar isso.
- Se `pysonar` nao for reconhecido no terminal, use `docker compose run --rm sonar-scanner`.
- Se o scanner rodar dentro de container, nao use `http://localhost:9000` como host do Sonar, porque dentro do container `localhost` aponta para o proprio container.

---

## Endpoints

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

## Testes

Os testes estao configurados com `pytest` e descoberta automatica via `pytest.ini`.

### Rodar todos os testes

```powershell
pytest
```

### Rodar apenas os testes do model `Produto`

```powershell
pytest tests/test_model_produto.py
```

### Rodar apenas os testes dos endpoints de produtos

```powershell
pytest tests/test_produtos_endpoints.py
```

### Cobertura atual dos testes do model

Arquivo: `tests/test_model_produto.py`

- valida `__tablename__` da classe `Produto`
- valida tipos das colunas (`id`, `nome`, `descricao`, `preco`, `quantidade`, `criado_em`, `atualizado_em`)
- valida campos obrigatorios (`nome`, `preco`, `quantidade`) e campo opcional (`descricao`)
- valida configuracoes de `server_default` (`criado_em`) e `onupdate` (`atualizado_em`)

### Cobertura atual dos testes de endpoints

Arquivo: `tests/test_produtos_endpoints.py`

- valida criacao de produto com `POST /produtos` (status `201` e campos retornados)
- valida listagem de produtos com `GET /produtos` (status `200` e itens persistidos)

### Setup compartilhado de testes

Arquivo: `tests/conftest.py`

- cria banco SQLite em memoria para os testes
- sobrescreve `get_db` com `app.dependency_overrides` para isolar os testes do MySQL
- cria e remove tabelas a cada execucao da fixture `client`

---

## Estrutura do Projeto

```text
crud-fastapi/
|-- app/
|   |-- database.py       # Base declarativa do SQLAlchemy
|   |-- main.py           # Aplicacao FastAPI principal
|   `-- model.py          # Model SQLAlchemy (Produto)
|-- tests/
|   |-- conftest.py                 # Fixtures e override de DB para testes
|   |-- test_model_produto.py       # Testes unitarios do model
|   `-- test_produtos_endpoints.py  # Testes de integracao dos endpoints
|-- .gitignore           # Arquivos ignorados pelo Git
|-- Dockerfile           # Configuracao Docker
|-- docker-compose.yaml  # Orquestracao de containers
|-- pytest.ini           # Configuracao do pytest
|-- requirements.txt     # Dependencias Python
`-- README.md            # Este arquivo
```

### `app/main.py`

Arquivo principal da aplicacao contendo:

- Instancia do FastAPI
- Rotas e endpoints

### `Dockerfile`

Imagem Docker baseada em `python:3.11-slim` que:

- instala dependencias Python
- copia o codigo da aplicacao
- inicia o servidor Uvicorn na porta 8000

### `requirements.txt`

Lista de pacotes Python necessarios:

- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `SQLAlchemy` - ORM para modelagem de dados
- `pytest` - Framework de testes
- `pytest-cov` - Relatorio de cobertura de testes

---

## Desenvolvimento

### Adicionar uma nova rota

Edite `app/main.py`:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Com `--reload` ativo, a mudanca sera refletida automaticamente.

### Instalar novos pacotes

```bash
pip install <nome-do-pacote>
pip freeze > requirements.txt
```

Depois, rebuild a imagem Docker:

```powershell
docker build -t crud-fastapi .
```

---

## Notas

- O projeto usa `--reload` no Dockerfile para desenvolvimento
- Em producao, remova a flag `--reload` do `Dockerfile`
- Certifique-se de que a porta 8000 esta disponivel

---

## Licenca

MIT

---

## Contribuindo

Sinta-se livre para abrir issues e pull requests!
