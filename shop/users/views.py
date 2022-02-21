from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from baskets.models import Basket
from common.views import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User

from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages

from django.urls import reverse
from django.conf import settings


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'

    def get_success_url(self):
        return reverse_lazy('index')


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались!'
    title = 'GeekShop - Регистрация'

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        print('CREATE')
        print(self.request.method)
        if self.request.method == 'POST':
            print(1)
        else:
            print(2)
        return context

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                messages.success(request, 'Вы успешно зарегестрировались')

            return HttpResponseRedirect(reverse('users:login'))


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'GeekShop - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


def verify(request, email, activation_key):
    user = User.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
        return render(request, 'users/verify.html')

    return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    subject = 'Verify your account'
    link = reverse('users:verify', args=[user.email, user.activation_key])
    message = f'{settings.DOMAIN}{link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
