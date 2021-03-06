from ast import For
from rest_framework import serializers
from forms_app.models import FormTemplate, FormField, FormEntry, FormFieldAnswer

class FormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = ['form_template_id', 'form_name']

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['field_id', 'field_name', 'type', 'options', 'mandatory', 'form_template']

class FormEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FormEntry
        fields = ['form_entry_id', 'form_template']

class FormFieldAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormFieldAnswer
        fields = ['answer', 'form_entry', 'form_field']

