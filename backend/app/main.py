from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    auth_router,
    ticket_router,
    ticket_activity_router,
    ticket_reply_router,
    user_router,
)

app = FastAPI(
    title="Support Desk API",
    description="A role-based Support Desk and Ticketing API",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ticket_router)
app.include_router(ticket_reply_router)
app.include_router(ticket_activity_router)


@app.get("/", tags=["Health"])
async def index():
    return {"status": "healthy", "service": "Support Desk API", "version": "1.0.0"}