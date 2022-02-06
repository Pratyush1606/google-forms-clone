from statistics import mode
from django.db import models

# Create your models here.
class FormTemplate(models.Model):
    form_id = models.BigAutoField(primary_key=True, editable=False)
    form_name = models.CharField(max_length=100)

class FormField(models.Model):
    field_id = models.BigAutoField(primary_key=True, editable=False)
    field_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    options = models.CharField(max_length=100, null=True)
    mandatory = models.CharField(max_length=100)
    form_template = models.ForeignKey(to=FormTemplate, related_name="form_fields", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('field_name', 'form_template',)




