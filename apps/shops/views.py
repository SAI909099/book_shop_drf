from drf_spectacular.utils import extend_schema
from rest_framework import status, mixins
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, GenericAPIView, CreateAPIView, \
    RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from shared.paginations import CustomPageNumberPagination
from shops.models import Country, Book, Author
from shops.serializers import CountryModelSerializer, BookModelSerializer, \
    WishlistModelSerializer, AddressListModelSerializer, AuthorModelSerializer, CartlistModelSerializer, \
    BookDetailModelSerializer

from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from shops.models import Address, Country,Cart
from shops.serializers import  CountryModelSerializer


from users.models import User




# --------------------------------counrtys --------------------------------

@extend_schema(tags=['countrys'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer

#----------------------------books---------------------------

@extend_schema(tags=['books'])
class BookListAPIView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer


@extend_schema(tags=['books'])
class BookRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailModelSerializer
    lookup_field = 'slug'


#----------------------address ----------------------------------------


@extend_schema(tags=['address'])
class AddressListCreateAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


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

# -------------------------------author -----------------------------------

@extend_schema(tags=['author'])
class AuthorDetailView(RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer

    def get_object(self):
        name = self.request.query_params.get('name', None)
        if name:
            first_name, last_name = name.split(" ", 1)
            return get_object_or_404(Author, first_name=first_name, last_name=last_name)
        return super().get_object()


# --------------------------cart ---------------------------------

@extend_schema(tags=['Cart'])
class CartLisrAPIView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartlistModelSerializer
    authentication_classes = ()

#----------------------------------page------------------------------

@extend_schema(tags=['page'])
class BookDetailAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailModelSerializer
    lookup_field = 'slug'

    def get_serializer_context(self):
        currency = self.request.user.profile.currency if self.request.user.is_authenticated else 'USD'
        return {'currency': currency}

@extend_schema(tags=['page'])
class PageListAPIView(ListAPIView):
    queryset = Book.objects.order_by('-id')
    serializer_class = BookDetailModelSerializer
    pagination_class = CustomPageNumberPagination

    def get_serializer_context(self):
        currency = self.request.user.profile.currency if self.request.user.is_authenticated else 'USD'
        return {'currency': currency}


