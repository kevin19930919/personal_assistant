from fastapi import APIRouter, HTTPException,Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import json
import sys
sys.path.append('/data2/kevin7552/personal_assistant/fastapi/core')
from neuralintents.assisant import Assisant




assisantRouter = APIRouter()

templates = Jinja2Templates(directory="templates")

#======initial model====================================================
assisant = Assisant()
assisant.load_model()
assisant.load_intents_file()
#===============================api======================================
@assisantRouter.get('/assisant')
def render_assisant(request: Request):
    return templates.TemplateResponse("chat_room.html", {"request": request})

@assisantRouter.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        responseMessage = assisant.request(sentence=message)
        response = jsonable_encoder(
            {
                'content':f"Message text was: {responseMessage}"
            }
        )
        await websocket.send_json(response)


