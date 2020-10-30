from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.http import HttpResponseRedirect
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('goods_list/', GoodsListView.as_view(), name='goods_list'),
    path('goods_list/<good_id>/', GoodsSelectView, name='goods_select'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('approval/', ApprovalView.as_view(), name='approval'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r'^', lambda x: HttpResponseRedirect('/goods_list/'))
]