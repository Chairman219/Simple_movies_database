from email.policy import default

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from datetime import date

from django.db.models import (
  DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField,
  Model, TextField, ManyToManyField, PositiveIntegerField
)



class Genre(Model):
  name = CharField(max_length=128)

  def __str__(self):
    return self.name


class Movie(Model):
  title = CharField(max_length=128)
  genre = ForeignKey(Genre, on_delete=DO_NOTHING)
  rating = IntegerField()
  released = DateField()
  description = TextField()
  created = DateTimeField(auto_now_add=True)
  directors = ManyToManyField('Director', related_name='directed_movies', blank=True)
  actors = ManyToManyField('Actor', related_name='appeared_in_movies', blank=True)

  def __str__(self):
    return self.title

class Actor(Model):
  name = CharField(max_length=128, default=None)
  surname = CharField(max_length=128, default=None)
  birth_date = DateField(default=date.today)


  @property
  def age(self): # funkce pro výpočet věku herce
    today = date.today()
    return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
    )

  def __str__(self):
    return self.name + " " + self.surname

class Director(Model):
  name = CharField(max_length=128, default=None)
  surname = CharField(max_length=128, default=None)

  def __str__(self):
    return self.name + " " + self.surname


class Comment(Model):
  user = ForeignKey(User, on_delete=DO_NOTHING, blank=True, null=True)
  content_type = ForeignKey(ContentType, on_delete=DO_NOTHING, blank=True, null=True)
  object_id = PositiveIntegerField(blank=True, null=True)
  content_object = GenericForeignKey('content_type', 'object_id')
  text = TextField()
  created = DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user}: {self.text[:20]}"

class Rating(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)  # Který uživatel dal hodnocení
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")  # Film, který je hodnocen
  score = models.PositiveIntegerField()  # Hodnocení na škále 1–10

  class Meta:
    unique_together = ('user', 'movie')  # Každý uživatel může hodnotit film pouze jednou

  def __str__(self):
    return f"{self.user.username} rated {self.movie.title}: {self.score}"

  @staticmethod
  def calculate_average_rating(movie):
    ratings = Rating.objects.filter(movie=movie)
    if ratings.exists():
      return ratings.aggregate(models.Avg('score'))['score__avg']
    return 0