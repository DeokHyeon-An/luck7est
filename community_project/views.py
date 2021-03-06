from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q
from chat.models import User, ChatRoom, VoteHistory
from issue.models import Issue
from chat.functions import index_redirect
from chat.forms import ProfileForm
from django.views.generic import DetailView, UpdateView, ListView
from allauth.account.views import PasswordChangeView
from allauth.account.utils import send_email_confirmation
from braces.views import LoginRequiredMixin, UserPassesTestMixin

def index(request):
  return redirect('chat/')


class CustomPasswordChangeView(PasswordChangeView):
  def get_success_url(self):
      return reverse("index")


class ProfileView(DetailView):
  model = User
  template_name = "chat/profile.html"
  pk_url_kwarg = "user_id"
  context_object_name = "profile_user"

  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs)
  #   user_id = self.kwargs.get("user_id")
  #   vote_history = VoteHistory.objects.filter(Q(vote_b = self.request.user)|Q(vote_a = self.request.user)).distinct()

  #   context["vote_history"] = vote_history
  #   return context


class UserVoteView(ListView):
    model = VoteHistory
    template_name = "chat/user_vote.html"
    context_object_name = "vote_history"
    ordering = ["-dt_created"]
    paginate_by = 10

    def get_queryset(self):
      user_id = self.kwargs.get("user_id")
      return VoteHistory.objects.filter(Q(vote_b = self.request.user)|Q(vote_a = self.request.user)).distinct()


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "chat/profile_update_form.html"

    def get_object(self, queryset = None):
        return self.request.user

    def get_success_url(self):
        return reverse("profile", kwargs=({"user_id": self.request.user.id}))


def account_email_confirmation_required(request):
  send_email_confirmation(request, request.user)
  return render(request, 'chat/email_confirmation_required.html')


class TotalAdminView(UserPassesTestMixin, ListView):
    model = ChatRoom
    template_name = "chat/total_admin.html"
    context_object_name = "chatrooms"
    ordering = ["dt_created"]

    raise_exception = index_redirect 

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      issue_top10 = Issue.objects.all().order_by('-id')[:10]
      vote_history = VoteHistory.objects.all()
      context['issue_top10'] = issue_top10
      context['vote_history'] = vote_history
      return context

    def test_func(self, user):
        return user.is_superuser