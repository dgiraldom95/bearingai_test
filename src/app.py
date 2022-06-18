from io import BytesIO
import json
from fastapi import Depends, FastAPI, UploadFile
from joblib import load
import pandas as pd
import sys
import os
from sklearn.pipeline import Pipeline
import uvicorn
import numpy as np
from api.fuel_predictor.fuel_predictor_dtos import TripData
from api.middlewares.check_api_key import check_api_key
from fastapi.responses import PlainTextResponse, JSONResponse


app = FastAPI(
    title="Iris ML API", description="API for iris dataset ml model", version="1.0"
)


@app.on_event("startup")
async def load_model():
    # Add preprocessor module to path as it has to be defined in file for `load` to work
    sys.path.append(os.path.join(os.path.dirname(__file__), "models"))

    global model
    global preprocessor

    model = load("src/models/predictor.joblib")
    preprocessor = load("src/models/preprocessor.joblib")


@app.post("/predict", dependencies=[Depends(check_api_key)])
async def get_prediction(dataPoint: TripData):
    dataPointDict = {
        "Date": dataPoint.Date,
        "Latitude_degree": dataPoint.Latitude_degree,
        "Longitude_degree": dataPoint.Longitude_degree,
        "Beaufort": dataPoint.Beaufort,
        "Speed(Ground)": dataPoint.Speed,
        "M/E REVOLUTION": dataPoint.Revolution,
    }

    X = pd.DataFrame.from_dict([dataPointDict])
    print(X.head())

    X = preprocessor.transform(X)
    y = model.predict(X)

    return JSONResponse(content={"prediction": y[0]})


@app.post("/predict/from_file", dependencies=[Depends(check_api_key)])
async def get_file_predictions(data: UploadFile):
    X = pd.read_csv(BytesIO(await data.read()))

    X = preprocessor.transform(X)
    y = model.predict(X)

    csv = pd.DataFrame(y).to_csv(header=["FOC"], index=False)
    return PlainTextResponse(csv)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="info")
