from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Recebimento, ItemRecebimento, Produto

router = APIRouter(prefix="/recebimento", tags=["Recebimentos"])

@router.post("/")
def iniciar_recebimento(db: Session = Depends(get_db)):
    recebimento = Recebimento()
    db.add(recebimento)
    db.commit()
    db.refresh(recebimento)
    return {"id": recebimento.id, "data": recebimento.data, "itens": []}

@router.post("/{id}/item")
def adicionar_item(id: int, dun14: str, quantidade: int, db: Session = Depends(get_db)):
    recebimento = db.query(Recebimento).filter(Recebimento.id == id).first()
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento não encontrado")
    produto = db.query(Produto).filter(Produto.dun14 == dun14).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    item = ItemRecebimento(
        recebimento_id=id,
        dun14=dun14,
        nome_produto=produto.nome,
        quantidade=quantidade
    )
    db.add(item)
    db.commit()
    return {"mensagem": "Item adicionado", "produto": produto.nome, "quantidade": quantidade}

@router.get("/{id}/relatorio")
def relatorio(id: int, db: Session = Depends(get_db)):
    recebimento = db.query(Recebimento).filter(Recebimento.id == id).first()
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento não encontrado")
    return {
        "id": recebimento.id,
        "data": recebimento.data,
        "itens": [
            {"produto": i.nome_produto, "dun14": i.dun14, "quantidade": i.quantidade}
            for i in recebimento.itens
        ]
    }