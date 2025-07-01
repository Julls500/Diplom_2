import endpoints
from data import Message
import allure
from api_methods import Request, Order


class TestGetUserOrders:

    @allure.title('200 OK и успешное получение списка заказов авторизованным пользователем.')
    @allure.description('Создаем пользователя фикстурой created_user.'
                        ' Создаем два заказа с accessToken пользователя и сохраняем их номера.'
                        ' Отправлям GET запрос на ручку /api/orders с accessToken пользователя.'
                        ' Проверяем, что ответ 200 ОК, и создаем список из номеров заказов из ответа.'
                        ' Проверяем что теле ответа два заказа и их номера совпадают с созданными.'
                        ' Созданный пользователь удаляется из системы фикстурой created_user по accessToken.')
    def test_get_user_orders_user_authorized_success_200(self, created_user):
        token = created_user.get("accessToken")
        burger1 = Request.post(endpoints.ORDER, Order.make_burger(), token)
        burger1_number = burger1.json()["order"]["number"]
        burger2 = Request.post(endpoints.ORDER, Order.make_burger(), token)
        burger2_number = burger2.json()["order"]["number"]
        response = Request.get(endpoints.ORDER, token)
        r = response.json()
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.text}'
        user_orders = Order.nums_list(r)
        assert len(user_orders) == 2 and burger1_number in user_orders and burger2_number in user_orders, f'Номера заказов пользователя не совпадают с созданными.'

    @allure.title('401 Unauthorized при запросе на получение списка заказов пользователя без авторизации.')
    @allure.description(' Отправлям GET запрос на ручку /api/orders без accessToken.'
                        ' Проверяем, что ответ 401 Unauthorized, и "message" в теле ответа "You should be authorised"')
    def test_get_user_orders_user_not_authorized_shows_error_401(self):
        response = Request.get(endpoints.ORDER, '')
        assert response.status_code == 401, f'Ожидалось: 401 Unauthorized, получено {response.text}'
        assert response.json().get("message") == Message.unauthorized, f'Ожидалось {Message.unauthorized}, получено {response.json().get("message")}'
