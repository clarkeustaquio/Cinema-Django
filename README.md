# Cinema-Django
Online Cinema Booking System
Site: https://cinema-django.herokuapp.com/

# Admin Panel and BackEnd
Supports creating objects in Theater, Movies, Genres, User's History.
And automate the creation of number of seats and schedules when instantiating a movie object.

 - Full Customization on Django-Allauth for templates, emails, and prompted messages.
 - Customized class for ModelAdmin.
 - Implement security for object creation, such as correct dates, and relation with other models.
 - Implement an algorithm to embed youtube videos.
 - Automate slug fields

Uses django-storages for Amazon Web Service.
Movie banners are stored in Amazon S3 Bucket.

Included movie ratings, but represented as a Like and Dislike functionality.

Uses the default django authentication model for Django-Allauth.
Also supports Social (Gmail and Twitter) and Local accounts.

For EmailBackEnd, SendGrid SMTP is used.

Implementation of Celery for Asynchronous Task.
 - Automated seats that is already played in the Cinema will automatically deleted after a day.
 - But movies are not will be deleted, it still present and can be used in Movies API.
   This is to help other developers when they need the information about the movie.


# Django-Rest-Framework
Supports for all movies that is in the database.
Also allow searching movies by, api/title='movie-title'/
DRF is also used for the search functionality of the application.

# Payment
Implement the use of Stripe for payment method.
It redirects the user to checkout section and fill the required fields for the payment.

Stripe checkout is customized with additional images for better look in checkout.
If payment is successful, ticket receipt is sent into user's email address.
And logged the ticket on the user's history.

# FrontEnd
For the design Bootstrap4 is used.
Along with javascript and jquery.

 - Swiper ("Customized")
 - Bootstrap Autocompletion ("Here it applies the Django-Rest-Framework as a reference for the movies")
 - DataTables ("Customized")
 
Ajax call is also supported for selecting seats in the auditorium. 
And for Liking and Disliking the movie as well.

 - Top Movies are computed base on the total percentage of likes and dislike.
 - Now Showing movies are filtered by the date span given in the model.
 - Coming Soon movies are filtered if the current date is still less than, than the said date.

The Web Application also supports the mobile view. But it is recommended to use in Desktop View
for better user experience and bug less.

