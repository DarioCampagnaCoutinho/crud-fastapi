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

