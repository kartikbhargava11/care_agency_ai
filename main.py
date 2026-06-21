# this file is the entry point
# initiates the app and registers the routes

# architecture -> event driven async pipeline
# goal is to decouple the waiting time from the computing time
# FastAPI uses an ASGI (async server gateway interface) server model powered by uvicorn
# never allows network pipes to sit idle
# handles 1000s of incoming concurrent requests on a single CPU thread by context switching between them

from fastapi import FastAPI # pull in core FastAPI framework class, contains built-in logic required to listen to network traffic, generate automatic documentation, and handle web communication protocols
from config.settings import settings # imports global variables from a single source of truth
from app.routers import router as care_router # imports a routing subsystem 

app = FastAPI( # instantiating the FastAPI object and naming it app
    # passing metadata to application's wrapper 
    # FastAPI builds a documentation page using this info.
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Scalable, enterprise structured AI logistics analytics platform built natively on FastAPI guidelines."
)

# take all the endpoints register them
app.include_router(care_router)


# a simple web route running a GET network packet request at /health
# tags parameters tells the auto generated documentation to group this endpoint under a section called "System Diagnostics"
# async is crucial for FastAPI best practices, it instructs server to handle this request asynchronously
# if 1000 users hit this health check endpoint at the same time, the server's thread loop will process them concurrently instead of blocking them
@app.get("/health", tags=["System Diagnostics"])
async def system_health():
    return {"status": "healthy", "model_configured": settings.AI_MODEL}
