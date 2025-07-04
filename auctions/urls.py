from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create_listing"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("category", views.categories_view, name="show_categories"),
    path("get_child_categories", views.get_child_categories, name="get_child_categories"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listings/<int:id>/favorite_listing", views.favorite_listing, name="favorite_listing")
]