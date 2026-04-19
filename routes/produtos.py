from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Produto

router = APIRouter(prefix="/produto", tags=["Produtos"])

@router.get("/{dun14}")
def buscar_produto(dun14: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.dun14 == dun14).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"dun14": produto.dun14, "nome": produto.nome, "unidade": produto.unidade}