from django.contrib import admin
from polls.models import Poll,Choice

class ChoiceInline(admin.TabularInline):#Another option is StackedInline
  model = Choice
  extra = 3
#A class that controls how the Poll object is displayed in admin page.
class PollAdmin(admin.ModelAdmin):
  fieldsets = [
      (None,               {'fields':['question']}),
      ('Date information', {'fields':['pub_date'], 'classes':['collapse']}),
  ]
  inlines = [ChoiceInline]
  list_display = ('question', 'pub_date', 'was_published_recently') #Displays in columns
  list_filter = ['pub_date'] #Allows filtering
  search_fields = ['question'] #Creates a searchbox

admin.site.register(Poll, PollAdmin)#Register Poll using PollAdmin class
#admin.site.register(Choice)#Register Choice using default ModelAdmin class
