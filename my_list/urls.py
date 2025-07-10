from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="home-page"),
    path("register", views.RegisterPageView.as_view(), name="register-user"),
    path("login", views.LoginPageView.as_view(), name="login-user"),
    path("logout", views.LogoutView.as_view(), name="logout-user"),
    path("delete/<int:id>", views.DeleteView.as_view(), name="delete-task"),
    path("done/<int:id>", views.MarkDoneView.as_view(), name="mark-done")
]
