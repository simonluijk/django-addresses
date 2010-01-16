import unittest

from addressbook.conf import settings
from addressbook.models import Address, Country


class AddressTestCase(unittest.TestCase):
    def testAddAddress(self):
        saved = settings.NORMALISE_TO_UPPER

        settings.NORMALISE_TO_UPPER = False
        address = Address.objects.create(
            contact_name = "name",
            address_one = "one",
            address_two = "two",
            town = "town",
            county = "county",
            postcode = "post",
            country = Country.objects.get(pk=1)
        )
        self.assertEquals(address.contact_name, 'name')

        settings.NORMALISE_TO_UPPER = True
        address = Address.objects.create(
            contact_name = "name",
            address_one = "one",
            address_two = "two",
            town = "town",
            county = "county",
            postcode = "post",
            country = Country.objects.get(pk=1)
        )
        self.assertEquals(address.contact_name, 'NAME')
        self.assertEquals(address.address_one, 'ONE')
        self.assertEquals(address.address_two, 'TWO')
        self.assertEquals(address.town, 'TOWN')
        self.assertEquals(address.county, 'COUNTY')
        self.assertEquals(address.postcode, 'POST')
        self.assertEquals(address.country.name, 'AFGHANISTAN')

        settings.NORMALISE_TO_UPPER = saved


    def testPrintAddress(self):
        address = Address.objects.create(
            contact_name = "name",
            address_one = "one",
            address_two = "two",
            town = "town",
            county = "county",
            postcode = "post",
            country = Country.objects.get(pk=1)
        )
        self.assertEquals(address.as_p(), 
            'NAME<br />\nONE<br />\nTWO<br />\nTOWN<br />\nCOUNTY<br />\nPOST<br />\nAFGHANISTAN'
        )
        address = Address.objects.create(
            contact_name = "name",
            address_one = "one",
            town = "town",
            county = "county",
            postcode = "post",
            country = Country.objects.get(pk=1)
        )
        self.assertEquals(address.as_p(), 
            'NAME<br />\nONE<br />\nTOWN<br />\nCOUNTY<br />\nPOST<br />\nAFGHANISTAN'
        )
