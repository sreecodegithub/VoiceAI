from dataclasses import replace
import json
import os
from subprocess import CREATE_DEFAULT_ERROR_MODE
from typing import Text
from django.db.models.fields import DateField
from django.db.models.functions.comparison import Cast
from django.db.models.query import InstanceCheckMeta
from django.http.request import HttpHeaders
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
import requests
from requests import api
from requests.api import request
# from requests.models import Request
from .userclass import Administrator_User, Standard_User
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, timedelta
import datetime
import time
from .models import *
from django.db.models import Count, Sum, Avg, Max, Min
from django.http import HttpResponseRedirect
import re
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from dashboard import userclass
from django.forms import ModelForm
from . forms import SMSUserForm
from twilio.rest import Client 
 


   
#authorize api and get access token
def getAccessToken():
    strPassword ='password'
    payload = {'client_id':client_id,'client_secret':client_secret,'username':auth_id,'password':auth_secret,'grant_type':strPassword}
    response = requests.post("https://api.dubber.net/"+region+"/v1/token", params=payload)
    return response

def getDubPoints(request):
    try:
        apiDB = DubberAPIToken.objects.all().first()
        region = apiDB.region
        account_id = apiDB.account_id
        payload ={'count': '100'}
        response = requests.get("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/dub_points", headers={"Authorization":"Bearer "+access_token},params= payload)
    except:
        x= 10
    finally:
        return response  

def getAccountInfo():
    response = ""
    try:
        apiDB = DubberAPIToken.objects.all().first()
        region = apiDB.region
        access_token=apiDB.accessToken
        response = requests.get("https://api.dubber.net/"+region+"/v1/profile",headers={"Authorization":"Bearer "+access_token})
    except:
        x= 10
    finally:
        return response  

def getAdminUsers(request):
    try:    
        apiDB = DubberAPIToken.objects.all().first()
        region = apiDB.region
        account_id = apiDB.account_id
        access_token=apiDB.accessToken
        payload ={'role': 'Administrator','count':'100'}
        response = requests.get("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/users", headers={"Authorization":"Bearer "+access_token},params= payload)
    except:
        x= 10
    finally:
        return response  

def getStandardUsers(request):
    apiDB = DubberAPIToken.objects.all().first()
    region = apiDB.region
    account_id = apiDB.account_id
    access_token=apiDB.accessToken
    payload ={'role': 'Standard%20User','count':'100'}
    response = requests.get("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/users", headers={"Authorization":"Bearer "+access_token},params= payload)
    return response  

def get_csv_dwnld_link(from_date,to_date):
    apiDB = DubberAPIToken.objects.all().first()
    region = apiDB.region
    account_id = apiDB.account_id
    access_token=apiDB.accessToken    
    body_data = {'from_date':from_date,
            'to_date':to_date}
            #
    response = requests.post("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/data_exports", headers={"Authorization":"Bearer "+access_token,"Content-Type":"application/json","X-Date-Format":"ISO8601"},data= json.dumps(body_data) )
    #time.sleep(30)
    return response
def get_accessTokenDetailsfromDB():
    accessTokenDetails  = DubberAPIToken.objects.all()
    return accessTokenDetails

#def addSecs(tm, secs):
    #fulldate = datetime.datetime(datetime.date.year., datetime.date.month, datetime.date.day, tm.hour, tm.minute, tm.second)
    #fulldate = fulldate + datetime.timedelta(seconds=secs)
    #return fulldate

def getRecordingURL(request,recordingID):
 
    apiDB = DubberAPIToken.objects.all().first()
    region = apiDB.region
    access_token=apiDB.accessToken
    payload ={'listener': ''}
    response = requests.get("https://api.dubber.net/"+region+"/v1/recordings/"+str(recordingID), headers={"Authorization":"Bearer "+access_token},params= payload)
    return response  



def getRecordingAIInfo(request,recordingID):
 
    apiDB = DubberAPIToken.objects.all().first()
    region = apiDB.region
    access_token=apiDB.accessToken
    account_id = apiDB.account_id
    response =  requests.get("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/recordings/"+str(recordingID)+"/ai", headers={"Authorization":"Bearer "+access_token})
    return response  


def getRegionandAccessToken():
    apiDB = DubberAPIToken.objects.all().first()
    print(apiDB)
    access_token = apiDB.accessToken
    print(access_token)
 


# Create your views here.
def home(request):
    return render(request,'dashboard/api_login.html')

def account_info(request):
        response = getAccountInfo()
        account_json = response.json()
        return render(request,'dashboard/account_info.html',{'account_json':account_json,'page_name':'Account Information'})

def api_token_info(request):
    apiDB = DubberAPIToken.objects.get(number=1)
    access_token =apiDB.accessToken 
    refresh_token= apiDB.refreshToken
    token_expiry=apiDB.tokenExpiry
    return render(request,'dashboard/api_token_info.html',{'access_token':access_token,'token_expiry':token_expiry,'refresh_token':refresh_token})

def api_login(request):
    
    global region,account_id,auth_id,auth_secret,client_id,client_secret,accessToken
    if request.method == 'POST':
        region = request.POST.get('region')
        account_id = request.POST.get('account_id')
        auth_id = request.POST.get('auth_id')
        auth_secret = request.POST.get('auth_secret')
        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')

        # request.session['region'] = region
        # request.session['auth_id'] = auth_id
        # request.session['auth_secret'] = auth_secret
        # request.session['client_id'] = client_id
        # request.session['client_secret'] = client_secret
        # request.session['account_id'] = account_id
        global access_token, token_expiry , refresh_token ,user_context
  
        response = getAccessToken()
        if response.ok == True:
            json_response = response.json()
            
            access_token = str(json_response["access_token"])
            token_expiry = int(json_response["expires_in"])
            refresh_token = str(json_response["refresh_token"])
            user_context = str(json_response["user_context"])
            


            # request.session['access_token'] = access_token
            # request.session['token_expiry'] = token_expiry
            # request.session['refresh_token'] = refresh_token
            # request.session['user_context'] = user_context
    
            apiDB = DubberAPIToken.objects.count()
            if( apiDB < 1):
                apiDB = DubberAPIToken(number=1,accessToken=access_token,refreshToken=refresh_token,tokenExpiry=token_expiry,region=region,auth_id=auth_id,auth_secret=auth_secret,client_id=client_id,client_secret=client_secret,account_id=account_id)
                apiDB.save()
            else:
                apiDB = DubberAPIToken.objects.get(number=1)
                apiDB.accessToken = access_token
                apiDB.refreshToken= refresh_token
                apiDB.tokenExpiry=token_expiry
                apiDB.region = region
                apiDB.auth_id=auth_id
                apiDB.auth_secret=auth_secret 
                apiDB.client_id = client_id 
                apiDB.client_secret = client_secret
                apiDB.account_id=account_id
                apiDB.save()

            return render(request,'dashboard/api_token_info.html',{'access_token':access_token,'token_expiry':token_expiry,'refresh_token':refresh_token,'user_context':user_context,'page_name':'API Token Information'})
        else:
            error_msg = response.text
            posted_url = response.url
            return render(request,'dashboard/api_login_failed.html',{'error_msg':error_msg,'posted_url':posted_url})

    else:
         return render(request,'dashboard/api_login_failed.html')


def license_detail(request):
        response = getDubPoints(request)
        json_response = response.json()['dub_points']
        index = len(json_response)
        totalDUBPoints = index
        totalActiveDUBPoints = 0
        totalSuspendedDUBPoints = 0
        totalTypeRecorderDUBPoints=0
        totalTypeAPIDUBPoints =0
        totalTypeMeetingDUBPoints =0
        totalAIDUBPoints = 0
        totalNonAIDUBPoints =0
        for i in range(0,index):
            #Check for Type
            if(json_response[i]["type"] == "Recorder"):
                totalTypeRecorderDUBPoints = totalTypeRecorderDUBPoints + 1
            elif(json_response[i]["type"] == "Api"):
                totalTypeAPIDUBPoints = totalTypeAPIDUBPoints + 1
            elif(json_response[i]["type"] == "Meeting"):
                totalTypeMeetingDUBPoints = totalTypeMeetingDUBPoints + 1
            #Check for Status
            if(json_response[i]["status"] == "Active"):
                totalActiveDUBPoints = totalActiveDUBPoints + 1
            else:
                totalSuspendedDUBPoints = totalSuspendedDUBPoints + 1
            #Check fo AI
            if(json_response[i]["ai"] == True):
                totalAIDUBPoints = totalAIDUBPoints + 1
            else:
                totalNonAIDUBPoints = totalNonAIDUBPoints + 1

        DUB_TotalDUBPoints = totalDUBPoints
        DUB_ActiveDUBPoints = totalActiveDUBPoints
        DUB_SuspendedDUBPoints = totalSuspendedDUBPoints
        DUB_RecorderDUBPoints = totalTypeRecorderDUBPoints
        DUB_APIDUBPoints = totalTypeAPIDUBPoints
        DUB_MeetingDUBPoints = totalTypeMeetingDUBPoints
        DUB_AIDUBPoints = totalAIDUBPoints
        DUB_NonAIDUBPoints = totalNonAIDUBPoints

        labels = []
        data = []    

        labels.append("Active")
        data.append(DUB_ActiveDUBPoints)

        labels.append("Suspended")
        data.append(DUB_SuspendedDUBPoints)

        LicenseTypelabels = []
        LicenseTypedata = []    

        LicenseTypelabels.append("Recorder")
        LicenseTypedata.append(DUB_RecorderDUBPoints)

        LicenseTypelabels.append("API")
        LicenseTypedata.append(DUB_APIDUBPoints)
        
        LicenseTypelabels.append("Meeting")
        LicenseTypedata.append(DUB_MeetingDUBPoints)
       
        return render(request,'dashboard/license_detail.html',{'page_name':'License','DUB_TotalDUBPoints':DUB_TotalDUBPoints,'DUB_ActiveDUBPoints':DUB_ActiveDUBPoints,'DUB_SuspendedDUBPoints':DUB_SuspendedDUBPoints,'DUB_RecorderDUBPoints':DUB_RecorderDUBPoints,'DUB_APIDUBPoints':DUB_APIDUBPoints,'DUB_MeetingDUBPoints':DUB_MeetingDUBPoints,'DUB_AIDUBPoints':DUB_AIDUBPoints,'DUB_NonAIDUBPoints':DUB_NonAIDUBPoints,'data':data,'labels':labels,'LicenseTypelabels':LicenseTypelabels,'LicenseTypedata':LicenseTypedata,'page_name':'License Dashboard'})

def admin_user(request):
    response = getAdminUsers(request)
    admin_user_json = response.json()['users']

    page = request.GET.get('page', 1)
    paginator = Paginator(admin_user_json, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'dashboard/admin_user.html',{'users':users,'page_name':'Administrator User Information'})

def standard_user(request):
    response = getStandardUsers(request)
    standard_user_json = response.json()['users']
    page = request.GET.get('page', 1)
    paginator = Paginator(standard_user_json, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'dashboard/standard_user.html',{'users':users,'page_name':'Standard User Information'})

def data_export_csv(request):


    if request.method == 'POST':
        from_date = request.POST.get('from_date')+" 11:22:03"
        to_date = request.POST.get('to_date')+" 11:22:03"
        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        fdt_year = from_date.year
        fdt_month = from_date.month
        fdt_day = from_date.day


        to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S")
        tdt_year = to_date.year
        tdt_month = to_date.month
        tdt_day = to_date.day
        f_date = date(fdt_year,fdt_month,fdt_day)
        t_date = date(tdt_year,tdt_month,tdt_day)
        day_duration = t_date - f_date
        if(day_duration.days > 30):
            error_msg ='Please enter a value between 1 and 30 days'
       
            return render(request,'dashboard/data_export_csv.html',{'page_name':'Data Export','error_msg':error_msg})
        else:
            #"from_date": "2020-06-09T00:00:00+01:00",
	        #"to_date": "2020-07-09T10:30:00+01:00"
    
            fn_from_date = f_date.isoformat()+'T00:00:00+01:00'
            fn_to_date = t_date.isoformat()+'T10:30:00+01:00'
            response = get_csv_dwnld_link(fn_from_date,fn_to_date)
            json_response = response.json()
            report_status = json_response['status']
            report_id = json_response['id']
            if(report_status == 'Active'):
                export_url = json_response['export_url']
                return render(request,'dashboard/download_csv.html',{'page_name':'Data Export','export_url':export_url})
            else:
                while(report_status=='Pending'):
                    response = requests.get("https://api.dubber.net/"+'sandbox'+"/v1/"+"data_exports/"+report_id, headers={'Content-Type':'application/json', "Authorization":"Bearer "+access_token })
                    json_response = response.json()
                    report_status = json_response['status']
                    time.sleep(2)
                export_url = json_response['export_url']
                return render(request,'dashboard/download_csv.html',{'page_name':'Data Export','export_url':export_url})
                
    else:
        return render(request,'dashboard/data_export_csv.html',{'page_name':'Data Export'})


def bulkdownload_calls(request):

   if request.method == 'POST':
        folder_path = request.POST.get('folder_path')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        dubberfiles = DubberCallRecording.objects.filter(startDate__gte=from_date,startDate__lte=to_date)
        record_count = dubberfiles.count() * 3
        if record_count == 0:
            error_msg="Sorry no call recordings are found for the period selected"
            return render(request,'dashboard/bulkdownload_calls.html',{'page_name':'Bulk Download of Calls',"error_msg":error_msg})
        recordingID=""
        for record in dubberfiles:
            recordingID = record.recordingID
            recording_date = record.startDate.strftime("%m/%d/%Y").replace('/','_')
            recording_time=record.startTime.replace(':','_')
            extension = record.recordingChannel
            customFileName=str(recording_date)+"_"+recording_time+"_"+extension+"_"+str(recordingID)
            
            time.sleep(2)
            #getmp3file
            response = getRecordingURL(request,recordingID)
            recording_url = response.json()['recording_url']
            r = requests.get(recording_url, stream=True)
            abs_filename = folder_path+"\\"+ str(customFileName) +".mp3"
            if r.ok:
                print("saving to", os.path.abspath(folder_path))
                with open(abs_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            os.fsync(f.fileno())
            else:  # HTTP status code 4XX/5XX
                print("Download failed: status code {}\n{}".format(r.status_code, r.text))
            #getmetadata
            metadatafile = folder_path+"\\"+ str(customFileName)+".dat"
            with open(metadatafile, 'w') as outfile:
                json.dump(response.json(), outfile, indent=4)

            #getAIdata
            try:
                time.sleep(2)
                response =  getRecordingAIInfo(request,recordingID)
                ai_jsondata = response.json()
                aifile = folder_path+"\\"+ str(customFileName)+".ai"
                with open(aifile, 'w') as outfile:
                    json.dump(ai_jsondata, outfile, indent=4)
            except:
                x=0

        return render(request,'dashboard/bulkdownload_detail.html',{'page_name':'Download details',"record_count":record_count,"folder_path":folder_path})
   else:
        return render(request,'dashboard/bulkdownload_calls.html',{'page_name':'Bulk Download of Calls'})

def calldetailrecord(request):
    cdr_table = DubberCallRecording.objects.all().order_by('-startDate')
    return render(request, 'dashboard/call_detail_table.html',{"cdr_table":cdr_table})

def smsUser_list_view(request):
    smsUserTable = DubberSMSNotificationList.objects.all()
    return render(request, "dashboard/smsUser_list_view.html", {"smsUserTable":smsUserTable})

def smsUser_create_view(request):
    # dictionary for initial data with
    # field names as keys
 
    # add the dictionary during initialization
    form = SMSUserForm(request.POST or None)
    try:
        if form.is_valid():
            form.save()
            return redirect("smsUser_list_view")
    except:
         print("error")
    return render(request, "dashboard/smsUser_create_view.html",{"form":form})

# update view for details
def smsUser_update_view(request, id):
     item = DubberSMSNotificationList.objects.get(id=id)
     form = SMSUserForm(request.POST or None,instance=item)

     if form.is_valid():
         form.save()
         return redirect("smsUser_list_view")
     return render(request,"dashboard/smsUser_update_view.html",{"form":form,"item":item})

# delete view for details
def smsUser_delete_view(request, id):
    # dictionary for initial data with
    # field names as keys
 
    # fetch the object related to passed id
    obj = get_object_or_404(DubberSMSNotificationList, id = id)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("smsUser_list_view")
 
    return render(request, "dashboard/smsUser_delete_view.html", {"obj":obj})

@csrf_exempt
def webhook_listener(request):
    print(request)
    byteformat = request.body
    requestInfo =  json.loads(byteformat)
    headers = request.headers

    #Webook Registration
    str_X_Hook_Secret ="X-Hook-Secret"
    str_notification_url="notification_url"
    str_event_type="event_type"
    str_resource_url ="resource_url"
    if(str_X_Hook_Secret in headers ):
        str_value = str(headers[str_X_Hook_Secret])
        dubberWebhookIDandSecret = DubberWebhookIDandSecret(notificationURL=requestInfo,X_Hook_Secret=str_value,createdDate=datetime.datetime.now())
        dubberWebhookIDandSecret.save()
        return HttpResponse(status=200)
    elif(str_notification_url in requestInfo):
        notificationURL_value = str(requestInfo[str_notification_url])
        eventType_value=requestInfo[str_event_type]
        resource_url_value=str(requestInfo[str_resource_url])
        dubberWebhookNotification = DubberWebhookNotification(notificationURL=notificationURL_value,eventType=eventType_value,resourceURL=resource_url_value,createdDate=datetime.datetime.now())
        dubberWebhookNotification.save()
        showWebhookNotification(request,resource_url_value)
    return HttpResponse(status=200)


def showWebhookNotification(request,resourceURL):
    print(resourceURL)
    splitURL = resourceURL.split('/')
    print(splitURL)
    recordingID = splitURL[6]
    print (recordingID)
    response = getRecordingURL(request,recordingID)
    print(response)
    jsondata = response.json()  
    if(jsondata["call_type"] != "meeting"):
        call_from = jsondata["from"]
        call_to = jsondata["to"]
    
    recording_id = jsondata["id"]
    call_type = jsondata["call_type"]
    recording_dubpointid = jsondata["dub_point_id"]
    unformatted_time = jsondata["start_time"]
    regex =re.compile("\d{2}:\d{2}:\d{2}")
    call_start_time = regex.findall(unformatted_time)[0]
    temp_datetime =  unformatted_time

    regex= re.compile("\d{2}\s\D{3}\s\d{4}")
    call_start_date = regex.findall(temp_datetime)[0]
    call_start_date = datetime.datetime.strptime(call_start_date, '%d %b %Y').date()
    call_duration = jsondata["duration"]
    recording_channel = jsondata["channel"]
    recording_held =  jsondata["held"]
    recording_type = jsondata["type"]


#get ai and speech to text transcription details of the recording
#get tone info
#sleep for 2 second
    time.sleep(2)
    try:
        http_aireq =  requests.get("https://api.dubber.net/"+region+"/v1/accounts/"+account_id+"/recordings/"+recording_id+"/ai", headers={"Authorization":"Bearer "+access_token})
        ai_jsondata = http_aireq.json()
        nAnalytical = ai_jsondata["document_emotion"]["analytical"]
        nAnger = ai_jsondata["document_emotion"]["anger"]
        nConfident = ai_jsondata["document_emotion"]["confident"]
        nFear = ai_jsondata["document_emotion"]["fear"]
        nJoy = ai_jsondata["document_emotion"]["joy"]
        nSadness = ai_jsondata["document_emotion"]["sadness"]
        nTentative = ai_jsondata["document_emotion"]["tentative"]

#get overall sentiment
        nSentiment = ai_jsondata["document_sentiment"]
    
        if(-1 <= nSentiment <= -.1):
            sentiment_text = "Negative"
        elif (-.1 <= nSentiment <= 1):
            sentiment_text ="Neutral"
        else:
            sentiment_text="Positive"

#get speech to text transcription
        nSpeechlength = len(ai_jsondata["sentences"])
        recording_transcription = ""
        for i in range(0, nSpeechlength):
            temptext = ai_jsondata["sentences"][i]["content"]
            recording_transcription = recording_transcription +" "+">"+" "+ temptext +"\n\n"
        
        time.sleep(2)

    except:
        print("No AI information")
        #nAnalytical,nAnger,nConfident,nFear,nSadness,nJoy,nSentiment,nTentative = "0","0","0","0","0","0","0","0"
        #Transcription, sentiment_text = "",""
        #nSpeechlength = len(ai_jsondata["sentences"])
        #for i in range(0, nSpeechlength):
            #temptext = ai_jsondata["sentences"][i]["content"]
            #Transcription = Transcription +" "+">"+" "+ temptext +"\n\n"

    #insert data into Dubber DB callrecording table

    # dubbercallrecordingtable = DubberCallRecording(recordingID=recording_id,callFrom=call_from,callTo=call_to,callType=call_type,startDate=call_start_date,startTime=call_start_time,callDuration=call_duration,recordingChannel=recording_channel,held=recording_held,interactionType= recording_type,dubPointID=recording_dubpointid,transcription=recording_transcription,sentiment=sentiment_text,createdDate=datetime.datetime.now(),anger=nAnger,confident=nConfident,fear=nFear,sadness=nSadness,joy=nJoy,analytical=nAnalytical,tentative=nTentative)
    # dubbercallrecordingtable.save()
    return redirect(request,'dashboard/webhookNotification.html',{'callType':call_type,'recording_channel':recording_channel,'call_start_time':call_start_time})

    print("Data saved successfully")


def SendSMS(request,id):
    account_sid = ''#twilio api
    auth_token = '' #twilio api
    client = Client(account_sid, auth_token) 
    cdrDB = DubberCallRecording.objects.get(recordingID=id)
    cdrDate = cdrDB.startDate.strftime("%m/%d/%Y")
    cdrTime =cdrDB.startTime
    cdrFrom=cdrDB.callFrom
    cdrTo=cdrDB.callTo
    cdrSentiment=cdrDB.sentiment
    smsContent = "Voice AI Alert: Call Recording "+ "Date: "+cdrDate+" Time: "+cdrTime+" From: "+cdrFrom+" To: "+cdrTo+" Sentiment: "+cdrSentiment

    smsDB = DubberSMSNotificationList.objects.all()
    for rec in smsDB:
        if(rec.active == True):
            try:
                message = client.messages.create(  
                                    messaging_service_sid='', #twilio api
                                    body=smsContent,      
                                    to=rec.smsNumber,
                                ) 
            except:
                    return render(request,'dashboard/sms_status.html',{'smsContent':'Message sending failed'})

    return render(request,'dashboard/sms_status.html',{'smsContent':smsContent})
  


def PerformanceDashboard(request):
    #number of recordings
    cdrDB = DubberCallRecording.objects.all()
    cdrCount = cdrDB.count()

    #number of inbound calls
    cdrDB = DubberCallRecording.objects.filter(callType='inbound')
    cdrIBCallCount = cdrDB.count()

    #number of outbound calls
    cdrDB = DubberCallRecording.objects.filter(callType='outbound')
    cdrOBCallCount = cdrDB.count()

    #number of outbound calls
    cdrDB = DubberCallRecording.objects.filter(callType='meeting')
    cdrMeetingCallCount = cdrDB.count()

    #total call duration
    cdrDB = DubberCallRecording.objects.aggregate(Sum('callDuration'))
    cdrTotalDuration = timedelta(seconds=cdrDB['callDuration__sum'])

    #average call duration
    cdrDB = DubberCallRecording.objects.aggregate(Avg('callDuration'))
    cdrAvgDuration = timedelta(seconds=cdrDB['callDuration__avg'])
    cdrAvgDuration = str(cdrAvgDuration).split(".")[0]

    #maximum call duration
    cdrDB = DubberCallRecording.objects.aggregate(Max('callDuration'))
    cdrMaxDuration = timedelta(seconds=cdrDB['callDuration__max'])

    #maximum call duration
    cdrDB = DubberCallRecording.objects.aggregate(Min('callDuration'))
    cdrMinDuration = timedelta(seconds=cdrDB['callDuration__min'])


    labels = []
    data = []

    labels.append("Inbound")
    data.append(cdrIBCallCount)

    labels.append("Outbound")
    data.append(cdrOBCallCount)

    labels.append("Meeting")
    data.append(cdrMeetingCallCount)
    
    return render(request,'dashboard/calldetail_dashboard.html',{'page_name':'Performance Dashboard','cdrCount':cdrCount,'cdrIBCallCount':cdrIBCallCount,'cdrOBCallCount':cdrOBCallCount,'cdrMeetingCallCount':cdrMeetingCallCount,'cdrTotalDuration':cdrTotalDuration,'cdrAvgDuration':cdrAvgDuration,'cdrMaxDuration':cdrMaxDuration,'cdrMinDuration':cdrMinDuration, 'labels': labels, 'data': data,})
 




       
