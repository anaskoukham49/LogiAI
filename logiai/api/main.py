
"""LogiAI FastAPI application."""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from logiai import config
from logiai.api.schemas import Livraison, PredictionOut
from logiai.api.security import require_admin, verify_api_key
from logiai.config import MODEL_PATH
from logiai.predict import Predictor


# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("logiai")

state: dict = {}


# --------------------------------------------------
# Application lifecycle
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting LogiAI API")

    if MODEL_PATH.exists():
        state["predictor"] = Predictor(MODEL_PATH)
        logger.info("ML model loaded successfully")
    else:
        logger.error("ML model not found: %s", MODEL_PATH)

    yield

    state.clear()
    logger.info("LogiAI API shutting down")


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="LogiAI",
    version="1.0.0",
    description="Predicts delivery delay risk using machine learning.",
    lifespan=lifespan,
)


# --------------------------------------------------
# HTTP request logging middleware
# --------------------------------------------------

@app.middleware("http")
async def request_logging(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "%s %s | status=%s | duration=%.2fms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response

    except Exception:
        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.exception(
            "%s %s | status=500 | duration=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise


# --------------------------------------------------
# CORS configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


# --------------------------------------------------
# API endpoints
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": "predictor" in state,
        "auth_configured": bool(config.API_KEY),
    }


@app.get("/v1/model-info", dependencies=[Depends(require_admin)])
def model_info():
    """Administrative model information."""
    return {
        "model_path": str(MODEL_PATH),
        "loaded": "predictor" in state,
    }


@app.post(
    "/v1/predict",
    response_model=PredictionOut,
    dependencies=[Depends(verify_api_key)],
)
def predict(livraison: Livraison):
    predictor = state.get("predictor")

    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded",
        )

    return PredictionOut(**predictor.predict(livraison.model_dump()))
