from fastapi import FastAPI
from routers import projects, skills, techs, login
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://portfoliomateoozino.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(techs.router)
app.include_router(skills.router)
app.include_router(login.router)