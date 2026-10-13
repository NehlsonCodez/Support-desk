from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

@app.get("/")
async def index():
    return {"page": "index"}