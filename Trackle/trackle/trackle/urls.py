from django.contrib import admin
from django.urls import path, include
from reqs.views import pisay, students, teachers

urlpatterns = [
    path('', include("reqs.urls")),
    path('admin/', admin.site.urls),
    path('', include("django.contrib.auth.urls")),
    path('signup/', pisay.SignUpView.as_view(), name='signup'),
    path('signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
]
