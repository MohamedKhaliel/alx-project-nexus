from django.test import TestCase
from django.utils import timezone
from .models import Poll, Option, Vote


class ModelsSmokeTests(TestCase):
    def test_poll_option_vote(self):
        poll = Poll.objects.create(title='Test', expires_at=timezone.now())
        opt = Option.objects.create(poll=poll, text='A')
        vote = Vote.objects.create(poll=poll, option=opt, voter_id='u1')
        self.assertEqual(vote.option, opt)

# Create your tests here.
