import endpoints
from data import Message
from utils import Request, Generator, Order
import allure
import pytest


class TestCreateOrder:

    @allure.title('200 OK Успешное создание заказа и появление заказа в списках заказов при создании заказа авторизованным пользователем с валидными ингредиентами.')
    @allure.description(' Создаем пользователя фикстурой created_user.'
                        ' Создаем payload для заказа.'
                        ' Отправлям POST запрос на ручку /api/orders с accessToken пользователя.'
                        ' Проверяем, что ответ 200 ОК и получаем из ответа номер заказа.'
                        ' Получаем список заказов пользователя и проверяем что среди них есть заказ с таким номером.'
                        ' Получаем список 50 последних заказов и проверяем что среди них есть заказ с таким номером.'
                        ' Созданный пользователь удаляется из системы фикстурой created_user по accessToken.')
    def test_create_order_user_authorized_valid_ingredients_order_created_200(self, created_user):
        payload = Order.make_burger()
        token = created_user.get("accessToken")
        response = Request.post(endpoints.ORDER, payload, token)
        assert response.status_code == 200, f'Заказ не сформирован. Ожидалось: 200 OK, получено {response.text}'
        created_order_number = response.json()["order"]["number"]
        user_orders = Order.order_nums(endpoints.ORDER, token)
        all_orders = Order.order_nums(endpoints.ALL_ORDERS, '')
        assert created_order_number in user_orders, f'Заказ не появился в списке заказов пользоваеля.'
        assert created_order_number in all_orders, f'Заказ не появился в списке всех заказов.'

    @allure.title('401 Unauthorized при создании заказа без авторизации с валидными ингредиентами.')
    @allure.description('Создаем payload для заказа.'
                        ' Отправлям POST запрос на ручку /api/orders без accessToken.'
                        ' Проверяем, что ответ 401 Unauthorized.'
                        ' Комментарий:поведение системы при создании заказа неавторизованным пользователем не описано. ОР рекомендован наставником. Подтвержденный баг.')
    @pytest.mark.xfail(reason="Поведение системы при создании заказа неавторизованным пользователем не описано. ОР рекомендован наставником. Подтвержденный баг.")
    def test_create_order_user_not_authorized_valid_ingredients_shows_error_401(self):
        payload = Order.make_burger()
        response = Request.post(endpoints.ORDER, payload, '')
        assert response.status_code == 401, f'Ожидалось: 401 Unauthorized, получено {response.text}'

    @allure.title('400 Bad Request при создании заказа авторизованным пользователем без ингредиентов.')
    @allure.description('Создаем пользователя фикстурой created_user.'
                        ' Отправлям POST запрос на ручку /api/orders с accessToken и пустым payload.'
                        ' Проверяем, что ответ 400 Bad request и "message" в теле ответа "Ingredient ids must be provided".'
                        ' Созданный пользователь удаляется из системы фикстурой created_user по accessToken.')
    def test_create_order_user_authorized_no_ingredients_shows_error_400(self, created_user):
        payload = []
        token = created_user.get("accessToken")
        response = Request.post(endpoints.ORDER, payload, token)
        assert response.status_code == 400, f'Ожидалось: 400 Bad request, получено {response.text}'
        assert response.json().get("message") == Message.no_ingredients, f'Ожидалось {Message.no_ingredients}, получено {response.json().get("message")}'

    @allure.title('400 Bad Request при создании заказа без авторизации и без ингредиентов.')
    @allure.description('Отправлям POST запрос на ручку /api/orders без accessToken и пустым payload.'
                        ' Проверяем, что ответ 400 Bad request и "message" в теле ответа "Ingredient ids must be provided".')
    def test_create_order_user_not_authorized_no_ingredients_shows_error_400(self):
        payload = []
        token = ''
        response = Request.post(endpoints.ORDER, payload, token)
        assert response.status_code == 400, f'Ожидалось: 400 Bad request, получено {response.text}'
        assert response.json().get("message") == Message.no_ingredients, f'Ожидалось {Message.no_ingredients}, получено {response.json().get("message")}'

    @allure.title('500 Internal Server Error при создании заказа авторизованным пользователем с невалидным хеш среди ингредиентов.')
    @allure.description('Создаем пользователя фикстурой created_user.'
                        ' Создаем payload для заказа.'
                        ' Генерируем ингредиент с невалидным хеш и добавляем его к payload.'
                        ' Отправлям POST запрос на ручку /api/orders с accessToken пользователя и payload.'
                        ' Проверяем, что ответ 500 Internal Server Error.'
                        ' Созданный пользователь удаляется из системы фикстурой created_user по accessToken.')
    def test_create_order_user_authorized_invalid_ingredient_hash_shows_error_500(self, created_user):
        payload = Order.make_burger()
        invalid_hash = Generator.hash()
        token = created_user.get("accessToken")
        payload["ingredients"].append(invalid_hash)
        response = Request.post(endpoints.ORDER, payload, token)
        assert response.status_code == 500, f'Ожидалось: 500 Bad request, получено {response.text}'
