from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from shops.models import Address, Country, Book
from shops.serializers import AddressModelSerializer, CountryModelSerializer, BookModelSerializer, \
    WishlistModelSerializer


@extend_schema(tags=['address'])
class AddressListCreateAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressModelSerializer


@extend_schema(tags=['countrys'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer

@extend_schema(tags=['books'])
class BookListAPIView(ListCreateAPIView):
    queryset= Book.objects.all()
    serializer_class = BookModelSerializer

@extend_schema(tags=['wishlist'])
class WishListAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_calss = WishlistModelSerializer