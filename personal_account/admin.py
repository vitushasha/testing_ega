from django.contrib import admin

from personal_account.models import Users, Document, DocumentType, UserType, GenderType


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'deleted', 'login', 'create_user', 'create_datetime')
    list_filter = ('create_datetime', 'create_user', 'modify_datetime', 'modify_user')
    ordering = ('-create_datetime',)
    search_fields = ('id', 'login', 'last_name', 'first_name', 'patr_name', 'create_datetime')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'deleted', 'user', 'create_datetime', 'create_user')
    list_filter = ('create_datetime', 'create_user', 'modify_datetime',  'modify_user')
    ordering = ('-create_datetime',)

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'deleted', 'create_datetime', 'create_user')
    list_filter = ('create_datetime', 'create_user', 'modify_user', 'modify_datetime')
    ordering = ('-create_datetime',)
    search_fields = ('id', 'name', 'create_user')

@admin.register(GenderType)
class GenderTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'deleted', 'create_datetime', 'create_user')
    list_filter = ('create_datetime', 'create_user', 'modify_user', 'modify_datetime')
    ordering = ('-create_datetime',)
    search_fields = ('id', 'name', 'create_user')

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'deleted', 'create_datetime', 'create_user')
    list_filter = ('create_datetime', 'create_user', 'modify_user', 'modify_datetime')
    ordering = ('-create_datetime',)
    search_fields = ('id', 'name', 'create_user')
