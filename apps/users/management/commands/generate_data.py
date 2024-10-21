from random import randint

from celery.utils.functional import first
from dateutil.tz import UTC
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from faker.proxy import Faker

from shops.models import Country, Book, Review
from users.models import User, Author, Address


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    model_list = {'user', 'author', 'address', 'book', 'review'}

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.f = Faker()
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        for model in self.model_list:
            parser.add_argument(f'--{model}', type=int, default=0)

    def _book(self, count=0):
        book_list = list()
        for _ in range(count):
            book = Book(
                
                overview=self.f.sentence(),
                used_good_price=self.f.numerify(),
                features=self.f.json(),
                new_price=self.f.numerify(),
                ebook_price=self.f.numerify(),
                audiobook_price=self.f.numerify(),
                reviews_count=self.f.numerify(),

            )
            book.save()
            author = Author.objects.order_by('?').first()
            book.author.set([author])
            book_list.append(book)

        Book.objects.bulk_create(book_list)
        self.stdout.write(self.style.SUCCESS(f"Book malumotlari {count} tadan qo'shildi"))

    def _user(self, count=0):
        user_list = list()
        for _ in range(count):
            user_list.append(User(
                email=self.f.email(domain='gmail.com'),
                name=self.f.name(),
                is_active=self.f.boolean(),
                password=make_password(self.f.password()),
                date_joined=self.f.date_time(tzinfo=UTC),
            ))
        User.objects.bulk_create(user_list)
        self.stdout.write(self.style.SUCCESS(f"User malumotlari {count} tadan qo'shildi"))

    def _author(self, count=0):
        author_list = list()
        for _ in range(count):
            author_list.append(Author(
                first_name=self.f.first_name(),
                last_name=self.f.last_name(),
                description=self.f.text()
            ))
        Author.objects.bulk_create(author_list)
        self.stdout.write(self.style.SUCCESS(f"Author malumotlari {count} tadan qo'shildi"))

    def _address(self, count=0):
        address_list = list()
        for _ in range(count):
            address_list.append(Address(
                first_name=self.f.first_name(),
                last_name=self.f.last_name(),
                address_line_1=self.f.address(),
                address_line_2=self.f.address(),
                city=self.f.city(),
                state=self.f.state(),
                postal_code=self.f.postalcode(),
                country_id=Country.objects.order_by('?').values_list('id', flat=True).first(),
                user_id=User.objects.order_by('?').values_list('id', flat=True).first(),

            ))
        Address.objects.bulk_create(address_list)
        self.stdout.write(self.style.SUCCESS(f"Address malumotlari {count} tadan qo'shildi"))

    def _review(self, count=0):
        review_list = []
        for _ in range(count):
            review_list.append(Review(
                name=self.f.name(),
                description=self.f.sentence(),
                start=randint(1, 5),
                book_id=Book.objects.order_by('?').values_list('id', flat=True).first(),
            ))
        Review.objects.bulk_create(review_list)
        self.stdout.write(self.style.SUCCESS(f"Review malumotlari {count} tadan qo'shildi"))


    def handle(self, *args, **options):
        for name in self.model_list & set(options):
            getattr(self, f'_{name}')(options[name])

        self.stdout.write(self.style.SUCCESS(f"Barcha malumotlar qo'shildi"))

        # try:
        #     poll = Poll.objects.get(pk=poll_id)
        # except Poll.DoesNotExist:
        #     raise CommandError('Poll "%s" does not exist' % poll_id)
        #