from django.utils.module_loading import import_string
from rest_framework import serializers

DocumentsSerializer = import_string('personal_account.models.serializers.documents_serializer.DocumentsSerializer')

class UserSerializer(serializers.ModelSerializer):
    documents = DocumentsSerializer(many=True)
    class Meta:
        model = import_string('personal_account.models.Users')
        fields = (
            'login',
            'password',
            'first_name',
            'last_name',
            'patr_name',
            'deleted',
            'create_datetime',
            'modify_datetime',
            'gender_type',
            'type',
            'create_user',
            'modify_user',
            'documents',
        )
