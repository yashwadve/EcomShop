from django import forms
from accounts.models import Address


class CheckoutForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        empty_label=None,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            profile = getattr(user, 'profile', None)
            if profile:
                self.fields['address'].queryset = profile.addresses.all()