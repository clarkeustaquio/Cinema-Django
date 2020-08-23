from django.contrib import admin
from .models import Movie, Theater, CinemaSeat, OperationTime, Schedule, Genre

# Register your models here.

admin.site.site_header = "Cinema Dashboard"

class TheaterAdmin(admin.ModelAdmin):
    list_display = ('theater', 'capacity', 'operation_time')

class CinemaSeatAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'seat', 'date', 'time_char_field', 'paid')

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('movie', 'start_time', 'end_time')
    list_filter = ['start_time']


admin.site.register(Theater, TheaterAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(CinemaSeat, CinemaSeatAdmin)

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(OperationTime)

