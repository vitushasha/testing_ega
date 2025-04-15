from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from personal_account.models import Users, Document
from personal_account.utils.get_params import get_param
from personal_account.utils.helpers import get_valid_data, parse_users_data_from_request, get_users_credentials

from logger import logger

from django.utils import timezone

from personal_account.models.serializers import UserSerializer


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user and request.user.type.id == 1 and request.user.type.name == 'Администратор'


class UsersApiView(APIView):
    permission_classes = (IsAdministrator,)

    @get_param('users', list)
    def get(self, request, format=None):
        users = Users.objects.all()
        if request.data.get('users'):
            usernames = request.data.get('users')
            users = users.filter(login__in=usernames, deleted=False)
        if users.exists():
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response("No users", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        """Метод для создания и обновления пользователей"""

        response_data = []

        users_data = parse_users_data_from_request(request)

        # Списки пользователей для создания и обновления
        users_to_create = []
        users_to_update = []
        # Список со всеми документами из запроса
        # сначала запишем все документы и пройдемся по ним отдельно
        documents_data = []

        result_data = {}

        for user_data in users_data:
            credentials = get_users_credentials(user_data)
            if not credentials:
                continue
            user_data.update(credentials)
            user_data.pop('Credentials')

            if not user_data.get('Documents'):
                logger.debug(f'No Documents data for user: {user_data}')

            # Добавляем документы пользователя ко всем
            documents = user_data.get('Documents')
            # Записываем логин соответствующего пользователя к каждому документу, чтобы потом удобно его определять
            for document in documents:
                document['user_login'] = user_data['username']
                documents_data.append(document)

            # Если пользователь с указанным login уже существует, то обновляем данные, когда они отличаются
            if Users.objects.filter(login=user_data['username']).exists():
                user = Users.objects.get(login=user_data['username'])

                valid_data = get_valid_data(user_data, user)

                # Если данные полностью совпадают, то переходим к следующему
                if all([valid_data[field] == user.__dict__[field]
                        if field != 'password' else (user.check_password(valid_data['password']) or valid_data['password'] == user.password)
                        for field in valid_data]):
                    continue

                if user.deleted:
                    logger.debug(f'Update user, who was deleted: {user.login}')

                valid_data['modify_user'] = request.user
                valid_data['modify_datetime'] = timezone.now()
                users_to_update.append(valid_data)

            # Если пользователя нет, то добавляем в список к созданию
            else:
                valid_data = get_valid_data(user_data)
                valid_data['create_user'] = request.user
                users_to_create.append(valid_data)

        try:
            # Создаем и обновляем пачкой всех пользователей
            Users.objects.bulk_create_users(users_to_create)
            Users.objects.bulk_update_users(users_to_update)
            if not users_to_update and not users_to_create:
                result_data['Users_results'] = 'No users to create or update, or update or bad request'
            else:
                result_data['Users_results'] = (f'Updated: {", ".join([user["login"] for user in users_to_update])}\n'
                                                  f'Created: {", ".join([user["login"] for user in users_to_create])}')
        except Exception as e:
            logger.debug(f'Creating or updating users error: {e}')

        # Списки документов к созданию/обновлению
        docs_to_create = []
        docs_to_update = []
        for doc_data in documents_data:
            user = Users.objects.filter(login=doc_data['user_login'], deleted=False).first()

            # Проверяем, есть ли уже такой документ
            if Document.objects.filter(user=user,
                                       type_id=int(doc_data['documentType_id'])).exists():
                doc = Document.objects.get(user=user, type_id=doc_data['documentType_id'])
                # Если данные различаются, тогда добавляем документ в список к обновлению
                if doc.data != doc_data:
                    doc.data = doc_data
                    doc.modify_datetime = timezone.now()
                    doc.modify_user = request.user
                    docs_to_update.append(doc)
            else:
                if list(filter(lambda x: x.type.id == int(doc_data['documentType_id']) and x.user == user, docs_to_create)):
                    logger.debug(f'Duplicate document type for user. Document data: {doc_data}, user: {user}')
                    continue
                doc = Document(user=user,
                               type_id=int(doc_data['documentType_id']),
                               data=doc_data,
                               create_user=request.user)
                docs_to_create.append(doc)

        # Также создаем и обновляем пачкой все документы
        try:
            Document.objects.bulk_create(docs_to_create)
            Document.objects.bulk_update(docs_to_update, fields=['data', 'modify_datetime', 'modify_user'])
        except IntegrityError as e:
            logger.debug(f'There are duplicates documents types for users')
            return Response("Documents types for any users duplicates", status=status.HTTP_400_BAD_REQUEST)
        if not docs_to_update and not docs_to_create:
            result_data['Documents_results'] = 'No documents to create or update, or bad request'
        else:
            result_data['Documents_results'] = (f'Updated: {", ".join([doc.data["id"] for doc in docs_to_update])}\n'
                                                  f'Created: {", ".join([doc.data["id"] for doc in docs_to_create])}')
        response_data.append(result_data)

        return Response(data=response_data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        users_data = parse_users_data_from_request(request)
        if not users_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        users_to_delete = []
        for user_data in users_data:
            credentials = get_users_credentials(user_data)
            if not credentials:
                continue
            users_to_delete.append(credentials.get('username'))

        users = Users.objects.filter(login__in=users_to_delete, deleted=False)
        if not users:
            return Response(status=status.HTTP_404_NOT_FOUND)

        for user in users:
            user.active = False
            user.deleted = True
            user.modify_user = request.user
            user.modify_datetime = timezone.now()

        documents = Document.objects.filter(user__login__in=users_to_delete, deleted=False)
        for document in documents:
            document.deleted = True
            document.modify_user = request.user
            document.modify_datetime = timezone.now()

        Users.objects.bulk_update(users, fields=['deleted', 'modify_user', 'modify_datetime'])
        Document.objects.bulk_update(documents, fields=['deleted', 'modify_user', 'modify_datetime'])
        return Response(status=status.HTTP_200_OK)
