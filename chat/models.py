from __future__ import division
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
from chat.validators import validate_no_special_characters
from django.db import connection

# Create your models here.
class User(AbstractUser):
  nickname = models.CharField(
    max_length=15,
    unique=True, 
    null=True,
    validators=[validate_no_special_characters],
    error_messages={'unique': '이미 사용중인 닉네임입니다.'},
  )

  profile_pic = models.ImageField(
    default="default_profile_pic.png", upload_to="profile_pics"
  )
  
  intro = models.CharField(max_length=60, blank=True)

  point = models.IntegerField(default=0)

  def __str__(self):
      return self.email
  

class ChatRoom(models.Model):
  CATEGORY_CHOICES = [
    ("시사이슈", "시사이슈"),
    ("연예", "연예"),
    ("스포츠", "스포츠"),
    ("기타", "기타"),
  ]

  chat_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="기타")

  title = models.CharField(max_length=50)

  content_vote = models.CharField(max_length=50, blank=True)

  content_a = models.CharField(max_length=50, blank=True)

  content_b = models.CharField(max_length=50, blank=True)

  dt_created = models.DateTimeField(auto_now_add=True)

  dt_modified = models.DateTimeField(auto_now=True)

  vote_a = models.ManyToManyField(User, related_name='vote_a', blank=True)

  vote_b = models.ManyToManyField(User, related_name='vote_b', blank=True)

  connect_user = models.ManyToManyField(User, related_name='connect_user', blank=True)

  open = models.BooleanField(default=True)

  def __str__(self):
    return self.title
  
  @classmethod
  def truncate(cls):
      with connection.cursor() as cursor:
          cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))

class VoteHistory(models.Model):
  title = models.CharField(max_length=50)

  content_vote = models.CharField(max_length=50, blank=True)

  content_a = models.CharField(max_length=50, blank=True)

  content_b = models.CharField(max_length=50, blank=True)

  dt_created = models.DateTimeField()

  dt_end = models.DateTimeField(auto_now_add=True)

  vote_a = models.ManyToManyField(User, related_name='vote_a_history', blank=True)

  vote_b = models.ManyToManyField(User, related_name='vote_b_history', blank=True)

  def __str__(self):
    return self.title