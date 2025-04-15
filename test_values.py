from personal_account.models import GenderType, UserType, DocumentType, Users

user = Users.objects.first()

genders_types = [GenderType(name='Женский', create_user=user), GenderType(name='мужской', create_user=user)]
for genders_type in genders_types:
    genders_type.save()

users_types = [UserType(name='Администратор', create_user=user), GenderType(name='Пользователь', create_user=user)]
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
