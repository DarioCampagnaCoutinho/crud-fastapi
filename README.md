# CRUD FastAPI

Uma aplicacao simples de API REST construida com **FastAPI** e containerizada com **Docker**.

## Indice

- [Requisitos](#requisitos)
- [Instalacao](#instalacao)
- [Execucao](#execucao)
- [Docker](#docker)
- [Observabilidade](#observabilidade)
- [Endpoints](#endpoints)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## Requisitos

- Python 3.11+
- MySQL 8.0, se for executar sem Docker
- Docker e Docker Compose Plugin (opcional, para containerizacao)

---

## Instalacao

### 1. Clone o repositorio

```bash
git clone <seu-repositorio>
cd crud-fastapi
```

### 2. Crie um ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ative o ambiente virtual

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
source .venv/bin/activate
```

### 4. Instale as dependencias

```bash
pip install -r requirements.txt
```

---

## Execucao

### Localmente (sem Docker)

Defina a variavel `DATABASE_URL` para um MySQL em execucao. Exemplo:

```powershell
$env:DATABASE_URL="mysql+pymysql://user:user123@localhost:3306/crud_db"
```

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
docker run -p 8000:8000 `
  -e DATABASE_URL="mysql+pymysql://user:user123@host.docker.internal:3306/crud_db" `
  crud-fastapi
```

### Rodar com volume (desenvolvimento)

```powershell
docker run -p 8000:8000 -v "C:\Users\dario\PycharmProjects\crud-fastapi\app:/app/app" crud-fastapi
```

Observacao: esse modo tambem precisa de `DATABASE_URL` apontando para um MySQL acessivel pelo container.

### Usar Docker Compose

```powershell
docker compose up
```

Para parar:

```powershell
docker compose down
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

## Observabilidade

O projeto agora inclui um stack basico de observabilidade com:

- `Grafana` para dashboards
- `Prometheus` para metricas
- `Loki` para armazenamento e consulta de logs
- `Promtail` para coleta de logs dos containers Docker

### Subir o stack

```powershell
docker compose up -d grafana prometheus loki promtail
```

### URLs

- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`
- Loki API: `http://localhost:3100/loki/api/v1/status/buildinfo`
- Loki healthcheck: `http://localhost:3100/ready`

Observacao: acessar `http://localhost:3100/` diretamente retorna `404 not found` e isso e esperado. O Loki nao expoe uma UI na raiz; use o Grafana para explorar logs ou os endpoints acima para validar o servico.

### Credenciais padrao do Grafana

- usuario: `admin`
- senha: `admin`

Voce pode sobrescrever essas credenciais com as variaveis `GRAFANA_ADMIN_USER` e `GRAFANA_ADMIN_PASSWORD`.

### Como os logs chegam ao Grafana

- O `promtail` descobre os containers via Docker socket
- Os logs `stdout` e `stderr` dos containers sao enviados ao `loki`
- O `grafana` ja sobe com `Prometheus` e `Loki` provisionados como datasources

### Ver logs no Grafana

1. Abra `http://localhost:3000`
2. Va em `Explore`
3. Selecione a datasource `Loki`
4. Consulte, por exemplo:

```text
{compose_project="crud-fastapi"}
```

Ou filtre por servico:

```text
{compose_service="api"}
```

### Observacao sobre metricas

O `Prometheus` ja esta pronto no Compose, mas a API FastAPI ainda nao expoe um endpoint `/metrics`. Portanto:

- logs no Grafana/Loki ja ficam disponiveis com esse stack
- metricas detalhadas da aplicacao ainda exigem instrumentacao da API

Se quiser, o proximo passo natural e adicionar metricas da FastAPI para o `Prometheus`.

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

### GET `/health`

Retorna o status basico da aplicacao.

**Resposta:**

```json
{
  "status": "Ok"
}
```

### POST `/produtos`

Cria um novo produto.

**Exemplo de payload:**

```json
{
  "nome": "Teclado Mecanico",
  "descricao": "Switch blue",
  "preco": 299.9,
  "quantidade": 10
}
```

### GET `/produtos`

Lista os produtos cadastrados.

Parametros opcionais:

- `skip`: deslocamento inicial da consulta
- `limit`: quantidade maxima de itens retornados

### PUT `/produtos/{produto_id}`

Atualiza parcialmente um produto existente.

**Exemplo de payload:**

```json
{
  "preco": 4299.9,
  "quantidade": 4
}
```

Se o produto nao existir, retorna `404`.

### DELETE `/produtos/{produto_id}`

Remove um produto existente.

Se o produto nao existir, retorna `404`.

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
- valida atualizacao de produto com `PUT /produtos/{id}` (status `200`)
- valida erro ao atualizar produto inexistente (status `404`)
- valida exclusao de produto com `DELETE /produtos/{id}` (status `204`)
- valida erro ao excluir produto inexistente (status `404`)

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
|   |-- database.py       # Configuracao do banco e sessao SQLAlchemy
|   |-- main.py           # Aplicacao FastAPI principal e endpoints
|   |-- model.py          # Model SQLAlchemy (Produto)
|   `-- schemas.py        # Schemas Pydantic de entrada e saida
|-- monitoring/
|   |-- grafana/
|   |   `-- provisioning/
|   |       `-- datasources/
|   |           `-- datasources.yml  # Datasources provisionadas no Grafana
|   |-- loki/
|   |   `-- loki-config.yml          # Configuracao do Loki
|   |-- prometheus/
|   |   `-- prometheus.yml           # Configuracao do Prometheus
|   `-- promtail/
|       `-- promtail-config.yml      # Configuracao do Promtail
|-- tests/
|   |-- conftest.py                 # Fixtures e override de DB para testes
|   |-- test_model_produto.py       # Testes unitarios do model
|   `-- test_produtos_endpoints.py  # Testes de integracao dos endpoints
|-- .env.example         # Exemplo de variaveis de ambiente
|-- .gitignore           # Arquivos ignorados pelo Git
|-- Dockerfile           # Configuracao Docker
|-- docker-compose.yaml  # Orquestracao de containers
|-- pytest.ini           # Configuracao do pytest
|-- requirements.txt     # Dependencias Python
|-- run-sonar.ps1        # Script auxiliar para analise no SonarQube
|-- sonar-project.properties  # Configuracao do projeto Sonar
`-- README.md            # Este arquivo
```

### `app/main.py`

Arquivo principal da aplicacao contendo:

- Instancia do FastAPI
- Rotas `GET /`, `GET /health`, `POST /produtos`, `GET /produtos`, `PUT /produtos/{id}` e `DELETE /produtos/{id}`

### `app/database.py`

Contem:

- leitura da variavel de ambiente `DATABASE_URL`
- criacao do `engine` SQLAlchemy
- fabrica de sessoes `SessionLocal`
- dependencia `get_db`

### `app/schemas.py`

Define os schemas Pydantic:

- `ProdutoCreate`
- `ProdutoUpdate`
- `ProdutoResponse`

### `Dockerfile`

Imagem Docker baseada em `python:3.11-slim` que:

- instala dependencias Python
- copia o codigo da aplicacao
- inicia o servidor Uvicorn na porta 8000
- usa `--reload`, o que favorece desenvolvimento, nao producao

### `requirements.txt`

Lista de pacotes Python necessarios:

- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `SQLAlchemy` - ORM para modelagem de dados
- `PyMySQL` - Driver MySQL usado pela aplicacao
- `pydantic` - Validacao e serializacao dos schemas
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

- A aplicacao cria as tabelas automaticamente ao iniciar via `Base.metadata.create_all(bind=engine)`
- O projeto usa `--reload` no Dockerfile para desenvolvimento
- Em producao, remova a flag `--reload` do `Dockerfile`
- A execucao local sem Docker depende de um MySQL acessivel pela `DATABASE_URL`
- Certifique-se de que as portas `8000`, `3000`, `3100`, `9090` e `9000` estejam disponiveis quando usar o stack completo

---

## Licenca

MIT

---

## Contribuindo

Sinta-se livre para abrir issues e pull requests!
