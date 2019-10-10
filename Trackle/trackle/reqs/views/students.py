from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import StudentSubjectsForm, StudentSignUpForm
from ..models import Requirement, Student, User, Section, Subject, Comment, Report
from datetime import datetime

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:requirement_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentSubjectsView(UpdateView):
    model = Student
    form_class = StudentSubjectsForm
    template_name = 'reqs/students/subjects_form.html'
    success_url = reverse_lazy('students:requirement_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Your subjects have been updated.')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class RequirementListView(ListView):
    model = Requirement
    ordering = ('name', )
    context_object_name = 'requirements'
    template_name = 'reqs/students/requirement_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_subjects = student.subjects.values_list('pk', flat=True)
        queryset = Requirement.objects.filter(subject__in=student_subjects) \
                .exclude(duedate__lt=datetime.now().date()) \
                .order_by('-duedate', '-name', '-subject')
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenRequirementListView(ListView):
    context_object_name = 'taken_requirements'
    template_name = 'reqs/students/finished_requirement_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_subjects = student.subjects.values_list('pk', flat=True)
        queryset = Requirement.objects.filter(subject__in=student_subjects) \
                .exclude(duedate__gt=datetime.now().date()) \
                .order_by('-duedate', '-name', '-subject')
        return queryset

@method_decorator([login_required, student_required], name='dispatch')
class AddCommentView(CreateView):
    model = Comment
    fields = ('content',)
    template_name = 'reqs/students/student_add_comment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.writer = self.request.user
        comment.requirement = Requirement.objects.filter(pk = self.kwargs['pk']).first()
        comment.save()
        messages.success(self.request, 'The comment was successfully created!')
        pk = self.kwargs['pk']
        return redirect('students:requirement_details', pk)

@method_decorator([login_required, student_required], name='dispatch')
class AddReportView(CreateView):
    model = Report
    fields = ('content',)
    template_name = 'reqs/students/student_add_report.html'

    def form_valid(self, form):
        report = form.save(commit=False)
        report.writer = self.request.user
        report.requirement = Requirement.objects.filter(pk = self.kwargs['pk']).first()
        report.save()
        messages.success(self.request, 'The report was successfully created!')
        pk = self.kwargs['pk']
        return redirect('students:requirement_details', pk)

@method_decorator([login_required, student_required], name='dispatch')
class RequirementView(ListView):
    context_object_name = 'requirement'
    template_name = 'reqs/students/requirement_form.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Requirement.objects.filter(pk=pk)
        return queryset
