from django.shortcuts import render, redirect
from chat.models import ChatRoom, User
from issue.models import Issue
from chat.functions import confirmation_required_redirect, index_redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import user_passes_test
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress


# def index(request): 
#     chatrooms = ChatRoom.objects.all()
#     return render(request, 'chat/index.html',{
#       'chatrooms': chatrooms,
#     })

class IndexView(ListView):
    model = ChatRoom
    template_name = "chat/index.html"
    context_object_name = "chatrooms"
    ordering = ["dt_created"]

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      point_top10 = User.objects.all().order_by('-point')[:10]
      issue_top10 = Issue.objects.all()[:10]
      context["point_top10"] = point_top10
      context['issue_top10'] = issue_top10
      return context


def check_verified(user):
    if user.is_authenticated:
        return EmailAddress.objects.filter(user=user, verified=True).exists()
    else:
        return True

@user_passes_test(check_verified, '/account/email-confirmation-required')
def room(request, room_no):
    room = ChatRoom.objects.get(id=room_no)
    issue_top10 = Issue.objects.all()[:10]
    opinion = '아직 투표하지 않았습니다.'

    if request.user.is_authenticated:
      if room.vote_a.filter(email = request.user.email):
        opinion = 'A'
      elif room.vote_b.filter(email = request.user.email):
        opinion = 'B'

    if request.method == 'POST':
      selection = request.POST['choice']
      if selection == 'vote_a':
        room.vote_a.add(request.user)
        room.vote_b.remove(request.user)
      elif selection == 'vote_b':
        room.vote_b.add(request.user)
        room.vote_a.remove(request.user)
      else:
        room.vote_a.remove(request.user)
        room.vote_b.remove(request.user)
      return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return render(request, 'chat/room.html', {
        'room_no': room_no,
        'room': room,
        'issue_top10' : issue_top10,
        'opinion': opinion,
    })

def check_superuser(user):
    return user.is_superuser

@user_passes_test(check_superuser, 'index')
def room_admin(request, room_no):
    room = ChatRoom.objects.get(id=room_no)
    a_list = room.vote_a.all()
    b_list = room.vote_b.all()

    if request.method == 'POST':
      selection = request.POST['give_point']
      if selection == 'vote_a':
        for person_a in a_list:
          person_a.point += 100
          person_a.save()
      elif selection == 'vote_b':
        for person_b in b_list:
          person_b.point += 100
          person_b.save()
      else:
        if a_list.count() == b_list.count():
          for person_a in a_list:
            person_a.point += 100
            person_a.save()
          for person_b in b_list:
            person_b.point += 100
            person_b.save()
        elif a_list.count() > b_list.count():
          for person_a in a_list:
            person_a.point += 100
            person_a.save()
        elif a_list.count() < b_list.count():
          for person_b in b_list:
            person_b.point += 100
            person_b.save()
      return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return render(request, 'chat/room_admin.html', {
        'room_no': room_no,
        'room': room,
    })


# 참고용
# class RoomAdminDetailView(UserPassesTestMixin, DetailView):
#     model = ChatRoom
#     template_name = "chat/room_admin.html"
#     pk_url_kwarg = "room_no"
#     context_object_name = "room"

#     raise_exception = index_redirect  

#     def test_func(self, user):
#         return user.is_superuser