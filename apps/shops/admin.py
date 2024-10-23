from django.contrib import admin
from django.contrib.admin import ModelAdmin
from mptt.admin import DraggableMPTTAdmin

from shops.models import Book, Address, Category, Section


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryModelAdmin(DraggableMPTTAdmin):
    pass

@admin.register(Section)
class SectionModelAdmin(ModelAdmin):
    pass