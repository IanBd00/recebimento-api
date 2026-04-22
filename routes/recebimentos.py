from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db
from models import Recebimento, ItemRecebimento, Produto
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/recebimento", tags=["Recebimentos"])

@router.post("/")
def iniciar_recebimento(db: Session = Depends(get_db)):
    recebimento = Recebimento()
    db.add(recebimento)
    db.commit()
    db.refresh(recebimento)
    return {"id": recebimento.id, "data": recebimento.data, "itens": []}

@router.post("/{id}/item")
def adicionar_item(id: int, dun14: str, db: Session = Depends(get_db)):
    recebimento = db.query(Recebimento).filter(Recebimento.id == id).first()
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento não encontrado")
    produto = db.query(Produto).filter(Produto.dun14 == dun14).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    item_existente = db.query(ItemRecebimento).filter(
        ItemRecebimento.recebimento_id == id,
        ItemRecebimento.dun14 == dun14
    ).first()

    if item_existente:
        item_existente.quantidade += 1
        db.commit()
        return {"mensagem": "Quantidade atualizada", "produto": produto.nome, "quantidade": item_existente.quantidade}
    else:
        item = ItemRecebimento(
            recebimento_id=id,
            dun14=dun14,
            nome_produto=produto.nome,
            quantidade=1
        )
        db.add(item)
        db.commit()
        return {"mensagem": "Item adicionado", "produto": produto.nome, "quantidade": 1}

@router.patch("/{id}/finalizar")
def finalizar_recebimento(id: int, nome: str, db: Session = Depends(get_db)):
    recebimento = db.query(Recebimento).filter(Recebimento.id == id).first()
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento não encontrado")
    recebimento.nome = nome
    db.commit()
    return {"mensagem": "Recebimento finalizado", "id": id, "nome": nome}

@router.get("/historico")
def listar_historico(
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Recebimento).filter(Recebimento.nome != None)

    if data_inicio:
        query = query.filter(Recebimento.data >= datetime.fromisoformat(data_inicio))
    if data_fim:
        query = query.filter(Recebimento.data <= datetime.fromisoformat(data_fim + "T23:59:59"))

    recebimentos = query.order_by(Recebimento.data.desc()).all()

    return [
        {
            "id": r.id,
            "nome": r.nome,
            "data": r.data,
            "total_itens": len(r.itens),
            "total_caixas": sum(i.quantidade for i in r.itens)
        }
        for r in recebimentos
    ]

@router.get("/{id}/relatorio")
def relatorio(id: int, db: Session = Depends(get_db)):
    recebimento = db.query(Recebimento).filter(Recebimento.id == id).first()
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento não encontrado")
    return {
        "id": recebimento.id,
        "nome": recebimento.nome,
        "data": recebimento.data,
        "itens": [
            {"produto": i.nome_produto, "dun14": i.dun14, "quantidade": i.quantidade}
            for i in recebimento.itens
        ]
    }