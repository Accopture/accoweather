from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import json, psycopg, asyncio, os, httpx, pathlib
import uvicorn, pydantic
import functions


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.cities = await functions.fetch_all_cities()
    app.countries = await functions.fetch_all_countries()
    app.api_key = functions.api_key_function()
    yield


class WeatherRequest(pydantic.BaseModel):
    city: str

class WeatherServer(FastAPI, functions.DatabaseClass):
    def __init__(self):
        super().__init__(lifespan=lifespan)
        self.add_api_route(path="/api/weather/cities", endpoint=self.get_locations, methods=["GET"])
        self.add_api_route(path="/api/weather/countries", endpoint=self.get_countries, methods=["GET"])
        self.add_api_route(path="/api/weather/", endpoint=self.get_weather, methods=["POST"])
        self.add_api_route(path="/weather", endpoint=self.serve_static_files, methods=["GET"])
        self.mount("/static", StaticFiles(directory="static"), name="static")
        self.openweathermap_url = "https://api.openweathermap.org/data/2.5/weather"
        self.countries = None
        self.cities = None
        self.api_key = None
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    @staticmethod
    @functions.DatabaseClass.initiate_connection
    async def _geocode(cur, city: WeatherRequest):
        await cur.execute("SELECT latitude, longitude FROM weatherapi.cities WHERE city_name = %s", [city])
        cur_results = await cur.fetchall()
        return {"lat": cur_results[0][0], "lon": cur_results[0][1]}
        
    async def serve_static_files(self):
        return FileResponse("static/main.html")
        
    async def get_locations(self):
        return self.cities
    
    async def get_countries(self):
        return self.countries
        
    async def get_weather(self, request: WeatherRequest):
        coordinates = await self._geocode(city=request.city)
        params = {"lat": coordinates.get("lat"), "lon": coordinates.get("lon"), "appid": self.api_key, "units": "metric"}
        print(coordinates)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.openweathermap_url, params=params)
            print(response)
            results = response.json()
            
        main_output = functions.filter_weather_response(results)
        return main_output
        

    
app = WeatherServer()
if __name__ == "__main__":
    uvicorn.run(app, host="10.0.0.100", port=8000)
