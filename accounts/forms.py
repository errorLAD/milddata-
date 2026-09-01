from django import forms
<<<<<<< HEAD
from django.contrib.auth import authenticate
=======
>>>>>>> 496b5bca247b3229a4c9b01e2990654b44a11985
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "you@company.com"}),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"placeholder": "Create a password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm password"})

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].lower()
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
<<<<<<< HEAD
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={"placeholder": "demo@demo.com or username", "autofocus": True}),
=======
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@company.com", "autofocus": True}),
>>>>>>> 496b5bca247b3229a4c9b01e2990654b44a11985
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Your password"}),
    )
<<<<<<< HEAD

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            user_obj = User.objects.filter(email__iexact=username_or_email).first() or User.objects.filter(username__iexact=username_or_email).first()
            if user_obj:
                self.user_cache = authenticate(self.request, username=user_obj.username, password=password)
            else:
                self.user_cache = authenticate(self.request, username=username_or_email, password=password)

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
=======
>>>>>>> 496b5bca247b3229a4c9b01e2990654b44a11985
