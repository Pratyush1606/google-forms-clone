# Generated by Django 3.2.12 on 2022-02-06 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormTemplate',
            fields=[
                ('form_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('form_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('field_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('field_name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('options', models.CharField(max_length=100, null=True)),
                ('mandatory', models.CharField(max_length=100)),
                ('form_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='forms_app.formtemplate')),
            ],
            options={
                'unique_together': {('field_name', 'form_template')},
            },
        ),
    ]