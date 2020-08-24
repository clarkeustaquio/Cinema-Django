import stripe
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import request
from cinema_core.views import _calculate_order
from django.contrib.auth.decorators import login_required
from urllib.error import HTTPError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from cinema_core.models import CinemaSeat
from accounts.models import History
# Create your views here.

@login_required
def payment(request):
    orders = _calculate_order(request)
    context = dict()

    if orders['total_amount'] != 0:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],    
            customer_email="{}".format(request.user.email),
            submit_type="book",
            line_items=[{
                'quantity': 1,
                'amount': orders['total_amount'] * 100,
                'currency': 'php',
                'description': "Enjoy the latest international & local films with your family & friends at Cinema!",
                'name': 'Total Amount',
                'images': ['https://i.imgur.com/XSQACIF.jpg'],
            }],
            success_url=request.build_absolute_uri(reverse('payment:payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('cinema:index')),
        )
        
        context = {
            'cart_orders': len(orders['ticket_orders']),
            'ticket_orders': orders['ticket_orders'],
            'total_amount': orders['total_amount'],
            'previous_url': request.META.get('HTTP_REFERER'),
        }

        context['session'] = session.id
        context['public_key'] = settings.STRIPE_PUBLIC_KEY

    return render(request, 'payment/payment.html', context)
    

@login_required
def payment_success(request):
    ticket_orders = list()
   
    for key, value in request.session.items():
        if key == str(value):
            ticket_orders.append(key)
            cinema_seat = CinemaSeat.objects.get(id=value)
            cinema_seat.paid = False
            cinema_seat.save()

            history = History.objects.create(
                user=request.user,
                movie=cinema_seat.movie,
                theater=cinema_seat.theater,
                price=cinema_seat.movie.movie_price,
                seat=cinema_seat.seat,
                time=cinema_seat.time,
                date=cinema_seat.date,
            )

    if len(ticket_orders):
        orders = _calculate_order(request)
        subject = "Ticket Receipt"
        message = "Cinema ticket info"
        recipient_list = [request.user.email]
        html_message = render_to_string(
            'email/ticket_receipt.html', 
            context = {
                'cart_orders': len(orders['ticket_orders']),
                'ticket_orders': orders['ticket_orders'],
                'total_amount': orders['total_amount'],
            }
        )

        ticket_receipt = send_mail(
            subject=subject,
            message=message,
            from_email="clark.eustaquio@gmail.com",
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=html_message
        )

    for ticket in ticket_orders:
        request.session.pop(ticket)

    return render(request, 'payment/payment_success.html')

@login_required
def payment_failed(request):
    return render(request, 'payment/payment_failed.html')