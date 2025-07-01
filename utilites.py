import logging
import allure
from faker import Faker
import random
import string


class Funcs:

    @staticmethod
    def message(message):
        allure.attach('', message, attachment_type=allure.attachment_type.TEXT)
        logging.info(message)

    @staticmethod
    @allure.step('Изменение одного из полей данных для соответствия тестовому сценарию.')
    def change_payload_param(param, key, value):
        param[key] = value
        return param

    @staticmethod
    @allure.step('Oбновление токенов в данных пользователя')
    def update_user_tokens(user, response):
        user["accessToken"] = response.json()["accessToken"]
        user["refreshToken"] = response.json()["refreshToken"]

    @staticmethod
    @allure.step('Создание payload  для логина из данных зарегистрированного пользователя.')
    def login_payload(user):
        payload = {
            "email":f'{user["user"]["email"]}',
            "password": f'{user["user"]["password"]}'
            }
        return payload

    @staticmethod
    @allure.step('Создание header c токеном авторизации.')
    def auth_header(token):
        header = {
            "Content-Type": "application/json",
            'Authorization': f'{token}'
            }
        return header


class Generator:

    @staticmethod
    @allure.step('Генерация уникальных данных пользователя.')
    def get_user_payload():
        fake = Faker()
        return {
            "email": f'"{fake.email()}"',
            "password": f'"{fake.password()}"',
            "name": ''.join(random.choice(string.ascii_lowercase) for i in range(8)).capitalize()
            }

    @staticmethod
    @allure.step('Генерация хеша ингредиентов.')
    def hash():
        fake = Faker()
        return fake.md5()
