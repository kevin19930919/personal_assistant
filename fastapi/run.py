from typing import Optional
from fastapi import FastAPI
from view import assisant
import uvicorn
app = FastAPI()

app.include_router(assisant.assisantRouter)

if __name__ == '__main__':
    
    uvicorn.run(app, host="0.0.0.0", port=8000)