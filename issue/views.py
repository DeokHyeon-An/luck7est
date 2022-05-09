from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from community_project.views import index
from .models import Issue
from .forms import IssueForm


# Create your views here.



#issue app 내용

class IssueCreateView(CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issue/add_issue.html'

    def get_success_url(self):
        return reverse('index')
