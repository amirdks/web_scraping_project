from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from account_module.forms import LoginForm
from utils.normalize_email import normalize_email


# Create your views here.
class LoginView(View):
    def dispatch(self, request):
        if not request.user.is_authenticated:
            return super().dispatch(request)
        else:
            return redirect(reverse("search_view"))

    def get(self, request):
        context = {
            "form": LoginForm()
        }
        return render(request, "account_module/login.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=normalize_email(form.cleaned_data.get('email')),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect(request.POST.get('next', '/'))
            else:
                form.add_error('email', 'کاربری با مشخصات زیر یافت نشد')
        return render(request, 'account_module/login.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('home_view'))
        logout(request)
        return redirect(reverse('login_view'))
