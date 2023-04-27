from django.urls import path
from . import views

urlpatterns = [
    path("", views.SearchView.as_view(), name="search_view"),
    path("test/", views.TestView.as_view(), name="testt_view"),
    # path("all/", views.AllResultView.as_view(), name="all_result_view"),
    path("v/<str:search>/", views.ResultView.as_view(), name="result_view"),
]
