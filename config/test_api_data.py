class RESPONSE_TEXT:
    LOGIN_USED = 'Этот логин уже используется'
    NOT_ENOUGH_DATA_TO_CREATE = 'Недостаточно данных для создания учетной записи'
    ORDERS_COURIER_NOT_FOUND = 'Курьер с идентификатором 9999999 не найден'
    COURIER_NOT_FOUND = 'Учетная запись не найдена'
    NOT_ENOUGH_DATA_TO_LOGIN = 'Недостаточно данных для входа'

class MOCK_RESPONSE:
    MOCK_RESPONSE_FOR_COURIER_1 = {
        "orders": [
            {
                "id": 100,
                "courierId": 1,
                "firstName": "Иван",
                "lastName": "Иванов",
                "address": "ул. Ленина, д. 10",
                "metroStation": "3",
                "phone": "+7 999 111 22 33",
                "rentTime": 3,
                "deliveryDate": "2024-07-20T15:00:00.000Z",
                "track": 112233,
                "color": ["BLACK"],
                "comment": "Оставить у двери",
                "createdAt": "2024-07-19T10:00:00.000Z",
                "updatedAt": "2024-07-19T10:05:00.000Z",
                "status": 2
            }
        ]
    }