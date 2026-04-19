from fastapi import FastAPI
from routes import produtos, recebimentos

app = FastAPI(title="API de Recebimento de Estoque")

app.include_router(produtos.router)
app.include_router(recebimentos.router)

@app.get("/")
def root():
    return {"status": "API funcionando"}