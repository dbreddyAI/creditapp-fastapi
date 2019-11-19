import pickle
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
import pandas as pd
from encoder import MyEncoder


app = FastAPI()


# Custom Unpickler because our program doesn't run as __main__
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "encoder"
        return super().find_class(module, name)


# Load all pickled items
lr_model = pickle.load(open('data/model.pkl', 'rb'))
enc = CustomUnpickler(open('data/encoder.pkl', 'rb')).load()
features = pickle.load(open('data/features.pkl', 'rb'))


# FastAPI use BaseModel to validate data
class Data(BaseModel):
    custserv_calls: int
    eve_mins: float
    intl_mins: float
    vmail_message: int
    intl_calls: int
    night_mins: float
    day_mins: float
    intl_plan: bool


class ResponseModel(BaseModel):
    creditability: str


# Main app goes here
@app.post('/predict', response_model=ResponseModel)
async def predict(data: Data):
    # Dictionary to convert BaseModel to pandas column names
    feature_dict = {
        'custserv_calls': 'CustServ Calls',
        'eve_mins': 'Eve Mins',
        'intl_mins': 'Intl Mins',
        'vmail_message': 'VMail Message',
        'intl_calls': 'Intl Calls',
        'night_mins': 'Night Mins',
        'day_mins': 'Day Mins',
        'intl_plan': 'Int\'l Plan'
    }
    # Load data, feature selection, feature engineer data
    data_dict = data.dict()
    to_predict = {feature_dict[i]: data_dict[i] for i in feature_dict}
    to_predict = pd.DataFrame(to_predict, index=[0])
    to_predict = to_predict[features]
    X = enc.transform(to_predict)
    prediction = lr_model.predict(X)
    # Return prediction
    return {
        'creditability': list(map(
            lambda x: 'Good' if int(x) == 1 else 'Bad', [prediction[0]]
        ))[0]
    }


@app.get('/predict_get', response_model=ResponseModel)
async def predict_get(
    custserv_calls: int = 0,
    eve_mins: float = 0,
    intl_mins: float = 0,
    vmail_message: int = 0,
    intl_calls: int = 0,
    night_mins: float = 0,
    day_mins: float = 0,
    intl_plan: bool = True
):
    # Dictionary to convert BaseModel to pandas column names
    feature_dict = {
        'custserv_calls': 'CustServ Calls',
        'eve_mins': 'Eve Mins',
        'intl_mins': 'Intl Mins',
        'vmail_message': 'VMail Message',
        'intl_calls': 'Intl Calls',
        'night_mins': 'Night Mins',
        'day_mins': 'Day Mins',
        'intl_plan': 'Int\'l Plan'
    }
    # Load data, feature selection, feature engineer data
    data_dict = {
        'custserv_calls': custserv_calls,
        'eve_mins': eve_mins,
        'intl_mins': intl_mins,
        'vmail_message': vmail_message,
        'intl_calls': intl_calls,
        'night_mins': night_mins,
        'day_mins': day_mins,
        'intl_plan': intl_plan
    }
    to_predict = {feature_dict[i]: data_dict[i] for i in feature_dict}
    to_predict = pd.DataFrame(to_predict, index=[0])
    to_predict = to_predict[features]
    X = enc.transform(to_predict)
    prediction = lr_model.predict(X)
    # Return prediction
    return {
        'creditability': list(map(
            lambda x: 'Good' if int(x) == 1 else 'Bad', [prediction[0]]
        ))[0]
    }
