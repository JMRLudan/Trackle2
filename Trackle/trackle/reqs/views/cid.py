from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import cid_required
from ..forms import StudentSubjectsForm, StudentSignUpForm
from ..models import Requirement, Student, User, Section, Subject, Comment, Report
from datetime import datetime

@method_decorator([login_required, cid_required], name='dispatch')
class RequirementListView(ListView):
    model = Requirement
    ordering = ('name', )
    context_object_name = 'requirements'
    template_name = 'reqs/cid/cid_requirements.html'

    def get_queryset(self):
        queryset = Requirement.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['requirement'] = Requirement.objects.all() \
                .exclude(duedate__lt=datetime.now().date()) \
                .order_by('-duedate', '-name', '-subject')
        return super(RequirementListView, self).get_context_data(**kwargs)

@method_decorator([login_required, cid_required], name='dispatch')
class DoneRequirementListView(ListView):
    model = Requirement
    ordering = ('name', )
    context_object_name = 'requirements'
    template_name = 'reqs/cid/cid_requirements_done.html'

    def get_queryset(self):
        queryset = Requirement.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['requirement'] = Requirement.objects.all() \
                .exclude(duedate__gt=datetime.now().date()) \
                .order_by('duedate', '-name', '-subject')
        return super(DoneRequirementListView, self).get_context_data(**kwargs)

@method_decorator([login_required, cid_required], name='dispatch')
class RequirementView(ListView):
    context_object_name = 'req'
    template_name = 'reqs/cid/requirement_details.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Requirement.objects.filter(pk=pk)
        return queryset

@method_decorator([login_required, cid_required], name='dispatch')
class AddCommentView(CreateView):
    model = Comment
    fields = ('content',)
    template_name = 'reqs/cid/cid_add_comment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.writer = self.request.user
        comment.requirement = Requirement.objects.filter(pk = self.kwargs['pk']).first()
        comment.save()
        messages.success(self.request, 'The comment was successfully created!')
        pk = self.kwargs['pk']
        return redirect('cid:requirement_details', pk)

@method_decorator([login_required, cid_required], name='dispatch')
class ReportListView(ListView):
    model = Report
    ordering = ('dateAdded', )
    context_object_name = 'reports'
    template_name = 'reqs/cid/cid_reports.html'

    def get_queryset(self):
        queryset = Report.objects.all() \
                .exclude(checked= True)
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['report'] = Report.objects.all() \
                .exclude(checked=True)\
                .order_by('dateAdded', '-requirement', '-writer')
        return super(ReportListView, self).get_context_data(**kwargs)

@method_decorator([login_required, cid_required], name='dispatch')
class ReportDoneListView(ListView):
    model = Report
    ordering = ('dateAdded', )
    context_object_name = 'reports'
    template_name = 'reqs/cid/cid_reports_done.html'

    def get_queryset(self):
        queryset = Report.objects.all() \
                .exclude(checked= False)
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['report'] = Report.objects.all() \
                .exclude(checked= False)\
                .order_by('dateAdded', '-requirement', '-writer')
        return super(ReportDoneListView, self).get_context_data(**kwargs)

@method_decorator([login_required, cid_required], name='dispatch')
class ReportUpdateView(UpdateView):
    model = Report
    fields = ('checked',)
    #ADD THING TO UPDATE LAST EDITED
    context_object_name = 'reports'
    template_name = 'reqs/cid/cid_report_update.html'
    success_url = reverse_lazy('cid:reports_all')

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing requirements that belongs
        to the logged in user.
        '''
        queryset = Report.objects.all()
        return queryset
