from django import forms

from store.models import User,Order

from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Password"}),label="Enter Password")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm Password"}),label="Confirm Password")

    class Meta:

        model=User

        fields=["username","email","phone"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Username"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter E-mail"}),
            "phone":forms.TextInput(attrs={"class":"form-control ","placeholder":"Enter Phone Number"})
        }


class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":'form-control','placeholder':'Enter User Name'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control','placeholder':'Enter Password'}))


class OrderForm(forms.ModelForm):

    class Meta:

        model=Order

        fields=["address","phone","payment_method","pincode"]

        widgets={

            "address":forms.Textarea(attrs={"class":"","placeholder":"Enter Address"}),
            "phone":forms.TextInput(attrs={"class":"","placeholder":"Enter Phone"}),
            "payment_method":forms.Select(choices=Order.PAYMENT_OPTIONS,attrs={"class":""}),
        }