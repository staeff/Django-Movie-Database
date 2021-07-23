import datetime
import uuid
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser


def custom_year_validator(value):
    if value < 1888 or value > datetime.datetime.now().year:
        raise ValidationError(
            _('%(value)s is not a correct year!'),
            params={'value': value},
        )


class Movie(models.Model):

    class Meta:
        ordering = ('movie_id',)

    movie_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField(validators=[custom_year_validator], blank=True)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=0)
    number_of_rating = models.IntegerField(default=0)
    imdb_rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=0)
    genre = models.ManyToManyField(to='movies.Genre', related_name='movies')

    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.movie_id)])

    def __str__(self):
        return f'{self.title} ({self.year})'


RATING_CHOICES = [(i, i) for i in range(1, 6)]


class UserRating(models.Model):
    user_rating = models.IntegerField(choices=RATING_CHOICES, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_rating2')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_rating')

    def __str__(self):
        return f'{self.movie.title} ({self.movie.year}) takes {self.user_rating}/5 by {self.user}'


GENRE_CHOICES = (("Action", "Action"),
                 ("Adventure", "Adventure"),
                 ("Animation", "Animation"),
                 ("Children", "Children"),
                 ("Comedy", "Comedy"),
                 ("Crime", "Crime"),
                 ("Documentary", "Documentary"),
                 ("Drama", "Drama"),
                 ("Fantasy", "Fantasy"),
                 ("Film-Noir", "Film-Noir"),
                 ("Horror", "Horror"),
                 ("Musical", "Musical"),
                 ("Mystery", "Mystery"),
                 ("Romance", "Romance"),
                 ("Sci-Fi", "Sci-Fi"),
                 ("Thriller", "Thriller"),
                 ("War", "War"),
                 ("Western", "Western"),)


class Genre(models.Model):
    genre = models.CharField(choices=GENRE_CHOICES, max_length=50, unique=True)

    def __str__(self):
        return self.genre
