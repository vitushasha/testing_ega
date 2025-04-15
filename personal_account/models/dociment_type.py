from django.db import models


class DocumentType(models.Model):
    name = models.CharField(max_length=255,verbose_name='Название типа документа')
    deleted = models.BooleanField(
        default=False,
        verbose_name='Отметка об удалении записи'
    )

    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    modify_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата и время последнего изменения записи'
    )

    create_user = models.ForeignKey(
        'Users',
        null=True,blank=True,
        on_delete=models.SET_NULL,
        related_name='created_document_types',
        verbose_name='Автор создания записи'
    )
    modify_user = models.ForeignKey(
        'Users',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='modified_document_types',
        verbose_name='Автор последнего изменения записи'
    )

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'

    def __str__(self):
        return self.name
