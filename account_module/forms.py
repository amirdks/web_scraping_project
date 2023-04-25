import re

from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())

    def clean_email(self):
        value = self.cleaned_data.get("email")
        regex = r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$"
        matched = re.search(
            "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", value
        )
        if not matched:
            raise forms.ValidationError("ایمیل وارد شده معتبر نمیباشد")
        return value
