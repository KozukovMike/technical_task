import requests
import bcrypt
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
from db.CRUD.users import CRUDUser
from statements.bd_models import User, Role, UserRoleAssociation
from db.conn_to_bd import PostgresClient
from db.CRUD.currency import CRUDCurrency
from pars_pars.parsssssssss import ParsNBRB
from db.CRUD.roles import CRUDRole
from db.CRUD.user_role_association import CRUDUserRoleAssociation
# from parser.connection_to_nbrb import ParsNBRB


app = FastAPI()
scheduler = BackgroundScheduler()

# Создаем объект Jinja2Templates для работы с шаблонами
templates = Jinja2Templates(directory='templates')

list_of_instances = []
country_names = []


# def hash_pass(password: str) -> str:
#     salt = bcrypt.gensalt()
#     entered_password = password.encode('utf-8')
#     password_hash = bcrypt.hashpw(entered_password, salt)
#     return password_hash.decode('utf-8')


def create_admin() -> None:
    user = User(
        username="admin",
        password_hash=''
    )
    CRUDUser.add(instance=user)
    user_id = CRUDUser.get_by_username(instance='admin').user_id
    ura = UserRoleAssociation(
        user_id=user_id,
        role_id=1,
    )
    CRUDUserRoleAssociation.add(instance=ura)
    user = User(
        username="manager",
        password_hash=''
    )
    CRUDUser.add(instance=user)
    user_id = CRUDUser.get_by_username(instance='manager').user_id
    ura = UserRoleAssociation(
        user_id=user_id,
        role_id=2,
    )
    CRUDUserRoleAssociation.add(instance=ura)

def read_from_db():
    global list_of_instances, country_names
    # нужно раскоментить при первом запуске
    # CRUDCurrency.delete_all()
    # ParsNBRB.pars_with_offrate()
    list_of_instances = PostgresClient.from_bd(table_name='currencies')
    country_names = [i['Cur_Name'] for i in list_of_instances]
    print(country_names)

@app.on_event("startup")
def start_scheduler():
    read_from_db()
    create_admin()
    scheduler.add_job(read_from_db, 'interval', days=1)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

@app.get('/ping')
def ping():
    return 'pong'
#
@app.post("/table", response_class=HTMLResponse)
def show_table(request: Request):
    try:
        global list_of_instances, country_names
        print(country_names)
        new_list_of_instances = [i for i in list_of_instances if i['Cur_Name'] in country_names]
        return templates.TemplateResponse("table.html", {"request": request, "items": new_list_of_instances})
    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def get_login_form(request: Request):
    return templates.TemplateResponse("login_form.html", {"request": request})


@app.post("/")
async def process_login(username: str = Form(...), password: str = Form(None)):

    user = CRUDUser.get_by_username(instance=username)

    if user is None:
        salt = bcrypt.gensalt()
        entered_password = password.encode('utf-8')
        password_hash = bcrypt.hashpw(entered_password, salt)
        user = User(username=username, password_hash=password_hash.decode('utf-8'))
        CRUDUser.add(instance=user)
        user_id = CRUDUser.get_by_username(instance=username).user_id
        ura = UserRoleAssociation(
            user_id=user_id,
            role_id=3,
        )
        CRUDUserRoleAssociation.add(instance=ura)
        return RedirectResponse(url="/table")

    user_id = CRUDUser.get_by_username(instance=username).user_id
    role_id = CRUDUserRoleAssociation.get_by_user_id(instance_id=user_id).role_id

    if role_id == 1:
        return RedirectResponse(url="/admin_page")
    elif role_id == 2:
        return RedirectResponse(url="/manager")
    if password is None:
        return {"message": "Укажите пароль"}
    entered_password = password.encode('utf-8')
    if bcrypt.checkpw(entered_password, user.password_hash.encode('utf-8')):
        return RedirectResponse(url="/table")
    else:
        return {"message": "Неправильное имя пользователя или пароль"}

@app.post("/admin_page", response_class=HTMLResponse)
async def admin_page(request: Request,
                    username_admin: str = Form(None),
                    username_delete: str = Form(None)):
    with open("templates/admin.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return templates.TemplateResponse("admin.html", {"request": request, "username_admin": username_admin, "username_delete": username_delete})

@app.post("/assign_admin_role", response_class=HTMLResponse)
async def assign_admin_role(request: Request,
                            username_admin: str = Form(None)):
    user_id = CRUDUser.get_by_username(instance=username_admin).user_id
    CRUDUserRoleAssociation.add(instance=UserRoleAssociation(user_id=user_id, role_id=1))
    role_id = CRUDUserRoleAssociation.get_by_user_id(instance_id=user_id).role_id
    return templates.TemplateResponse("admin_result.html", {"request": request, "username": username_admin})

@app.post("/delete_user", response_class=HTMLResponse)
async def delete_user(request: Request,
                      username_delete: str = Form(None)):
    user_id = CRUDUser.get_by_username(instance=username_delete).user_id
    CRUDUserRoleAssociation.delete_by_user_id(instance_id=user_id)
    CRUDUser.delete_by_id(instance_id=user_id)
    return templates.TemplateResponse("admin_result.html", {"request": request, "username": username_delete})

@app.post("/manager", response_class=HTMLResponse)
async def manager(request: Request, selected_countries: list = Form([])):
    try:
        global list_of_instances
        print(selected_countries)
        return templates.TemplateResponse("manager.html", {"request": request, "items": list_of_instances, "selected_countries": selected_countries})
    except Exception as e:
        return {"error": str(e)}

@app.post("/assign_manager_role", response_class=HTMLResponse)
async def assign_manager_role(request: Request, username_manager: str = Form(None)):
    user_id = CRUDUser.get_by_username(instance=username_manager).user_id
    CRUDUserRoleAssociation.add(instance=UserRoleAssociation(user_id=user_id, role_id=2))
    role_id = CRUDUserRoleAssociation.get_by_user_id(instance_id=user_id).role_id
    return templates.TemplateResponse("admin_result.html", {"request": request, "username": username_manager})

@app.post("/manager/show_selected")
async def show_selected(request: Request, selected_countries: list = Form([])):
    global country_names
    country_names = selected_countries
    return templates.TemplateResponse("manager_result.html", {"request": request})
