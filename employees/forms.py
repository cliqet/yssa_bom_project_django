from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from .models import Employee
from utilities.password import get_password_help_text, get_password_pattern


password_help_text = get_password_help_text()

# Regex pattern for password validation
password_validator = RegexValidator(
    regex=get_password_pattern(),
    message=password_help_text
)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput,
        validators=[password_validator],  
        help_text=password_help_text)
    password2 = forms.CharField(
        label="Password confirmation", 
        widget=forms.PasswordInput,
        help_text='Confirm password'
    )

    class Meta:
        model = Employee
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = (
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can "
            "change the password <a href=\"%s\"><strong>here</strong></a>."
        ) % reverse_lazy('admin:auth_user_password_change', args=[self.instance.id])

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Employee
        fields = '__all__'
