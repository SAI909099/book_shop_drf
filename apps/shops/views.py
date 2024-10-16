from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from shops.models import Country, Book
from shops.serializers import CountryModelSerializer, BookModelSerializer, \
    WishlistModelSerializer


# @extend_schema(tags=['address'])
# class AddressListCreateAPIView(ListCreateAPIView):
#     queryset = Address.objects.all()
#     serializer_class = AddressModelSerializer


@extend_schema(tags=['countrys'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer


@extend_schema(tags=['books'])
class BookListAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer


@extend_schema(tags=['wishlist'])
class WishListAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_calss = WishlistModelSerializer


from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from shops.models import Address, Country
from shops.serializers import AddressModelSerializer, CountryModelSerializer


@extend_schema(tags=['users'])
class AddressListCreateAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

@extend_schema(tags=['users'])
class AddressListUpdateAPIView(UpdateAPIView):
    queryset = Address.objects.all()
    seralizer_class = AddressModelSerializer
    permission_class = IsAuthenticated,

@extend_schema(tags=['users'])
class AddressDestroyAPIView(DestroyAPIView):
    queryset = Address.objects.all()
    seralizer_class = AddressModelSerializer
    permission_class = IsAuthenticated,



@extend_schema(tags=['users'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
    authentication_classes = ()


