from io import BytesIO
from fastapi import Depends, UploadFile, APIRouter, Request
import config
import pandas as pd
from api.fuel_predictor.fuel_predictor_dtos import TripData
from api.middlewares.check_api_key import check_api_key
from fastapi.responses import PlainTextResponse, JSONResponse

router = APIRouter()

"""
Returns a prediction on a single trip data point
"""
@router.post("/predict", dependencies=[Depends(check_api_key)])
async def get_prediction(request: Request, dataPoint: TripData):
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

    X = config.preprocessor.transform(X)
    y = config.model.predict(X)

    return JSONResponse(content={"prediction": y[0]})

"""
Returns predictions for multiple trip datapoints as a paintext csv
"""
@router.post("/predict/from_file", dependencies=[Depends(check_api_key)])
async def get_file_predictions(data: UploadFile):
    X = pd.read_csv(BytesIO(await data.read()))

    X = config.preprocessor.transform(X)
    y = config.model.predict(X)

    csv = pd.DataFrame(y).to_csv(header=["FOC"], index=False)
    return PlainTextResponse(csv)
