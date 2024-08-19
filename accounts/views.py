
from django.contrib.auth.decorators import login_required
from accounts.models import Listing, ShippingDetails, contact, Listing
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import RegistrationForm,ListingForm, ReviewForm,LoginForm, ShippingForm
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse





def home_view(request):
    listings = Listing.objects.all()
    return render(request, 'accounts/home.html', {'listings': listings})



def register_view(request):
    error_message = None  # Initialize error message variable
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            # Check if the username already exists
            User = get_user_model()  # Get the custom user model
            if User.objects.filter(username=username).exists():
                # If the username already exists, set the error message
                error_message = "Username already exists. Please choose a different username."
            else:
                # If the username is unique, create the new user
                user = User.objects.create_user(username=username, password=password)
                if role == 'buyer':
                    user.is_buyer = True
                elif role == 'seller':
                    user.is_seller = True
                user.save()
                # Redirect to respective dashboard
                if user.is_buyer:
                    return redirect('home')
                elif user.is_seller:
                    return redirect('seller_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form, 'error_message': error_message})



def custom_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_authenticated:
                    if user.is_buyer:
                        return redirect('home')  # Redirect buyer to buyer dashboard
                    elif user.is_seller:
                        return redirect('seller_dashboard')  # Redirect seller to seller dashboard
            else:
                messages.error(request, 'Invalid username or password')  # Display error message
    else:
        form = LoginForm()
    return render(request, 'accounts/custom_login.html', {'form': form})




def seller_dashboard(request):
    seller_listings = Listing.objects.filter(seller=request.user)
    return render(request, 'accounts/seller_dashboard.html', {'seller_listings': seller_listings})


def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.seller = request.user
            # Check if images were uploaded
            if 'images' in request.FILES:
                new_listing.images = request.FILES['images']
            new_listing.save()
            return redirect('home')  # Redirect to home page after saving listing
    else:
        form = ListingForm()

    return render(request, 'accounts/add_listing.html', {'form': form})




def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = ListingForm(instance=listing)

    return render(request, 'accounts/edit_listing.html', {'form': form})



def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        listing.delete()
        return redirect('seller_dashboard')
    return redirect('seller_dashboard')


def listing_detail_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    return render(request, 'accounts/listing_detail.html', {'listing': listing})




def buy_now(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    return redirect('home')


@login_required
def shipping_form_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == 'POST':
        data = request.POST.copy()
        data['listing'] = listing
        data['listing_id'] = listing.pk
        form = ShippingForm(data)
        if form.is_valid():
            shipping_details = form.save(commit=False)
            shipping_details.user = request.user
            shipping_details.save()

            # Redirect to payment selection with the shipping details ID
            return redirect('payment_selection', shipping_id=shipping_details.pk)
    else:
        form = ShippingForm()

    return render(request, 'accounts/shipping_form.html', {'listing': listing, 'form': form})




def payment_selection(request, shipping_id):
    shipping_details = get_object_or_404(ShippingDetails, pk=shipping_id)

    return render(request, 'accounts/payment_selection.html', {'shipping_details': shipping_details})





def process_payment(request, pk):
    print('----------------------------pk', pk)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method == 'cash_on_delivery':

            return render(request, 'accounts/order_success.html', {'payment_method': 'Cash on Delivery','listing_id':pk})

        elif payment_method == 'card_payment':

            return redirect('checkout', pk=pk)

    return render(request, 'error.html')

def error_view(request):
    return render(request, 'error.html')






stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request, pk):
    print('pk++++++++++++++++++++++++++++++++++++++++++', pk)
    listing = get_object_or_404(Listing, id=pk)
    amount = int(listing.price * 100)
    if request.method == 'POST':

        token = request.POST['stripeToken']

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Example charge',
                source=token,
            )

            return redirect('payment_success',listing_id=pk)
        except stripe.error.CardError as e:
            # Card was declined
            return render(request, 'accounts/checkout.html', {'error': e.error.message,'pk':pk})

    return render(request, 'accounts/checkout.html', {'pk':pk,'amount':amount})


def payment_success(request,listing_id):
    return render(request, 'accounts/order_success.html', {'listing_id':listing_id})



@csrf_exempt
def stripe_webhook(request):

    return HttpResponse(status=200)



def leave_review_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.reviewer = request.user
            review.save()
            return redirect('listing_detail', listing_id=listing.id)
    else:
        form = ReviewForm()
    return render(request, 'accounts/leave_review.html', {'form': form, 'listing': listing})


def about(request):
    return render(request, 'accounts/about.html')


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if name and email and message:
            contact.objects.create(name=name, email=email, message=message)
            return redirect('/')
    return render(request, 'accounts/contact.html')

