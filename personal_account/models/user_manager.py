from django.contrib.auth.models import BaseUserManager
from typing import List


class CustomUserManager(BaseUserManager):
    def create_user(self, login, password, **extra_fields):

        if not login or not password:
            raise ValueError('Users must have login and password')

        user = self.model(login=login, **extra_fields)
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, login, password, **extra_fields):

        extra_fields.update({'is_staff': True, 'is_superuser': True})

        return self.create_user(login,
                                password,
                                **extra_fields)

    def bulk_create_users(self, users_data: List[dict]):
        if not users_data:
            return
        users_to_create = []
        for user_data in users_data:
            password = user_data.pop('password')
            user = self.model(**user_data)
            user.set_password(password)
            users_to_create.append(user)

        self.bulk_create(users_to_create)

    def bulk_update_users(self, users_data: List[dict]):
        if not users_data:
            return
        users_logins = [user_data['login'] for user_data in users_data]
        users = self.filter(login__in=users_logins)
        users_to_update = []
        for user, user_data in zip(users, users_data):
            for field, value in user_data.items():
                setattr(user, field, value)
            users_to_update.append(user)

        fields = users_data[0].keys()

        self.bulk_update(users_to_update, fields=fields)
