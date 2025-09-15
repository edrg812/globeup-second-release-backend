from django.contrib import admin

# Register your models here.
from .models import SMTPMail

admin.site.register(SMTPMail)