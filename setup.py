from distutils.core import setup

# Dynamically calculate the version
version_tuple = __import__('addressbook').VERSION
if version_tuple[2] is not None:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]

setup(
    author = 'Simon Luijk',
    author_email = 'simon@simonluijk.com',
    name = 'django-addresses',
    version = version,
    description = 'Some forms around a few models to manage addresses',
    url = 'https://github.com/simonluijk/django-addresses',
    packages = [
        'addressbook',
        'addressbook.conf',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
