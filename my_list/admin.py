from django.contrib import admin
from django.contrib.auth.models import User
from .models import Tasks

# Register your models here.

admin.site.register(Tasks)