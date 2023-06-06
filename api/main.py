from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

# from . import models
# from .database import engine

routes = [post, user, auth, vote]

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for model in routes:
    print("Adding ", model, " to the router.")
    app.include_router(model.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
