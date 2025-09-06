import requests
import responses

from config.test_api_data import RESPONSE_TEXT
from config.test_api_data import MOCK_RESPONSE
import allure
from config.settings import URL,API

@allure.suite('Яндекс Самокат. Получение списка заказов GET /api/v1/orders')
class TestOrdersList:

    @allure.title('Проверка получения списка заказов, без указания query параметров')
    def test_get_orders_list_success_without_query(self):
        r = requests.get(f"{URL.MAIN_URL}{API.LIST_ORDERS}")
        data = r.json()
        assert r.status_code == 200
        assert "orders" in data
        assert isinstance(data["orders"], list)

    @allure.title('Проверка получения списка заказов по конкретному курьеру с указанием query courierId')
    @responses.activate
    def test_mock_get_orders_list_success_with_query_courier_id(self):
        url = f"{URL.MAIN_URL}{API.LIST_ORDERS}?courierId=1"
        responses.add(
            method=responses.GET,
            url=url,
            match_querystring=True,
            json=MOCK_RESPONSE.MOCK_RESPONSE_FOR_COURIER_1,
            status=200
        )
        r = requests.get(f'{URL.MAIN_URL}{API.LIST_ORDERS}', params={"courierId": 1})
        assert r.status_code == 200
        assert "orders" in r.json()
        assert isinstance(r.json()["orders"], list)
        assert len(r.json()["orders"]) == 1
        for order in r.json()["orders"]:
            assert order["courierId"] == 1

    @allure.title('Проверка ошибки 404 при передаче несуществующего courierId')
    def test_get_orders_list_failed(self):
        r = requests.get(f'{URL.MAIN_URL}{API.LIST_ORDERS}?courierId=9999999')
        assert r.status_code == 404
        assert r.json()['message'] == RESPONSE_TEXT.ORDERS_COURIER_NOT_FOUND

    @allure.title('Проверка получения списка заказов с учетом фильтрации по query nearestStation')
    def test_get_orders_list_success_with_query_nearest_station_1_or_2(self):
        r = requests.get(f'{URL.MAIN_URL}{API.LIST_ORDERS}?nearestStation=["1", "2"]')
        assert r.status_code == 200
        assert "orders" in r.json()
        assert isinstance(r.json()["orders"], list)
        for order in r.json()["orders"]:
            metro_station = order.get("metroStation")
            assert metro_station in ["1", "2"]

    @allure.title('Проверка получения списка заказов c учетом ограничения по выдаче query limit')
    def test_get_orders_list_success_with_query_limit_10(self):
        r = requests.get(f'{URL.MAIN_URL}{API.LIST_ORDERS}?limit=10&page=0')
        assert r.status_code == 200
        assert "orders" in r.json()
        assert isinstance(r.json()["orders"], list)
        assert len(r.json()["orders"]) <= 10

    @allure.title('Проверка получения списка заказов c учетом ограничения по выдаче по query limit и метро query nearest_station')
    def test_get_orders_list_success_with_query_limit_10_and_nearest_station_110(self):
        r = requests.get(f'{URL.MAIN_URL}{API.LIST_ORDERS}?limit=10&page=0&nearestStation=["110"]')
        assert r.status_code == 200
        assert "orders" in r.json()
        assert isinstance(r.json()["orders"], list)
        assert len(r.json()["orders"]) <= 10
        for order in r.json()["orders"]:
            metro_station = order.get("metroStation")
            assert metro_station in ["110"]
