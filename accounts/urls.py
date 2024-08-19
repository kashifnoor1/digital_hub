from django.urls import path
from . import views 
from .views import custom_login_view, listing_detail_view, leave_review_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', custom_login_view, name='custom_login'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/add-listing/', views.add_listing, name='add_listing'),
    path('buy/<int:listing_id>/', views.buy_now, name='buy_now'),
    path('buy-now/<int:listing_id>/shipping/', views.shipping_form_view, name='shipping_form'),
    path('seller/edit-listing/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('seller/delete-listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('payment/<int:shipping_id>/', views.payment_selection, name='payment_selection'),
    path('process-payment/<int:pk>/', views.process_payment, name='process_payment'),
    path('error/', views.error_view, name='error'),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('payments/<int:listing_id>', views.payment_success, name='payment_success'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('about', views.about, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('listing/<int:listing_id>/', views.listing_detail_view, name='listing_detail'),
    path('leave_review/<int:listing_id>/', leave_review_view, name='leave_review'),
]
