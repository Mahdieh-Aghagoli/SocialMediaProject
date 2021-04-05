from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from common.validators import mobile_length_validator, mobile_validator, validate_not_empty


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    friends = models.ManyToManyField("Profile", blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True,
                                    validators=[mobile_length_validator, mobile_validator, validate_not_empty],
                                    help_text='Please use the follow format :<em>09- - - - - - - - -</em>')
    GENDER_CHOICES = [('Female', 'Female'), ('Male', 'Male'), ('None', 'None')]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='None')
    birthday = models.DateField(blank=True, null=True,
                                help_text='Please use the follow format :<em>YYYY-MM-DD</em>')
    slug = models.SlugField(verbose_name="Slug", allow_unicode=True, unique=True, blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
