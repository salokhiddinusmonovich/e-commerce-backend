from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import UserType
from django.templatetags.static import static


class User(AbstractUser):
    user_type = models.IntegerField(choices=UserType, default=UserType.CUSTOMER)
    phone = models.CharField(max_length=13, null=True, blank=True)
    is_delete = models.BooleanField(default=False)


    def __str__(self):
        return self.username


    @property
    def is_admin(self):
        return self.user_type == 0

    @property
    def is_customer(self):
        return self.user_type == 1



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    realname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar2.jpn')
        return avatar

    @property
    def name(self):
        if self.realname:
            name = self.realname
        else:
            name = self.user.username
        return name