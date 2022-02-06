from multiprocessing import managers
from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction

from forms_app.serializers import FormTemplateSerializer, FormFieldSerializer
from forms_app.models import FormTemplate, FormField

class form_template(APIView):

    def get(self, request, form_template_id):
        try:
            form_template = FormTemplate.objects.get(form_template_id=form_template_id)
        except FormTemplate.DoesNotExist:
            return Response(data={"erorr": "Form Templates Doesn't Exist :("}, status=status.HTTP_400_BAD_REQUEST)

        form_fields = form_template.form_fields.all()
        form_fields_serializers = FormFieldSerializer(form_fields, many=True)
        data = {
            "form_template_id": form_template_id,
            "form_name": form_template.form_name,
            "form_fields": list(form_fields_serializers.data)
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request, form_template_id):
        try:
            form_template = FormTemplate.objects.get(form_template_id=form_template_id)
        except FormTemplate.DoesNotExist:
            return Response(data={"erorr": "Form Templates Doesn't Exist :("}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        try:
            with transaction.atomic():
                # Updating the form name
                form_name = data.get("form_name")
                serializer = FormTemplateSerializer(form_template, data={"form_name": form_name}, partial=True)
                if(serializer.is_valid()):
                    serializer.save()
                else:
                    # Raising error to restore db to original entries
                    raise ValidationError("Invalid Data")
                
                '''
                Updating the form fields
                Here all the previous field entries will be deleted and 
                the current entries will be saved
                '''
                previous_form_fields = form_template.form_fields.all()
                # Deleting all previous field entries
                previous_form_fields.delete()

                 # Getting new form field details from list
                form_fields_list = data.get("form_fields")
                # Adding form_template_id to every fields dictionary
                for field in form_fields_list:
                    field["form_template"] = form_template_id
                serializers = FormFieldSerializer(data=form_fields_list, many=True)
                if(serializers.is_valid()):
                    serializers.save()
                    return Response(data="Form Template Updated Successfully", status=status.HTTP_201_CREATED)
                
                # Raising error to restore db to original entries
                raise ValidationError("Invalid Data")

        except Exception as e:
            return Response(data={"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, form_template_id):
        try:
            form_template = FormTemplate.objects.get(form_template_id=form_template_id)
        except FormTemplate.DoesNotExist:
            return Response(data={"erorr": "Form Templates Doesn't Exist :("}, status=status.HTTP_400_BAD_REQUEST)
        
        form_template.delete()
        return Response(data={"Form Template Deleted!"}, status=status.HTTP_200_OK)


class form_templates_list(APIView):

    def get(self, request):
        form_templates = FormTemplate.objects.all()
        serializers = FormTemplateSerializer(form_templates, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        try:
            # Retrieving form name and saving the form template instance
            form_name = data.get("form_name")
            form_template = FormTemplate(form_name=form_name)
            form_template.save()
            
            # Getting form field details from list
            form_fields_list = data.get("form_fields")
            # Adding form_template_id to every fields dictionary
            for field in form_fields_list:
                field["form_template"] = form_template.form_template_id
            serializers = FormFieldSerializer(data=form_fields_list, many=True)
            if(serializers.is_valid()):
                serializers.save()
                return Response(data="Form Template Created Successfully", status=status.HTTP_201_CREATED)
            
            # Deleting the form just created
            form_template.delete()
            # Returning Bad Request
            return Response(data={"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)




