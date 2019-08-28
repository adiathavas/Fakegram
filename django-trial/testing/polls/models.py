from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


# creating my model

class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('data published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username


class Selection(models.Model):
    topic = models.CharField(max_length=200)
    def __str__(self):
        return self.topic
