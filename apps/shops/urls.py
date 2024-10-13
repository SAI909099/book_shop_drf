from django.urls import path, include

from shops.views import AddressListCreateAPIView, CountryListAPIView, BookListAPIView, WishListAPIView

urlpatterns = [
    path('address/', AddressListCreateAPIView.as_view()),
    path('country/', CountryListAPIView.as_view()),

    path('book/', BookListAPIView.as_view()),
    path('wish-list', WishListAPIView.as_view()),
]