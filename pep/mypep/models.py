from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProfileModel(models.Model):
    """
        User Profile Model for User details
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='images', default="",
                                   blank=True, null=True)
    user_gender = models.CharField(max_length=300, blank=True, null=True)
    user_location = models.TextField(max_length=300, blank=True, null=True)
    user_job_role = models.CharField(max_length=300, blank=True, null=True)
    user_bio = models.CharField(max_length=300, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    # Slugify Function
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)


# Signal for user onetoone field
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)


class AuthModel(models.Model):
    """
    Auth Model 
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
