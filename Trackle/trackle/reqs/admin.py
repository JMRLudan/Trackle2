from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User, Subject, Requirement, Student, Section, Comment, Report

# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Requirement)
admin.site.register(Student)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(Report)
