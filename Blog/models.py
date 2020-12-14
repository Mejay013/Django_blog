# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Looked(models.Model):
    looked = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'looked'

class Article(models.Model):
    article_title = models.CharField('Заголовок статьи',max_length=200)
    article_text = models.TextField('Текст статьи')
    date_publish = models.DateTimeField('Дата публикации')
    article_image = models.ImageField(default='default.png',blank=True)

    def __str__(self):
        return self.article_title
    
    def check_relevance(self):
        return self.date_publish >= timezone.now()- datetime.timedelta(days=1)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE )
    comment_title = models.CharField('Автор комментария',max_length=40)
    comment_text = models.CharField('Текст комментария',max_length=200)
    comment_author_image = models.ImageField(default='default_avatar.jpg',blank=True )
    author_id = models.IntegerField('Id автора',default=1)

    def __str__(self):
        return self.comment_title +str('/     /') + self.comment_text 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField('Личный статус',max_length=100 , null = True)
    profile_avatar = models.ImageField(null=True,blank=True , default='default_avatar.jpg')
    date_birthday = models.DateField('Дата рождения',null = True)
    featured_articles_list = models.CharField('Избранные статьи',max_length=1000 ,null = True )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()