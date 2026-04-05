def test_criar_produto(client):
    payload = {
        "nome": "Teclado Mecanico",
        "descricao": "Switch blue",
        "preco": 299.90,
        "quantidade": 10,
    }

    response = client.post("/produtos", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["nome"] == payload["nome"]
    assert body["descricao"] == payload["descricao"]
    assert body["preco"] == payload["preco"]
    assert body["quantidade"] == payload["quantidade"]
    assert "criado_em" in body


def test_listar_produtos(client):
    produtos = [
        {"nome": "Mouse", "descricao": "Sem fio", "preco": 120.0, "quantidade": 5},
        {"nome": "Monitor", "descricao": "24 polegadas", "preco": 899.9, "quantidade": 2},
    ]

    for produto in produtos:
        post_response = client.post("/produtos", json=produto)
        assert post_response.status_code == 201

    response = client.get("/produtos")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["nome"] == "Mouse"
    assert body[1]["nome"] == "Monitor"


def test_atualizar_produto_sucesso(client):
    payload = {
        "nome": "Notebook",
        "descricao": "16GB RAM",
        "preco": 4500.0,
        "quantidade": 3,
    }
    created = client.post("/produtos", json=payload)
    assert created.status_code == 201
    produto_id = created.json()["id"]

    update_payload = {
        "preco": 4299.9,
        "quantidade": 4,
    }

    response = client.put(f"/produtos/{produto_id}", json=update_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == produto_id
    assert body["nome"] == payload["nome"]
    assert body["preco"] == update_payload["preco"]
    assert body["quantidade"] == update_payload["quantidade"]


def test_atualizar_produto_nao_encontrado(client):
    response = client.put(
        "/produtos/9999",
        json={"preco": 10.0},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


def test_deletar_produto_sucesso(client):
    payload = {
        "nome": "Headset",
        "descricao": "USB",
        "preco": 199.9,
        "quantidade": 7,
    }
    created = client.post("/produtos", json=payload)
    assert created.status_code == 201
    produto_id = created.json()["id"]

    response = client.delete(f"/produtos/{produto_id}")

    assert response.status_code == 204

    list_response = client.get("/produtos")
    assert list_response.status_code == 200
    ids = [produto["id"] for produto in list_response.json()]
    assert produto_id not in ids


def test_deletar_produto_nao_encontrado(client):
    response = client.delete("/produtos/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"
