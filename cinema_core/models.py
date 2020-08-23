from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, datetime, time, timedelta
from django.template.defaultfilters import slugify

# Create your models here.

class OperationTime(models.Model):
    opening = models.TimeField()
    closing = models.TimeField()

    def __str__(self):
        return "{} to {}".format(self.opening, self.closing)

class Theater(models.Model):
    theater = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(default=5)
    limit_per_day = models.IntegerField(default=4)
    operation_time = models.ForeignKey(OperationTime, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.theater

class Genre(models.Model):
    genre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.genre

class Movie(models.Model):
    theater = models.OneToOneField(Theater, on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=150, unique=True)
    movie_price = models.IntegerField()
    movie_length = models.DurationField()
    movie_genre = models.ManyToManyField(Genre)
    movie_banner = models.ImageField(upload_to='movie_banner')
    movie_description = models.TextField()
    directors = models.TextField()
    screen_play = models.TextField()

    movie_link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField()
    slug = models.SlugField(max_length=250, allow_unicode=True, blank=True, default="Automated")

    def _create_schedule(self):
        theater_start = self.theater.operation_time.opening
        theater_end = self.theater.operation_time.closing
        movie_break = 30 # in minutes

        movie_duration = self.movie_length.total_seconds()
        hours = int(movie_duration // 3600)
        minutes = int((movie_duration % 3600) // 60)

        theater_hour = theater_start.hour + hours
        theater_minute = theater_start.minute + minutes
        current = theater_start.replace(hour=theater_hour, minute=theater_minute)

        for limit in range(self.theater.limit_per_day):
                schedule = Schedule.objects.update_or_create(
                    movie=self,
                    start_time=theater_start,
                    end_time=current,
                )
                current_hour = current.hour
                current_minute = current.minute
                total_minute = current_minute + movie_break

                if total_minute < 60:
                    theater_start = current.replace(minute=current_minute+movie_break)
                else:
                    calculate_minute = total_minute - 60
                    theater_start = current.replace(hour=current_hour+1, minute=calculate_minute)
                
                temp = theater_start
                calculate_hour = temp.hour + hours
                if calculate_hour < theater_end.hour:
                    current = temp.replace(hour=calculate_hour, minute=temp.minute+minutes)
                else:
                    break

    def _create_seats(self):
        start_date = self.start_date
        end_date = self.end_date
        span = end_date - start_date

        seat_row_range = 10
        seat_label = [chr(letter) for letter in range(65, 91)]
        seat_col_range = self.theater.capacity // seat_row_range
    
        for day in range(span.days + 1):
            date_display = start_date + timedelta(days=day)
            for time in Schedule.objects.filter(movie=self):
                row_track = 0
                col_track = 0
                for capacity in range(self.theater.capacity):
                    row_track += 1
                    
                    if row_track > seat_row_range:
                        row_track = 1
                        if col_track < seat_col_range:
                            col_track += 1

                    display = "{}-{}".format(seat_label[col_track], row_track)

                    if not date_display < date.today():
                        cinema_seat = CinemaSeat.objects.update_or_create(
                            movie=self,
                            theater=self.theater, 
                            seat=display, 
                            time=time,
                            date=date_display.strftime('%B %d, %Y - %A'),
                            time_char_field=str(time),
                            actual_date=date_display,
                        )

    def clean(self):    
        if self.start_date > self.end_date:
            raise ValidationError("- Dates are incorrect!")
    
    def __str__(self):
        return self.movie_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.movie_title)
        # https://youtu.be/ybji16u608U - url
        # Please copy the actual url by right clicking on youtube videos
        
        url_link = self.movie_link.rindex('/') + 1
        code_link = self.movie_link[url_link:]
        generated_link = "https://youtube.com/embed/" + code_link
        self.movie_link = generated_link

        if len(self.movie_description) > 350:
            self.movie_description = self.movie_description[:350]

        super(Movie, self).save(*args, **kwargs)
        self._create_schedule()
        self._create_seats()

class Schedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_constraint=False)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        start_time = self.start_time.strftime("%I:%M %p")
        end_time = self.end_time.strftime("%I:%M %p")
        
        return "{} to {}".format(start_time, end_time)

class CinemaSeat(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_constraint=False)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    seat = models.CharField(max_length=5)
    time = models.ForeignKey(Schedule, on_delete=models.CASCADE, editable=False)
    date = models.CharField(max_length=150, editable=False)
    paid = models.BooleanField(default=True)
    time_char_field = models.CharField(max_length=150, default=None, editable=False)
    actual_date = models.DateField()


    def __str__(self):
        return "{} | {} | {} - {}".format(
                self.theater, self.seat, 
                self.time, self.date
            )

