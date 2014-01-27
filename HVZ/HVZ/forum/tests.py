from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.conf import settings

from HVZ.basetest import BaseTest, HUGH_MANN, ROB_ZOMBIE
from HVZ.main.models import Player, Game
from HVZ.forum.models import Thread, Post


class CurrentGameThreadsTestCase(BaseTest):
    def setUp(self):
        c = Client()
        self.login_as_tabler(c)

        c.post(reverse('register'), ROB_ZOMBIE)
        z = Player.objects.get()
        z.team = 'Z'
        z.save()

        c.post(reverse('register'), HUGH_MANN)

    def test_logged_out(self):
        c = Client()
        uri = reverse('current_game_threads')
        r = c.get(uri)
        self.assertRedirects(r, 'login/?next=%s' % uri)

    def test_empty(self):
        c = Client()
        c.post(reverse('login'), HUGH_MANN)

        r = c.get(reverse('current_game_threads'))
        self.assertEqual(r.status_code, 200)


class ThreadDetailTestCase(BaseTest):
    def setUp(self):
        c = Client()
        self.login_as_tabler(c)

        c.post(reverse('register'), ROB_ZOMBIE)
        z = Player.objects.get()
        z.team = 'Z'
        z.save()

        c.post(reverse('register'), HUGH_MANN)

    def test_get_invalid_thread(self):
        c = Client()
        c.post(reverse('login'), HUGH_MANN)

        r = c.get(reverse('thread_detail', kwargs={
            'pk': 42,
            'slug': 'meaning-of-life'
        }))

        self.assertEqual(r.status_code, 404)

    def test_logged_out(self):
        c = Client()
        c.post(reverse('login'), HUGH_MANN)

        c.post(
            reverse('thread_create'),
            {
                'title': 'War and Peace',
                'team': 'H',
                'post_body': 'lorem ipsum',
            }
        )

        c.logout()
        thread_uri = reverse('thread_detail', kwargs={
            'pk': 42,
            'slug': 'meaning-of-life'
        })

        r = c.get(thread_uri)
        self.assertRedirects(r, 'login/?next=%s' % thread_uri)

    def test_players_can_make_threads(self):
        c = Client()
        c.post(reverse('login'), HUGH_MANN)

        self.assertEqual(Thread.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)

        c.post(
            reverse('thread_create'),
            {
                'title': 'War and Peace',
                'team': 'H',
                'post_body': 'lorem ipsum',
            }
        )

        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Post.objects.count(), 1)

        h = Player.objects.get(team='H')
        t = Thread.objects.get()
        p = Post.objects.get()

        self.assertEqual(t.title, 'War and Peace')
        self.assertEqual(t.team, 'H')
        self.assertEqual(p.thread, t)

        self.assertEqual(p.author, h)
        self.assertEqual(p.body.raw, 'lorem ipsum')

    def test_deny_thread_to_opponents(self):
        c = Client()
        c.post(reverse('login'), HUGH_MANN)
        c.post(
            reverse('thread_create'),
            {
                'title': 'War and Peace',
                'team': 'H',
                'post_body': 'lorem ipsum',
            }
        )

        t = Thread.objects.get()

        c.post(reverse('login'), ROB_ZOMBIE)
        r = c.get(reverse('thread_detail', kwargs={'pk': t.pk, 'slug': t.slug}))
        self.assertEqual(r.status_code, 403)

        self.assertEqual(Post.objects.count(), 1)

        r = c.post(
            reverse('thread_detail', kwargs={'pk': t.pk, 'slug': t.slug}),
            { 'body': 'brans' }
        )

        self.assertEqual(r.status_code, 403)
        self.assertEqual(Post.objects.count(), 1)

    def test_illegal_thread_creation(self):
        self.assertEqual(Thread.objects.count(), 0)

        c = Client()
        c.post(reverse('login'), ROB_ZOMBIE)
        r = c.post(reverse('thread_create'), {
            'title': "It's safe, guys!",
            'team': 'H',
            'post_body': 'Really.',
        })

        self.assertEqual(len(r.context[0].get('form').errors), 1)
        self.assertEqual(Thread.objects.count(), 0)

    def test_public_thread(self):
        c = Client()
        c.post(reverse('login'), HUGH_MANN)
        c.post(
            reverse('thread_create'),
            {
                'title': 'War and Peace',
                'team': 'B',
                'post_body': 'lorem ipsum',
            }
        )

        t = Thread.objects.get()

        c.post(reverse('login'), ROB_ZOMBIE)
        r = c.get(reverse('thread_detail', kwargs={'pk': t.pk, 'slug': t.slug}))
        self.assertEqual(r.status_code, 200)

        r = c.post(
            reverse('thread_detail', kwargs={'pk': t.pk, 'slug': t.slug}),
            { 'body': 'dolor sit amet' },
            follow=True
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Post.objects.count(), 2)

        z = Player.objects.get(team='Z')
        p = Post.objects.get(author=z)
        self.assertEqual(p.body.raw, 'dolor sit amet')

    def test_illegal_posting(self):
        game = Game.objects.get()
        human_thread = Thread(
            game=game,
            title="Humans Only",
            slug="humans-only",
            team="H"
        )

        human_thread.full_clean()
        human_thread.save()

        zombie = Player.objects.get(team='Z')

        self.assertEqual(Post.objects.count(), 0)

        post = Post(
            thread=human_thread,
            author=zombie,
            created=settings.NOW(),
            body="H4%0R3D"
        )

        self.assertRaises(ValidationError, post.full_clean)
