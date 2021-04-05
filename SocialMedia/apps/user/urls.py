from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView
from django.urls import path, re_path

from . import views
from .views import AutocompleteSearch

urlpatterns = [
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='user/password_reset.html'),
         name='password-reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
         name='password-reset-done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('register/', views.register, name='register-user'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.SearchView, name='search'),

    # re_path(r'autocomplete/(?P<slug>[-\w]+)/', AutocompleteSearch.as_view(), name='autocomplete'),
    ###request stuff
    path('users/', views.users_list, name='users_list'),
    path('users/<slug>/', views.profile_view, name='profile_view'),
    path('friends/', views.friend_list, name='friend_list'),
    path('users/frined-request/send/<int:id>/', views.send_friend_request, name='send_friend_request'),
    path('users/friend-request/cancel/<int:id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('users/friend-request/accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
    path('users/friend-request/delete/<int:id>/', views.delete_friend_request, name='delete_friend_request'),
    path('users/friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
