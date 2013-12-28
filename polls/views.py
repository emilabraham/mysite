from django.shortcuts import render, get_object_or_404
from polls.models import Poll,Choice
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
#These imports are needed if you are not using the shortcut.
from django.http import HttpResponse,Http404,HttpResponseRedirect
#from django.template import RequestContext,loader

#TODO:Figure out how to filter out Polls with fewer than 2 choices.

#def index(request): #First argument is an HttpRequest object
  #Non-shortcut way
  #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
  #template = loader.get_template('polls/index.html')
  #context = RequestContext(request, {
  #  'latest_poll_list': latest_poll_list,
  #})
  #return HttpResponse(template.render(context))

  #Normal way
  #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
  #context = {'latest_poll_list': latest_poll_list}
  #return render(request, 'polls/index.html', context)

#def detail(request, poll_id): #Second argument is data from regex.
  #return HttpResponse("You're looking at poll %s" % poll_id)
  #Non-shortcut way. This way is bad because it uses Model code. Keep Model and View separate.
  #try:
  #  poll = Poll.objects.get(pk=poll_id)#This is model code.
  #except Poll.DoesNotExist:
  #  raise Http404
  #return render(request, 'polls/details.html', {'poll':poll})#Last argument is basically context

  #Normal way
  #poll = get_object_or_404(Poll, pk=poll_id)
  #return render(request, 'polls/details.html', {'poll':poll})

#def results(request, poll_id):
  #return HttpResponse("You're looking at the results of poll %s" % poll_id)
  #poll = get_object_or_404(Poll, pk=poll_id)
  #return render(request,'polls/results.html',{'poll':poll})

#After Refactoring with generic views:
class IndexView(generic.ListView):
  template_name = 'polls/index.html' #Replaces to default:polls/poll_list.html
                                     #<app_name>/<model_name>_.html
  context_object_name = 'latest_poll_list'

  def get_queryset(self):
    #Old get_queryset() method.
    #Return last 5 published polls
    #return Poll.objects.order_by('-pub_date')[:5]

    #New get_queryset() method.
    """
    Return the last 5 published polls(Not including those to be published
    in the future.
    """
    return Poll.objects.filter(
        pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Poll
  template_name = 'polls/details.html'

  def get_queryset(self):
    """
    Exlcudes any polls that aren't published yet.
    """
    return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
  model = Poll
  template_name = 'polls/results.html'

def vote(request, poll_id):
  #return HttpResponse("You're voting on poll %s" % poll_id)
  p = get_object_or_404(Poll,pk=poll_id)
  try:
    selected_choice = p.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    #Redisplay the poll voting form
    return render(request, 'polls/details.html', {
      'poll': p,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    #Always return an HttpResponseRedirect after dealing with POST data in case a user hits back.
    #Otherwise, data might be posted twice.
    return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
