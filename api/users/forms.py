from allauth.account.forms import (
    SignupForm,
    LoginForm,
    AddEmailForm,
    ChangePasswordForm,
    SetPasswordForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    UserTokenForm,
)
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.socialaccount.forms import DisconnectForm
from allauth.mfa.base.forms import AuthenticateForm, ReauthenticateForm
from allauth.mfa.totp.forms import ActivateTOTPForm, DeactivateTOTPForm
from django.contrib.auth import forms as admin_forms
from django import forms
from django.forms import EmailField, CharField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation
from api.users.widgets import MyImageField

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField, "username": CharField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = (
            "email",
            "username",
        )
        field_classes = {"email": EmailField, "username": CharField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
            "username": {"unique": _("This username has already been taken.")},
        }


class UserForm(forms.ModelForm):
    email = EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("example@company.com"),
            },
        ),
    )
    username = CharField(
        label=_("User Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Admin"),
            },
        ),
    )

    first_name = CharField(
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Bonnie"),
            },
        ),
    )
    last_name = CharField(
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Green"),
            },
        ),
    )

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "images")
        widgets = {
            "images": MyImageField(),
        }

        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
            "username": {"unique": _("This username has already been taken.")},
        }

    def clean_username(self):
        return self.cleaned_data["username"].strip()

    def clean_images(self):
        return self.cleaned_data["images"]

    def clean_email(self):
        if self.cleaned_data["email"] == "":
            self.add_error("email", 'The field "Email" is required.')
        else:
            return self.cleaned_data["email"].strip()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):
        user = super().save()
        user.images = self.cleaned_data["images"]
        # pprint(user.images)
        user.save()
        return user


class UserSignupForm(SignupForm):
    # add form fields here
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    # add form fields here
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class MyCustomLoginForm(LoginForm):
    # add form fields here
    def login(self, *args, **kwargs):
        return super().login(*args, **kwargs)


class MyCustomAddEmailForm(AddEmailForm):
    # add form fields here
    def save(self, request):
        email_address_obj = super().save(request)
        return email_address_obj


class MyCustomChangePasswordForm(ChangePasswordForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomSetPasswordForm(SetPasswordForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomResetPasswordForm(ResetPasswordForm):
    # add form fields here
    def save(self, request):
        email_address = super().save(request)
        return email_address


class MyCustomResetPasswordKeyForm(ResetPasswordKeyForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomSocialDisconnectForm(DisconnectForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomReauthenticateForm(ReauthenticateForm):
    # add form fields here
    def save(self):
        super(MyCustomAuthenticateForm, self).save()


class MyCustomAuthenticateForm(AuthenticateForm):
    # add form fields here
    def save(self):
        super(MyCustomReauthenticateForm, self).save()


class MyCustomActivateTOTPForm(ActivateTOTPForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomUserTokenForm(UserTokenForm):
    # add form fields here
    def save(self):
        super().save()


class MyCustomDeactivateTOTPForm(DeactivateTOTPForm):
    # add form fields here
    def save(self):
        super().save()


class AdminUserCreateForm(forms.ModelForm):
    email = EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("example@company.com"),
            },
        ),
    )
    username = CharField(
        label=_("User Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Admin"),
            },
        ),
    )

    first_name = CharField(
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Bonnie"),
            },
        ),
    )
    last_name = CharField(
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Green"),
            },
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                ":type": "showPassword ? 'text' : 'password'",
                "class": "custom_text_input",
                "autocomplete": "current-password",
                "placeholder": _("Password"),
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        widget=forms.PasswordInput(
            attrs={
                ":type": "showPassword2 ? 'text' : 'password'",
                "class": "custom_text_input",
                "placeholder": _("Password (again)"),
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "images",
        )
        widgets = {
            "images": MyImageField(),
        }

        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
            "username": {"unique": _("This username has already been taken.")},
        }

    def clean_username(self):
        return self.cleaned_data["username"].strip()

    def clean_images(self):
        return self.cleaned_data["images"]

    def clean_email(self):
        # email = self.cleaned_data["email"].strip()
        # user = User.objects.filter(email__iexact=email).first()

        # if user:
        #     print(user)
        #     self.add_error("email", "Already Exists")
        # else:
        #     return email
        if self.cleaned_data["email"] == "":
            self.add_error("email", 'The field "Email" is required.')
        else:
            return self.cleaned_data["email"].strip()

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")
        if password != confirm_password:
            self.add_error("password1", "Password and confirm password does not match.")
        return cleaned_data

    def save(self):
        user = super().save()
        user.images = self.cleaned_data["images"]
        # pprint(user.images)
        user.save()
        return user


class AdminUserUpdateForm(forms.ModelForm):
    email = EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("example@company.com"),
            },
        ),
    )
    username = CharField(
        label=_("User Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Admin"),
            },
        ),
    )

    first_name = CharField(
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Bonnie"),
            },
        ),
    )
    last_name = CharField(
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={
                "class": "custom_text_input",
                "required": True,
                "placeholder": ("Green"),
            },
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "images",
            "is_superuser",
            "is_active",
        )
        widgets = {
            "images": MyImageField(),
            "is_superuser": forms.CheckboxInput(
                attrs={"class": "custom_checkbox_input", "required": False}
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "custom_checkbox_input", "required": False}
            ),
        }

        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
            "username": {"unique": _("This username has already been taken.")},
        }

    def clean_username(self):
        return self.cleaned_data["username"].strip()

    # def clean_images(self):
    #     return self.cleaned_data["images"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        user = User.objects.filter(email__iexact=email).first()
        # print(user)
        if not user:
            self.add_error("email", "Already Exists")
        else:
            return email

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self):
        user = super().save()
        # user.images = self.cleaned_data["images"]
        # pprint(user.images)
        user.save()
        return user
