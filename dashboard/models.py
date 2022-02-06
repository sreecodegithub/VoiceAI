from django.db import models

# Create your models here.

class DubberUserTable(models.Model):
    firstName = models.CharField(max_length=150)
    lastName = models.CharField(max_length=150)
    userName = models.CharField(max_length=150)
    roleType = models.CharField(max_length=150)

 
    
class DubberAPIToken(models.Model):
    number = models.IntegerField(default=1)
    region = models.CharField(max_length=50,blank=True)
    auth_id=models.CharField(max_length=600,blank=True)
    auth_secret=models.CharField(max_length=600,blank=True)
    client_id = models.CharField(max_length=600,blank=True)
    client_secret =models.CharField(max_length=600,blank=True)
    account_id = models.CharField(max_length=600,blank=True)
    accessToken = models.CharField(max_length=600)
    refreshToken = models.CharField(max_length=600)
    tokenExpiry = models.BigIntegerField()
    expiryTime = models.DateTimeField(blank=True, null=True)

class DubberCallRecording(models.Model):
   # (recording_id,call_from,call_to,call_type,start_time,call_duration,recording_channel,analytical,anger,confident,fear,sadness,joy,sentiment,tentative,transcription,creation_datetime,accountid,region,recording_url,start_date,sentiment_text,call_tag_1, call_tag_2, call_tag_3, call_tag_4)
    recordingID = models.BigIntegerField(primary_key=True)
    callFrom = models.CharField(max_length=45, blank=True)
    callTo = models.CharField(max_length=45, blank=True) 
    callType = models.CharField(max_length=45, blank=True)
    startTime = models.CharField(max_length=45, blank=True)
    startDate = models.DateField(blank=True)
    callDuration = models.IntegerField(blank=True)
    recordingChannel = models.CharField(max_length=45, blank=True)
    held = models.CharField(max_length=10, blank=True)
    interactionType = models.CharField(max_length=20, blank=True)
    dubPointID = models.CharField(max_length=250, blank=True)
    transcription = models.TextField( blank=True) 
    sentiment = models.CharField(max_length=10, blank=True)
    analysed = models.CharField(max_length=10, blank=True)
    createdDate = models.DateTimeField( blank=True)
    

    anger = models.FloatField( blank=True)
    confident = models.FloatField( blank=True)
    fear = models.FloatField( blank=True)
    sadness = models.FloatField( blank=True)
    joy = models.FloatField( blank=True)
    analytical = models.FloatField( blank=True)
    tentative = models.FloatField( blank=True)


class DubberLastInsertedRecording(models.Model):
    beforeID = models.IntegerField()
    createdDate = models.DateTimeField( blank=True)


class DubberWebhookIDandSecret(models.Model):
    notificationURL = models.TextField(blank=True)
    X_Hook_Secret = models.CharField(max_length=250,blank=True)
    createdDate = models.DateTimeField( blank=True)

class DubberWebhookNotification(models.Model):
    eventType = models.CharField(max_length=100,blank=True)
    notificationURL= models.TextField(blank=True)
    resourceURL=models.TextField(blank=True)
    createdDate = models.DateTimeField( blank=True)

class DubberSMSNotificationList(models.Model):
    user = models.CharField(max_length=250)
    smsNumber = models.BigIntegerField()
    active = models.BooleanField(default=False)


class DubberSMSLogs(models.Model):
    user = models.CharField(max_length=250)
    smsType = models.CharField(max_length=250,blank=False)
    smsNumber = models.BigIntegerField()
    smsContent = models.TextField(blank=True)
    smsStatus = models.TextField()