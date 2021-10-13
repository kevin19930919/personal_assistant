from fastapi import APIRouter, HTTPException,Request
from fastapi.responses import RedirectResponse
import sys
sys.path.append('/data2/kevin7552/personal_assistant/fastapi/core')
from neuralintents.assisant import Assisant
from AIDMS_module import AIDMSHandler
from week_report import WeekReport

#=========responese function==================
def send_mail():
    Filepath = input("what file you want to attach?(abs path plz)")
    WeekReport.send_mail(Filepath)

def stop_apache_server():
    pop = subprocess.Popen('sudo service apache2 stop',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = pop.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if stderr:
        print(f'stop apache2 fail: {stderr}')
        return False
    else:
        print('stop apache server success')
        return True    

def mount_AIDMS_db():
    AIDMSHandler.mount_AIDMS_db_impl()


assisantRouter = APIRouter()

function_maps = {
    'send_mail':send_mail,
    'mount_AIDMS_db':mount_AIDMS_db
}
# @assisantRouter.get("/assisant")
# async def command_assisant(message : str):
#     return json

@assisantRouter.get('/assisant')
def update_assisant(sentence:str):
    assisant = Assisant(function_maps)
    assisant.load_model()
    assisant.load_intents_file()
    assisant.get_response(sentence=sentence)