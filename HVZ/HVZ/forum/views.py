from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Count, Max
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from HVZ.main.models import Player, Game
from HVZ.forum.models import Thread, Post
from HVZ.forum.forms import ThreadCreateForm, PostCreateForm


class CurrentGameThreadsView(TemplateView):
    template_name = "forum/current-game-threads.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CurrentGameThreadsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        try:
            self.game = Game.nearest_game()
        except Game.DoesNotExist:
            raise PermissionDenied("There are no ongoing games!")

        context = (
            super(CurrentGameThreadsView, self).get_context_data(*args, **kwargs)
        )

        context['player'] = self.player

        context['thread_groups'] = (
            (t, self.get_threads_for_team(t)) for t in ('H', 'Z', 'B')
        )

        return context

    def get_threads_for_team(self, team):
        if (
            team != 'B' and
            self.player.team != team and
            not self.player.user.is_staff
        ):
            return None

        return Thread.objects.filter(
            game=self.game,
            team=team
        ).annotate(
            num_posts=Count('post_set'),
            last_updated=Max('post_set__created'),
        )


@login_required
def thread_detail_view(request, pk, slug):
    thread = get_object_or_404(Thread, pk=pk)
    player = Player.user_to_player(request.user, thread.game)

    if not thread.visible_to_player(player):
        raise PermissionDenied('You cannot see this thread!')

    if request.method == 'POST':
        form = PostCreateForm(request.POST, player=player, thread=thread)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(
                reverse(
                    'thread_detail',
                    kwargs = {'pk': int(pk), 'slug': slug},
                )
            )
    else:
        form = PostCreateForm(player=player, thread=thread)

    return render(
        request,
        'forum/thread-detail.html',
        {
            'form': form,
            'thread': thread,
            'player': player,
            'posts': Post.objects.filter(thread=thread).order_by('created')
        },
    )


class ThreadCreate(FormView):
    form_class = ThreadCreateForm
    template_name = "forum/thread-create.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse(
            'thread_detail',
            kwargs = {'pk': self.thread.pk, 'slug': self.thread.slug},
        )

    def get_form_kwargs(self):
        kwargs = super(ThreadCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.thread = form.save(commit=True)
        return super(ThreadCreate, self).form_valid(form)
