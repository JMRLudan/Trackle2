from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teacher_required
from ..forms import TeacherSignUpForm, RequirementForm
from ..models import Requirement, User, Subject, Comment, Section
from datetime import datetime


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:req_change_list')


@method_decorator([login_required, teacher_required], name='dispatch')
class RequirementListView(ListView):
    model = Requirement
    ordering = ('name', )
    context_object_name = 'requirements'
    template_name = 'reqs/teachers/req_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.requirements \
            .select_related('subject') \
            .order_by('-duedate', '-name', '-subject')
        return queryset

@method_decorator([login_required, teacher_required], name='dispatch')
class SubjectCreateView(CreateView):
    model = Subject
    fields = ('name','sypscience','section')
    template_name = 'reqs/teachers/sub_add_form.html'

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.teacher = self.request.user
        subject.save()
        messages.success(self.request, 'The subject was successfully created!')
        return redirect('teachers:req_change_list')

@method_decorator([login_required, teacher_required], name='dispatch')
class RequirementCreateView(CreateView):
    model = Requirement
    form_class = RequirementForm
    template_name = 'reqs/teachers/req_add_form.html'
    context_object_name = 'requirement'


    def get_context_data(self, **kwargs):
        kwargs['requirement'] = Requirement.objects.all() \
                .exclude(duedate__lt=datetime.now().date()) \
                .order_by('duedate', 'name', 'subject')
        return super(RequirementCreateView, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(RequirementCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        requirement = form.save(commit=False)
        requirement.owner = self.request.user
        requirement.save()
        messages.success(self.request, 'The requirement was successfully created!')
        return redirect('teachers:requirement_change', requirement.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class RequirementUpdateView(UpdateView):
    model = Requirement
    fields = ('name', 'subject', 'details','duedate',)
    #ADD THING TO UPDATE LAST EDITED
    context_object_name = 'requirement'
    template_name = 'reqs/teachers/requirement_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing requirements that belongs
        to the logged in user.
        '''
        return self.request.user.requirements.all()

    def get_success_url(self):
        return reverse('teachers:requirement_change', kwargs={'pk': self.object.pk})

@method_decorator([login_required, teacher_required], name='dispatch')
class AddCommentView(CreateView):
    model = Comment
    fields = ('content',)
    template_name = 'reqs/teachers/teacher_add_comment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.writer = self.request.user
        comment.requirement = Requirement.objects.filter(pk = self.kwargs['pk']).first()
        comment.save()
        messages.success(self.request, 'The comment was successfully created!')
        pk = self.kwargs['pk']
        return redirect('teachers:requirement_change', pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class RequirementDeleteView(DeleteView):
    model = Requirement
    context_object_name = 'requirement'
    template_name = 'reqs/teachers/requirement_delete_confirm.html'
    success_url = reverse_lazy('teachers:req_change_list')

    def delete(self, request, *args, **kwargs):
        requirement = self.get_object()
        messages.success(request, 'The requirement %s was successfully deleted!' % requirement.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.requirements.all()
