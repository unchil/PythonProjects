from . import views


app_name = "supplydemand"

urlpatterns = [
    path("", views.FiveMinuteSD.getLast1HR(), name="one_hr")
]