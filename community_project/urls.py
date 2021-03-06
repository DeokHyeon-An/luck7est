"""community_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('total_admin/', views.TotalAdminView.as_view(), name='total_admin'),
    path('chat/', include('chat.urls')),
    path('issue/', include('issue.urls')),
    path('account/email-confirmation-required',views.account_email_confirmation_required,name="account_email_confirmation_required"),
    path('account/email-confirmation-done',TemplateView.as_view(template_name="chat/email_confirmation_done.html"),name="account_email_confirmation_done"),
    path('account/password/change/', views.CustomPasswordChangeView.as_view(), name="account_password_change"),
    path('account/', include('allauth.urls')),
    path('', views.index, name='index'),
    path('users/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('votes/<int:user_id>/', views.UserVoteView.as_view(), name='user-vote'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)