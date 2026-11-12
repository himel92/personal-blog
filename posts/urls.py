from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/<slug:slug>/", views.post_detail, name="post_detail"),
    path("posts/<slug:slug>/comment/", views.add_comment, name="add_comment"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="posts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/create/", views.create_post, name="create_post"),
    path("dashboard/edit/<str:pk>/", views.edit_post, name="edit_post"),
    path("dashboard/delete/<str:pk>/", views.delete_post, name="delete_post"),
]
