from django.urls import path
from .views import RegestrationView , CustomLoginView

urlpatterns = [
    path("registration/", RegestrationView.as_view(), name="registration"),
    path("login/", CustomLoginView.as_view(), name="login"),
]