import os
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models.user import Profile, FriendRequest
from ..post.models.post import Post


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login! {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


@login_required()
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST,
                                  request.FILES,
                                  instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Account has been updated.')
            return redirect('profile')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    # return redirect(reverse('profile', kwargs={'uform': uform, 'pform': pform}))

    return render(request, 'user/profile.html', {'uform': uform, 'pform': pform})


class UpdateProfile(View):
    model = Profile
    template_name = 'update_profile.html'

    def get(self, request, **kwargs):
        user = Profile.objects.get(id=request.user.id)
        form = ProfileUpdateForm(initial=user.__dict__)
        return render(request, self.template_name, locals())

    def post(self, request, **kwargs):
        user = Profile.objects.get(id=request.user.id)
        form = ProfileUpdateForm(initial=user.__dict__)
        os.remove(user.propic.path)
        form.ProfileUpdateForm(request.POST, request.FILES, instance=user)
        form.save()
        return redirect('/')


@login_required
def SearchView(request):
    if request.method == 'POST':
        user_search = request.POST.get('search')
        print(user_search)
        results = User.objects.filter(username__startswith=user_search)
        context = {
            'results': results
        }
        return render(request, 'user/search_result.html', context)


#
# @login_required
# def autocompleteModel(request):
#     if request.is_ajax():
#         q = request.GET.get('term', '')
#         search_qs = User.objects.filter(username__startswith=q)
#         results = []
#         for r in search_qs:
#             results.append(r.username)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data, mimetype)

# @login_required
# def autocompleteModel(request):
#     if 'term' in request.GET:
#         qs = User.objects.filter(username__istartswith=request.GET.get('term'))
#         usernames = []
#         for u in qs:
#             usernames.append(u.username)
#         return JsonResponse(usernames, safe=False)
#     return render(request, 'user/search_result.html')

class AutocompleteSearch(View):
    def get(self, request, slug):
        if 'item' in request.GET:
            qs = User.objects.exclude(slug=slug).filter(user_name__icontains=request.GET.get('item'))
            search_result = []
            for user in qs:
                search_result.append(user.slug)
            return JsonResponse(search_result, safe=False)
        return render(request, 'user/search.html')


@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    my_friends = request.user.profile.friends.all()
    sent_to = []
    friends = []
    for user in my_friends:
        friend = user.friends.all()
        for f in friend:
            if f in friends:
                friend = friend.exclude(user=f.user)
        friends += friend
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends += random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    for se in sent_friend_requests:
        sent_to.append(se.to_user)
    context = {
        'users': friends,
        'sent': sent_to
    }
    return render(request, "user/users_list.html", context)


def friend_list(request):
    p = request.user.profile
    friends = p.friends.all()
    context = {
        'friends': friends
    }
    return render(request, "user/friend_list.html", context)


@login_required
def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first():
        request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))


@login_required
def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))


def delete_friend(request, id):
    user_profile = request.user.profile
    friend_profile = get_object_or_404(Profile, id=id)
    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)
    return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))


@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    u = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
    user_posts = Post.objects.filter(user_name=u)

    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(FriendRequest.objects.filter(
                from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'friend_request_sent'

        # if we have recieved a friend request
        if len(FriendRequest.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'u': u,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
        'post_count': user_posts.count
    }

    return render(request, "user/profile-view.html", context)
