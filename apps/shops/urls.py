from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shops.views import AddressListCreateAPIView, CountryListAPIView, BookListAPIView, WishListAPIView, \
    AddressDestroyUpdateAPIView

router = DefaultRouter()
# router.register(r'wishlists', WishListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('country/', CountryListAPIView.as_view()),

    path('address/', AddressListCreateAPIView.as_view()),
    # path('address-update/', AddressListUpdateAPIView.as_view()),
    path('address/<int:pk>', AddressDestroyUpdateAPIView.as_view()),

    path('books', BookListAPIView.as_view(), name='book-list'),
    path('books/<str:slug>', BookListAPIView.as_view(), name='book-list'),

    path('wish-list', WishListAPIView.as_view()),
]
