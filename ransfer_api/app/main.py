from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.endpoints import transfers

app = FastAPI(title="RX Transfer Service", version="1.0.0")

# Include routers
app.include_router(transfers.router, prefix="/api/v1/transfers", tags=["transfers"])

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "healthy"}) 