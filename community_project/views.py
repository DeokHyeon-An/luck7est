from django.shortcuts import redirect, render
from django.urls import reverse
from chat.models import User
from chat.forms import ProfileForm
from django.views.generic import DetailView, UpdateView
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

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user_id = self.kwargs.get("user_id")
    return context

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

