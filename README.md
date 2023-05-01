## django-addresses

django-addresses is a Django package that provides a simple way to store and manage postal addresses in your Django models. It supports common address fields such as street address, city, state/province, postal code, and country.
Installation

You can install django-addresses using pip:

```sh
pip install django-addresses
```

Then, add addresses to your INSTALLED_APPS setting in Django's settings.py file:

```python
INSTALLED_APPS = [
    # ...
    'addresses',
    # ...
]
```

Finally, run the migrations to create the necessary database tables:

```sh
python manage.py migrate addresses
```

## Usage

Here's a basic example of how to use django-addresses in your Django models:

```python
from django.db import models
from addresses.models import AddressField

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    address = AddressField(blank=True, null=True)
```

In this example, we've added an AddressField to a model called MyModel. The AddressField provides a convenient way to store and retrieve postal addresses, without having to define individual fields for each address component.

You can also access the individual components of an address (such as street address and postal code) using the Address object returned by the AddressField:

```python
my_model = MyModel.objects.create(
    name='John Doe',
    address=Address(
        street='123 Main St.',
        city='Anytown',
        state='CA',
        postal_code='12345',
        country='US'
    )
)

print(my_model.address.street) # prints '123 Main St.'
```

## Contributing

Contributions to django-addresses are always welcome! If you find a bug, have an idea for a new feature, or want to contribute code, please open an issue or submit a pull request on GitHub.

## License

django-addresses is released under the MIT License. See the LICENSE file for details.

## Setup development environment

To set up your development environment, it's important to have the necessary versions of Python and Django installed. Here's how you can do it:

Install pyenv to manage different versions of Python:

```sh
curl https://pyenv.run | bash
```

Install the following versions of Python with pyenv:

```sh
pyenv install 3.9.16 3.10.11 3.11.3
```

This will give you a range of Python versions to work with, including the latest releases.

Install Django in each of your Python environments:

```sh
pyenv global 3.11.3  # Set the version you want to use globally
python -m pip install Django==3.2.4  # Install Django for Python 3.11.3
# Repeat for each Python version you installed
```

Run tests using tox to ensure your code is compatible with all installed versions of Python:

```sh
tox -e django42-py3{9,10,11}
```

Before committing code, validate it using pre-commit. This will automatically run each time you commit changes:

```sh
python -m pip install pre-commit
pre-commit install
pre-commit run --all-files
```
