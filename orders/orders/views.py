from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.views.generic.edit import FormView, View
from rest_framework.views import APIView
from django.shortcuts import redirect, render
from django.core.mail import send_mail

from .validation import input_validation
from .models import Shop, Category, Good, AdditionalGoodParameter
from .forms import OrdersUserChangeForm, OrdersUserCreationForm, OrdersUserLoginForm


class RegistrationView(FormView):
    form_class = OrdersUserCreationForm
    success_url = '/orders/'
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        send_mail('Регистрация прошла успешно', 'Вы зарегистрированы', 'django_test_diploma@mail.ru', [form.data['email'],], fail_silently=False)
        user = authenticate(username=form.data['email'], password=form.data['password1'])
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationView, self).form_invalid(form)


class LoginView(FormView):
    form_class = OrdersUserLoginForm
    success_url = '/orders/'
    template_name = 'registration/login.html'

    def form_valid(self, form):
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, template_name='registration/logged_out.html')


class OrdersView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_vendor:
            return render(request, template_name='orders/vendor.html')
        else:
            return render(request, template_name='orders/not_vendor.html')


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_vendor:
            return HttpResponse('Ошибка: вы залогинились не как поставщик')

        if input_validation(request):
            shop, _ = Shop.objects.get_or_create(name=request.data['shop'])

            for category in request.data['categories']:
                category, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])

            for good in request.data['goods']:
                current_good, _ = Good.objects.get_or_create(category=category,
                                                    model=good['model'],
                                                    name=good['name'],
                                                    price=good['price'],
                                                    price_rrc=good['price_rrc'],
                                                    quantity=good['quantity'])
                current_good.shops.add(shop)

                for parameter, value in good['parameters'].items():
                    AdditionalGoodParameter.objects.get_or_create(good=current_good,
                                                                  parameter=parameter,
                                                                  value=value)

            return (HttpResponse('Данные приняты'))
        else:
            return HttpResponse('Ошибка: проверьте корректность данных')

    def put(self, request, *args, **kwargs):
        return(HttpResponse('Orders put'))