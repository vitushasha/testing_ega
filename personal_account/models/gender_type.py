from django.db import models


class GenderType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    deleted = models.BooleanField(default=False, verbose_name='Отметка об удалении записи')

    create_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания записи'
    )
    modify_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата и время последнего изменения записи'
    )

    create_user = models.ForeignKey(
        'Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_genders',
        verbose_name='Автор создания записи'
    )
    modify_user = models.ForeignKey(
        'Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_genders',
        verbose_name='Автор последнего изменения записи'
    )

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Гендеры'

    def __str__(self):
        return self.name
