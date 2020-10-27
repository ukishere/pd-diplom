from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView

def first_page_view(request):
    return(HttpResponse('First Page'))

def test_display(request):
    return(HttpResponse('Test'))

class RegistrationView(FormView):
    form_class = UserCreationForm
    success_url = '/test/'
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationView, self).form_invalid(form)