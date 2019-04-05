from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:req_change_list')
        elif request.user.is_cid:
            return redirect('cid:requirements_all')
        else:
            return redirect('students:requirement_list')
    return render(request, 'reqs/home.html')
