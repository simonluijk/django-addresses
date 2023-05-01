from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from addressbook.conf import settings


class Country(models.Model):
    iso_code = models.CharField(_("ISO code"), max_length=2, unique=True)
    name = models.CharField(_("name"), max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("country")
        verbose_name_plural = _("countries")


class TimeStampedModel(models.Model):
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Address(TimeStampedModel):
    contact_name = models.CharField(_("contact name"), max_length=50)
    address_one = models.CharField(_("address one"), max_length=50)
    address_two = models.CharField(_("address two"), max_length=50, blank=True)
    town = models.CharField(_("town"), max_length=50)
    county = models.CharField(_("county"), max_length=50, blank=True)
    postcode = models.CharField(_("postcode"), max_length=50)
    country = models.ForeignKey(
        Country, verbose_name=_("country"), on_delete=models.PROTECT
    )
    is_deleted = models.BooleanField(_("is deleted"), default=False)

    def __init__(self, *args, **kwargs):
        if settings.NORMALISE_TO_UPPER:
            for field in self._meta.get_fields():
                if isinstance(field, models.CharField):
                    try:
                        kwargs[field.name] = kwargs[field.name].upper()
                    except KeyError:
                        pass
        super(Address, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.contact_name

    def _output_html(self, template, separator):
        output = []
        rows = (
            self.contact_name,
            self.address_one,
            self.address_two,
            self.town,
            self.county,
            self.postcode,
            self.country,
        )
        for row in rows:
            if row:
                output.append(template % {"field": force_str(row)})
        return mark_safe(separator.join(output))

    def as_p(self):
        return self._output_html("%(field)s", "<br />\n")

    def save(self, *args, **kwargs):
        if settings.NORMALISE_TO_UPPER:
            for field in self._meta.get_fields():
                if isinstance(field, models.CharField):
                    setattr(self, field.name, getattr(self, field.name).upper())
        super(Address, self).save(*args, **kwargs)

    class Meta:
        ordering = ["created"]
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
        get_latest_by = "created"


class AddressField(models.ForeignKey):
    def __init__(self, **kwargs):
        kwargs.setdefault("to", Address)
        kwargs.setdefault("on_delete", models.PROTECT)
        super().__init__(**kwargs)
