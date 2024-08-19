from django import forms
from .models import ShippingDetails,Listing,Review



class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone', max_length=15)
    city = forms.CharField(label='City', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    role = forms.ChoiceField(label='Select Role', choices=[('buyer', 'Buyer'), ('seller', 'Seller')])



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'img1', 'img2', 'img3', 'ram', 'rom', 'model']





class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']









class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        fields = ['name', 'email', 'phone_number', 'city', 'address', 'listing']
        widgets = {
            'listing': forms.HiddenInput(),
        }



