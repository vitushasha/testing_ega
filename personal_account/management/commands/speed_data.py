from personal_account.models import GenderType, UserType, DocumentType, Users
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seeds the database with initial test data'

    def handle(self, *args, **kwargs):

        user = Users.objects.create_superuser(login='superuser_login', password='password')

        genders_types = [GenderType(name='Мужской', create_user=user), GenderType(name='Женский', create_user=user)]
        for genders_type in genders_types:
            genders_type.save()

        users_types = [UserType(name='Администратор', create_user=user), UserType(name='Пользователь', create_user=user)]
        for users_type in users_types:
            users_type.save()

        documents_types = [
            DocumentType(name='Паспорт', create_user=user),
            DocumentType(name='Полис', create_user=user),
            DocumentType(name='СНИЛС', create_user=user),
            DocumentType(name='ИНН', create_user=user),
        ]

        for documents_type in documents_types:
            documents_type.save()

        user.type = UserType.objects.get(id=1)
        user.gender_type = GenderType.objects.get(id=1)
        user.create_user = user
        user.save()
