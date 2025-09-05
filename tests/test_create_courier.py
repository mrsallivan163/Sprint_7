import requests
import allure

from config import URL, API
from helpers import register_new_courier_and_return_login_password, generate_random_string

@allure.suite('Яндекс Самокат. Создание курьера POST /api/v1/courier')
class TestCreateCourier:

    @allure.title('Проверка создания курьера, когда заполнены все поля')
    def test_create_courier_success_when_fill_all_fields(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"login": login, "password": password, "firstName": first_name}
        r=requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 201
        assert r.json() == {'ok': True}

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_not_create_two_identical_couriers(self):
        data_user = register_new_courier_and_return_login_password()
        payload = {"login":data_user[0],"password":data_user[1], "firstName":data_user[2]}
        r=requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 409
        assert r.json()['message'] == 'Этот логин уже используется'

    @allure.title('Проверка, что нельзя создать курьера без обязательного поля password')
    def test_create_courier_missing_password_is_failed(self):
        payload = {"login": "Vova123", "firstName": "Vovka"}
        r = requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 400
        assert r.json()['message'] == 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверка, что нельзя создать курьера без обязательного поля login')
    def test_create_courier_missing_login_is_failed(self):
        payload = {"password": "1234", "firstName": "Vovka"}
        r = requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 400
        assert r.json()['message'] == 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверка, что можно создать курьера если не передать опциональное поле firstName')
    def test_create_courier_success_missing_firstname_optional(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        payload = {"login": login, "password": password}
        r = requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 201
        assert r.json() == {'ok': True}
