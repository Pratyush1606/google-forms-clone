from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction

from forms_app.serializers import FormTemplateSerializer, FormFieldSerializer, FormEntrySerializer, FormFieldAnswerSerializer
from forms_app.models import FormTemplate, FormField, FormEntry, FormFieldAnswer

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

class form_entry(APIView):

    def get(self, request, form_entry_id):
        try:
            form_entry = FormEntry.objects.get(form_entry_id=form_entry_id)
        except FormEntry.DoesNotExist:
            return Response(data={"erorr": "Form Entry Doesn't Exist :("}, status=status.HTTP_400_BAD_REQUEST)

        # Getting form entry field answers
        field_data = {}
        fields_answers = form_entry.form_answers.all()
        for field_answer in fields_answers:
            curr_field_name = field_answer.form_field.field_name
            curr_field_answer = field_answer.answer
            field_data[curr_field_name] = curr_field_answer
        
        # Making combined data
        data = {
            "form_entry_id": form_entry_id,
            "form_name": form_entry.form_template.form_name,
            "form_field_answers": field_data
        }
        return Response(data=data, status=status.HTTP_200_OK)

class form_entries_list(APIView):

    def get(self, request, form_template_id):
        try:
            form_template = FormTemplate.objects.get(form_template_id=form_template_id)
        except FormTemplate.DoesNotExist:
            return Response(data={"erorr": "Form Templates Doesn't Exist :("}, status=status.HTTP_400_BAD_REQUEST)
        
        form_entries = form_template.form_entries.all()
        serializers = FormEntrySerializer(form_entries, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, form_template_id):
        try:
            form_template = FormTemplate.objects.get(form_template_id=form_template_id)
        except FormTemplate.DoesNotExist:
            return Response(data={"erorr": "Form Templates Doesn't Exist :("}, status=status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        try:
            # Getting form entry answers
            form_field_answers = data.get("form_field_answers")
            # Making a Form Entry Instance
            serializer = FormEntrySerializer(data={"form_template": form_template_id})
            if(serializer.is_valid()):
                serializer.save()
                form_entry = FormEntry.objects.get(form_entry_id=serializer.data.get("form_entry_id"))
            else:
                return Response(data={"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
            # Making the answers entries
            data = []
            for curr_ans in form_field_answers:
                for form_field_name, form_field_answer in curr_ans.items():
                    try:
                        # Getting the respective field_id corresponding to this curr_form_field
                        form_field = FormField.objects.get(field_name=form_field_name, form_template=form_template_id)
                        data.append({
                            "answer": form_field_answer,
                            "form_entry": form_entry.form_entry_id,
                            "form_field": form_field.field_id
                        })
                    except Exception as e:
                        # Deleting the newly created form entry and returning invalid data
                        form_entry.delete()
                        return Response(data={"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Saving the answers
            serializers = FormFieldAnswerSerializer(data=data, many=True)
            if(serializers.is_valid()):
                serializers.save()
                return Response(data="Form Entry Created Successfully", status=status.HTTP_201_CREATED)
            
            # Deleting the newly created form entry and returning invalid data
            form_entry.delete()
            return Response(data={"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

