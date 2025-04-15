
# Описание проекта

## Требования
- Python 3.10
- Django 5
- Django Rest Framework
- PostgreSQL

## Развертывание

1. Клонируйте проект с GitHub в вашу IDE, например, PyCharm.

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # Для Windows используйте venv\Scriptsctivate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте базу данных PostgreSQL и настройте подключение в файле `local_settings.py`, который должен быть создан в корне проекта. Для этого скопируйте пример из `example_local_settings.py` в новый файл `local_settings.py` и укажите правильные параметры для подключения к вашей базе данных.

5. Примените миграции:
```bash
python manage.py migrate
```

7. Для создания тестовых данных в базе данных выполните команду. Эта команда создаст суперпользователя Django и типы пользователей, гендеров и документов.
```bash
python manage.py speed_data
```

## Тестовые данные

Проект содержит несколько тестовых JSON файлов, которые могут быть полезны для проверки.

## API

Приложение может обрабатывать следующие запросы:

- **POST**, **GET**, **DELETE** запросы на создание и изменение пользователей и их документов.
- Получение информации о пользователе (для текущего пользователя) и его документах с фильтром по документам.
- Получение информации о всех пользователях (только если вы администратор).

### Запуск приложения

После запуска локального сервера на порту 8000, доступно API по адресу:
```
http://localhost:8000/api/
```

### Методы

#### Получение списка пользователей

`GET /api/users/`

Параметры фильтрации: 
- `users`: список логинов пользователей, разделенных запятой.

#### Получение информации о текущем пользователе и его документах

`GET /api/profile/`

Параметры фильтрации:
- `doc_ids`: список ID документов, разделенных запятой.

### Авторизация

Авторизация осуществляется по токену. Для получения токена нужно отправить POST запрос на:
```
POST /api/authtoken/
```
Тело запроса должно содержать:
```json
{
  "login": "<ваш_логин>",
  "password": "<ваш_пароль>"
}
```
В ответ будет возвращен токен, который необходимо указать в заголовке "Authorization" для аутентификации при отправке каждого запроса.

Пример заголовка для авторизации:
```
Authorization: Token <token>
```

## Пример JSON для POST/DELETE запросов

```json
[
    {
      "id": 80087332,
      "referralGUID": "F234FG244422FFFFF4:232RFS",
      "referralDate": "2024-01-23T18:55:02",
      "Data": [
        {
          "Sender": {
            "Organization": {
                "oid": "1.2.5.23.543.1234.18972",
                "fullName": "СП.АРМ"
            }
          },
          "Users": [
            {
                "id": 1504926,
                "lastName": "Иванова",
                "firstName": "Екатерина",
                "patrName": "Петровна",
                "birthDate": "1996-06-08",
                "sex": "2",
                "phoneNumber": "9999999999",
                "snils": "12495797018",
                "inn": "027801597819",
                "socStatus_id": "102",
                "socStatusFed_Code": "8",
                "pid": null,
                "parPersonSurName_SurName": null,
                "parPersonFirName_FirName": null,
                "parPersonSecName_SecName": null,
                "deputyKind_id": null,
                "deputyOrg_id": "0",
                "documentAuthority_id": null,
                "documentDeputy_Ser": null,
                "documentDeputy_Num": null,
                "documentDeputy_Issue": null,
                "documentDeputy_begDate": null,
                "legalStatusVZN_id": null,
                "legalStatusVZN_Name": null,
                "legalStatusVZN_pid": null,
                "legalStatusVZN_pName": null,
                "employment_id": null,
                "familyStatus_id": null,
                "personFamilyStatus_IsMarried": null,
                "Credentials":{
                    "username": "login",
                    "pass": "pwd"
                },
                "Address": {
                    "id": "11337703",
                    "value": "450015, РОССИЯ, БАШКОРТОСТАН РЕСП, Г УФА, СОВЕТСКИЙ РАЙОН, РЫБНАЯ УЛ, д. 5, корп. Б, кв. ",
                    "org_id": null,
                    "post_id": null,
                    "guid": "8479A314-A179-4874-A8FD-AC7CED2BCEE5"
                },           
                "Documents": [
                    {
                      "id": "18382434", 
                      "documentType_id": 2,
                      "documentType_Name": "Полис ОМС",
                      "sprTerr_id": "1075",
                      "type": "ОМС",
                      "series": 12433,
                      "number": "0253310891000710",
                      "smo_id": "8000229",
                      "beginDate": "2021-12-14",
                      "endDate": null,
                      "orgDep_Name": "РЕСО МЕД",
                      "formType_id": "3",
                      "lpu_id": "150028"
                    },
                    {
                      "id": "18383277",
                      "documentType_id": "1",
                      "documentType_Name": "Паспорт гражданина Российской Федерации",
                      "series": "86 21",
                      "number": "407195",
                      "beginDate": "2021-11-02",
                      "endDate": null,
                      "isTwoNation": null,
                      "orgDep_id": "32625",
                      "orgDep_Name": "МВД по Республике Башкортостан",
                      "personEvn_begDT": "2023-10-26 08:58:19",
                      "lpu_id": "150028"
                    }
                  ]
            }
          ]        
        }
      ]
    }
  ]
```

## Интерфейс

У Django Rest Framework есть свой интерфейс для отображения данных.
Для удобного отображения данных в браузере можно перейти по адресу с любым GET запросом к методу, который его поддерживает
Например:

```
http://localhost:8000/api/users/
```