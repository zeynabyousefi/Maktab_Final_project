from django.shortcuts import render
from django.views import View
# Create your views here.


class EmailView(View):
    # form = EmailForm
    template_name = 'emails/inbox.html'

    def get(self, request):
        return render(request, self.template_name)