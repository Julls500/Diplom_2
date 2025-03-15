from utils import User, Generator
import pytest
import allure


@allure.step('Генерация данных для регистрации нового пользователя, получение деталей и удаление зарегистрированного пользователя после теста.')
@pytest.fixture
def user_payload():
    user = Generator.get_user_payload()
    yield user
    User.delete(user.get("accessToken"))

@allure.step('Регистрация нового пользователя, получение деталей и удаление зарегистрированного пользователя после теста.')
@pytest.fixture
def created_user():
    user = User.register()
    yield user
    User.delete(user.get("accessToken"))
