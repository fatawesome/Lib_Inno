from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from login.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """
    A form for creating users. Includes all required fields and a repeated password.
    """

    subtype = forms.ChoiceField(label='User type', choices=[('Students', 'Students'), ('Visiting Professors', 'Visiting Professors'), ('Professors', 'Professors'),
               ('TAs', 'TAs'), ('Instructors', 'Instructors')], required=True)

    def __init__(self, *args, caller_is_admin=False, **kwargs):
        self.caller_is_admin = caller_is_admin
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if self.caller_is_admin:
            self.fields['subtype'].choices += [('Librarians (Priv1)', 'Librarians (Priv1)'),
                                               ('Librarians (Priv2)', 'Librarians (Priv2)'),
                                               ('Librarians (Priv3)', 'Librarians (Priv3)')]

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'address',
                  'subtype',
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

    def get_or_create_group(self, name):
        if Group.objects.filter(name=name).count() != 0:
            return Group.objects.get(name=name)
        group = Group.objects.create(name=name)
        return group

    def save(self, commit=True):
        """
        Saves the provided password in hashed format
        """

        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        if self.cleaned_data['subtype'] == 'Librarians (Priv1)':
            user.groups.add(self.get_or_create_group('Librarians (Priv1)'))
        elif self.cleaned_data['subtype'] == 'Librarians (Priv2)':
            user.groups.add(self.get_or_create_group('Librarians (Priv2)'))
        elif self.cleaned_data['subtype'] == 'Librarians (Priv3)':
            user.groups.add(self.get_or_create_group('Librarians (Priv3)'))
        elif self.cleaned_data['subtype'] == 'Students':
            user.groups.add(self.get_or_create_group('Students'))
        elif self.cleaned_data['subtype'] == 'Visiting Professors':
            user.groups.add(self.get_or_create_group('Visiting Professors'))
        else: # if self.cleaned_data['subtype'] equal 'Instructors' or 'TAs' or 'Professors'
            user.groups.add(self.get_or_create_group('Faculty'))

        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on the user,
    but replaces the password field with admin's password hash display field.
    """
    subtype = forms.ChoiceField(label='User type',
                                choices=[('Students', 'Students'), ('Visiting Professors', 'Visiting Professors'),
                                         ('Professors', 'Professors'),
                                         ('TAs', 'TAs'), ('Instructors', 'Instructors')], required=True)

    def __init__(self, *args, caller_is_admin=False, **kwargs):
        self.caller_is_admin = caller_is_admin
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        if self.caller_is_admin:
            self.fields['subtype'].choices += [('Librarians (Priv1)', 'Librarians (Priv1)'),
                                               ('Librarians (Priv2)', 'Librarians (Priv2)'),
                                               ('Librarians (Priv3)', 'Librarians (Priv3)')]

    class Meta:
        model = CustomUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'subtype',
                  'address',
                  )

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        """
        return self.initial['password']
