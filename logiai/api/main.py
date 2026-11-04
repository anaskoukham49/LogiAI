"""L'API LogiAI : python -m uvicorn logiai.api.main:app --reload"""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from logiai import config
from logiai.api.schemas import Livraison, PredictionOut
from logiai.api.security import require_admin, verify_api_key
from logiai.config import MODEL_PATH
from logiai.predict import Predictor

state: dict = {}  # contient le "predictor" une fois le modèle chargé


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Exécuté UNE fois, au démarrage du serveur (pas à chaque requête)
    if MODEL_PATH.exists():
        state["predictor"] = Predictor(MODEL_PATH)
    yield
    state.clear()


app = FastAPI(
    title="LogiAI",
    version="1.0.0",
    description="Prédit le risque de retard d'une livraison à partir de ses caractéristiques.",
    lifespan=lifespan,
)

# Configuration CORS pour autoriser le client web
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": "predictor" in state,
        "auth_configured": bool(config.API_KEY),
    }


@app.get("/v1/model-info", dependencies=[Depends(require_admin)])
def model_info():
    """Route réservée aux administrateurs."""
    return {"model_path": str(MODEL_PATH), "loaded": "predictor" in state}


@app.post(
    "/v1/predict",
    response_model=PredictionOut,
    dependencies=[Depends(verify_api_key)],
)
def predict(livraison: Livraison):
    predictor = state.get("predictor")
    if predictor is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return PredictionOut(**predictor.predict(livraison.model_dump()))