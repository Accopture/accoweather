import os
import asyncio
import psycopg
import json
from pathlib import Path
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

class DatabaseClass:
    @staticmethod
    def get_creds():
        database_creds ={
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "dbname": os.getenv("DB_DATABASE")
    }
        return database_creds
    
    @classmethod
    def initiate_connection(cls, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            credentials = cls.get_creds()
            async with await psycopg.AsyncConnection.connect(**credentials) as conn:
                async with conn.cursor() as cur:
                    return await func(cur, *args, **kwargs)
        return wrapper
        
@DatabaseClass.initiate_connection
async def fetch_all_cities(cur):
    await cur.execute("SELECT city_name FROM weatherapi.cities ORDER BY country ASC")
    results = await cur.fetchall()
    return results

@DatabaseClass.initiate_connection
async def fetch_all_countries(cur):
    await cur.execute("SELECT full_name FROM weatherapi.countries ORDER BY full_name ASC")
    results = await cur.fetchall()
    return results

def api_key_function():
    return os.getenv("API_KEY")

def filter_weather_response(results):
    return_var =  {'weather': results['weather'][0]['description'].capitalize(),
        'main': results['weather'][0]['main'].lower(),
        'temp': results['main']['temp'],
        'feels_like': results['main']['feels_like'],
        'humidity': results['main']['humidity'],
        'wind_speed': results['wind']['speed']}
    return return_var