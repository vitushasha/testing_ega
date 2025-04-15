from django.db import models


class Document(models.Model):
    data = models.JSONField(verbose_name='Данные документов в формате JSON')
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

    user = models.ForeignKey(
        'Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name='Пользователь',
    )

    type = models.ForeignKey(
        'DocumentType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
        verbose_name='Тип документа',
    )

    create_user = models.ForeignKey(
        'Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_documents',
        verbose_name='Автор создания записи',
    )

    modify_user = models.ForeignKey(
        'Users',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_documents',
        verbose_name='Автор последнего изменения записи'
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        constraints = [
            models.UniqueConstraint(fields=['user', 'type'], name='unique_document_type_per_user')
        ]

    def __str__(self):
        return f'{self.type.name} пользователя {self.user.display_name}'