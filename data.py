from faker import Faker
import random
import string


class UserData:
    fake = Faker()

    email = fake.email()
    name = ''.join(random.choice(string.ascii_lowercase) for i in range(8)).capitalize()


class Message:

    user_exists = "User already exists"
    required_field_missing = "Email, password and name are required fields"
    incorrect_login_details = "email or password are incorrect"
    unauthorized = "You should be authorised"
    email_exists = "User with such email already exists"
    no_ingredients = "Ingredient ids must be provided"
    email_sent = "Reset email sent"
