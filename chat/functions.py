from django.shortcuts import redirect
from allauth.account.utils import send_email_confirmation

def confirmation_required_redirect(self, request):
    send_email_confirmation(request, request.user)
    return redirect("account_email_confirmation_required")

def index_redirect(self, request):
    return redirect("index")

