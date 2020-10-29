from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.conf.urls import url
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda x: HttpResponseRedirect('/orders/')),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name="register"),
]

urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += [
    url(r'^', lambda x: HttpResponseRedirect('/orders/'))
]