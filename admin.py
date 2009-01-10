from django.contrib import admin
from addressbook.models import Country, Address


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'iso_code',
        'name'
    )

class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'contact_name',
        'address_one',
        'county',
        'country',
        'status'
    )


admin.site.register(Country, CountryAdmin)
admin.site.register(Address, AddressAdmin)
