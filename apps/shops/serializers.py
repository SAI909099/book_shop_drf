from rest_framework.serializers import ModelSerializer

from shops.models import Address, Country, Book


class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class AddressModelSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'



class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class WishlistModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
