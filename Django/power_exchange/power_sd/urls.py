from django.urls import path
from . import views
from . import app

app_name = "power_sd"

urlpatterns = [
    path("", views.index, name="index")
]
