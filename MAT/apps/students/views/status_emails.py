import csv
import io
import os
from smtplib import SMTPException, SMTPServerDisconnected

import pandas as pd
from django.core.mail import EmailMultiAlternatives, get_connection, send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from MAT.apps.authentication.models import CohortMembership
from MAT.config.settings.base import env

from ..utils import send_mass_status_mail

from_email=os.getenv('FROM_EMAIL')
def process_final_list(records,next_module=None,cc_list=None):
        """
        Utility function for constructing mail message details according
        to the recommendation status of each student. 
        It then calls send_mass_status_mail function 
        which sends each mail message to its corresponding recipient. 

            Parameters:
                1. pandas dataframe
                2. next_module
        """
        mailing_list=[]
        result ={"success":False,
                "status":''
                }        
       
        for index,row in records.iterrows(): 
            dynamic_data={
            'username': row['Student'].replace(',',''),
            'next_module':next_module,
            'reasons':row.get('Reason','')
            }   
            if row['Final Recommendation'] == '' or row['Final Recommendation'].lower() == 'yes':
                pass_html_message = render_to_string('full_acceptance_email_template.html', dynamic_data)
                mailing_list.append( ('Congratulations! Passing to Next Phase - [attendance, completion, interpersonal, quality] Condition', '.', pass_html_message,from_email,[row['Email']],cc_list))
            elif row['Final Recommendation'].lower()=='no':
                failed_html_message = render_to_string('not_passing_email_template.html', dynamic_data)
                mailing_list.append( ('Not Passing to the Next Phase - [attendance, completion, quality, interpersonal]', '.', failed_html_message,from_email,[row['Email']],cc_list))            
            elif row['Final Recommendation'].lower()=='probation':
                probation_html_message = render_to_string('probation_email_template.html', dynamic_data)
                mailing_list.append( ('Passing to Next Phase - Probation', '.', probation_html_message,from_email,[row['Email']],cc_list))            

        datatuple=tuple(mailing_list)
        try:
            send_mass_status_mail(datatuple)
            result['success']=True
            result['status']=status.HTTP_200_OK

            return result
 
        except SMTPServerDisconnected as disconnected:
            result.update({'errors':[f'{str(disconnected)}']})
            result['status']=status.HTTP_403_FORBIDDEN
            return result  
        except SMTPException as smtp:
            result.update({'errors':[f'{str(smtp)}']})
            result['status']=status.HTTP_403_FORBIDDEN
            return result                   

def get_ip_specifics(columns):
    """
    Utility function for dynamically picking IP name and total marks for each IP
    from the spreadsheet.
    Parameters:
        1. list of all columns/labels in the dataframe
    """
    ip_specifics,ips={},[]
    for key in columns:
        if 'ip' in key.lower():
            split_key=key.split('/')
            ip_specifics.update({split_key[0]:int(split_key[1])})
            ips.append(key)
    return {'ip_specifics':ip_specifics,'ips':ips}

def process_module_status_list(records,cc_list=None):
        """
        Utility function for constructing mail message details according
        to the recommendation status of each student. 
        It then calls send_mass_status_mail function 
        which sends each mail message to its corresponding recipient. 

            Parameters:
                1. pandas dataframe
        """
        mailing_list=[]
        ip_specifics=get_ip_specifics(records.columns.tolist())
        result ={"success":False,
                "status":''
                }
        
        for index,row in records.iterrows(): 
            dynamic_data={
                'username': row['Student'].replace(',',''),
                'attendance':row.get('Attendance'),
                'ips':ip_specifics.get('ip_specifics'),
                'scores':{ip_no.split('/')[0]:row[ip_no] for ip_no in ip_specifics.get('ips') },
                'improvements':row.get('Reason','')
            }              
            if row['Status Recommendation'] == '' or row['Status Recommendation'].lower() == 'yes':   
                pass_html_message = render_to_string('on_track_template.html',dynamic_data)
                mailing_list.append( ('A Quick status Update!', '.', pass_html_message,from_email,[row['Email']],cc_list))
            elif row['Status Recommendation'].lower()=='no':
                not_on_track_html_message = render_to_string('not_on_track_template.html',dynamic_data )
                mailing_list.append( ('A Quick status Update!', '.', not_on_track_html_message,from_email,[row['Email']],cc_list))         

        datatuple=tuple(mailing_list)
        try:
            send_mass_status_mail(datatuple) 
            result['success']=True
            result['status']=status.HTTP_200_OK
            return result
        except SMTPServerDisconnected as disconnected:
            result.update({'errors':[f'{str(disconnected)}']})
            result['status']=status.HTTP_403_FORBIDDEN
            return result  
        except SMTPException as smtp:
            result.update({'errors':[f'{str(smtp)}']})
            result['status']=status.HTTP_403_FORBIDDEN
            return result              

class FinalListEmail(APIView):
    """
    Endpoint for sending final list status emails.
    Parameters:
    1. csv file - preferebly in form data format(file)
    2. next_module - name of next cohort module.(str)
    3. cohort - name of cohort(str)

    """
    parser_classes = (MultiPartParser,)

    def post(self,request,format=None):
        try:
            file_object = request.FILES['file']
            dataframe = pd.read_csv(io.StringIO(file_object.read().decode('utf-8')), delimiter=',')
            dataframe.dropna(axis='index',how='all',subset=['Email'],inplace=True)
            dataframe.dropna(axis='columns',how='all',inplace=True)
            cohort_list = CohortMembership.objects.filter(cohort__id=int(request.data.get('cohort_id'))) 
            cc_list=[cohort.user for cohort in cohort_list]
            response=process_final_list(dataframe,request.data['next_module'],cc_list)               
        except TypeError as t_error:
            response={}
            response.update({"type_error":f"{t_error}"})  
            response.update({"status":status.HTTP_400_BAD_REQUEST})  

        except KeyError as file_error:
            response={}
            response.update({"file_error":f"{file_error}"})  
            response.update({"status":status.HTTP_400_BAD_REQUEST})  

        return Response(response,status=response.get('status'))

class StatusEmail(APIView):
    """
    Endpoint for sending mid-module status emails.
    Parameters:
    1. csv file - preferebly in form data format(file)
    2. cohort - name of cohort(str)
    """  
    parser_classes = (MultiPartParser, )
    

    def post(self,request,format=None):
        response=None
        try:
            file_object = request.FILES['file']
            dataframe = pd.read_csv(io.StringIO(file_object.read().decode('utf-8')), delimiter=',')            
            dataframe.dropna(axis='index',how='all',subset=['Email'],inplace=True)
            dataframe.dropna(axis='columns',how='all',inplace=True)
            cohort_list = CohortMembership.objects.filter(cohort__id=int(request.data.get('cohort_id'))) 
            cc_list=[cohort.user for cohort in cohort_list]            
            response=process_module_status_list(dataframe,cc_list)
        except TypeError as t_error:
            response={}
            response.update({"type_error":f"{t_error}"})  
            response.update({"status":status.HTTP_400_BAD_REQUEST})  

        except KeyError as file_error:
            response={}
            response.update({"file_error":f"{file_error}"})  
            response.update({"status":status.HTTP_400_BAD_REQUEST})  
        return Response(response,status=response.get('status'))
        
