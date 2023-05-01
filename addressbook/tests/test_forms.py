from django.test import TestCase
from addressbook.conf import settings
from addressbook.forms import AddressForm


class FormTestCase(TestCase):
    fixtures = [
        "initial_data",
    ]

    def test_simple(self):
        form = AddressForm(
            {
                "contact_name": "Test name",
                "address_one": "Address One",
                "town": "Town",
                "postcode": "PostCode",
                "country": 1,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        data = form.cleaned_data
        data["country"] = str(data["country"])
        self.assertEqual(
            data,
            {
                "address_one": "Address One",
                "address_two": "",
                "contact_name": "Test name",
                "country": "AFGHANISTAN",
                "county": "",
                "postcode": "PostCode",
                "town": "Town",
            },
        )
