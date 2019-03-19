from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.utils.timezone import now

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Subject(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    sypscience = models.BooleanField()
    name = models.CharField(max_length=30)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_section')
    color = models.CharField(max_length=7, default='#007bff')
    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Section(models.Model):
    name = models.CharField(max_length=30)
    grade = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.name

class Requirement(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requirements')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='req_sub')
    details = models.TextField(null=True, blank=True)
    dateAdded = models.DateField(default=now,editable=False)
    dateUpdated = models.DateTimeField(auto_now=True)
    duedate = models.DateField()

    def __str__(self):
        return self.name

class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='req_comment')
    dateAdded = models.DateField(default=now,editable=False)
    content = models.TextField(null=True, blank=True)


class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    subjects = models.ManyToManyField('Subject', related_name='subjected_students')
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='Student_Section')


    def __str__(self):
        return self.user.username
