from dataclasses import asdict
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import uuid

app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: str

@app.get("/")
def root():
    return { "Hello": "Fast API !" }

@app.get('/cities')
def get_cities():
    result = []

    print(db)
    for city in db:
        print(city)
        print(city['name'])
        url = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
        print(url)
        response = requests.get(url)

        if (response.status_code == 200):
            currentTime = response.json()['datetime']
            result.append({
                'name': city['name'],
                'timezone': city['timezone'],
                'currentTime': currentTime
            })

    return result

@app.post('/cities')
def create_cities(city: City):
    db.append(city.dict())

    print(db)

    return city

@app.delete('/cities/{index}')
def delete_cities(index: int):
    return db.pop(index)