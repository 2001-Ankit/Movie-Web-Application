from . import views
from django.urls import path
from .views import home_view

urlpatterns = [
    path("", views.home_view, name="home"),
    path("top_movies",views.top_movies,name="top_movies")
]
