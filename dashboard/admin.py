from django.contrib import admin
from .models import DubberAPIToken

# Register your models here.
admin.site.register(DubberAPIToken)

class DubberAPITokenAdmin(admin.ModelAdmin):
    list_display =['accessToken','refreshToken','tokenExpiry','expiryTime']