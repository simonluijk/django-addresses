from django.apps import apps
from django.test import TransactionTestCase
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.utils import timezone


class TestMigrations(TransactionTestCase):
    """
    A base test case to test migrations.
    """

    migrate_from = None
    migrate_to = None

    def getApps(self, config):
        return self.executor.loader.project_state(config).apps

    def setUp(self):
        assert (
            self.migrate_from and self.migrate_to
        ), "TestCase '{}' must define migrate_from and migrate_to".format(
            type(self).__name__
        )

        app_name = apps.get_containing_app_config(type(self).__module__).name
        self.migrate_from = [
            (
                app_name,
                self.migrate_from,
            )
        ]

        self.migrate_to = [
            (
                app_name,
                self.migrate_to,
            )
        ]

        self.executor = MigrationExecutor(connection)

        # Reverse to the original migration
        self.executor.migrate(self.migrate_from)

        # Set up any pre-migration state
        self.setUpBeforeMigration()

        # Run the migration to test
        self.executor.loader.build_graph()
        self.executor.migrate(self.migrate_to)

        # Set up any post-migration state
        self.setUpAfterMigration()

    def setUpBeforeMigration(self):
        """
        Override this method to set up any pre-migration state.
        """

    def setUpAfterMigration(self):
        """
        Override this method to set up any post-migration state.
        """


class IsDeletedForwardMigration(TestMigrations):
    available_apps = ["addressbook"]
    migrate_from = "0001_initial"
    migrate_to = "0002_auto_20230427_1033"

    def setUpBeforeMigration(self):
        apps = self.getApps(self.migrate_from)
        Address = apps.get_model("addressbook", "Address")
        Country = apps.get_model("addressbook", "Country")

        country = Country.objects.create(name="Example")

        self.address1 = Address.objects.create(
            contact_name="name",
            address_one="one",
            town="town",
            county="county",
            postcode="post",
            country=country,
            status=0,
        )
        self.address2 = Address.objects.create(
            contact_name="name",
            address_one="one",
            town="town",
            county="county",
            postcode="post",
            country=country,
            status=2,
        )

    def test_forward_migration(self):
        apps = self.getApps(self.migrate_to)
        Address = apps.get_model("addressbook", "Address")
        address1 = Address.objects.get(pk=self.address1.pk)
        address2 = Address.objects.get(pk=self.address2.pk)

        self.assertFalse(address1.is_deleted)
        self.assertTrue(address2.is_deleted)


class IsDeletedBackwardMigration(TestMigrations):
    available_apps = ["addressbook"]
    migrate_from = "0002_auto_20230427_1033"
    migrate_to = "0001_initial"

    def setUpBeforeMigration(self):
        apps = self.getApps(self.migrate_from)
        Address = apps.get_model("addressbook", "Address")
        Country = apps.get_model("addressbook", "Country")

        country = Country.objects.create(name="Example")

        self.address1 = Address.objects.create(
            contact_name="name",
            address_one="one",
            town="town",
            county="county",
            postcode="post",
            country=country,
            is_deleted=False,
        )
        self.address2 = Address.objects.create(
            contact_name="name",
            address_one="one",
            town="town",
            county="county",
            postcode="post",
            country=country,
            is_deleted=True,
        )

    def test_forward_migration(self):
        apps = self.getApps(self.migrate_to)
        Address = apps.get_model("addressbook", "Address")
        address1 = Address.objects.get(pk=self.address1.pk)
        address2 = Address.objects.get(pk=self.address2.pk)

        self.assertEqual(address1.status, 0)
        self.assertEqual(address2.status, 2)
