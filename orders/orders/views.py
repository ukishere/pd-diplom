from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from rest_framework.views import APIView

from .validation import input_validation
from .models import Shop, Category, Good, AdditionalGoodParameter



# from django.core.validators import URLValidator, ValidationError
# from django.shortcuts import render


class RegistrationView(FormView):
    form_class = UserCreationForm
    success_url = '/orders/'
    template_name = 'registration/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationView, self).form_invalid(form)


class OrdersView(APIView):
    def get(self, request, *args, **kwargs):
        return(HttpResponse('Orders get'))

    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Для работы с сервисом необходимо пройти аутентификацию'}, status=403)
        #
        # if request.user.is_vendor:
        #     return JsonResponse({'Status': False, 'Error': 'Для данного действия необходимы специальные права представителя магазина'}, status=403)

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