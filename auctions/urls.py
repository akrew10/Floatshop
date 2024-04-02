from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("listing/<int:Listing_id>", views.listing, name="listing"),
    path("category", views.category, name="category"),
    path("removeWatchlist/<int:Listing_id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:Listing_id>", views.addWatchlist, name="addWatchlist"),
    path("addComment/<int:Listing_id>", views.addComment, name="addComment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addBid/<int:Listing_id>", views.addBid, name="addBid"),
    path("closeAuction/<int:Listing_id>", views.closeAuction, name="closeAuction")
]
