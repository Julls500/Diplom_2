import allure
import endpoints
from data import Message
from utils import Funcs, Request
import pytest


class TestLogin:

    @allure.title('200 OK при успешной авторизации пользователя.')
    @allure.description('Создаем пользователя фикстурой created_user.'
                        ' Создаем payload для авторизации пользователя из данных регистрации.'                        
                        ' Отправлям POST запрос на ручку /api/auth/login.' 
                        ' Проверяем, что ответ 200 ОК и в теле ответа "email" и "name" совпадают с данными пользователя.'
                        ' Обновляем accessToken и refreshToken в данных пользователя.'
                        ' Созданный пользователь удаляется из системы фикстурой created_user по accessToken.')
    def test_user_login_existing_user_success_200(self, created_user):
        payload = Funcs.login_payload(created_user)
        response = Request.post(endpoints.USER_AUTHORIZE, payload, '')
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.text}'
        assert (response.json().get("user").get("email") == created_user["user"]["email"]
                and response.json().get("user").get("name") == created_user["user"]["name"]), f'Данные пользователя не совпадают {response.text}'
        Funcs.update_user_tokens(created_user, response)

    @allure.title('401 Unauthorized при авторизации пользователя с неверным логином или паролем и без них.')
    @allure.description('Параметрический тест.'
                        ' Создаем пользователя фикстурой created_user.'
                        ' Создаем payload для авторизации пользователя из данных регистрации.' 
                        ' Изменяем одно из полей payload на пустую строку или некорректное значение.'
                        ' Отправлям POST запрос на ручку /api/auth/login.' 
                        ' Проверяем, что ответ 401 Unauthorized и в теле ответа "message" "email or password are incorrect".'
                        ' Созданный пользователь удаляется из системы фикстурой created_user по accessToken.')
    @pytest.mark.parametrize('invalid_param, value', [["email", ""], ["email", "wrong@email.com"], ["password", ""], ["password", "wrong_password"]])
    def test_user_login_invalid_login_params_shows_error_401(self, created_user, invalid_param, value):
        payload = Funcs.login_payload(created_user)
        Funcs.change_payload_param(payload, invalid_param, value)
        response = Request.post(endpoints.USER_AUTHORIZE, payload, '')
        assert response.status_code == 401, f'Ожидалось: 401 Unauthorized, получено {response.text}'
        assert response.json().get("message") == Message.incorrect_login_details, f'Ожидалось {Message.incorrect_login_details}, получено {response.json().get("message")}'
