from django.contrib.auth.forms import UserCreationForm
from django.db.models import Model
from django.forms import (
  CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea, ModelForm, DateInput
)
from viewer.models import Genre, Movie, Actor, Director, Comment


class MovieForm(ModelForm):

  class Meta:
    model = Movie
    fields = '__all__'

#   title = CharField(max_length=128)
#   genre = ModelChoiceField(queryset=Genre.objects)
#   rating = IntegerField(min_value=1, max_value=10)
#   released = DateField()
#   description = CharField(widget=Textarea, required=False)

class GenreForm(ModelForm):

  class Meta:
    model = Genre
    fields = '__all__'

class ActorForm(ModelForm):

  class Meta:
    model = Actor
    fields = '__all__'

class DirectorForm(ModelForm):

  class Meta:
    model = Director
    fields = '__all__'

class SearchForm(Form):
  search_field = CharField(max_length=100)

class SignUpForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    fields = ["username", "first_name"]

    def save(self, commit=True):
      self.instance.is_active = False # výběr toho zda jsou nově vytvořené účty uživatelů ihned aktivní nebo ne, False = ne True = ano
      return super().save(commit)

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['text']