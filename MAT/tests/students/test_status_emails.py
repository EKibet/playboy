import time
from django.urls import reverse
from django.core import mail
import pytest
from MAT.apps.students.utils import send_mass_status_mail
from MAT.apps.authentication.models import CohortMembership

class TestStatusEmails():
    @pytest.mark.django_db
    def test_send_status_emails_successfully(self, client,new_tm, file_data,get_or_create_token,wrong_file_data,email_backend_setup,new_cohort,key_errored_related_file_data):
        new_cohort.save()
        token = get_or_create_token
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        file_data2=file_data
        headers = {
            'HTTP_CONTENT_TYPE':'multipart/form-data'
        }
        key_errored_data={
            'file':key_errored_related_file_data['file'],
        }        
        data={
            'file':file_data['file'],
            'cohort_id':new_cohort.id,
        }
        key_error_response = client.post(reverse('students:send_status_emails'),key_errored_data, **headers)
        type_error_response = client.post(reverse('students:send_status_emails'),wrong_file_data, **headers)            
  
        response = client.post(
            reverse('students:send_status_emails'), data, **headers)        
        file_error_response = client.post(reverse('students:send_status_emails'),  **headers)            
        assert key_error_response.status_code == 400       
        assert type_error_response.status_code == 400       
        assert file_error_response.status_code == 400   
        assert response.status_code==200    
        time.sleep(1)
        assert len(mail.outbox) == 3
    def test_can_send_final_list_emails_successfully(self, client, file_data,get_or_create_token,wrong_file_data,email_backend_setup,new_cohort,key_errored_related_file_data):
        token = get_or_create_token
        new_cohort.save()

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        headers = {
            'HTTP_CONTENT_TYPE':'multipart/form-data'
        }        
        
        
        key_errored_data={
            'file':key_errored_related_file_data['file'],
            'next_module':'Django'            
        } 
        data={
            'file':file_data['file'],
            'cohort_id':new_cohort.id,
            'next_module':'Django'

                }
        
        
        response = client.post(
            reverse('students:send_final_status_emails'), data, **headers)
        file_error_response = client.post(reverse('students:send_final_status_emails'),  **headers)            
        key_error_response = client.post(reverse('students:send_final_status_emails'),key_errored_data, **headers)
        type_error_response = client.post(reverse('students:send_final_status_emails'),wrong_file_data, **headers)            
        
        assert key_error_response.status_code == 400   
        assert response.status_code==200    
        assert type_error_response.status_code == 400       
        assert file_error_response.status_code == 400       
        time.sleep(1)
        assert len(mail.outbox) == 3
