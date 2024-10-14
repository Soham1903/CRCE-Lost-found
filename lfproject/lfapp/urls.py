from django.urls import path

from .views import *

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("home/", home, name="home"),
    path("upload/", upload, name="upload"),
    path("search/", search, name="search"),
    path('logout/', logout_view, name='logout')
]