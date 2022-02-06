from django import forms
from django.db.models import fields
from .models import DubberSMSNotificationList, DubberSMSLogs

class SMSUserForm(forms.ModelForm):

    class Meta:
        model = DubberSMSNotificationList
        fields = ["user","smsNumber","active"] 