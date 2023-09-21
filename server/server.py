import requests
import bcrypt
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
from db.CRUD.users import CRUDUser
from statements.bd_models import User
from db.conn_to_bd import PostgresClient
from db.CRUD.currency import CRUDCurrency
from pars_pars.parsssssssss import ParsNBRB
# from parser.connection_to_nbrb import ParsNBRB


app = FastAPI()
scheduler = BackgroundScheduler()

# Создаем объект Jinja2Templates для работы с шаблонами
templates = Jinja2Templates(directory='templates')

list_of_instances = []
def read_from_db():
    global list_of_instances
    CRUDCurrency.delete_all()
    ParsNBRB.pars_with_offrate()
    list_of_instances = PostgresClient.from_bd(table_name='currencies')


@app.on_event("startup")
def start_scheduler():
    read_from_db()
    scheduler.add_job(read_from_db, 'interval', days=1)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

@app.get('/ping')
def ping():
    return 'pong'
#
@app.post("/table")
def show_table(request: Request):
    try:
        global list_of_instances
        return templates.TemplateResponse("table.html", {"request": request, "items": list_of_instances})
    except Exception as e:
        return {"error": str(e)}

@app.get('/table')
def show_table(request: Request):
    return {'message': 'dd'}


@app.get("/")
async def get_login_form(request: Request):
    return templates.TemplateResponse("login_form.html", {"request": request})


@app.post("/")
async def process_login(username: str = Form(...), password: str = Form(...)):
    user = CRUDUser.get_by_username(instance=username)

    if user is None:
        salt = bcrypt.gensalt()
        entered_password = password.encode('utf-8')
        password_hash = bcrypt.hashpw(entered_password, salt)
        user = User(username=username, password_hash=password_hash.decode('utf-8'))  # Decode the hash
        CRUDUser.add(instance=user)
        return RedirectResponse(url="/table")

    entered_password = password.encode('utf-8')
    if bcrypt.checkpw(entered_password, user.password_hash.encode('utf-8')):
        return RedirectResponse(url="/table")
    else:
        return {"message": "Неправильное имя пользователя или пароль"}
