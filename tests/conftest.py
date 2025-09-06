import allure
import pytest
import requests
from config.settings import URL, API
from utils.api_client import register_new_courier_and_return_login_password


@pytest.fixture
@allure.step('Регистрация курьера')
def registered_courier():
    with allure.step("Регистрация нового курьера и возврат логина, пароля и имени"):
        credentials = register_new_courier_and_return_login_password()
        return credentials

@pytest.fixture
@allure.step('Авторизация курьера')
def login_courier(registered_courier):
    with allure.step("Авторизация курьера и возврат его id"):
        login, password, firstname = registered_courier
        payload = {"login": login, "password": password}
        r = requests.post(f"{URL.MAIN_URL}{API.LOGIN_COURIER}", data=payload)
        courier_id = r.json()["id"]
        return login, password, firstname, courier_id,
