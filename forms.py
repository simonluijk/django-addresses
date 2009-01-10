from django import forms
from addressbook.models import Address


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('status',)


class AddAddressUpperForm(AddAddressForm):
    def clean(self):
        for key in self.cleaned_data.keys():
            if isinstance(self.cleaned_data[key], unicode):
                self.cleaned_data[key] = self.cleaned_data[key].upper()
        return self.cleaned_data
