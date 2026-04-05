from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db, Base
from app.model import Produto
from app.schemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse


# Criar tabelas
Base.metadata.create_all(bind=engine)


app = FastAPI(title="CRUD Produtos", version="1.0.0")


@app.post("/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


@app.get("/produtos", response_model=List[ProdutoResponse], status_code=status.HTTP_200_OK)
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    produtos = db.query(Produto).offset(skip).limit(limit).all()
    return produtos


# UPDATE
@app.put("/produtos/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    dados_atualizacao = produto.model_dump(exclude_unset=True)
    for campo, valor in dados_atualizacao.items():
        setattr(db_produto, campo, valor)

    db.commit()
    db.refresh(db_produto)
    return db_produto

# DELETE
@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}

@app.get("/")
def hello_world():
    return "Hello World!"


@app.get("/health")
def health_check():
    return {'status': 'Ok'}
