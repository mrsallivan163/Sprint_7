import requests
import allure

from utils.api_client import delete_courier
from config.test_api_data import RESPONSE_TEXT
from config.settings import URL, API

@allure.suite('Яндекс Самокат. Логин курьера POST /api/v1/courier/login')
class TestLoginCourier:

    @allure.title('Проверка, что курьер может залогиниться под созданной записью')
    def test_login_courier_success_when_fill_all_fields(self, login_courier):
        login, password, _, courier_id= login_courier
        payload = {"login": login, "password": password}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
        assert r.status_code == 200
        assert "id" in r.json()
        assert isinstance(r.json()["id"], int)
        try:
            delete_courier(courier_id)
        except:
            pass

    @allure.title('Проверка, что нельзя авторизоваться несуществующим login')
    def test_login_wrong_login(self, login_courier):
        login, password, _, courier_id= login_courier
        payload_wrong = {"login": "wrong", "password": password}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload_wrong)
        assert r.status_code == 404
        assert r.json()['message'] == RESPONSE_TEXT.COURIER_NOT_FOUND
        try:
            delete_courier(courier_id)
        except:
            pass

    @allure.title('Проверка, что нельзя авторизоваться c неправильным паролем')
    def test_login_wrong_password(self, login_courier):
        login, password, _, courier_id= login_courier
        payload_wrong = {"login": login, "password": "wrong"}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload_wrong)
        assert r.status_code == 404
        assert r.json()['message'] == RESPONSE_TEXT.COURIER_NOT_FOUND
        try:
            delete_courier(courier_id)
        except:
            pass

    @allure.title('Проверка, что нельзя авторизоваться курьером без указания обязательного поля login')
    def test_failed_login_courier_missing_login_is_failed(self):
        payload = {"password":"1234"}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
        assert r.status_code == 400
        assert r.json()['message'] == RESPONSE_TEXT.NOT_ENOUGH_DATA_TO_LOGIN

    @allure.title('Проверка, что нельзя авторизоваться курьером без указания обязательного поля password')
    def test_login_courier_missing_password_is_failed(self):
        payload = {"login": "Vova123"}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
        assert r.status_code == 400
        assert r.json()['message'] == RESPONSE_TEXT.NOT_ENOUGH_DATA_TO_LOGIN
