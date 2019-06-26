from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import autocomplete, search
from utils.tools import generate_prefix


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入autocomplete
app.include_router(
    autocomplete.router,
    prefix=generate_prefix("autocompelte"),
    tags=["autocomplete"]
)

# 导入search
app.include_router(
    search.router,
    prefix=generate_prefix("search"),
    tags=["search"]
)
