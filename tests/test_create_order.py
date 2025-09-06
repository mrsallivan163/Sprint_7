import requests
import pytest
import allure

from utils.api_client import cancel_order
from config.settings import URL, API


@allure.suite('Яндекс Самокат. Создание заказа POST /api/v1/orders')
class TestCreateOrder:

    @allure.title('Проверка, что можно создать заказ с разными цветами')
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": "Python",
            "lastName": "Pythonov",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-06-06",
            "comment": "i'm snaeke",
            "color": color
        }

        r = requests.post(f"{URL.MAIN_URL}{API.CREATE_ORDER}", json=payload)
        assert r.status_code == 201
        assert "track" in r.json()
        track = r.json()["track"]
        assert isinstance(r.json()["track"], int)
        try:
            cancel_order(track)
        except:
            pass

