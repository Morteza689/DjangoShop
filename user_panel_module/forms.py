from django import forms
from account_module.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from order_module.models import Order

class EditUserOrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['posted','ref_code_post']

        widgets = {
            'posted': forms.CheckboxInput(attrs={
                'class': 'input-element',
            }),
            'ref_code_post': forms.NumberInput(attrs={
                'class': 'input-element'
            })}

        labels = {
            'posted': 'ارسال شده',
            'ref_code_post': 'کد پیگیری پست',
        }




class EditUserProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'abuot_user', 'national_code']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input-element',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input-element'
            }),
            'abuot_user': forms.Textarea(attrs={
                'class': 'input-element',
                'rows': 5,
            }),
            'national_code': forms.NumberInput(attrs={
                'class': 'input-element',
            })}

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'abuot_user': 'درباره',
            'national_code': 'کد ملی'
        }


class EditUserAddressForm(forms.Form):
    receiver=forms.CharField(
        label='گیرنده',
        widget=forms.TextInput(attrs={
            'class':'input-element'
        }),
        validators=[
        validators.MinLengthValidator(10)
        ])

    number_receiver=forms.IntegerField(
        label='شماره تلفن گیرنده',
        widget=forms.NumberInput(attrs={
            'class': 'input-element',
        }),
        )

    address = forms.CharField(
        label='آدرس',
        widget=forms.Textarea(attrs={
            'class': 'input-element',
            'rows': 5,
        }))

    zipcode = forms.IntegerField(
        label='کد پستی',
        widget=forms.NumberInput(attrs={
            'class': 'input-element',
        }))


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'class': 'input-element'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'input-element'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'input-element'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class ActiveNummerForm(forms.Form):
    number_active_code = forms.IntegerField(
        label='کد ارسال شده را وارد کنید',
        widget=forms.NumberInput(attrs={
            'class': 'input-element'
        }),
    )


class AddNumberForm(forms.Form):
    number = forms.IntegerField(
        label='شماره همراه',
        widget=forms.NumberInput(attrs={
            'class': 'input-element'
        }))