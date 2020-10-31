from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save()

        user_image = Image.open(self.image.path)
        # if user image larger than 300x300 pixels then resize to 300x300 pixels, and then save to original image file path
        if user_image.height > 300 or user_image.width > 300:
            user_image.thumbnail((300, 300))
            user_image.save(self.image.path)
