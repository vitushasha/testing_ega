from django.utils.module_loading import import_string
from rest_framework import serializers


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = import_string('personal_account.models.Document')
        fields = '__all__'
