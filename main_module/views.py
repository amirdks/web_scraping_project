import datetime
import math

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from unidecode import unidecode

from main_module.forms import SearchForm
from main_module.models import Job
from main_module.tasks import fetch_data_from_site


# Create your views here.

class SearchView(View):
    def get(self, request):
        form = SearchForm()
        context = {
            "form": form
        }
        return render(request, "main_module/search.html", context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get("search")
            return redirect(reverse("result_view", kwargs={"search": search}))
        return render(request, "main_module/search.html", {"form": form})


class ResultView(View):
    def get(self, request, search):
        jobs = Job.objects.filter(title__contains=search)
        return render(request, "main_module/result.html", context={"jobs": jobs})


class TestView(View):
    def get(self, request):
        res = fetch_data_from_site()
        print(res)
        return HttpResponse("aha")
