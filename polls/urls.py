from django.conf.urls import patterns,url
from polls import views
'''
urlpatterns = patterns('',
    #Example: /polls/    Remember the root URLconf links to this when reading /polls/
    url(r'^$', views.index, name='index'),
    #Example: /polls/5/
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    #Example: /polls/5/results/
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    #Example: /polls/5/vote/
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
'''

#After refactoring with generic views:
urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
