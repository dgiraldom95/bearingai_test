from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import pandas as pd
from math import sin, cos, pi


class DateTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X["date_parsed"] = pd.to_datetime(X["Date"])

        X["year"] = X["date_parsed"].map(lambda date: date.year)
        X["month"] = X["date_parsed"].map(lambda date: date.month)
        X["day"] = X["date_parsed"].map(lambda date: date.day)
        X["hour"] = X["date_parsed"].map(lambda date: date.hour)

        X = X.drop(["Date", "date_parsed"], axis=1)
        return X


"""
Transforms lat and long feature into x,y,z cartesian features (Because -180 == 180 in original coordinates)
"""
class CartesianTransfomer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        to_radians = lambda x: (x * pi) / 180
        calc_x = lambda lat, long: cos(to_radians(lat)) * cos(to_radians(long))
        calc_y = lambda lat, long: cos(to_radians(lat)) * sin(to_radians(long))
        calc_z = lambda lat: sin(to_radians(lat))

        X["x"] = list(map(calc_x, X["Latitude_degree"], X["Longitude_degree"]))
        X["y"] = list(map(calc_y, X["Latitude_degree"], X["Longitude_degree"]))
        X["z"] = list(map(calc_z, X["Latitude_degree"]))

        X = X.drop(["Latitude_degree", "Longitude_degree"], axis=1)

        return X


column_transformer = ColumnTransformer(
    remainder="passthrough",
    transformers=[
        ("minmax", MinMaxScaler(), ["year", "month", "day", "hour"]),
        (
            "standard",
            StandardScaler(),
            ["Speed(Ground)", "M/E REVOLUTION", "x", "y", "z"],
        ),
        (
            "ordinal",
            OrdinalEncoder(categories=[["low", "medium", "high"]]),
            ["Beaufort"],
        ),
    ],
)


preprocessor = Pipeline(
    [
        ("cartesian_transformer", CartesianTransfomer()),
        ("date_transformer", DateTransformer()),
        ("column_transformer", column_transformer),
    ]
)
