from django import forms
from django.conf import settings
from django.utils.text import slugify

from HVZ.main.models import Game, Player
from HVZ.forum.models import Thread, Post


class ThreadCreateForm(forms.Form):
    title = forms.CharField(required=True)

    post_body = forms.CharField(
        widget=forms.Textarea(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        del kwargs['user']
        super(ThreadCreateForm, self).__init__(*args, **kwargs)
        self.fields["team"] = forms.ChoiceField(
            choices=Thread.legal_teams(self.user)
        )

    def clean(self):
        return super(ThreadCreateForm, self).clean()

    def save(self, commit=False):
        def grab(s):
            return self.cleaned_data[s]

        game = Game.nearest_game()
        player = Player.user_to_player(self.user, game)

        self.thread = Thread(
            game=game,
            team=grab('team'),
            title=grab('title'),
            slug=slugify(grab('title')),
        )

        self.thread.save()

        post = Post(
            author=player,
            thread=self.thread,
            body=grab('post_body'),
            created=settings.NOW(),
        )

        if commit:
            post.save()

        return self.thread

class PostCreateForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.player = kwargs['player']
        self.thread = kwargs['thread']
        del kwargs['player']
        del kwargs['thread']

        super(PostCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=False):
        post = Post(
            author=self.player,
            thread=self.thread,
            body=self.cleaned_data['body'],
            created=settings.NOW(),
        )

        if commit:
            post.save()

        return post
