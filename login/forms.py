from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from login.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """
    A form for creating users. Includes all required fields and a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    class Meta:
        model = CustomUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'address',
                  'group',
                  )

    def clean_password2(self):
        """
        Check that two passwords match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        """
        Saves the provided password in hashed format
        """
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user,
    but replaces the password field with admin's password hash display field.
    """
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name',
                  'last_name',
                  'phone_number',
                  'group',
                  'address',
                  'is_admin',
                  'is_active',
                  )

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial['password']
