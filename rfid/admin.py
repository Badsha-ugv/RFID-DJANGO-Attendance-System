from django.contrib import admin

from .models import RFIDCard,UserInfo,UserLog

admin.site.register(RFIDCard) 
admin.site.register(UserInfo) 
admin.site.register(UserLog) 

