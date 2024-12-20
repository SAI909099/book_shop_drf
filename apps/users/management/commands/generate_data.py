# from decimal import Decimal
# from random import randint
#
# from celery.utils.functional import first
# from dateutil.tz import UTC
# from django.contrib.auth.hashers import make_password
# from django.core.management.base import BaseCommand
# from faker.generator import random
# from faker.proxy import Faker
#
# from shops.models import Country, Book, Review , Author
# from users.models import User,  Address
#
#
# class Command(BaseCommand):
#     help = "Closes the specified poll for voting"
#     model_list = {'user', 'author', 'address', 'book', 'review'}
#
#     def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
#         self.f = Faker()
#         super().__init__(stdout, stderr, no_color, force_color)
#
#     def add_arguments(self, parser):
#         for model in self.model_list:
#             parser.add_argument(f'--{model}', type=int, default=0)
#
#     def _book(self, count=0):
#         book_list = []
#
#         for _ in range(count):
#             book = Book(
#                 overview=self.f.sentence(),
#                 used_good_price=self.f.numerify(),
#                 new_price=self.f.numerify(),
#                 ebook_price=self.f.numerify(),
#                 audiobook_price=self.f.numerify(),
#                 reviews_count=self.f.numerify(),
#                 features={
#                     'format': random.choice(['hardcover', 'softcover']),
#                     'publisher': self.f.company(),
#                     'pages': self.f.random_int(min=100, max=1000),
#                     'dimensions': f"{random.uniform(5.0, 8.0):.2f} x {random.uniform(8.0, 12.0):.2f} x {random.uniform(0.5, 2.0):.2f} inches",
#                     'shipping_weight': round(random.uniform(0.5, 5.0), 2),
#                     'languages': random.choice(['English', 'Spanish', 'French', 'German', 'Chinese']),
#                     'publication_date': str(self.f.date_this_century()),
#                     'isbn_13': self.f.random_int(9780000000000, 9789999999999),
#                     'isbn_10': self.f.random_int(1000000000, 9999999999),
#                     'edition': random.choice([1, 2, 3, None]),
#                 }
#             )
#             book_list.append(book)
#
#         Book.objects.bulk_create(book_list)
#
#         for book in book_list:
#             author = Author.objects.order_by('?').first()
#             if author:
#                 book.author.add(author)
#
#         self.stdout.write(self.style.SUCCESS(f"Books malumotlari {count} tadan qo'shildi "))
#
#
#     def _user(self, count=0):
#         user_list = list()
#         for _ in range(count):
#             user_list.append(User(
#                 email=self.f.email(domain='gmail.com'),
#                 name=self.f.name(),
#                 is_active=self.f.boolean(),
#                 password=make_password(self.f.password()),
#                 date_joined=self.f.date_time(tzinfo=UTC),
#             ))
#         User.objects.bulk_create(user_list)
#         self.stdout.write(self.style.SUCCESS(f"User malumotlari {count} tadan qo'shildi"))
#
#     def _author(self, count=0):
#         author_list = list()
#         for _ in range(count):
#             author_list.append(Author(
#                 first_name=self.f.first_name(),
#                 last_name=self.f.last_name(),
#                 description=self.f.sentence(),
#             ))
#         Author.objects.bulk_create(author_list)
#         self.stdout.write(self.style.SUCCESS(f"Author malumotlari {count} tadan qo'shildi"))
#
#     def _address(self, count=0):
#         address_list = list()
#         for _ in range(count):
#             address_list.append(Address(
#                 first_name=self.f.first_name(),
#                 last_name=self.f.last_name(),
#                 address_line_1=self.f.address(),
#                 address_line_2=self.f.address(),
#                 city=self.f.city(),
#                 state=self.f.state(),
#                 postal_code=self.f.postalcode(),
#                 country_id=Country.objects.order_by('?').values_list('id', flat=True).first(),
#                 user_id=User.objects.order_by('?').values_list('id', flat=True).first(),
#
#             ))
#         Address.objects.bulk_create(address_list)
#         self.stdout.write(self.style.SUCCESS(f"Address malumotlari {count} tadan qo'shildi"))
#
#     def _review(self, count=0):
#         review_list = []
#         for _ in range(count):
#             review_list.append(Review(
#                 name=self.f.name(),
#                 description=self.f.sentence(),
#                 # start=randint(1, 5),
#                 book_id=Book.objects.order_by('?').values_list('id', flat=True).first(),
#             ))
#         Review.objects.bulk_create(review_list)
#         self.stdout.write(self.style.SUCCESS(f"Review malumotlari {count} tadan qo'shildi"))
#
#
#     def handle(self, *args, **options):
#         for name in self.model_list & set(options):
#             getattr(self, f'_{name}')(options[name])
#
#         self.stdout.write(self.style.SUCCESS(f"Barcha malumotlar qo'shildi"))
#
#         # try:
#         #     poll = Poll.objects.get(pk=poll_id)
#         # except Poll.DoesNotExist:
#         #     raise CommandError('Poll "%s" does not exist' % poll_id)
#         #


from dateutil.tz import UTC
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker.proxy import Faker

from shops.models import Book, Section, Review, Category, Author, Country, Cart
from users.models import User, Address


class Command(BaseCommand):
    model_list = {'user', 'author', 'address', 'book', 'section', 'cart', 'review', 'category'}

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.f = Faker()
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        for model in self.model_list:
            parser.add_argument(f'--{model}', type=int, default=0)

    def _book(self):
        return Book(
            # slug=self.f.slug(),
            title=self.f.name(),
            used_good_price=self.f.pydecimal(left_digits=4, right_digits=2, positive=True),
            new_price=self.f.pydecimal(left_digits=4, right_digits=2, positive=True),
            ebook_price=self.f.pydecimal(left_digits=4, right_digits=2, positive=True),
            audiobook_price=self.f.pydecimal(left_digits=4, right_digits=2, positive=True),
            image=self.f.image_url(),
            overview=self.f.paragraph(),
            features={
                "format": self.f.random_element(elements=["Paperback", "Hardcover"]),
                "publisher": self.f.company(),
                "pages": self.f.random_int(min=50, max=1000),
                "dimensions": f"{self.f.random_number(digits=2)} x {self.f.random_number(digits=2)} x {self.f.random_number(digits=2)} inches",
                "shipping_weight": round(self.f.pyfloat(left_digits=1, right_digits=2, positive=True), 2),
                "languages": self.f.language_name(),
                "publication_date": self.f.date(),
                "isbn_13": self.f.isbn13(separator=""),
                "isbn_10": self.f.isbn10(separator=""),
                "edition": self.f.random_int(min=1, max=10),
            },
            format=self.f.random_element(elements=[Book.Format.HARDCOVER, Book.Format.PAPERBACK]),
            category_id=Category.objects.order_by('?').values_list('id', flat=True).first(),
        )

    def _user(self):
        return User(
            email=self.f.email(domain='gmail.com'),
            name=self.f.name(),
            is_active=self.f.boolean(),
            password=make_password(self.f.password()),
            date_joined=self.f.date_time(tzinfo=UTC),
        )

    def _address(self):
        return Address(
            first_name=self.f.first_name(),
            last_name=self.f.last_name(),
            address=self.f.address(),
            city=self.f.city(),
            state=self.f.state(),
            postal_code=self.f.postalcode(),
            phone_number=self.f.phone_number(),
            country_id=Country.objects.order_by('?').values_list('id', flat=True).first(),
            user_id=User.objects.order_by('?').values_list('id', flat=True).first(),
        )

    def _section(self):
        return Section(
            name_image=self.f.image_url(),
            intro=self.f.text(),
            banner=self.f.image_url(),
        )

    def _cart(self):
        return Cart(
            book_id=Book.objects.order_by('?').values_list('id', flat=True).first(),
            user_id=User.objects.order_by('?').values_list('id', flat=True).first(),
            quantity=self.f.random_int(min=1, max=100),
            format=self.f.text(),
            condition=self.f.text(),
            seller=self.f.user_name(),
            ship_from=self.f.address(),
        )

    def _review(self):
        return Review(
            name=self.f.name(),
            description=self.f.text(),
            stars=self.f.random_int(min=1, max=10),
            book_id=Book.objects.order_by('?').values_list('id', flat=True).first()
        )

    def _author(self):
        return Author(
            first_name=self.f.first_name(),
            last_name=self.f.last_name(),
            description=self.f.text(),
        )

    def _category(self):
        return Category.objects.insert_node(
            Category(
                name=self.f.word(),
                parent_id=Category.objects.order_by('?').values_list('id', flat=True).first(),
                section_id=Section.objects.order_by('?').values_list('id', flat=True).first()
            ),
            None
        )

    def _generate_object(self, cls, name, count=0):
        if name == 'book':
            for _ in range(count):
                book = self._book()
                book.save()
                book.author.set([Author.objects.order_by('?').first()])
        else:
            cls.objects.bulk_create([getattr(self, f'_{name}')() for _ in range(count)])
        self.stdout.write(self.style.SUCCESS(f"{cls.__name__} malumotlari {count} tadan qo'shildi"))

    def handle(self, *args, **options):
        _models = globals()
        for name in self.model_list & set(options):
            if options[name]:
                self._generate_object(_models[name.capitalize()], name, options[name])

        self.stdout.write(self.style.SUCCESS(f"Barcha malumotlar qo'shildi"))