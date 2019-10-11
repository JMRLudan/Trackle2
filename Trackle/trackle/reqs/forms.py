from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from reqs.models import (Student, Subject, User, Requirement, Section)

class DateForm(forms.Form):
    date = forms.DateField(input_formats=['%m/%d/%Y'])

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save()
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):

    # Student selects section/block, subjects come with the section/block
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        widget=forms.Select,
        required=True
    )

    # Only SYP sciences show up here as they aren't specific to a block
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.filter(sypscience=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit = True):
        user = super().save()
        user.is_student = True
        user.save()
        section = self.cleaned_data['section']  # No need to use get() here
        student = Student.objects.create(user=user, section=section)
        # Adds subjects connected to section to student's list of subjects
        student.subjects.add(*self.cleaned_data.get('subjects'))
        sectionsubs = Subject.objects.filter(section=section)
        sectionsubs = list(sectionsubs)
        student.subjects.add(*sectionsubs)
        return user

class StudentSubjectsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentSubjectsForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subject.objects.filter(sypscience=True)

    class Meta:
        model = Student
        fields = ('section', 'subjects')
        widgets = {
            'subjects': forms.CheckboxSelectMultiple
        }

class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ('name', 'subject', 'duedate','details')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(teacher=self.user)

class UpdateRequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ('name', 'subject', 'duedate','details')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UpdateRequirementForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(teacher=self.user)
