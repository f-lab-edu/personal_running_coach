from fastapi import FastAPI
from contextlib import asynccontextmanager
from interfaces.api import routers
from config import settings

@asynccontextmanager
async def lifespan(app:FastAPI):
    
    yield


app = FastAPI(lifespan=lifespan)
for r in routers:
    app.include_router(r)
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.web.host, port=settings.web.port, reload=True)