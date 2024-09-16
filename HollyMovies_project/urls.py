"""
URL configuration for HollyMovies_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import namedtuple
from re import search

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views


from viewer.models import Genre, Movie, Actor, Director, Comment
from viewer.views import hello, MoviesView, MovieDeleteView, MovieUpdateView, MovieCreateView, GenreCreateView, \
  GenreDeleteView, GenreUpdateView, GenreView, ActorView, ActorCreateView, ActorDeleteView, ActorUpdateView, \
  DirectorView, DirectorCreateView, DirectorDeleteView, DirectorUpdateView, search, SubmittableLoginView, \
  SubmittablePasswordChangeView, SignUpView, mypage, SubmittablePasswordResetView, movie_profile, actor_profile, \
  director_profile

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Comment)


urlpatterns = [
  path('admin/', admin.site.urls),
  path("mypage/",mypage, name="mypage"),
  path('hello/<s0>', hello),
  #path('', views.movies), #Function based view
  path('logout/', LogoutView.as_view(), name='logout'),
  path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
  path('password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
  path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
  path('password_reset/', SubmittablePasswordResetView.as_view(), name='password_reset'),
  path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  path('sign-up/', SignUpView.as_view(), name='sign_up'),
  path('', MoviesView.as_view(), name='index'), #Class based view
  path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
  path("movie/delete/<pk>", MovieDeleteView.as_view(), name="movie_delete"),
  path("movie/update/<pk>", MovieUpdateView.as_view(), name="movie_update"),
  path("genre/create", GenreCreateView.as_view(), name='genre_create' ),
  path("genre/delete/<pk>", GenreDeleteView.as_view(), name='genre_delete'),
  path("genre/update/<pk>", GenreUpdateView.as_view(), name='genre_update'),
  path("genres/", GenreView.as_view(), name='genres'),
  path("actors/", ActorView.as_view(), name='actors'),
  path("actors/create", ActorCreateView.as_view(), name='actor_create'),
  path("actors/delete/<pk>", ActorDeleteView.as_view(), name='actor_delete'),
  path("actors/update/<pk>", ActorUpdateView.as_view(), name='actor_update'),
  path("directors", DirectorView.as_view(), name='directors'),
  path("directors/create", DirectorCreateView.as_view(), name='director_create'),
  path("directors/delete/<pk>", DirectorDeleteView.as_view(), name="director_delete"),
  path("directors/update/<pk>", DirectorUpdateView.as_view(), name="director_update"),
  path("search/", search, name="search"),
  path("movie_profile/<int:movie_id>/", movie_profile, name="movie_profile"),
  path("actor_profile/<int:actor_id>/", actor_profile, name="actor_profile"),
  path("director_profile/<director_id>/", director_profile, name="director_profile"),



]

