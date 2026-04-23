from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Historico, Recebimento
from datetime import datetime

router = APIRouter(prefix="/historico", tags=["Histórico"])

@router.post("/")
def salvar_historico(recebimento_id: int, nome: str, db: Session = Depends(get_db)):
    recebimento = db.query(Recebimento).filter(Recebimento.id == recebimento_id).first()
    if not recebimento:
        raise HTTPException(status_code=404, detail="Recebimento não encontrado")

    existente = db.query(Historico).filter(Historico.recebimento_id == recebimento_id).first()
    if existente:
        existente.nome = nome
        db.commit()
        return existente

    historico = Historico(recebimento_id=recebimento_id, nome=nome)
    db.add(historico)
    db.commit()
    db.refresh(historico)
    return historico

@router.get("/")
def listar_historico(data_inicio: str = None, data_fim: str = None, db: Session = Depends(get_db)):
    query = db.query(Historico).order_by(Historico.data.desc())

    if data_inicio:
        query = query.filter(Historico.data >= datetime.fromisoformat(data_inicio))
    if data_fim:
        query = query.filter(Historico.data <= datetime.fromisoformat(data_fim))

    historicos = query.all()
    return [
        {
            "id": h.id,
            "nome": h.nome,
            "data": h.data,
            "recebimento_id": h.recebimento_id,
            "total_produtos": len(h.recebimento.itens),
            "total_caixas": sum(i.quantidade for i in h.recebimento.itens),
        }
        for h in historicos
    ]

@router.get("/{id}")
def detalhe_historico(id: int, db: Session = Depends(get_db)):
    h = db.query(Historico).filter(Historico.id == id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")
    return {
        "id": h.id,
        "nome": h.nome,
        "data": h.data,
        "recebimento_id": h.recebimento_id,
        "itens": [
            {
                "nome": i.nome_produto,
                "dun14": i.dun14,
                "quantidade": i.quantidade,
            }
            for i in h.recebimento.itens
        ],
    }