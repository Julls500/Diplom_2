import requests
import json
import logging
import allure
import endpoints
from faker import Faker
import random
import string

class User:

    @staticmethod
    @allure.step('Регистрация пользователя, проверка успешного ответа и возвращение всех известных данных (включая пароль и токены) для дальнейшего использования.')
    def register():
        user = Generator.get_user_payload()
        response = Request.post(endpoints.USER_REGISTER, user, '')
        if response.status_code == 200:
            Funcs.message(f'Пользователь создан')
            resp = response.json()
            resp["user"]["password"] = user.get("password")
            return resp
        else:
            Funcs.message(f'Пользователь не зарегистрирован: {response.status_code}, {response.text}.')

    @staticmethod
    @allure.step('Удаление пользователя и проверка успешного ответа.')
    def delete(access_token):
        response = Request.delete(endpoints.USER, access_token)
        if response.status_code == 202:
            Funcs.message(f'Пользователь удален')
        else:
            Funcs.message(f'Пользователь не удален: {response.status_code}, {response.text}.')

class Order:

    @staticmethod
    @allure.step('Получение данных об ингредиентах.')
    def get_ingredients():
        response = Request.get(endpoints.INGREDIENTS, '')
        if response.status_code == 200:
            Funcs.message(f'Список ингредиентов получен')
            return response.json()
        else:
            Funcs.message(f'Список ингредиентов не получен: {response.status_code}, {response.text}.')

    @staticmethod
    @allure.step('Создание списка ингредиентов с сортировкой по типу.')
    def sorted_ingredients():
        ingredients = Order.get_ingredients()
        sorted_ings = {
            "buns": [],
            "fillings": [],
            "sauces": []
            }
        for ing in ingredients.get('data'):
            if ing["type"] == "bun":
                sorted_ings["buns"].append(ing)
            elif ing["type"] == "sauce":
                sorted_ings["sauces"].append(ing)
            elif ing["type"] == "main":
                sorted_ings["fillings"].append(ing)
        return sorted_ings

    @staticmethod
    @allure.step('Создание бургера.')
    def make_burger():
        list =[]
        ings_list = Order.sorted_ingredients()
        bun = ings_list["buns"][random.randint(0, len(ings_list["buns"])-1)]
        sauce = ings_list["sauces"][random.randint(0, len(ings_list["sauces"])-1)]
        filling = ings_list["fillings"][random.randint(0, len(ings_list["fillings"])-1)]
        list.append(bun.get("_id"))
        list.append(bun.get("_id"))
        list.append(sauce.get("_id"))
        list.append(filling.get("_id"))
        burger = {
            "ingredients": list
            }
        return burger

    @staticmethod
    @allure.step('Формироваие списка из номеров заказов.')
    def nums_list(response):
        order_nums = []
        for order in response.get("orders"):
            order_nums.append(order["number"])
        return order_nums

    @staticmethod
    @allure.step('Получение списка c номерами заказов.')
    def order_nums(path, access_token):
        response = Request.get(path, access_token)
        if response.status_code == 200:
            Funcs.message(f'Список заказов получен')
            r = response.json()
            return Order.nums_list(r)
        else:
            Funcs.message(f'Список заказов не получен: {response.status_code}, {response.text}.')


class Request:

    @staticmethod
    @allure.step('POST request.')
    def post(path, payload, access_token):
        return requests.post(endpoints.URL_SERVICE + path, headers=Funcs.auth_header(access_token), data=json.dumps(payload))

    @staticmethod
    @allure.step('DELETE request.')
    def delete(path, access_token):
        return requests.delete(endpoints.URL_SERVICE + path, headers=Funcs.auth_header(access_token))

    @staticmethod
    @allure.step('PATCH request.')
    def patch(path, access_token, payload):
        return requests.patch(endpoints.URL_SERVICE + path, headers=Funcs.auth_header(access_token), data=json.dumps(payload))

    @staticmethod
    @allure.step('GET request.')
    def get(path, access_token):
        return requests.get(endpoints.URL_SERVICE + path, headers=Funcs.auth_header(access_token))


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
