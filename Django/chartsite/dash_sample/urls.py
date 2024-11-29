from django.urls import path

from . import views
from . import app8

app_name = "dash_sample"

urlpatterns = [
    path("", views.index, name="index")
]