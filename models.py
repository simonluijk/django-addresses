from datetime import datetime

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class Country(models.Model):
    iso_code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'countries'


class Address(models.Model):
    STATUS = [
        (0, 'Active'),
        (1, 'Display only'),
        (2, 'Deleted'),
    ]
    contact_name = models.CharField(max_length=50)
    address_one = models.CharField(max_length=50)
    address_two = models.CharField(max_length=50, blank=True)
    town = models.CharField(max_length=50)
    county = models.CharField(max_length=50, blank=True)
    postcode = models.CharField(max_length=50)
    country = models.ForeignKey(Country)
    status = models.IntegerField(choices=STATUS, default=0)

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    def __unicode__(self):
        return self.contact_name

    def _output_html(self, template, seperator=None):
        output = []
        for row in [self.contact_name, self.address_one, self.address_two, self.town, self.county, self.postcode, self.country]:
            if row:
                output.append(template % {'field': force_unicode(row)})
        if not seperator:
            seperator = u'\n'
        return mark_safe(seperato.join(output))

    def as_p(self):
        return self._output_html('%(field)s', '<br />\n')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = datetime.today()
        self.updated = datetime.today()
        super(Address, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name_plural = 'addresses'
