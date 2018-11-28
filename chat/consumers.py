from channels import Group
from channels.sessions import channel_session
from .models import Room
import json


@channel_session
def ws_connect(message):
    path = str(message['path'], encoding="utf8")
    prefix, label = path.strip('/').split('/')
    room, created = Room.objects.get_or_create(label=label)
    Group('chat-' + label).add(message.reply_channel)
    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    room = Room.objects.get(label=label)
    data = json.loads(message['text'])
    m = room.messages.create(handle=data['handle'], message=data['message'])
    Group('chat-'+label).send({'text': json.dumps({'handle': m.handle, 'message': m.message,
                                                   'timestamp': m.timestamp.timestamp()})})


@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    Group('chat-'+label).discard(message.reply_channel)

