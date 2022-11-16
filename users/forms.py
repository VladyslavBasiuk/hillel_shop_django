from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField


class SignUpForm(forms.ModelForm):
    error_messages = {'error_password': "Passwords do not match or "
                                        "there are not enough characters!"}
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        required=True
    )
    phone = PhoneNumberField(
        label='Phone',
        required=True)
    password = forms.CharField(
        min_length=6,
        max_length=24,
        label='Type your password',
        widget=forms.PasswordInput(),
        required=True
    )
    password_confirmation = forms.CharField(
        min_length=6,
        max_length=24,
        label='Confirm your password',
        widget=forms.PasswordInput(),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'phone', 'password', 'password_confirmation',)

    def is_valid(self):
        if not self.errors:
            password = self.cleaned_data['password']
            password_confirmation = self.cleaned_data['password_confirmation']
            if password is True and password_confirmation is True and password != password_confirmation:  # noqa
                self.errors.update(self.error_messages)
        return super().is_valid()

    def clean(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if password and password_confirmation \
                and password != password_confirmation:
            raise ValidationError("Passwords aren't equal")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_phone_valid = True
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             required=False)
    phone = forms.CharField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        phone = self.cleaned_data.get('phone')

        if not username and not phone:
            raise ValidationError('Email ot phone number is required')
        if password:
            kwargs = {'password': password, 'username': username}
            if phone and not username:
                kwargs.pop('username')
                kwargs.update({'phone': phone})
            self.user_cache = authenticate(self.request, **kwargs)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
