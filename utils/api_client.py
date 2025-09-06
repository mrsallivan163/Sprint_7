import requests
import allure
from config.settings import URL,API
from utils.helpers import generate_random_string

@allure.step('Регистрация курьера и возврат логина, пароля, имени курьера')
def register_new_courier_and_return_login_password():
    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass

@allure.step('Логин курьера и возврат его id')
def login_courier_and_return_id(payload):
    r=requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
    return r.json()["id"]

@allure.step('Отмена заказа')
def cancel_order(track):
    requests.put(f"{URL.MAIN_URL}{API.CANCEL_ORDER}{track}")

@allure.step('Удаление курьера')
def delete_courier(courier_id):
    requests.delete(f"{URL.MAIN_URL}{API.DELETE_COURIER}{courier_id}")