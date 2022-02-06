from django.urls import path
from forms_app import views

app_name = 'forms_app'
urlpatterns = [
    path('form/<int:form_template_id>', views.form_template.as_view(), name='form'),
    path('forms', views.form_templates_list.as_view(), name='forms'), 
    path('form_entry/<int:form_entry_id>', views.form_entry.as_view(), name="form_entry"),
    path('form_entries/<int:form_template_id>', views.form_entries_list.as_view(), name="form_entries"),  
]