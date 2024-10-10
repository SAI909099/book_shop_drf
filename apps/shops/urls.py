from django.urls import path

from shops.views import WishlistListCreateView, WishlistDeleteView

urlpatterns = [
    path('wishlist/', WishlistListCreateView.as_view(), name='wishlist-list'),
    path('wishlist/<int:book_id>/', WishlistDeleteView.as_view(), name='wishlist-delete'),

]