import datetime
import math

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from unidecode import unidecode

from account_module.models import Wallet
from core import settings
from main_module.forms import SearchForm
from main_module.models import Job
from main_module.tasks import fetch_data_from_site


def pagination(request, jobs, item_count):
    paginator = Paginator(jobs, item_count)  # Show 25 contacts per page.
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)
    return products


# Create your views here.

class SearchView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        form = SearchForm()
        try:
            wallet = Wallet.objects.get(user_id=request.user.id)
        except Wallet.DoesNotExist:
            return redirect(reverse("login_view"))
        context = {
            "form": form,
            "wallet": wallet
        }
        return render(request, "main_module/search.html", context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get("search")
            return redirect(reverse("result_view", kwargs={"search": search}))
        return render(request, "main_module/search.html", {"form": form})


class ResultView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, search):
        wallet = Wallet.objects.get(user_id=request.user.id)
        if wallet.current_balance >= -1:
            if search == "all":
                jobs = Job.objects.all()
            else:
                jobs = Job.objects.filter(title__contains=search)
            jobs = pagination(request, jobs, 24)
            # wallet.withdraw(1)
            return render(request, "main_module/result.html", context={"jobs": jobs, "search": search})
        else:
            return HttpResponseForbidden("شما باید ابتدا حساب خود را شارژ کنید")


class TestView(View):
    def get(self, request):
        res = fetch_data_from_site()
        print(res)
        return HttpResponse("aha")
