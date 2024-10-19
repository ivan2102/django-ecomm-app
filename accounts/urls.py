from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.register, name='register'),

    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name="email_verification"),

    path('email-verification-sent', views.email_verification_sent, name="email_verification_sent"),

    path('email-verification-success', views.email_verification_success, name="email_verification_success"),
    
    path('email-verification-failed', views.email_verification_failed, name="email_verification_failed"),

    # Login, logout
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    

    # User management
    path('dashboard', views.dashboard, name='dashboard'),
    path('update-profile', views.update_profile, name='update_profile'),
    path('delete-user', views.delete_user, name='delete_user'),

    # Password reset

    # Submit our email form
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name='reset_password'),

    # Success message that email was sent to reset our password
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name='password_reset_done'),

    # Password reset link
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name='password_reset_confirm'),

    # Success message that our password was reset
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name='password_reset_complete'),

    # Shipping address
    path('shipping-address', views.shipping_address, name='shipping_address'),

    # my orders
    path('my-orders', views.my_orders, name='my_orders')
    
]
