import pytest
import requests
import allure

from utils.api_client import login_courier_and_return_id, delete_courier
from config.settings import URL, API
from config.test_api_data import RESPONSE_TEXT
from utils.helpers import generate_random_string


@allure.suite('Яндекс Самокат. Создание курьера POST /api/v1/courier')
class TestCreateCourier():

    @allure.title('Проверка создания курьера, когда заполнены все поля')
    def test_create_courier_success_when_fill_all_fields(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"login": login, "password": password, "firstName": first_name}
        r=requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 201
        assert r.json() == {'ok': True}
        try:
            courier_id = login_courier_and_return_id(payload)
            delete_courier(courier_id)
        except:
            pass

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_not_create_two_identical_couriers(self, registered_courier):
        login, password, first_name = registered_courier
        payload = {"login":login,"password":password, "firstName":first_name}
        r=requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 409
        assert r.json()['message'] == RESPONSE_TEXT.LOGIN_USED
        try:
            courier_id = login_courier_and_return_id(payload)
            delete_courier(courier_id)
        except:
            pass

    @pytest.mark.parametrize(
        'payload', [
            {"login": "Vova123", "firstName": "Vovka"},
            {"password": "1234", "firstName": "Vovka"}
        ]
    )
    @allure.title('Проверка, что нельзя создать курьера если не переданы обязательные поля password и login')
    def test_create_courier_missing_required_field(self, payload):
        r = requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 400
        assert r.json()['message'] == RESPONSE_TEXT.NOT_ENOUGH_DATA_TO_CREATE

    @allure.title('Проверка, что можно создать курьера если не передать опциональное поле firstName')
    def test_create_courier_success_missing_firstname_optional(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        payload = {"login": login, "password": password}
        r = requests.post(f'{URL.MAIN_URL}{API.CREATE_COURIER}', data=payload)
        assert r.status_code == 201
        assert r.json() == {'ok': True}
        try:
            courier_id = login_courier_and_return_id(payload)
            delete_courier(courier_id)
        except:
            pass
