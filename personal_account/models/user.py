import base64

from django.contrib.auth.hashers import check_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from personal_account.models.user_manager import CustomUserManager


class Users(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=255, unique=True, verbose_name='Логин')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    first_name = models.CharField(max_length=255, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', null=True, blank=True)
    patr_name = models.CharField(max_length=255, verbose_name='Отчество', null=True, blank=True)
    deleted = models.BooleanField(default=False, verbose_name='Отметка об удалении записи')

    create_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    modify_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата и время последнего изменения записи'
    )

    gender_type = models.ForeignKey(
        'GenderType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='Пол'
    )
    type = models.ForeignKey(
        'UserType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='Тип пользователя'
    )
    create_user = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        verbose_name='Автор записи'
    )
    modify_user = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_users',
        verbose_name='Автор последнего изменения записи'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def set_password(self, password):
        super().set_password(password)
        self.password = base64.b64encode(self.password.encode('utf-8')).decode('utf-8')

    def check_password(self, raw_password):

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        decoded_password = base64.b64decode(self.password)

        return check_password(raw_password, decoded_password.decode(), setter)

    def to_dict(self) -> dict:
        return dict(login=self.login,
                    password=self.password,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    patr_name=self.patr_name,
                    gender_type=self.gender_type.id,
                    create_user=self.create_user,
                    create_datetime=self.create_datetime,
                    user_type=self.type,
                    modify_datetime=self.modify_datetime,
                    modify_user=self.modify_user)

    @property
    def display_name(self) -> str:
        names_list = [self.last_name, self.first_name, self.patr_name]
        existing_names = list(filter(None, names_list))
        if existing_names and self.first_name:
            return ' '.join(existing_names)

        return self.login

    def __str__(self):
        return self.display_name
