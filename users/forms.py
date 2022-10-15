from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    error_messages = {'error_password': "Passwords do not match or "
                                        "there are not enough characters!"}
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        required=True
    )
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
        model = User
        fields = ('email', 'password', 'password_confirmation',)

    def is_valid(self):
        if not self.errors:
            password = self.cleaned_data['password']
            password_confirmation = self.cleaned_data['password_confirmation']
            if password is True and password_confirmation is True and password != password_confirmation: # noqa
                self.errors.update(self.error_messages)
        return super().is_valid()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].split('@')[0]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
