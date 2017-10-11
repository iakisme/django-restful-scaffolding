# -*- coding: utf-8 -*-
from channels import Group
from channels.sessions import channel_session
from channels.routing import route
from common.storages import pubsub
import json
from common.storages import redis

@channel_session
def ws_connect(message):
    prefix, label = message['path'].strip('/').split('/')
    if prefix == 'page':
        message.reply_channel.send({"accept": True, "text": "后台已连接"})
    if prefix == 'index' and label == 'sqlrequest':
        message.reply_channel.send({"accept": True, "text": []})
    Group(prefix+'-'+label).add(message.reply_channel)

@channel_session
def ws_receive(message):
    # label = message.channel_session['room']
    # data = json.loads(message['text'])
    message.reply_channel.send({
        "text": message.content['text'],
    })


@channel_session
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)



channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_receive),
    route('websocket.disconnect', ws_disconnect),
]
