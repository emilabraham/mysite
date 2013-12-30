import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Poll, Choice
from django.core.urlresolvers import reverse

#Factory method to create polls
def create_poll(question, days):
  """
  Creates a poll offset by the given number of days. Positive and negative
  values are accepted.
  """
  return Poll.objects.create(question=question,
      pub_date=timezone.now() + datetime.timedelta(days=days))

def create_choice(choicetext, pollid):
  """
  Creates a choice associated with the poll of the given poll_id with text of given
  choice_text.
  """
  return Choice.objects.create(choice_text=choicetext,
      poll=pollid)

class PollDetailViewTests(TestCase):
  def test_detail_view_with_with_a_future_poll(self):
    """
    The detail view of a poll with a pub_date in the future should return
    a 404.
    """
    future_poll = create_poll(question='Future poll.', days=5)
    response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
    self.assertEqual(response.status_code, 404)

  def test_detail_view_with_a_past_poll(self):
    """
    The detail view of a poll with a pub_date in the past should display
    the polls question
    """
    past_poll = create_poll(question='Past poll.', days=-5)
    first_choice = create_choice('Hello World', past_poll)
    second_choice = create_choice('Goodbye World', past_poll)
    response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
    self.assertContains(response, past_poll.question, status_code=200)

class PollIndexViewTests(TestCase):
  def test_index_view_with_no_polls(self):
    """
    If no poll exists, an appropriate message should be displayed
    """
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available")
    self.assertQuerysetEqual(response.context['latest_poll_list'], [])

  def test_index_view_with_a_past_poll(self):
    """
    Polls with a pub_date in the past should be displayed on the index page.
    """
    past_poll = create_poll(question="Past poll.", days=-30)
    first_choice= create_choice('Hello World', past_poll)
    second_choice = create_choice('Goodbye World', past_poll)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
        response.context['latest_poll_list'],
        ['<Poll: Past poll.>']
    )

  def test_index_view_with_a_future_poll(self):
    """
    Polls with a pub_date in the future should not be displayed on the index page.
    """
    create_poll(question="Future poll.", days=30)
    response = self.client.get(reverse('polls:index'))
    self.assertContains(response, "No polls are available")
    self.assertQuerysetEqual(response.context['latest_poll_list'], [])

  def test_index_view_with_future_poll_and_past_poll(self):
    """
    Even if past and future polls exist, only past polls should be displayed.
    """
    past_poll = create_poll(question="Past poll.", days=-30)
    create_poll(question="Future poll.", days=30)
    first_choice = create_choice('Hello World', past_poll)
    second_choice = create_choice('Goodbye World', past_poll)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
        response.context['latest_poll_list'],
        ['<Poll: Past poll.>']
    )

  def test_index_view_with_two_past_polls(self):
    """
    The polls index may display multiple poles.
    """
    past_poll_1 = create_poll(question="Past poll 1.", days=-30)
    past_poll_2 = create_poll(question="Past poll 2.", days=-5)
    first_choice = create_choice('Hello World', past_poll_1)
    second_choice = create_choice('Goodbye World', past_poll_1)
    third_choice = create_choice('Stay still World', past_poll_2)
    fourth_choice = create_choice('Spin around World', past_poll_2)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
        response.context['latest_poll_list'],
        ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
    )

  def test_index_view_with_recent_poll_with_less_than_two_choices(self):
    """
    A poll with less than 2 choices should not be published.
    """
    create_poll(question="Poll1.", days=1)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_poll_list'], [])

  def test_index_view_with_future_poll_with_two_choices(self):
    """
    A future poll with 2 choices should not be published.
    """
    future_poll = create_poll(question="Future Poll.", days=30)
    first_choice = create_choice('Hello World', future_poll)
    second_choice = create_choice('Goodbye World', future_poll)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_poll_list'], [])

  def test_index_view_with_past_poll_with_less_than_two_choices(self):
    """
    A past poll with less than 2 choices should not be published.
    """
    create_poll(question="Poll1.", days=-5)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_poll_list'], [])

class PollMethodTests(TestCase):
  def test_was_published_recently_with_future_poll(self):
    """
    was_published_recently() should return False for polls whose pub_date
    is in the future.
    """
    future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
    self.assertEqual(future_poll.was_published_recently(), False)

  def test_was_published_recently_with_old_poll(self):
    """
    was_published_recently() should return Fals for polls whose pub_date is
    older than 1 day.
    """
    old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
    self.assertEqual(old_poll.was_published_recently(), False)

  def test_was_published_recently_with_recent_poll(self):
    """
    was_published_recently() should return True for polls whose pub_date is
    within 1 day.
    """
    recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
    self.assertEqual(recent_poll.was_published_recently(), True)
