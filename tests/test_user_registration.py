import allure
import endpoints
from data import Message
from utils import Funcs, Request, Generator
import pytest

class TestUserRegistration:

    @allure.title('200 OK при запросе на создание уникального пользователя.')
    @allure.description('Генерируем payload для создания пользователя фикстурой user_payload,'
                        ' Отправлям POST запрос на ручку /api/auth/register.' 
                        ' Проверяем, что ответ 200 ОК и в теле ответа "email" и "name" совпадают с payload.'
                        ' Также проверяем и что в ответе вернулись accessToken и refreshToken.'
                        ' Записываем accessToken и refreshToken из ответа в user_payload.'
                        ' Созданный пользователь удаляется из системы фикстурой user_payload по accessToken.')
    def test_user_registration_new_user_success_200(self, user_payload):
        response = Request.post(endpoints.USER_REGISTER, user_payload, '')
        assert response.status_code == 200, f'Ожидалось: 200 OK, получено {response.text}'
        assert response.json().get("user").get("email") == user_payload.get("email") and response.json().get("user").get("name") == user_payload.get("name"), f'Данные пользователя не совпадают {response.text}'
        assert len(response.json().get("accessToken")) != 0 and len(response.json().get("refreshToken")) != 0, 'Токен не получен'
        Funcs.update_user_tokens(user_payload, response)

    @allure.title('403 Forbidden при запросе на повторное создание пользователя.')
    @allure.description('Генерируем payload для создания пользователя фикстурой user_payload.'
                        ' Отправлям POST запрос на ручку /api/auth/register.'
                        ' Отправлям повторный POST запрос на ручку /api/auth/register.'                        
                        ' Проверяем, что ответ 403 Forbidden и в теле ответа сообщение "User already exists".'
                        ' Записываем accessToken и refreshToken из первого запроса в user_payload.'
                        ' Созданный пользователь удаляется из системы фикстурой user_payload по accessToken.')
    def test_user_registration_user_exists_shows_error_403(self, user_payload):
        response1 = Request.post(endpoints.USER_REGISTER, user_payload, '')
        response2 = Request.post(endpoints.USER_REGISTER, user_payload, '')
        assert response2.status_code == 403, f'Ожидалось: 403 Forbidden, получено {response2.text}'
        assert response2.json().get("message") == Message.user_exists, f'Ожидалось {Message.user_exists}, получено {response2.json().get("message")}'
        Funcs.update_user_tokens(user_payload, response1)

    @allure.title('403 Forbidden при запросе на создание пользователя без обязательных полей.')
    @allure.description('Параметрический тест.'
                        ' Генерируем payload для создания пользователя.'
                        ' Заменяем в payload последовательно один из параметров "email", "password", "name" на пустую строку.'
                        ' Отправлям POST запрос на ручку /api/auth/register.'                      
                        ' Проверяем, что ответ 403 Forbidden и в теле ответа сообщение "Email, password and name are required fields".')
    @pytest.mark.parametrize('key_to_change', ["email", "password", "name"])
    def test_user_registration_without_required_param_shows_error_403(self, key_to_change):
        user = Generator.get_user_payload()
        Funcs.change_payload_param(user, key_to_change, "")
        response = Request.post(endpoints.USER_REGISTER, user, '')
        assert response.status_code == 403, f'Ожидалось: 403 Forbidden, получено {response.text}'
        assert response.json().get("message") == Message.required_field_missing, f'Ожидалось {Message.required_field_missing}, получено {response.json().get("message")}'
