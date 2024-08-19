from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, contact
from .models import ShippingDetails
from .models import Listing
from .models import Review




class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_buyer', 'is_seller']


admin.site.register(CustomUser, CustomUserAdmin)






class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'category', 'ram', 'rom', 'model']


admin.site.register(Listing, ListingAdmin)





@admin.register(ShippingDetails)
class ShippingDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'phone_number', 'city', 'address', 'created_at', 'listing']
    search_fields = ['user__username', 'name', 'email', 'phone_number', 'city', 'address']
    list_filter = ['created_at', 'city']


@admin.register(contact)
class contactadmin(admin.ModelAdmin):
    list_display = ["id","name","email","message"]


@admin.register(Review)
class reviewadmin(admin.ModelAdmin):
    list_display = ["rating", "comment"]
