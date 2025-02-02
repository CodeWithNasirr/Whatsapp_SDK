from rest_framework import serializers
from .models import Create_Template


class CreateTemplateSerilizers(serializers.ModelSerializer):
    class Meta:
        model=Create_Template
        fields='__all__'