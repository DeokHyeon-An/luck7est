from django.urls import path 
from chat import views

urlpatterns = [ 
    path('' , views.IndexView.as_view() , name='index'), 
    path('<str:room_no>/', views.room, name='room'),
    path('<str:room_no>/admin/' , views.room_admin, name='room_admin'),
    path('vote_detail/<str:vote_no>/' , views.VoteHistoryDetailView.as_view() , name='vote_detail'),
]