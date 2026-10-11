from fastapi import FastAPI

from app.api.sensores import router as sensores_router
from app.api.mediciones import router as mediciones_router


app = FastAPI(
    title="API de adquisición y consulta de datos IoT",
    description=(
        "API para consultar sensores, magnitudes y mediciones "
        "del sistema IoT."
    ),
    version="1.0.0",
)

app.include_router(sensores_router)
app.include_router(mediciones_router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": "API IoT funcionando correctamente",
        "documentacion": "/docs",
    }
