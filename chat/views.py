from django.shortcuts import render, redirect
from chat.models import ChatRoom, User, VoteHistory
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
      issue_top10 = Issue.objects.all().order_by('-id')[:10]
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
    room_all = ChatRoom.objects.all().order_by('id')
    issue_top10 = Issue.objects.all()[:10]
    opinion = '아직 투표하지 않았습니다.'

    if room.vote_a.count() == 0 and room.vote_b.count() == 0:
      a_ratio = 0
      b_ratio = 0
    else:
      a_ratio = (room.vote_a.count() / (room.vote_a.count() + room.vote_b.count()))*100
      b_ratio = (room.vote_b.count() / (room.vote_a.count() + room.vote_b.count()))*100

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
        'room_all': room_all,
        'issue_top10' : issue_top10,
        'opinion': opinion,
        'a_ratio': a_ratio,
        'b_ratio': b_ratio,
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
      elif selection == 'vote_more':
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
      else:
        temp = VoteHistory.objects.create(
            title = room.title,
            content_vote = room.content_vote,
            content_a = room.content_a,
            content_b = room.content_b,
            dt_created = room.dt_created,
        )
        temp.vote_a.set(a_list)
        temp.vote_b.set(b_list)
        temp.save()

        room.content_vote = ''
        room.content_a = ''
        room.content_b = ''
        room.vote_a.clear()
        room.vote_b.clear()
        room.save()
      return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return render(request, 'chat/room_admin.html', {
        'room_no': room_no,
        'room': room,
    })


class VoteHistoryDetailView(DetailView):
    model = VoteHistory
    template_name = "chat/vote_detail.html"
    pk_url_kwarg = "vote_no"
    context_object_name = "vote"


# 참고용
# class RoomAdminDetailView(UserPassesTestMixin, DetailView):
#     model = ChatRoom
#     template_name = "chat/room_admin.html"
#     pk_url_kwarg = "room_no"
#     context_object_name = "room"

#     raise_exception = index_redirect  

#     def test_func(self, user):
#         return user.is_superuser