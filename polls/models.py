from django.db import models
import datetime
from django.utils import timezone

class Poll(models.Model):
  question = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')

  #__unicode__ method is kind of like a toString. Helps to identify the object
  def __unicode__(self):
    return self.question

  #Was the poll published recently?(Within a day)
  def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date < now
  was_published_recently.admin_order_field = 'pub_date'
  was_published_recently.boolean = True
  was_published_recently.short_description = 'Published recently?'

  #Does the poll have at least 2 choices?
  def has_enough_choices(self):
    return self.choice_set.count() >= 2

class Choice(models.Model):
  poll = models.ForeignKey(Poll)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  #__unicode__ method is kind of like a toString. Helps to identify the object
  def __unicode__(self):
    return self.choice_text
