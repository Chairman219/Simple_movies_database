from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from viewer.models import Movie, Genre, Actor, Director, Comment
from django.views.generic import FormView, ListView, CreateView, DeleteView, UpdateView
from logging import getLogger
from viewer.forms import MovieForm, GenreForm, ActorForm, DirectorForm, SearchForm, SignUpForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView, PasswordResetView


def mypage(request):
    return render(
        request, template_name="mypage.html",
        context={}
    )


def hello(request, s0):
    s1 = request.GET.get('s1', '')
    return render(
        request, template_name='hello.html',
        context={'adjectives': [s0, s1, 'beautiful', 'wonderful']}
    )


def movies(request):
    return render(
        request, template_name='movies.html',
        context={'movies': Movie.objects.all()}
    )


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie


LOGGER = getLogger()


class MovieCreateView(PermissionRequiredMixin, FormView):
    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('index')
    permission_required = "viewer.create_movie"

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description']
        )
        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "delete_movie.html"
    model = Movie
    success_url = reverse_lazy('index')
    permission_required = "viewer.delete_movie"


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('index')
    permission_required = "viewer.change_movie"


class GenreView(ListView):
    template_name = 'genre.html'
    model = Genre


class GenreCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = GenreForm
    success_url = reverse_lazy('genres')
    permission_required = "viewer.create_genre"


class GenreDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = Genre
    success_url = reverse_lazy('genres')
    permission_required = "viewer.delete_genre"


class GenreUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy('genres')
    permission_required = "viewer.change_genre"


class ActorView(ListView):
    template_name = 'actors.html'
    model = Actor


class ActorCreateView(PermissionRequiredMixin, CreateView):
    template_name = "form.html"
    form_class = ActorForm
    success_url = reverse_lazy('actors')
    permission_required = "viewer.create_actor"


class ActorDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = Actor
    success_url = reverse_lazy('actors')
    permission_required = "viewer.delete_actor"


class ActorUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "form.html"
    model = Actor
    form_class = ActorForm
    success_url = reverse_lazy('actors')
    permission_required = "viewer.change_actor"


class DirectorView(ListView):
    template_name = 'directors.html'
    model = Director


class DirectorCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = DirectorForm
    success_url = reverse_lazy('directors')
    permission_required = "viewer.create_director"


class DirectorDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = Director
    success_url = reverse_lazy('directors')
    permission_required = "viewer.delete_director"


class DirectorUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Director
    form_class = DirectorForm
    success_url = reverse_lazy('directors')
    permission_required = "viewer.change_director"


def search(request):
    to_find = request.GET.get("search_field", "")

    if to_find:
        movies = Movie.objects.filter(title__icontains=to_find).prefetch_related('actors', 'directors')
        genres = Genre.objects.filter(name__icontains=to_find)
        directors = Director.objects.filter(Q(name__icontains=to_find) | Q(surname__icontains=to_find))
        actors = Actor.objects.filter(Q(name__icontains=to_find) | Q(surname__icontains=to_find))
    else:
        movies = genres = directors = actors = None

    return render(
        request,
        template_name="search.html",
        context={
            "movies": movies,
            "genres": genres,
            "directors": directors,
            "actors": actors,
            "search_form": SearchForm
        }
    )


class SubmittableLoginView(LoginView):
    template_name = 'registrations/login.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'


class SignUpView(CreateView):
    template_name = "registrations/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("index")


class SubmittablePasswordResetView(PasswordResetView):
    template_name = "reset_password.html"

def actor_profile(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    movies = Movie.objects.filter(actors=actor)
    comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(actor), object_id=actor_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_object = actor
            comment.save()
            return redirect('actor_profile', actor_id=actor_id)
    else:
        form = CommentForm()

    return render(request, 'actor_profile.html', {
        'actor': actor,
        'comments': comments,
        "movies": movies,
        'form': form,
    })

def director_profile(request, director_id):
    director = get_object_or_404(Director, pk=director_id)
    movies = Movie.objects.filter(directors=director)
    comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(director), object_id=director_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_object = director
            comment.save()
            return redirect('director_profile', director_id=director_id)
    else:
        form = CommentForm()

    return render(request, 'director_profile.html', {
        'director': director,
        'comments': comments,
        "movies": movies,
        'form': form,
    })


def movie_profile(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    actors = movie.actors.all()
    directors = movie.directors.all()
    comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(movie), object_id=movie_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_object = movie
            comment.save()
            return redirect('movie_profile', movie_id=movie_id)
    else:
        form = CommentForm()

    return render(request, 'movie_profile.html', {
        'movie': movie,
        'comments': comments,
        'form': form,
        "actors": actors,
        "directors": directors
    })

