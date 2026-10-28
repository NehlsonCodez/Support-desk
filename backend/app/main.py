from fastapi import FastAPI, Depends, HTTPException
from routers import auth_router, ticket_router, ticket_activity_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(ticket_router)
app.include_router(ticket_activity_router)

@app.get("/")
async def index():
    return {"page": "index"}