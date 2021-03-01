# Generated by Django 3.1 on 2021-03-01 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.CharField(max_length=150, unique=True)),
                ('movie_price', models.IntegerField()),
                ('movie_length', models.DurationField()),
                ('movie_banner', models.ImageField(upload_to='movie_banner')),
                ('movie_description', models.TextField()),
                ('directors', models.TextField()),
                ('screen_play', models.TextField()),
                ('movie_link', models.URLField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('slug', models.SlugField(allow_unicode=True, blank=True, default='Automated', max_length=250)),
                ('movie_genre', models.ManyToManyField(to='cinema_core.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='OperationTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening', models.TimeField()),
                ('closing', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theater', models.CharField(max_length=10, unique=True)),
                ('capacity', models.IntegerField(default=5)),
                ('limit_per_day', models.IntegerField(default=4)),
                ('operation_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema_core.operationtime')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('movie', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='cinema_core.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='theater',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cinema_core.theater'),
        ),
        migrations.CreateModel(
            name='CinemaSeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.CharField(max_length=5)),
                ('date', models.CharField(editable=False, max_length=150)),
                ('paid', models.BooleanField(default=True)),
                ('time_char_field', models.CharField(default=None, editable=False, max_length=150)),
                ('actual_date', models.DateField()),
                ('movie', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='cinema_core.movie')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema_core.theater')),
                ('time', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='cinema_core.schedule')),
            ],
        ),
    ]
