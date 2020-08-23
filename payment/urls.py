from django.urls import path
from . import views 

app_name = 'payment'
urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
]