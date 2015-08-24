from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label=_("Username"), error_messages={
            'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    # new_password = forms.CharField(
    #     widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
    #     label=_("Password (again)"))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)

    # def clean_username(self):
    #     try:
    #         user = User.objects.get(username__iexact=self.cleaned_data['username'])
    #     except User.DoesNotExist:
    #         return self.cleaned_data['username']
    #     raise forms.ValidationError(_("The username already exists. Please try another one."))
    #
    # def clean(self):
    #     if 'password' in self.cleaned_data and 'new_password' in self.cleaned_data:
    #         if self.cleaned_data['password'] != self.cleaned_data['new_password']:
    #             raise forms.ValidationError(_("The two password fields did not match."))
    #     return self.cleaned_data