from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rooms.models import Room, Message
from rooms.nltk_tagging import process_message

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'rooms/rooms.html', {'rooms' : rooms})


@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)
    for message in messages:
        if message.is_fog:
            message.content = process_message(message.content)

    return render(request, 'rooms/room.html', {'room': room, 'messages': messages})