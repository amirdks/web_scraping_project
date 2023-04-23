from django.urls import path
from . import views

urlpatterns = [
    path("", views.SearchView.as_view(), name="search_view"),
    path("test/", views.TestView.as_view(), name="testt_view"),
    path("<str:search>/", views.ResultView.as_view(), name="result_view"),
]
