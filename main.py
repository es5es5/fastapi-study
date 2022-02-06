from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

db = [{
    'name': '서울',
    'timezone': 'Asia/Seoul'
}]

class City(BaseModel):
    name: str
    timezone: str

@app.get("/")
def root():
    return { "Hello": "Fast API !" }

@app.get('/cities')
def getCities():
    result = []

    print(db)
    for city in db:
        print(city)
        print(city['name'])
        url = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
        print(url)
        r = requests.get(url)

        currentTime = r.json()['datetime']
        result.append({
            'name': city['name'],
            'timezone': city['timezone'],
            'currentTime': currentTime
        })

    return result

@app.post('/cities')
def createCities(city: City):
    db.append(city.dict())

    print(db)

    return city
