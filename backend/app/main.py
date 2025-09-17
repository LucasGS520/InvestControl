""" Aplicação FastAPI básica para o InvestControl

Esta estrutura serve como ponto de partida para inicialização do projeto durante a fase de preparação.
"""

from fastapi import FastAPI

app = FastAPI(
    title="InvestControl API",
    version="0.1.0",
    description="API base do InvestControl para validação de infraestrutura na fase de preparação.",
)

@app.get("/health", tags=["Monitoramento"])
async def health_check():
    """ Rota de verificação de saúde para monitoramento básico da aplicação. """
    return {"status": "ok"}
