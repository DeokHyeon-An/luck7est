from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from community_project.views import index
from chat.functions import index_redirect

from .models import Issue
from .forms import IssueForm
from braces.views import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.



#issue app 내용

class IssueCreateView(UserPassesTestMixin, CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issue/add_issue.html'

    raise_exception = index_redirect 

    def get_success_url(self):
        return reverse('total_admin')

    def test_func(self, user):
        return user.is_superuser