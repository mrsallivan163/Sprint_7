import requests
import allure
from config import URL, API

@allure.suite('Яндекс Самокат. Логин курьера POST /api/v1/courier/login')
class TestLoginCourier:

    @allure.title('Проверка, что курьер может залогиниться под созданной записью')
    def test_login_courier_success_when_fill_all_fields(self, registered_courier):
        login, password, _ = registered_courier
        payload = {"login": login, "password": password}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
        assert r.status_code == 200
        assert "id" in r.json()
        assert isinstance(r.json()["id"], int)

    @allure.title('Проверка, что нельзя авторизоваться несуществующим login')
    def test_login_wrong_login(self, registered_courier):
        _, password, _ = registered_courier
        payload = {"login": "wrong", "password": password}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
        assert r.status_code == 404
        assert r.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка, что нельзя авторизоваться c неправильным паролем')
    def test_login_wrong_password(self, registered_courier):
        login, _, _ = registered_courier
        payload = {"login": login, "password": "wrong"}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
        assert r.status_code == 404
        assert r.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка, что нельзя авторизоваться курьером без указания обязательного поля login')
    def test_failed_login_courier_missing_login_is_failed(self):
        payload = {"password":"1234"}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
        assert r.status_code == 400
        assert r.json()['message'] == 'Недостаточно данных для входа'

    @allure.title('Проверка, что нельзя авторизоваться курьером без указания обязательного поля password')
    def test_login_courier_missing_password_is_failed(self):
        payload = {"login": "Vova123"}
        r = requests.post(f'{URL.MAIN_URL}{API.LOGIN_COURIER}', data=payload)
        assert r.status_code == 400
        assert r.json()['message'] == 'Недостаточно данных для входа'
