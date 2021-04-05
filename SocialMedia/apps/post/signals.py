from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from apps.user.models.user import Follow


@receiver(m2m_changed, sender=Follow)  # which list is changed
def add_follower(sender, instance, action, reverse, pk_set, followers=None, **kwargs):
    follows = []  # list of users main (logged ) user have followed
    logged_user = User.objects.get(username=instance)  # user who followed other users
    for i in pk_set:
        user = User.objects.get(pk=i)
        follows_obj = Follow.objects.get(user=user)
        followers.append(follows_obj)

    if action == "pre_add":
        for i in followers:
            i.follower.add(logged_user)
            i.save()

    if action == "pre_remove":
        for i in followers:
            i.follower.remove(logged_user)
            i.save()
