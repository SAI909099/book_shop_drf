from rest_framework.fields import HiddenField, CurrentUserDefault, IntegerField, BooleanField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from shops.models import Address, Country, Book, Author
from users.models import User



class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorModelSerializer(ModelSerializer):
    books = BookModelSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'description', 'books']


class WishlistModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'



class AddressListModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    postal_code = IntegerField(default=123400, min_value=0)
    has_shipping_address = BooleanField(write_only=True)
    has_billing_address = BooleanField(write_only=True)

    class Meta:
        model = Address
        exclude = ()

    def create(self, validated_data):
        _has_billing_address = validated_data.pop('has_billing_address')
        _has_shipping_address = validated_data.pop('has_shipping_address')

        _address = super().create(validated_data)
        _user: User = _address.user
        if _has_billing_address:
            _user.billing_address = _address
            _user.save()

        if _has_shipping_address:
            _user.shipping_address = _address
            _user.save()

        return _address

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['country'] = CountryModelSerializer(instance.country).data
        repr['has_billing_address'] = instance.user.billing_address_id == instance.id
        repr['has_shipping_address'] = instance.user.shipping_address_id == instance.id
        return repr



class BookDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        exclude = ()


class BookListModelSerializer(ModelSerializer):
    author = AuthorModelSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('title', 'slug', 'author', 'image')