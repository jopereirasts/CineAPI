from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Cinema Independente!"}