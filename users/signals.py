from django.db.models.signals import post_save
from django.contrib.auth.models import User     # sends the signal
from django.dispatch import receiver            # receives the signal and performs a task
from .models import Profile

        #signal       sender
# when User sends signal of post_save (user is saved) send the signal and the receiver is the create profile function
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()