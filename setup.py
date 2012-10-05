from distutils.core import setup

PACKAGE_NAME = 'django-addresses'

# Dynamically calculate the version
version_tuple = __import__('addressbook').VERSION
if version_tuple[2] is not None:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]

setup(
    author = 'Simon Luijk',
    author_email = 'simon@simonluijk.com',
    name = PACKAGE_NAME,
    version = version,
    description = 'Some forms around a few models to manage addresses',
    url = 'http://pypi.python.org/pypi/%s/' % PACKAGE_NAME,
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
