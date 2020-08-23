from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from random import random

app_name = 'cinema'

def generate_random():
    random_number = str(random())
    random_number = random_number.replace(".", "")
    return random_number

urlpatterns = [
    path('', views.index, name='index'),
    path('book-ticket/', views.book_ticket, name='book_ticket'),
    path('buy-ticket/<slug>/', views.buy_ticket, name='buy_ticket'),
    path('ticket-view/<slug>/', views.ticket_view, name='ticket_view'),
    path('snacks/', views.snacks, name='snacks'),
    
    path('user-select/{}<int:movie_id>{}?id={}<int:seat_id>{}/'.format(
        generate_random()[1:], generate_random(),
        generate_random(), generate_random()
    ), views._user_select, name='user_select'),

    path('search/', views.search_movie, name='search_movie'),
    path('redirect_now_showing/', views.redirect_now_showing, name='redirect_now_showing'),
    path('redirect_coming_soon/', views.redirect_coming_soon, name='redirect_coming_soon'),
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

