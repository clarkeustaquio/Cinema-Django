import stripe
from django.shortcuts import render, redirect, reverse
from .models import Movie, Schedule, CinemaSeat
from like_manager.models import Like, Dislike
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import date, datetime, timedelta
from django.forms.models import model_to_dict
from django.http import JsonResponse, request
from django.contrib.auth.decorators import login_required

# Create your views here.
current_date = date.today()
current_time = datetime.utcnow().time()

def _get_movies():
    _movies = Movie.objects.all()
    movies = list()
    coming_soon = list()

    for movie in _movies:
        if current_date >= movie.start_date and current_date <= movie.end_date:
            movies.append(Movie.objects.get(movie_title=movie.movie_title))

        if movie.start_date > current_date:
            coming_soon.append(Movie.objects.get(movie_title=movie.movie_title))

    context = {
        'movies': movies,
        'coming_soon': coming_soon,
    }

    return context

def _calculate_duration(movie_length):
    duration = movie_length
    total_seconds = int(duration.total_seconds())
    total_minutes = total_seconds // 60
    
    return total_minutes

def _movies(description_length=150):
    movies = _get_movies()

    for movie in movies['movies']:
        movie.movie_length = "{} Minutes".format(_calculate_duration(movie.movie_length))

        if len(movie.movie_description) >= description_length:
            movie.movie_description = movie.movie_description[:description_length] + "..."

        if len(movie.movie_description) == description_length:
            movie.movie_description += movie.movie_description +  "..."

    for movie in movies['coming_soon']:
        movie.movie_length = "{} Minutes".format(_calculate_duration(movie.movie_length))

        if len(movie.movie_description) >= description_length:
            movie.movie_description = movie.movie_description[:description_length] + "..."

        if len(movie.movie_description) == description_length:
            movie.movie_description += movie.movie_description +  "..."

    return movies

@login_required
def _calculate_order(request):
    total_amount = 0
    ticket_orders = list()
    serialized = list()

    for key, value in request.session.items():
        if key == str(value):
            cinema = CinemaSeat.objects.get(id=value)
            cinema_dict = model_to_dict(cinema)
            cinema_dict['movie_title'] = cinema.movie.movie_title
            cinema_dict['movie_price'] = cinema.movie.movie_price
            cinema_dict['date'] = str(cinema.date)
            cinema_dict['time'] = str(cinema.time)
            cinema_dict['movie_banner'] = str(cinema.movie.movie_banner.url)
            cinema_dict['theater_name'] = str(cinema.movie.theater)
            serialized.append(cinema_dict)
            ticket_orders.append(cinema)
            total_amount += cinema.movie.movie_price
    
    return {
        'total_amount': total_amount, 
        'ticket_orders': ticket_orders,
        'serialized': serialized,
    }    

@login_required
def _user_select(request, movie_id, seat_id):
    try:
        if request.is_ajax():
            seat = str(seat_id)
            if seat not in request.session:
                request.session[seat] = seat_id
            else:
                request.session.pop(seat)
    except KeyError:
        pass
    
    else:
        orders = _calculate_order(request)
        context = {
            'ticket_orders': orders['serialized'],
            'total_amount': orders['total_amount'],
            'cart': len(orders['serialized']),
        }   

        return JsonResponse(context, safe=False, status=200, json_dumps_params={'indent': 4})

def _calculate_like():
    movies = Movie.objects.all()
    like_dict = {}
    dislike_dict = {}
    total_dict = {}

    for movie in movies:
        if current_date >= movie.start_date and current_date <= movie.end_date:
            like_dict["{}".format(movie)] = len(Like.objects.filter(movie=movie.id))
            dislike_dict["{}".format(movie)] = len(Dislike.objects.filter(movie=movie.id))

        if movie.start_date > current_date:
            like_dict["{}".format(movie)] = len(Like.objects.filter(movie=movie.id))
            dislike_dict["{}".format(movie)] = len(Dislike.objects.filter(movie=movie.id))

    for like_key, like_val in like_dict.items():
        for dislike_key, dislike_val in dislike_dict.items():
            if like_key == dislike_key:
                if like_val != 0 or dislike_val != 0:
                    total_dict["{}".format(like_key)] = int((like_val/(like_val + dislike_val)) * 100)
                elif like_val == 0 and dislike_val == 0:
                    total_dict["{}".format(like_key)] = 0

    return total_dict

def index(request):
    movies = _movies(350)
    total_dict = _calculate_like()
    top_movies = {movie: total_count for movie, total_count in sorted(total_dict.items(), key=lambda total: total[1], reverse=True)}

    context = {
        'movies': movies['movies'], 
        'total_dict':total_dict,
        'top_movies': top_movies,
        'coming_soon': movies['coming_soon'],
    }

    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user)
        dislikes = Dislike.objects.filter(user=request.user)
        like_movie = [like.movie for like in likes]
        dislike_movie = [dislike.movie for dislike in dislikes]

        context['like_movie'] = like_movie
        context['dislike_movie'] = dislike_movie
    
    return render(request, 'cinema/index.html', context)

def book_ticket(request):
    movies = _movies(150)
    context = {'movies': movies['movies']}
    return render(request, 'cinema/book_ticket.html', context)

def buy_ticket(request, slug):
    day_spans = list()
    total_dict = _calculate_like()
    movie = get_object_or_404(Movie, slug=slug)
    movie.movie_length = "{} Minutes".format(_calculate_duration(movie.movie_length))
    theater_times = Schedule.objects.filter(movie=movie)

    span = movie.end_date - current_date
    for day in range(span.days + 1):
        days = current_date + timedelta(days=day)
        day_spans.append(days.strftime('%B %d, %Y - %A'))

    context = {
        'movie': movie,
        'day_spans': day_spans,
        'theater_times': theater_times,
        'total_dict': total_dict,
    }

    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user)
        dislikes = Dislike.objects.filter(user=request.user)
        like_movie = [like.movie for like in likes]
        dislike_movie = [dislike.movie for dislike in dislikes]

        context['like_movie'] = like_movie
        context['dislike_movie'] = dislike_movie

    return render(request, 'cinema/buy_ticket.html', context)

@login_required
def ticket_view(request, slug):
    movies = get_object_or_404(Movie, slug=slug)

    if request.method == "POST":
        request.session['theater_time'] = request.POST['theater_time']
        request.session['theater_date'] = request.POST['theater_date']

    cinema_seats = CinemaSeat.objects.filter(
        theater=movies.theater, 
        time_char_field=request.session.get('theater_time'),
        date=request.session.get('theater_date'),
    ).order_by('id')

    orders = _calculate_order(request)
    context = {
        'movies': movies,
        'cinema_seats': cinema_seats,
        'theater_time': request.session.get('theater_time'),
        'theater_date': request.session.get('theater_date'),
        'ticket_orders': orders['ticket_orders'],
        'total_amount': orders['total_amount'],
        'cart': len(orders['ticket_orders']),
    }   

    if request.session.get('theater_time') and request.session.get('theater_date'):
        return render(request, 'cinema/ticket_view.html', context)
    else:
        return redirect('cinema:book_ticket')

def snacks(request):
    return render(request, 'cinema/snacks.html', )


def search_movie(request):
    if request.method == "POST":
        try:
            movie = Movie.objects.get(movie_title__icontains=request.POST['search'])
       
        except Movie.DoesNotExist:  
            return render(request, 'cinema/search.html')

        else:
            return redirect('cinema:buy_ticket', slug=movie.slug)            

def redirect_now_showing(request):
    return redirect(reverse('cinema:index') + "#now_showing_section")

def redirect_coming_soon(request):
    return redirect(reverse('cinema:index') + "#coming_soon_section")