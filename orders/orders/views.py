from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.views.generic.edit import FormView, View
from rest_framework.views import APIView
from django.shortcuts import redirect, render
from django.core.mail import send_mail
import json

from .validation import *
from .models import *
from .forms import OrdersUserCreationForm, OrdersUserLoginForm


class RegistrationView(FormView):
    form_class = OrdersUserCreationForm
    success_url = '/goods_list/'
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
    success_url = '/goods_list/'
    template_name = 'registration/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, template_name='registration/logged_out.html')


def GoodsSelectView(request, good_id):
    check, path = default_check(request)
    if check:
        return redirect(path)

    good = Good.objects.filter(id=good_id).prefetch_related('shops', 'parameters')
    template = 'orders/goods_select.html'
    context = {'Good': good}
    return render(request, template, context)


class GoodsListView(APIView):
    def get(self, request, *args, **kwargs):
        check, path = default_check(request)
        if check:
            return redirect(path)

        goods = Good.objects.all().prefetch_related('shops', 'parameters')
        context = {'Goods': goods}
        template = 'orders/goods_list.html'

        if request.user.is_vendor:
            return render(request, template_name='orders/vendor.html')
        else:
            return render(request, template, context)


class BasketView(APIView):
    def get(self, request, *args, **kwargs):
        check, path = default_check(request)
        if check:
            return redirect(path)

        try:
            order = Order.objects.get(user=request.user, is_confirmed=False)
            ordered_goods = OrderedGoods.objects.filter(order=order.id)
            goods_price, delivery_price, final_price = price_calculation(ordered_goods)
            found = True

            context = {'OrderedGoods': ordered_goods,
                       'GoodsPrice': goods_price,
                       'DeliveryPrice': delivery_price,
                       'FinalPrice': final_price,
                       'Found': found}

        except Order.DoesNotExist:
            found = False
            context = {'Found': found}

        template = 'orders/basket.html'

        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        elif request.user.is_vendor:
            return HttpResponse('Ошибка: вы залогинились как поставщик')

        if basket_validation(request):
            data = json.loads(request.body)
            if data:
                current_order, _ = Order.objects.filter(is_confirmed=False).get_or_create(user=request.user)

            for object in data:
                current_ordered_goods, _ = OrderedGoods.objects.get_or_create(good_id=object['good_id'],
                                                                              shop_id=object['shop_id'],
                                                                              quantity=object['quantity'],
                                                                              order=current_order)

            return (HttpResponse('Данные приняты'))
        else:
            return HttpResponse('Ошибка: проверьте корректность данных')


class ApprovalView(APIView):
    def get(self, request, *args, **kwargs):
        check, path = default_check(request)
        if check:
            return redirect(path)

        user = User.objects.get(email=request.user)
        order = Order.objects.get(user=request.user, is_confirmed=False)

        context = {'User': user, 'For_whom': order.for_whom}
        template = 'orders/approval.html'

        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        elif request.user.is_vendor:
            return HttpResponse('Ошибка: вы залогинились как поставщик')

        if approval_validation(request):
            data = json.loads(request.body)
            if data:

                for object in data:
                    current_for_whom, _ = ForWhom.objects.get_or_create(city=object['city'],
                                                                       street=object['street'],
                                                                       house=object['house'],
                                                                       structure=object['structure'],
                                                                       building=object['building'],
                                                                       apartment=object['apartment'],
                                                                       phone=object['phone'])

                current_order, _ = Order.objects.filter(is_confirmed=False).get_or_create(user=request.user)
                current_order.for_whom = current_for_whom
                current_order.save()

            return (HttpResponse('Данные приняты'))
        else:
            return HttpResponse('Ошибка: проверьте корректность данных')


class FinalView(APIView):
    def get(self, request, *args, **kwargs):
        check, path = default_check(request)
        if check:
            return redirect(path)

        user = User.objects.get(email=request.user)

        try:
            order = Order.objects.get(user=request.user, is_confirmed=False)
            ordered_goods = OrderedGoods.objects.filter(order=order.id)
            _, _, final_price = price_calculation(ordered_goods)
            found = True
            order.is_confirmed = True
            order.save()
            send_mail(f'Спасибо за ваш заказ № {order.id}', '', 'django_test_diploma@mail.ru', [user.email,], fail_silently=False)
            context = {'Found': found, 'User': user, 'Order': order, 'FinalPrice': final_price}

        except Order.DoesNotExist:
            found = False
            context = {'Found': found}

        template = 'orders/final.html'

        return render(request, template, context)


class AllOrdersView(APIView):
    def get(self, request, *args, **kwargs):
        check, path = default_check(request)
        if check:
            return redirect(path)

        user = User.objects.get(email=request.user)
        orders = Order.objects.filter(user=request.user)
        context = {'Orders': orders}
        template = 'orders/all_orders.html'

        return render(request, template, context)

    def put(self, request, *args, **kwargs):
        order = Order.objects.get(id=request.query_params['order_id'])
        order.is_delivered = True
        order.save()
        return HttpResponse('Статус изменен')


def AllOrdersSelectView(request, order_id):
    check, path = default_check(request)
    if check:
        return redirect(path)

    ordered_goods = OrderedGoods.objects.filter(order=order_id)
    _, _, final_price = price_calculation(ordered_goods)
    template = 'orders/orders_select.html'
    context = {'OrderedGoods': ordered_goods, 'FinalPrice': final_price}

    return render(request, template, context)


class OrdersView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        elif not request.user.is_vendor:
            return redirect('goods_list')

        company_name = User.objects.get(email=request.user).company
        shop = Shop.objects.get(name=company_name)
        orders = OrderedGoods.objects.filter(shop_id=shop.id)
        context = {'Status': shop.status, 'Orders': orders}
        template = 'orders/vendor.html'

        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        elif not request.user.is_vendor:
            return HttpResponse('Ошибка: вы залогинились не как поставщик')

        if input_validation(request):
            shop, _ = Shop.objects.get_or_create(name=request.data['shop'])

            for category in request.data['categories']:
                category, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])

            for good in request.data['goods']:
                currnet_category = Category.objects.get(id=good['category'])
                current_good, _ = Good.objects.get_or_create(id=good['id'],
                                                    category=currnet_category,
                                                    model=good['model'],
                                                    name=good['name'],
                                                    price=good['price'],
                                                    price_rrc=good['price_rrc'],
                                                    quantity=good['quantity'])

                for parameter, value in good['parameters'].items():
                    parameter, _ = AdditionalGoodParameter.objects.get_or_create(parameter=parameter,
                                                                  value=value)
                    current_good.parameters.add(parameter)

                current_good.shops.add(shop)
                current_good.save()

            return (HttpResponse('Данные приняты'))
        else:
            return HttpResponse('Ошибка: проверьте корректность данных')

    def put(self, request, *args, **kwargs):
        company_name = User.objects.get(email=request.user).company
        shop = Shop.objects.get(name=company_name)
        if shop.status:
            shop.status = False
        else:
            shop.status = True
        shop.save()
        return(HttpResponse('Статус изменен'))