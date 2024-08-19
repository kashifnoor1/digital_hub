from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

from django.conf import settings
from django.db import models
from django.urls import reverse

# class Listing(models.Model):
#     seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.CharField(max_length=50)
#     images = models.ImageField(upload_to='listings/', blank=True, null=True)
#     ram = models.CharField(max_length=20, blank=True)
#     rom = models.CharField(max_length=20, blank=True)
#     model = models.CharField(max_length=50, blank=True)
#
#     def __str__(self):
#         return self.title


from django.db import models
from django.conf import settings

class Listing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    img1 = models.ImageField(upload_to='listings/', blank=True, null=True)
    img2 = models.ImageField(upload_to='listings/', blank=True, null=True)
    img3 = models.ImageField(upload_to='listings/', blank=True, null=True)
    ram = models.CharField(max_length=20, blank=True)
    rom = models.CharField(max_length=20, blank=True)
    model = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title




from django.db import models
from django.contrib.auth.models import User


class ShippingDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=False, blank=False)

    # Correct initialization of the model
    def __init__(self, *args, **kwargs):
        super(ShippingDetails, self).__init__(*args, **kwargs)
        # self.listing = None  # Initialize listing attribute to None

    def __str__(self):
        return f'Shipping Details for {self.user.username}'


class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()





class Review(models.Model):
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.listing.title} by {self.reviewer.username}'
