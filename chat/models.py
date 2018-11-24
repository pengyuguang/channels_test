from django.db import models
from django.utils import timezone

# Create your models here.
class Room(models.Model):
    """
    聊天室
    """
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label

class Message(models.Model):
    """
    消息
    """
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())