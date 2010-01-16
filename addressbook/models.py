from datetime import datetime

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from addressbook.conf import settings


class Country(models.Model):
    iso_code = models.CharField(_('ISO code'), max_length=2, unique=True)
    name = models.CharField(_('name'), max_length=60)


    def __unicode__(self):
        return self.name


    class Meta:
        ordering = ['name']
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class Address(TimeStampedModel):
    STATUS = [(0, 'Active'), (1, 'Display only'), (2, 'Deleted')]
    contact_name = models.CharField(_('contact name'), max_length=50)
    address_one = models.CharField(_('address one'), max_length=50)
    address_two = models.CharField(_('address two'), max_length=50, blank=True)
    town = models.CharField(_('town'), max_length=50)
    county = models.CharField(_('county'), max_length=50, blank=True)
    postcode = models.CharField(_('postcode'), max_length=50)
    country = models.ForeignKey(Country, verbose_name=_('country'))
    status = models.IntegerField(_('status'), choices=STATUS, default=0)


    def __init__(self, *args, **kwargs):
        if settings.NORMALISE_TO_UPPER:
            if 'contact_name' in kwargs:
                kwargs['contact_name'] = kwargs['contact_name'].upper()
            if 'address_one' in kwargs:
                kwargs['address_one'] = kwargs['address_one'].upper()
            if 'address_two' in kwargs:
                kwargs['address_two'] = kwargs['address_two'].upper()
            if 'town' in kwargs:
                kwargs['town'] = kwargs['town'].upper()
            if 'county' in kwargs:
                kwargs['county'] = kwargs['county'].upper()
            if 'postcode' in kwargs:
                kwargs['postcode'] = kwargs['postcode'].upper()
        super(Address, self).__init__(*args, **kwargs)


    def __unicode__(self):
        return self.contact_name


    def _output_html(self, template, seperator=None):
        output = []
        for row in [self.contact_name, self.address_one, self.address_two,
                    self.town, self.county, self.postcode, self.country]:
            if row:
                output.append(template % {'field': force_unicode(row)})
        if not seperator:
            seperator = u'\n'
        return mark_safe(seperator.join(output))


    def as_p(self):
        return self._output_html(u'%(field)s', u'<br />\n')


    def save(self, *args, **kwargs):
        if settings.NORMALISE_TO_UPPER:
            self.contact_name = self.contact_name.upper()
            self.address_one = self.address_one.upper()
            self.address_two = self.address_two.upper()
            self.town = self.town.upper()
            self.county = self.county.upper()
            self.postcode = self.postcode.upper()
        super(Address, self).save(*args, **kwargs)


    class Meta:
        ordering = ['created']
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
        get_latest_by = 'created'
