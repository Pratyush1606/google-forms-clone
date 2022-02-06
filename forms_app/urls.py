from django.urls import path
from forms_app import views

app_name = 'forms_app'
urlpatterns = [
    path("form/<int:form_template_id>", views.form_template.as_view(), name="form"),
    path("forms", views.form_templates_list.as_view(), name="forms"),    
]