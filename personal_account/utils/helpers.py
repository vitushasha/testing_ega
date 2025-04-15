from logger import logger
from personal_account.models import Users
from personal_account.models.user_type import UserType

def get_valid_data(request_data, user: Users = None) -> dict:
    """Метод для парса данных о пользователях из каждой записи"""

    try:
        gender_type_id = int(request_data.get('sex'))
    except TypeError:
        gender_type_id = 0
    except ValueError as e:
        logger.debug(f'Error: {str(e)}. Not valid value for gender type, gave "{request_data.get("sex")}", user data: {request_data}')
        gender_type_id = None

    if not user:
        return {
            'login': request_data.get('username'),
            'password': request_data.get('pass'),
            'first_name': request_data.get('first_name'),
            'last_name': request_data.get('last_name'),
            'patr_name': request_data.get('patr_name'),
            'gender_type_id': gender_type_id,
            'type': UserType.objects.exclude(name='Администратор').first(),
        }

    return {
        'login': request_data.get('username', user.__dict__.get('login')),
        'password': (request_data.get('pass', user.__dict__.get('_password'))),
        'first_name': request_data.get('first_name', user.__dict__.get('first_name')),
        'last_name': request_data.get('last_name', user.__dict__.get('last_name')),
        'patr_name': request_data.get('patr_name', user.__dict__.get('patr_name')),
        'gender_type_id': gender_type_id or user.__dict__.get('gender_type'),
    }

def parse_users_data_from_request(request):
    """Метод для парса пользователей из запроса"""

    users_data = []
    if not request.data or not isinstance(request.data, list):
        return

    for post in request.data:
        # берем информацию о пользователях из тела запроса в соответствии с примером
        post_data = post['Data']
        if not post_data or not isinstance(post_data, list):
            logger.debug('No Data in post')
            continue

        for data_from_post in post_data:

            if not data_from_post.get('Users') or not isinstance(data_from_post.get('Users'), list):
                logger.debug('No Users in Data')
                continue

            users_data.extend(data_from_post['Users'])
            return users_data

    return

def get_users_credentials(user_data):
    """Достаем credentials для каждого пользователя"""

    # В примере логин и пароль каждого пользователя лежат в объекте Credentials внутри каждого user'а,
    # поэтому распаковываем его для удобства, чтобы у нас логин и пароль
    # лежали на одном уровне со всеми остальными данными
    if not user_data.get('Credentials') or not isinstance(user_data.get('Credentials'), dict):
        logger.debug('No Credentials for User')
        return

    credentials = user_data['Credentials']
    if not credentials.get('username') or not credentials.get('pass'):
        logger.debug('No username or pass')
        return

    return credentials
