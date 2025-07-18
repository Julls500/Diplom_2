# Diplom_2

## Дипломный проект. Задание 2: API

### Автотесты для проверки API сервиса заказа бургеров Stellar Burgers

### Реализованные сценарии

Созданы тесты, покрывающие работу API эндпоинтов:

- Создание пользователя:                          POST '/api/auth/register'
- Логин пользователя:                             POST '/api/auth/login'
- Изменение данных пользователя:                  PATCH '/api/auth/user', POST '/api/password-reset'
- Создание заказа:                                POST '/api/orders'
- Получение заказов конкретного пользователя:     GET '/api/orders'

### Структура проекта

- tests - пакет, содержащий тесты, разделенные по классам
- conftest.py - фикстуры проекта
- data.py - файл со статическими данными
- endpoints.py - API эндпоинты
- pytest.ini - настройки pytest
- requirements.txt - зависимости проекта
- utils.py - вспомогательные статические методы проекта
- allure_results - отчет allure

**Установка зависимостей**

> `$ pip install -r requirements.txt`

**Получение отчета Allure**

> `$ allure serve allure_results`
