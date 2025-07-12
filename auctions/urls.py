from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("get_child_categories", views.get_child_categories, name="get_child_categories"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist_view", views.watchlist_view, name="watchlist"),
    path("listings/<int:id>/favorite_listing", views.favorite_listing, name="favorite_listing"),
    path("get_category_breadcrumb", views.get_category_breadcrumb, name="get_category_breadcrumb")
]