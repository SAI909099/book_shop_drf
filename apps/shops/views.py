from drf_spectacular.utils import extend_schema
from rest_framework import status, mixins
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response

from shops.models import Country, Book, Author
from shops.serializers import CountryModelSerializer, BookModelSerializer, \
    WishlistModelSerializer, AddressListModelSerializer, AuthorModelSerializer

from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from shops.models import Address, Country
from shops.serializers import  CountryModelSerializer


from users.models import User


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





@extend_schema(tags=['address'])
class AddressListCreateAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
#
# @extend_schema(tags=['address'])
# class AddressListUpdateAPIView(UpdateAPIView):
#     queryset = Address.objects.all()
#     seralizer_class = AddressListModelSerializer
#     permission_class = IsAuthenticated,

@extend_schema(tags=['address'])
class AddressDestroyUpdateAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        self._can_delete = qs.count() > 1
        return qs

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if self._can_delete:
            _user: User = request.user
            if instance.id in (_user.billing_address_id, _user.shipping_address_id):
                return Response({"message": "maxsus addresslar"})

            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "ozi 1ta qoldi!"})



@extend_schema(tags=['address'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
    authentication_classes = ()



@extend_schema(tags=['author'])
class AuthorListAPIView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
    authentication_classes = ()

