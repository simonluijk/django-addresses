from django.contrib import admin
from addressbook.models import Country, Address


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("iso_code", "name")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("contact_name", "address_one", "county", "country", "is_deleted")
    list_filter = ("is_deleted",)
