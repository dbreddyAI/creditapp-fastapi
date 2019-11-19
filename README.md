# Docker Creditability prediction API with FastAPI
Run FastAPI in docker container

# Run in Docker
```
docker pull ramottamado/creditapp-fastapi
docker run -d -p 80:80 ramottamado/creditapp-fastapi
```
Go to `localhost:80/predict` or `localhost:80/docs` to see documentation

# Run from folder (Not Docker)
```
pip install -r requirements.txt
cd app
uvicorn main:app
```
Go to `localhost:8000/predict` or `localhost:8000/docs` for documentation

# Usage

Send `POST` request to `localhost:80/predict` with data like this:
```
{
    "CustServ Calls":1,"Eve Mins":197.4,"Intl Mins":10.0,"VMail Message":25,
    "Intl Calls":3,"Night Mins":244.7,"Day Mins":265.1,
    "Int'l Plan":true
}
```
output should be like this:
```
{'creditability': 'Bad'}
```
