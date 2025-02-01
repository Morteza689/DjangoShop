from django import forms
from .models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields=['full_name','email','title','message']
        widgets={
            'full_name':forms.TextInput(attrs={
                'class':'form-control',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows':5,
                'id': 'message'
            })}
        labels={
            'full_name':'نام و نام خانوادگی' ,
            'email':'ایمیل'
        }
        error_messages={
            'full_name':{
                'required':'نام و نام خانوادگی راوارد کنید'
            }
        }













# class ContactUsForm(forms.Form):
#     full_name=forms.CharField(
#         label='نام و نام خانوادگی',
#         max_length=50,
#         error_messages={
#             'required' : 'نام و نام خانوادگی خود را وارد کنید'
#         },
#         widget=forms.TextInput(attrs={
#             'class':'form-control',
#             'placeholder':'نام نام خانوادگی',
#         }))
#
#
#
#     email=forms.EmailField(label='ایمیل',
#         error_messages={
#             'required':'ایمیل خود را وارد کنید'
#         },
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'ایمیل',
#         }))
#
#
#     title=forms.CharField(label='عنوان',
#         error_messages={
#             'required':'عنوان را وارد کنید'
#         },
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'عنوان',
#         }))
#
#     message = forms.CharField(
#         label='متن پیام',
#         error_messages={
#             'required':'متن پیام را وارد کنید'
#         },
#         widget = forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'متن پیام',
#             'id':'message'
#     }))


