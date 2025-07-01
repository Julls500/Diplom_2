import allure
import endpoints
from data import UserData, Message
from api_methods import Request, User
import pytest


class TestChangeUserData:

    @allure.title('200 OK при успешном обновлении данных авторизованного пользователя.')
    @allure.description('Параметрический тест.'
                        ' Создаем пользователя фикстурой created_user.'
                        ' Создаем payload для обновления данных пользователя ("email" или "name").'
                        ' Отправлям PATCH запрос на ручку /api/auth/user с accessToken пользователя.'
                        ' Проверяем, что ответ 200 ОК и в теле ответа обновленный параметр совпадает с изменяемым.'
                        ' Созданный пользователь удаляется из системы фикстурой created_user по accessToken.')
    @pytest.mark.parametrize('param, value', [["email", UserData.email], ["name", UserData.name]])
    def test_change_user_data_valid_params_user_authorized_success_200(self, created_user, param, value):
        payload = {
            f'{param}': f'"{value}"'
            }
        response = Request.patch(endpoints.USER, created_user.get("accessToken"), payload)
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.text}'
        assert response.json().get("user").get(f'{param}') == payload.get(f'{param}'), f'Данные пользователя не изменились {response.text}'

    @allure.title('401 Unauthorized при запросе на обновлении данных неавторизованного пользователя.')
    @allure.description('Параметрический тест.'
                        ' Создаем payload для обновления данных пользователя ("email" или "name").'
                        ' Отправлям PATCH запрос на ручку /api/auth/user с без accessToken.'
                        ' Проверяем, что ответ 401 Unauthorized и в теле ответа "message" "You should be authorised".')
    @pytest.mark.parametrize('param, value', [["email", UserData.email], ["name", UserData.name]])
    def test_change_user_data_valid_params_user_not_authorized_shows_error_401(self, param, value):
        payload = {
            f'{param}': f'"{value}"'
            }
        response = Request.patch(endpoints.USER, '', payload)
        assert response.status_code == 401, f'Ожидалось: 401 Unauthorized, получено {response.text}'
        assert response.json().get("message") == Message.unauthorized, f'Ожидалось {Message.unauthorized}, получено {response.json().get("message")}'

    @allure.title('403 Forbidden при запросе на обновлении "email" авторизованного пользователя на почту, которая уже используется.')
    @allure.description('Создаем пользователя фикстурой created_user.'
                        ' Создаем еще одного пользователя для получения уже существующего почтового адреса.'
                        ' Создаем payload для обновления "email" у created_user с почтой созданного пользователя.'
                        ' Отправлям PATCH запрос на ручку /api/auth/user с accessToken пользователя created_user.'
                        ' Проверяем, что ответ 403 Forbidden и в теле ответа "message" "User with such email already exists".'
                        ' created_user удаляется из системы фикстурой по accessToken.'
                        ' Созданный пользователь удаляется из системы в конце теста по своему accessToken')
    def test_change_user_data_existing_email_user_authorized_shows_error_403(self, created_user):
        existing_user = User.register()
        payload = {
            "email": existing_user["user"]["email"]
            }
        response = Request.patch(endpoints.USER, created_user.get("accessToken"), payload)
        User.delete(existing_user.get("accessToken"))
        assert response.status_code == 403, f'Ожидалось: 403 Forbidden, получено {response.text}'
        assert response.json().get("message") == Message.email_exists, f'Ожидалось {Message.email_exists}, получено {response.json().get("message")}'

    @allure.title('200 OK успешная отправка инструкции с кодом для восстановления пароля пользователя.')
    @allure.description('Создаем пользователя фикстурой created_user.'
                        ' Отправлям POST запрос на ручку /api/password-reset с email пользователя created_user.'
                        ' Проверяем что ответ 200 OK и в теле ответа вернулось сообщение "Reset email sent".'
                        ' Созданный пользователь удаляется из системы в конце теста по своему accessToken')
    def test_reset_password_email_sent_success_200(self, created_user):
        payload = {
            "email": created_user["user"]["email"]
            }
        response = Request.post(endpoints.RESET_PASSWORD, payload, '')
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.text}'
        assert response.json().get("message") == Message.email_sent, f'Ожидалось {Message.email_sent}, получено {response.json().get("message")}'
