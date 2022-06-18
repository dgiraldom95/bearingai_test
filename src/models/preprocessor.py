from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd


class DateTransformer(BaseEstimator, TransformerMixin):
    def transform(self, X, y=None):
        X["date_parsed"] = pd.to_datetime(X["Date"])

        X["year"] = X["date_parsed"].map(lambda date: date.year)
        X["month"] = X["date_parsed"].map(lambda date: date.month)
        X["day"] = X["date_parsed"].map(lambda date: date.day)
        X["hour"] = X["date_parsed"].map(lambda date: date.hour)

        X = X.drop(["Date", "date_parsed"], axis=1)
        return X

    def fit(self, X, y=None):
        return self


column_transformer = ColumnTransformer(
    remainder="passthrough",
    transformers=[
        (
            "minmax",
            MinMaxScaler(),
            ["Speed(Ground)", "M/E REVOLUTION", "Latitude_degree", "Longitude_degree"],
        ),
        ("ordinal", OrdinalEncoder(), ["Beaufort"]),
    ],
)


preprocessor = Pipeline(
    [
        ("date_transformer", DateTransformer()),
        ("column_transformer", column_transformer),
    ]
)
