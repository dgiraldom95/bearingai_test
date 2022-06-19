import sys
import os
import uvicorn
import config
from fastapi import FastAPI
from joblib import load
from api.fuel_predictor import fuel_predictor_controller

app = FastAPI(title="Fuel Predictor API", version="1.0")
app.include_router(fuel_predictor_controller.router)

"""
Load saved sklearn pipelines
"""
@app.on_event("startup")
async def load_model():
    # Add preprocessor module to path as it has to be defined in file for `load` to work
    sys.path.append(os.path.join(os.path.dirname(__file__), "models"))

    config.model = load("src/models/predictor.joblib")
    config.preprocessor = load("src/models/preprocessor.joblib")

"""
Healthcheck for docker
"""
@app.get("/health")
async def healthcheck():
    return


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info")
