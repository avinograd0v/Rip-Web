from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from polls.fulltext import SearchManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, default='../media/default-user.png')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + " profile"

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class Question(models.Model):
    objects = SearchManager(['header', 'content'])

    header = models.CharField(max_length=60)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User)
    publicationDate = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    rating = models.IntegerField(default=0)
    approved_by = models.ManyToManyField(User, related_name='questions_approved', blank=True)
    disapproved_by = models.ManyToManyField(User, related_name='questions_disapproved', blank=True)

    def get_absolute_url(self):
        return reverse("polls:question", kwargs={'pk': self.pk})

    def __str__(self):
        return self.header


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    publicationDate = models.DateTimeField(auto_now_add=True)
    isRight = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    approved_by = models.ManyToManyField(User, related_name='answers_approved', blank=True)
    disapproved_by = models.ManyToManyField(User, related_name='answers_disapproved', blank=True)

    def get_absolute_url(self):
        return reverse("polls:question", kwargs={'pk': self.question_id})

    def __str__(self):
        return self.content


class Tag(models.Model):
    word = models.CharField(max_length=20)

    def __str__(self):
        return self.word
