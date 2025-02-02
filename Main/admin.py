from django.contrib import admin
from .models import Create_Template,ReceivedMessage,MessageStatus
# Register your models here.

admin.site.register(Create_Template)
admin.site.register(ReceivedMessage)
admin.site.register(MessageStatus)