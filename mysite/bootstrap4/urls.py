from django.conf.urls import url
from . import views

urlpatterns = [
    url("", views.bootstrap4_index, name="index"),
]