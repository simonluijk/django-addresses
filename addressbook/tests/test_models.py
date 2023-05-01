from django.test import TestCase, override_settings
from django.utils import timezone
from unittest.mock import patch
from addressbook.conf import settings
from addressbook.models import Address, Country


class AddressTestCase(TestCase):
    fixtures = [
        "initial_data",
    ]

    @override_settings(USE_TZ=True)
    def test_timestamps(self):
        fixed_create = timezone.datetime(2023, 4, 27, tzinfo=timezone.utc)
        fixed_modified = timezone.datetime(2023, 4, 28, tzinfo=timezone.utc)
        with patch.object(timezone, "now", return_value=fixed_create):
            address = Address.objects.create(
                contact_name="Contact Name",
                address_one="one",
                town="town",
                county="county",
                postcode="post",
                country=Country.objects.get(pk=1),
            )

        self.assertEqual(address.created, fixed_create)
        self.assertEqual(address.modified, fixed_create)

        with patch.object(timezone, "now", return_value=fixed_modified):
            address.save()

        self.assertEqual(address.created, fixed_create)
        self.assertEqual(address.modified, fixed_modified)

    def test_add_address(self):
        saved = settings.NORMALISE_TO_UPPER

        settings.NORMALISE_TO_UPPER = False
        address = Address.objects.create(
            contact_name="Contact Name",
            address_one="one",
            address_two="two",
            town="town",
            county="county",
            postcode="post",
            country=Country.objects.get(pk=1),
        )
        self.assertEqual(str(address), "Contact Name")
        self.assertEqual(address.contact_name, "Contact Name")

        settings.NORMALISE_TO_UPPER = True
        address = Address.objects.create(
            contact_name="Contact Name",
            address_one="one",
            address_two="two",
            town="town",
            county="county",
            postcode="post",
            country=Country.objects.get(pk=1),
        )
        self.assertEqual(str(address), "CONTACT NAME")
        self.assertEqual(address.contact_name, "CONTACT NAME")
        self.assertEqual(address.address_one, "ONE")
        self.assertEqual(address.address_two, "TWO")
        self.assertEqual(address.town, "TOWN")
        self.assertEqual(address.county, "COUNTY")
        self.assertEqual(address.postcode, "POST")
        self.assertEqual(address.country.name, "AFGHANISTAN")

        settings.NORMALISE_TO_UPPER = saved

    def test_print_address(self):
        address = Address.objects.create(
            contact_name="Contact Name",
            address_one="one",
            address_two="two",
            town="town",
            county="county",
            postcode="post",
            country=Country.objects.get(pk=1),
        )
        self.assertEqual(
            address.as_p(),
            "CONTACT NAME<br />\nONE<br />\nTWO<br />\nTOWN<br />\nCOUNTY<br />\nPOST<br />\nAFGHANISTAN",
        )
        address = Address.objects.create(
            contact_name="Contact Name",
            address_one="one",
            town="town",
            county="county",
            postcode="post",
            country=Country.objects.get(pk=1),
        )
        self.assertEqual(
            address.as_p(),
            "CONTACT NAME<br />\nONE<br />\nTOWN<br />\nCOUNTY<br />\nPOST<br />\nAFGHANISTAN",
        )
