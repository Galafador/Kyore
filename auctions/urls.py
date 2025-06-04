from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.categories_view, name="show_categories" ),
    path("get_child_categories", views.get_child_categories, name="get_child_categories")
]
