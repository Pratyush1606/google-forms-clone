from ast import For
from rest_framework import serializers
from forms_app.models import FormTemplate, FormField

class FormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = ['form_id', 'form_name']

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['field_id', 'field_name', 'type', 'options', 'mandatory', 'form_template']

