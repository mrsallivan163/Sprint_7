import pytest
import requests
from config import URL, API
from helpers import register_new_courier_and_return_login_password

@pytest.fixture
def registered_courier():
    """Регистрация нового курьера и возврат логина, пароля и имени"""
    credentials = register_new_courier_and_return_login_password()
    assert len(credentials) == 3, "Не удалось зарегистрировать курьера"
    return credentials

@pytest.fixture
def login_courier(registered_courier):
    """Авторизация пользователя и возврат его id"""
    login, password, _ = registered_courier
    payload = {"login": login, "password": password}
    r = requests.post(f"{URL.MAIN_URL}{API.LOGIN_COURIER}", data=payload)
    assert r.status_code == 200, "Не удалось залогиниться"
    return r.json()["id"]