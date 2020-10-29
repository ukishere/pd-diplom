from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User


class OrdersUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(OrdersUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'


    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'is_vendor', 'first_name', 'second_name', 'third_name', 'company', 'position', 'password1', 'password2')


class OrdersUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'is_vendor',)


class OrdersUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(OrdersUserLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = 'Пароль'

    class Meta:
        model = User
        fields = ('email', 'password')