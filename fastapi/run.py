from typing import Optional
from fastapi import FastAPI
from view import assisant

app = FastAPI()

app.include_router(assisant.assisantRouter)