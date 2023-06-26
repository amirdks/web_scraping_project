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
from main_module.models import Job, JobSeeker
from main_module.utils import fetch_data_from_jobseeker, fetch_data_from_linkedin, fetch_data_from_jobinja, fetch_data_from_divar


def pagination(request, jobs, item_count):
    paginator = Paginator(jobs, item_count)  # Show 25 contacts per page.
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)
    return products


# Create your views here.

class SearchView(View):
    def get(self, request: HttpRequest):
        form = SearchForm()
        try:
            wallet = Wallet.objects.get(user_id=request.user.id)
        except Wallet.DoesNotExist:
            wallet = None
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


class ResultView(View):
    def get(self, request: HttpRequest, search):
        if request.user.is_authenticated:
            wallet = Wallet.objects.get(user_id=request.user.id)
        else:
            wallet = None
        if search == "all":
            jobs = Job.objects.all()
        else:
            jobs = Job.objects.filter(title__contains=search)
        jobs = pagination(request, jobs, 24)
        # wallet.withdraw(1)
        return render(request, "main_module/result.html",
                      context={"jobs": jobs, "search": search, "wallet": wallet})


# class TestView(View):
#     def get(self, request):
#         res = fetch_data_from_site()
#         print(res)
#         return HttpResponse("aha")


class RedirectView(LoginRequiredMixin, View):
    http_method_names = ["get"]

    def get(self, reqeust: HttpRequest, pk):
        user = reqeust.user
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return HttpResponse("آگهی مورد نظر شما یافت نشد")
        if user.is_authenticated:
            wallet = Wallet.objects.get(user_id=user.id)
            try:
                wallet.withdraw(1)
            except wallet.InsufficientBalance as e:
                return HttpResponse("موجودی شما برای دیدن آگهی جدید کافی نمیباشد")
            return redirect(job.link)
        else:
            return redirect("login_view")


class TestView(View):
    def get(self, request):
        fetch_data_from_jobseeker()
        fetch_data_from_linkedin()
        fetch_data_from_jobinja()
        fetch_data_from_divar()
        return HttpResponse("salam")


class ResultSeekerView(View):
    def get(self, request: HttpRequest, search):
        if request.user.is_authenticated:
            wallet = Wallet.objects.get(user_id=request.user.id)
        else:
            wallet = None
        if search == "all":
            jobs = JobSeeker.objects.all()
        else:
            jobs = JobSeeker.objects.filter(full_name__contains=search)
        jobs = pagination(request, jobs, 24)
        # wallet.withdraw(1)
        return render(request, "main_module/result_seeker.html",
                      context={"jobs": jobs, "search": search, "wallet": wallet})
