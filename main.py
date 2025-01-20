from fastapi import FastAPI
from sightseeing_llm_queries import *
from extract_data_from_chat import *
from tbo_sightseeing_queries import *
app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name : str):
    return {"message" : f"Hello {name}"}

@app.post("/startChat")
async def start_chat(userName : str):
    history,chat, system_instructions = start_chat()
    return {"chat_id" : id(chat), "history" : history}

@app.get("/listAttractions")
async def list_attractions():
    response =



